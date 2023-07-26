#!/bin/sh

echo "Pulling..."

for company in "company2"
do
    for repo in "frontend" "backend" "algs1" "algs2"
    do
        cmd="git pull"
        
        if ! eval $cmd; then
            echo "Failed to pull ${repo} of ${company} from command: ${cmd}"
            continue
        fi

        env=$(jq -r ".${company}.${repo}.env" config.json)
        
        if [ "$env" != "null" ]; then
            mv -f "${env}" "${company}/${repo}/.env"
        fi
    done
done

echo "Pulling Complete!"
exit 0
