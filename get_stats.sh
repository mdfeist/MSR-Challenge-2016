#!/bin/bash

cd $1

for d in */ ; do
	echo "=============================== NEW PROJECT ========================================"
	echo "$d"
	echo "===================================================================================="
	cd $d

	last="0"

	git log --reverse --format="%H %an" | while read line
	do
		#echo "$commit"
		stringarray=($line)

		commit=${stringarray[0]}
		author=${stringarray[1]}

		echo "#COMMIT_START"
		echo "#AUTHOR | $author"
		
		if [ "$last" != "0" ]
		then
			echo "#COMMIT | $commit $last"
			git difftool -y --tool=gumtree_cmp $commit $last
		else
			echo "#COMMIT | $commit"
			git difftool -y --tool=gumtree $commit
		fi
		echo "#COMMIT_END"

		last="$commit"
	done


	echo "===================================================================================="
	echo "DONE"
	echo "====================================================================================\n"
	
	cd ..
done