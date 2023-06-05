#!/bin/sh

echo "Building..."

for company in "company1" "company2"
do
    for repo in "frontend" "backend" "algs1" "algs2"
    do
        command=$(jq -r ".${company}.${repo}.build" config.json)
        repodir="${company}/${repo}/"

        if [ -d "$repodir" ]; then
            eval "cd ${repodir}"
            eval $command
            cd ../..
        else
            echo "Could not find ${repo} in ${company}. Skipping..."
        fi
    done
done

echo "Building Complete!"
