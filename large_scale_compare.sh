#!/bin/bash
scenario=$1 # "education" "therapist"
n=$2

export API_KEY=$(cat .openai_key)

# Models
items=("gpt-4o" "gpt-4o-mini" "gpt-3.5-turbo-0125")

echo "pairwise comparison for prompt"
# Loop through each combination of two items
for ((i=0; i<${#items[@]}; i++)); do
  for ((j=i+1; j<${#items[@]}; j++)); do
    m1="${items[i]}"
    m2="${items[j]}"
    echo "m1=${m1}, m2=${m2}, prompt"
    python quality_compare.py -s ${scenario} -m1 $m1 -m2 $m2 --api_key ${API_KEY} -n $n
    echo ""
  done
done
echo ""

echo "pairwise comparison for vanilla"
# Loop through each combination of two items
for ((i=0; i<${#items[@]}; i++)); do
  for ((j=i+1; j<${#items[@]}; j++)); do
    m1="${items[i]}"
    m2="${items[j]}"
    echo "m1=${m1}, m2=${m2}, vanilla"
    python quality_compare.py -s ${scenario} -m1 $m1 -m2 $m2 --api_key ${API_KEY} -n $n --m1_vanilla --m2_vanilla
    echo ""
  done
done
echo ""

echo "prmopt vs vanilla"
# Loop through each combination of two items
for ((i=0; i<${#items[@]}; i++)); do
  mm="${items[i]}"
  echo "m=${mm}, prmopt vs vanilla"
  python quality_compare.py -s ${scenario} -m1 $mm -m2 $mm --api_key ${API_KEY} -n $n --m2_vanilla
  echo ""
done
echo ""