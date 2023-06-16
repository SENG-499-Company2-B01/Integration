#!/bin/sh

echo "Cloning..."

for company in "company1" "company2"
do
    mkdir -p "$company"
    for repo in "frontend" "backend" "algs1" "algs2"
    do
        cmd=$(jq -r ".${company}.${repo}.clone" /app/config.json)
        
        if ! eval $cmd; then
            echo "Failed to clone ${repo} of ${company} from command: ${cmd}"
            continue
        fi

        env=$(jq -r ".${company}.${repo}.env" /app/config.json)
        
        if [ "$env" != "null" ]; then
            mv "${env}" "${company}/${repo}/.env"
        fi
    done
done

echo "Cloning Complete!"
exit 0
