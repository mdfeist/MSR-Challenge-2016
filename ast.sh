#!/bin/bash

if [ ${2: -5} == ".java" ] || [ ${3: -5} == ".java" ]
then
	echo "#STATS_START"
    echo "#FILE1 | $2"
    echo "#FILE2 | $3"

	java -cp ~/Windows/Documents/UofA/CMPUT664/Assignment2/gumtree-spoon-ast-diff/target/gumtree-spoon-ast-diff-0.0.3-SNAPSHOT-jar-with-dependencies.jar fr.inria.sacha.spoon.diffSpoon.DiffSpoonImpl $1 $2 $3

	echo "#STATS_END"
fi