#!/bin/bash

if [ ${1: -5} == ".java" ] || [ ${2: -5} == ".java" ]
then
    echo $1
	echo $2

	sh runDiff.sh $1 $2
fi