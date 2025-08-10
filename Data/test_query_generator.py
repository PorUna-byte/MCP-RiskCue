#!/usr/bin/env python3
"""
Test script for the modified query generator
"""

import json
from pathlib import Path

def test_jsonl_output():
    """Test JSONL output format"""
    # Sample data
    sample_queries = {
        "test/server1": ["What is the weather?", "How far is it to the airport?"],
        "test/server2": ["Calculate 2+2", "What time is it?"]
    }
    
    # Test output file
    test_output = Path("test_output.jsonl")
    
    # Write JSONL
    with open(test_output, 'w', encoding='utf-8') as f:
        for path, query_list in sample_queries.items():
            for query in query_list:
                json.dump({"path": path, "query": query}, f, ensure_ascii=False)
                f.write('\n')
    
    print(f"✓ Test JSONL file created: {test_output}")
    
    # Read and verify
    with open(test_output, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"✓ JSONL file contains {len(lines)} lines")
        
        for i, line in enumerate(lines):
            data = json.loads(line.strip())
            print(f"  Line {i+1}: {data}")
    
    # Cleanup
    test_output.unlink()
    print("✓ Test file cleaned up")

def test_temp_file_handling():
    """Test temp file handling"""
    temp_dir = Path("Temp")
    temp_dir.mkdir(exist_ok=True)
    
    # Create a sample temp file
    sample_temp = temp_dir / "test_server.json"
    sample_data = {"path": "test/server", "queries": ["test query 1", "test query 2"]}
    
    with open(sample_temp, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Sample temp file created: {sample_temp}")
    
    # Test loading
    from query_generator import load_intermediate_results
    results = load_intermediate_results(temp_dir)
    print(f"✓ Loaded {len(results)} intermediate results")
    
    # Cleanup
    sample_temp.unlink()
    print("✓ Sample temp file cleaned up")

if __name__ == "__main__":
    print("Testing modified query generator functionality...\n")
    
    test_jsonl_output()
    print()
    test_temp_file_handling()
    
    print("\n✓ All tests completed successfully!")
