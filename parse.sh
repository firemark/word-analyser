#!/bin/bash

set -e

function tt {
    /usr/bin/time -f "time: %es mem: %MkB" "$@"
}

step=1
function title {
    printf '%02d. %-50s ' $step "$1..."
    step=$[step + 1]
}

title 'Get ips and urls from logs'
tt awk '{ print $1, $11 }' logs > output/parsed_logs_1

title 'Extract terms from urls'
tt ./parse_urls_to_terms.py output/parsed_logs_1 > output/parsed_logs_2

title 'Sort urls per ip'
tt sort -s -k1,1 output/parsed_logs_2 > output/parsed_logs_3

title 'Concat terms per ip'
tt ./concat_terms.py output/parsed_logs_3 > output/parsed_logs_final

title 'Get banned ips'
tt ./ban_ips.py output/parsed_logs_1 > output/banned_ips

title 'Drop banned ips from logs'
tt grep -vFf output/banned_ips output/parsed_logs_3 > output/parsed_logs_4

title 'Concat terms without banned ips per ip'
tt ./concat_terms.py output/parsed_logs_3 > output/parsed_logs_final_without_banned_ips
