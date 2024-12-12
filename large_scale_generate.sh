scenario=$1 # "education" "therapist"
n=$2

export API_KEY=$(cat .openai_key)

for mm in 'gpt-4o' 'gpt-4o-mini' 'gpt-3.5-turbo-0125'
do
    echo "generate ${mm}, #samples= ${n}"
    python generate.py -s ${scenario} -m ${mm} --api_key ${API_KEY} -n $n
    echo ""
    echo ""
done