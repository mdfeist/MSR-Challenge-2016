#!/bin/bash

DIRECTORY="repositories_100"
NUMBER=100

# Read all repositories from BOA output
ALL_GITHUB_REPOS=()
while IFS='' read -r line || [[ -n "$line" ]]; do
    ALL_GITHUB_REPOS+=($line)
done < "$1"

# Randomly Select 100
GITHUB_REPOS=()
while [ ${#GITHUB_REPOS[@]} -lt $NUMBER ]
do
	repo=${ALL_GITHUB_REPOS[$RANDOM % ${#ALL_GITHUB_REPOS[@]} ]}
	GITHUB_REPOS+=($repo)
	GITHUB_REPOS=$(echo "${GITHUB_REPOS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')
done

# Pull repositories
if [ -d "$DIRECTORY" ]; then
	rm -R $DIRECTORY
fi

mkdir $DIRECTORY
cd $DIRECTORY

for repo in "${GITHUB_REPOS[@]}"
do
	# do whatever on $repo
	git clone $repo
done

