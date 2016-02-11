#!/bin/bash

cd $1

for d in */ ; do
    echo "$d"
    cd $d

    last="0"

	git log --format="%H" | while read commit
	do
		#echo "$commit"

		if [ "$last" != "0" ]
		then
			echo "Diff: $last - $commit"
			git difftool -y $last $commit
    	fi

    	last="$commit"
	done
	echo "DONE\n\n"
    cd ..
done