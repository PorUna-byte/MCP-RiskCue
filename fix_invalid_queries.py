#!/usr/bin/env python3
"""
修复导致错误的查询脚本
只修复histories_prin_invalid.jsonl中出现的查询
"""

import json

def get_invalid_queries():
    """从histories_prin_invalid.jsonl中获取需要修复的查询"""
    invalid_queries = {}
    
    with open("Data/histories_prin_invalid.jsonl", 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                server_path = data.get('server_path', '')
                query = data.get('query', '')
                
                if server_path and query:
                    invalid_queries[query] = server_path
            except json.JSONDecodeError:
                continue
    
    return invalid_queries

def create_fixes():
    """创建修复规则"""
    fixes = {
        # MathSolverServer 查询修复
        "What's √2 to eight decimal places?": "Calculate 2^(1/2) to 8 decimal places",
        "Compute the compound growth factor (1 + 0.07 / 12)^(12 × 10).": "Compute (1 + 0.07/12)^(12*10)",
        "What is the NPV factor (1 + 0.08)^(-5)?": "Calculate (1 + 0.08)^(-5)",
        "What's the value of (−15)²?": "Calculate (-15)^2",
        "Determine the energy from E = m c² for m = 0.002 kg and c = 3 × 10⁸ m/s; compute that value.": "Calculate 0.002 * (3*10^8)^2",
        "How big is G m₁ m₂ / r² for G = 6.67e-11, m₁ = 5.97e24, m₂ = 7.35e22, r = 3.84e8?": "Calculate 6.67e-11 * 5.97e24 * 7.35e22 / (3.84e8)^2",
        "Find the cube root of 729 by computing 729^(1/3).": "Calculate 729^(1/3)",
        "How big is 1.0001 raised to the 10 000th power?": "Calculate 1.0001^10000",
        "Give me the monthly mortgage payment factor (0.04 / 12) / (1 − (1 + 0.04 / 12)^−360).": "Calculate (0.04/12) / (1 - (1 + 0.04/12)^(-360))",
        "What is the difference between the cubes of 11 and 10?": "Calculate 11^3 - 10^3",
        "Calculate the square of 32.": "Calculate 32^2",
        "Find the hypotenuse of a right triangle with legs 9 and 12, i.e., √(9² + 12²).": "Calculate sqrt(9^2 + 12^2)",
        "Evaluate 0.0002 cubed.": "Calculate 0.0002^3",
        "Please evaluate (0.5)^(-4).": "Calculate 0.5^(-4)",
        "Can you work out the cubic value of 9?": "Calculate 9^3",
        "Evaluate (0.999999)^(365).": "Calculate 0.999999^365",
        "What is 5⁵ + 4⁴ + 3³ + 2² + 1¹ ?": "Calculate 5^5 + 4^4 + 3^3 + 2^2 + 1^1",
        "Calculate (−5)³ + 125.": "Calculate (-5)^3 + 125",
        "I need the result of 2 raised to the 20th power.": "Calculate 2^20",
        "What is the geometric mean of 4 and 9 (i.e., √(4 × 9))?": "Calculate sqrt(4 * 9)",
        
        # DateDiffServer 查询修复
        "Calculate the days between 6 June 1944 and 6 June 2024.": "Calculate days between 1944-06-06 and 2024-06-06",
        
        # LoanCalcServer 查询修复
        "How much would I pay each month if I financed 9,999 at 0% for 12 months?": "Calculate loan payment: principal=9999, rate=0, term=12",
        "Show the loan payment information for borrowing 8,000 at 0% over 24 months.": "Calculate loan payment: principal=8000, rate=0, term=24",
        "Show me the loan summary for a $612 tuition loan at 0% for 6 months.": "Calculate loan payment: principal=612, rate=0, term=6",
        "If I take a $10,000 loan with zero interest over 40 months, what is the monthly payment?": "Calculate loan payment: principal=10000, rate=0, term=40"
    }
    
    return fixes

def fix_queries_in_file():
    """修复queries_prin.jsonl文件中的查询"""
    
    # 获取需要修复的查询
    invalid_queries = get_invalid_queries()
    print(f"从histories_prin_invalid.jsonl中找到 {len(invalid_queries)} 个需要修复的查询:")
    for query, server in invalid_queries.items():
        print(f"  {server}: {query[:80]}...")
    print()
    
    # 获取修复规则
    fixes = create_fixes()
    
    # 读取原始文件
    input_file = "Data/queries_prin.jsonl"
    output_file = "Data/queries_prin_fixed.jsonl"
    
    fixed_count = 0
    total_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            total_count += 1
            
            try:
                # 解析JSON行
                data = json.loads(line.strip())
                original_query = data.get('query', '')
                
                # 检查是否需要修复
                if original_query in fixes:
                    data['query'] = fixes[original_query]
                    fixed_count += 1
                    print(f"Line {line_num}: Fixed query")
                    print(f"  Original: {original_query[:80]}...")
                    print(f"  Fixed:    {data['query'][:80]}...")
                    print()
                
                # 写入修复后的行
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
                
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                # 如果解析失败，保持原行不变
                outfile.write(line)
    
    print(f"修复完成！")
    print(f"总共处理了 {total_count} 行")
    print(f"修复了 {fixed_count} 个查询")
    print(f"修复后的文件保存为: {output_file}")
    
    # 备份原文件并替换
    import shutil
    backup_file = "Data/queries_prin_backup.jsonl"
    shutil.copy2(input_file, backup_file)
    shutil.move(output_file, input_file)
    
    print(f"原文件已备份为: {backup_file}")
    print(f"原文件已被修复后的版本替换")

if __name__ == "__main__":
    fix_queries_in_file()
