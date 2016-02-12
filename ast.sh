#!/bin/bash

if [ ${2: -5} == ".java" ] || [ ${3: -5} == ".java" ]
then
    echo $2
	echo $3
	echo "---"

	java -cp ~/Windows/Documents/UofA/CMPUT664/Assignment2/gumtree-spoon-ast-diff/target/gumtree-spoon-ast-diff-0.0.3-SNAPSHOT-jar-with-dependencies.jar fr.inria.sacha.spoon.diffSpoon.DiffSpoonImpl $1 $2 $3
fi