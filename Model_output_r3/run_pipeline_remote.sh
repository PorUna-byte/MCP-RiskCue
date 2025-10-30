for i in {1..20}; do
echo "Run ${i}/20"
python pipeline_remote.py --show-progress
done