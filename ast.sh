#!/bin/bash

is_java="*.java^"
valid=false

if [[ $1 =~ $is_java ]]; then
    valid=true
fi

if [[ $2 =~ $is_java ]]; then
    valid=true
fi

if [ $valid ]
then
	exit
fi

echo $1
echo $2

java -cp ~/Windows/Documents/UofA/CMPUT664/Assignment2/gumtree-spoon-ast-diff/target/gumtree-spoon-ast-diff-0.0.3-SNAPSHOT-jar-with-dependencies.jar fr.inria.sacha.spoon.diffSpoon.DiffSpoonImpl $1 $2