for i in {1..10}; do
echo "Run ${i}/10"
python pipeline_remote.py --show-progress
done