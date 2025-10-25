for i in {1..5}; do
echo "Run ${i}/5"
python pipeline_remote.py --show-progress
done