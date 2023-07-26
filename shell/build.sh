#!/bin/sh

echo "Building..."

nocache=$1

for company in "company2"
do
    for repo in "frontend" "backend" "algs1" "algs2"
    do
        command=$(jq -r ".${company}.${repo}.build" config.json)
        if [[ "$nocache" == "False" ]]; then
            command+=" --no-cache"
        fi
        repodir="${company}/${repo}/"

        echo "Building ${repo} in ${company}..."

        if [ -d "$repodir" ]; then
            eval "cd ${repodir}"
            eval $command
            cd ../../
        else
            echo "Could not find ${repo} in ${company}. Skipping..."
        fi
    done
done

echo "Building Complete!"
exit 0
