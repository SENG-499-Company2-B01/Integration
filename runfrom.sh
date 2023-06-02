#!/bin/sh

echo "Starting Containers..."

# Arguments should be passed as 1 or 2
frontend=$1
backend=$2
algs1=$3
algs2=$4

run_repo() {
    repo=$1
    company=$2

    command=$(jq -r ".${company}.${repo}.run" config.json)
    repodir="${company}/${repo}/"

    if [ -d "$repodir" ]; then
        eval "cd ${repodir}"
        eval $command
        cd ../..
    else
        echo "Could not find ${repo} in ${company}. Skipping..."
    fi
}

[ "$frontend" -eq 1 ] && run_repo "frontend" "company1"
[ "$backend" -eq 1 ] && run_repo "backend" "company1"
[ "$algs1" -eq 1 ] && run_repo "algs1" "company1"
[ "$algs2" -eq 1 ] && run_repo "algs2" "company1"

[ "$frontend" -eq 2 ] && run_repo "frontend" "company2"
[ "$backend" -eq 2 ] && run_repo "backend" "company2"
[ "$algs1" -eq 2 ] && run_repo "algs1" "company2"
[ "$algs2" -eq 2 ] && run_repo "algs2" "company2"

echo "Completed Starting Containers!"
