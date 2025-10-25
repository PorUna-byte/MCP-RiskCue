#!/usr/bin/env python3
"""
Extract examples from env_info.json and format them in LaTeX format.
For each risk type, extract one example and output observation, safe_twin, and explanation.
Uses different models for different risk types to increase diversity.
"""

import json
from pathlib import Path

# Define the risk types in order with their corresponding model files
# This ensures diversity by using different models for different risk types
RISK_TYPE_MODEL_MAPPING = [
    ("Sensitive Data Exfiltration", "gpt_4o_env_info.json"),
    ("Covert Channel Attack", "claude_3_7_sonnet_20250219_env_info.json"),
    ("Malicious Code Execution", "grok_4_env_info.json"),
    ("Privilege Escalation", "gemini_2.5_pro_env_info.json"),
    ("Persistence via Backdoor Implantation", "deepseek_r1_env_info.json"),
    ("Cache or Local State Pollution", "o3_2025_04_16_env_info.json"),
    ("Delayed or Timed Trigger Attacks", "kimi_k2_0711_preview_env_info.json"),
    ("Denial-of-Service", "doubao_1_5_pro_32k_250115_env_info.json"),
    ("Log Explosion Attacks", "glm_4.5v_env_info.json")
]

def load_json_data(json_file_path):
    """Load JSON data from file."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_example_from_file(json_file_path, risk_type):
    """Extract one example for a specific risk type from a JSON file."""
    data = load_json_data(json_file_path)
    
    for item in data:
        if 'enhanced_data' in item and 'risk_type' in item['enhanced_data']:
            if item['enhanced_data']['risk_type'] == risk_type:
                return {
                    'observation': item['enhanced_data']['observation'],
                    'safe_twin': item['enhanced_data']['safe_twin'],
                    'explanation': item['enhanced_data']['explanation'],
                    'model': item['enhanced_data'].get('model_name', 'unknown')
                }
    
    return None

def escape_latex(text):
    """Escape special LaTeX characters, particularly % -> \\%"""
    # Replace % with \%
    return text.replace('%', '\\%')

def format_latex_output(examples_with_models):
    """Format examples in LaTeX format with proper escaping."""
    output = []
    
    for idx, (risk_type, model_file, example) in enumerate(examples_with_models, start=4):
        if example:
            # Escape LaTeX special characters ONLY in observation, safe_twin, explanation
            observation = escape_latex(example['observation'])
            safe_twin = escape_latex(example['safe_twin'])
            explanation = escape_latex(example['explanation'])
            
            # Label index is idx - 3 (since idx starts from 4, so type1 = 4-3 = 1)
            label_idx = idx - 3
            
            # Format the LaTeX block
            latex_block = f"""\\newtcblisting{{promptbox{idx}}}{{
  listing only, breakable, enhanced,
  colback=gray!3, colframe=black!15, boxrule=0.6pt, arc=2pt,
  title=System Logs for {risk_type},
  coltitle=black,            % 标题文字颜色
  colbacktitle=gray!15,      % （可选）标题背景
  fonttitle=\\bfseries,       % （可选）标题加粗
  listing options={{style=promptutf}}
}}
\\label{{systemlog:type{label_idx}}}
\\begin{{promptbox{idx}}}

Risky System Log:
{observation}
Safe Twin (Benign, hard negative):
{safe_twin}
Explanation:
{explanation}

\\end{{promptbox{idx}}}

"""
            output.append(latex_block)
        else:
            print(f"Warning: No example found for {risk_type} in {model_file}")
    
    return '\n'.join(output)

def main():
    base_dir = Path(__file__).parent
    output_file = base_dir / 'examples.txt'
    
    print(f"Extracting examples from {len(RISK_TYPE_MODEL_MAPPING)} different models...")
    print(f"This increases diversity by using different models for different risk types.\n")
    
    # Extract examples from different model files
    examples_with_models = []
    
    for risk_type, model_file in RISK_TYPE_MODEL_MAPPING:
        json_file = base_dir / model_file
        print(f"Extracting '{risk_type}' from {model_file}...")
        
        example = extract_example_from_file(json_file, risk_type)
        examples_with_models.append((risk_type, model_file, example))
        
        if example:
            print(f"  ✓ Found example (model: {example['model']})")
        else:
            print(f"  ✗ No example found")
    
    print(f"\nFormatting LaTeX output with proper escaping...")
    latex_output = format_latex_output(examples_with_models)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_output)
    
    print(f"\nDone! Output written to {output_file}")
    print(f"\nExtracted examples for:")
    for i, (risk_type, model_file, example) in enumerate(examples_with_models, start=4):
        if example:
            print(f"  promptbox{i}: {risk_type} (from {model_file})")

if __name__ == '__main__':
    main()

