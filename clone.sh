#!/bin/sh

echo "Cloning..."

for company in "company1" "company2"
do
    mkdir -p "$company"
    for repo in "frontend" "backend" "algs1" "algs2"
    do
        url=$(jq -r ".${company}.${repo}.url" config.json)
        
        if ! git clone "${url}" "${company}/${repo}"; then
            echo "Failed to clone ${repo} of ${company} from URL: ${url}"
        fi
    done
done

echo "Cloning Complete!"