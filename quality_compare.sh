#!/bin/bash

# Models
items=("gpt-4o" "gpt-4o-mini" "gpt-3.5-turbo-0125")

# Loop through each combination of two items
for ((i=0; i<${#items[@]}; i++)); do
  for ((j=i+1; j<${#items[@]}; j++)); do
    m1="${items[i]}"
    m2="${items[j]}"
    python quality_compare.py -s education -m1 $m1 -m2 $m2 --api_key ${API_KEY} -n 5
  done
done



model_names=