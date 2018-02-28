#!/bin/bash

set -e

function tt {
    /usr/bin/time -f 'time: %es mem: %MkB' "$@"
}

step=1
function title {
    printf '%02d. %-50s ' $step "$1..."
    step=$[step + 1]
}

function sort_and_uniq {
    uniq -c | sort -s -n -k1,1
}

title 'Get only urls from logs'
tt awk '{ print $11 }' logs | sed 's/\?.*$//g' | sed 's/"//g' > an-output/analyzed_logs_1 

title 'Count unique urls'
tt sort an-output/analyzed_logs_1 | sort_and_uniq > an-output/unique_urls

title 'Count unique words'
tt egrep -io '[a-z][a-z0-9]+' an-output/analyzed_logs_1 | \
   sort | sort_and_uniq > an-output/unique_words

title 'Get ips and urls from logs'
tt awk '{ print $1, $11 }' logs > an-output/analyzed_logs_2 

title 'Count redirects'
tt ./count_redirects.py an-output/analyzed_logs_2 > an-output/count_redirects

title 'Count unique ips'
tt awk '{ print $1 }' logs | sort_and_uniq > an-output/unique_ips
