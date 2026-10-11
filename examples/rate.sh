#!/usr/bin/env sh
# sh examples/rate.sh USD EUR [bank]
curl -s "https://allratestoday.com/api/open/central-bank/${3:-ecb}?source=${1:-USD}&target=${2:-EUR}"
echo
