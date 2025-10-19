#!/usr/bin/env python3
"""
Combine different model's env_info.json files into train and test datasets.
"""

import json
import os
import glob
from collections import defaultdict
from typing import Dict, List, Any
import argparse

def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Warning: Expected list in {file_path}, got {type(data)}")
                return []
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return data

def combine_model_data(model_files: List[str], test_models: List[str]) -> tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Combine data from multiple model files and organize by risk_type for train and test sets."""
    train_data = defaultdict(list)
    test_data = defaultdict(list)
    
    # Define risky types to filter out
    risky_types = [
        "Sensitive Data Exfiltration",
        "Covert Channel Attack", 
        "Malicious Code Execution",
        "Privilege Escalation",
        "Persistence via Backdoor Implantation",
        "Cache or Local State Pollution",
        "Delayed or Timed Trigger Attacks",
        "Denial-of-Service",
        "Log Explosion Attacks",
        "Safe",
    ]
    
    for file_path in model_files:
        print(f"Loading data from {file_path}...")
        data = load_json_file(file_path)
        
        if not data:
            print(f"  No data found in {file_path}")
            continue
        
        # Extract model name from file path
        model_name = os.path.basename(file_path).replace('_env_info.json', '')
        print(f"  Loaded {len(data)} entries from {model_name}")
        
        # Determine if this model should go to test set
        is_test_model = model_name in test_models
        target_data = test_data if is_test_model else train_data
        
        # Process each entry
        for entry in data:
            if 'enhanced_data' in entry:
                enhanced_data = entry['enhanced_data']
                risk_type = enhanced_data.get('risk_type', 'Unknown')
                observation = enhanced_data.get('observation', '')
                safe_twin = enhanced_data.get('safe_twin', '')
                
                # Filter out observations that contain risky type names
                def contains_risky_type(text):
                    """Check if text contains any risky type names."""
                    if not text:
                        return False
                    text_lower = text.lower()
                    for risky_type in risky_types:
                        if risky_type.lower() in text_lower:
                            return True
                    return False
                
                # Only add observations that don't contain risky type names and are at least 500 characters
                if observation and not contains_risky_type(observation) and len(observation) >= 500:
                    target_data[risk_type].append(observation)
                
                # Add safe_twin only if it doesn't contain risky type names and is at least 500 characters
                if safe_twin and not contains_risky_type(safe_twin) and len(safe_twin) >= 500:
                    target_data["Safe"].append(safe_twin)
            else:
                print(f"  Warning: Entry missing enhanced_data: {entry.get('task_id', 'unknown')}")
    
    return dict(train_data), dict(test_data)

def generate_statistics(train_data: Dict[str, List[str]], test_data: Dict[str, List[str]]) -> None:
    """Generate and print statistics about the combined data."""
    print("\n" + "="*60)
    print("COMBINED DATA STATISTICS")
    print("="*60)
    
    print("\nTRAIN DATA:")
    train_total = 0
    for risk_type, descriptions in train_data.items():
        count = len(descriptions)
        print(f"  {risk_type}: {count} descriptions")
        train_total += count
    print(f"  Total train descriptions: {train_total}")
    
    print("\nTEST DATA:")
    test_total = 0
    for risk_type, descriptions in test_data.items():
        count = len(descriptions)
        print(f"  {risk_type}: {count} descriptions")
        test_total += count
    print(f"  Total test descriptions: {test_total}")
    
    print(f"\nTotal descriptions: {train_total + test_total}")

def save_to_json_file(combined_data: Dict[str, List[str]], output_file: str) -> None:
    """Save combined data to a JSON file."""
    print(f"\nSaving combined data to {output_file}...")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving to JSON file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Combine different model env_info.json files into train and test datasets')
    parser.add_argument('--input-pattern', default='*_env_info.json', 
                       help='Pattern to match input files (default: *_env_info.json)')
    parser.add_argument('--train-output', default='env_info_train.json',
                       help='Output train JSON file (default: env_info_train.json)')
    parser.add_argument('--test-output', default='env_info_test.json',
                       help='Output test JSON file (default: env_info_test.json)')
    parser.add_argument('--test-models', nargs='*', default=['gpt_4o', 'deepseek_r1'],
                       help='Models to include in test set (default: gpt_4o deepseek_r1)')
    parser.add_argument('--exclude-models', nargs='*', default=[],
                       help='Models to exclude from combination')
    
    args = parser.parse_args()
    
    print("Combining model env_info.json files into train and test datasets...")
    print(f"Input pattern: {args.input_pattern}")
    print(f"Test models: {args.test_models}")
    print(f"Excluding models: {args.exclude_models}")
    
    # Find all matching files
    all_files = glob.glob(args.input_pattern)
    
    if not all_files:
        print(f"No files found matching pattern: {args.input_pattern}")
        return
    
    print(f"Found {len(all_files)} total files matching pattern")
    
    # Filter out excluded models and combined files
    model_files = []
    for file_path in all_files:
        model_name = os.path.basename(file_path).replace('_env_info.json', '')
        
        # Skip combined files and excluded models
        if not model_name.startswith('combined') and model_name not in args.exclude_models:
            model_files.append(file_path)
        else:
            print(f"  Skipping {file_path} (excluded or combined file)")
    
    print(f"Processing {len(model_files)} model files:")
    for file_path in model_files:
        model_name = os.path.basename(file_path).replace('_env_info.json', '')
        is_test = model_name in args.test_models
        print(f"  - {file_path} -> {'TEST' if is_test else 'TRAIN'}")
    
    if not model_files:
        print("No files to process after filtering")
        return
    
    # Combine data
    train_data, test_data = combine_model_data(model_files, args.test_models)
    
    if not train_data and not test_data:
        print("No data to combine")
        return
    
    # Generate statistics
    generate_statistics(train_data, test_data)
    
    # Save train and test data to JSON files
    if train_data:
        save_to_json_file(train_data, args.train_output)
    
    if test_data:
        save_to_json_file(test_data, args.test_output)
    
    print("\n✓ Combination completed successfully!")
    print(f"Train data saved to: {args.train_output}")
    print(f"Test data saved to: {args.test_output}")

if __name__ == "__main__":
    main()
