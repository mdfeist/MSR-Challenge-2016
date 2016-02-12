#!/bin/bash

cd $1

for d in */ ; do
	echo "=============================== NEW PROJECT ========================================"
	echo "$d"
	echo "===================================================================================="
	cd $d

	last="0"

	git log --reverse --format="%H" | while read commit
	do
		#echo "$commit"

		echo "===================================================================================="
		if [ "$last" != "0" ]
		then
			echo "Diff: $last $commit"
			git difftool -y --tool=gumtree_cmp $commit $last
		else
			echo "Diff: $commit"
			git difftool -y --tool=gumtree $commit
		fi
		echo "===================================================================================="

		last="$commit"
	done


	echo "===================================================================================="
	echo "DONE"
	echo "====================================================================================\n"
	
	cd ..
done