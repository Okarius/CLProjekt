#!/bin/bash

file=$1

wcl=$(wc -l <  $file)
echo "$file: $((wcl-1)) entries"

nf=$(awk '{print NF}' $file | sort -nu)

echo "num. features: $((nf -2))"

echo "distribution"
tail -n +2 $file | cut -f $nf | sort | uniq -c

wcu=$(cut -f 1 $file | sort | uniq | wc -l)
echo "uniqe: $wcu"

echo "distribution of unique"
#tail -n +2 $file | cut -f 1,$nf > dbg
tail -n +2 $file | cut -f 1,$nf | awk -F"[. ]" '!a[$1]++' | cut -f 2 | sort | uniq -c
