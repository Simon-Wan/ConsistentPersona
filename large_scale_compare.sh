#!/bin/bash
scenario=$1 # "education" "therapist"
n=$2

export API_KEY=$(cat .openai_key)

# Models
items=("gpt-4o" "gpt-4o-mini" "gpt-3.5-turbo-0125")

# Loop through each combination of two items
for ((i=0; i<${#items[@]}; i++)); do
  for ((j=i+1; j<${#items[@]}; j++)); do
    m1="${items[i]}"
    m2="${items[j]}"
    python quality_compare.py -s ${scenario} -m1 $m1 -m2 $m2 --api_key ${API_KEY} -n $n
  done
done
