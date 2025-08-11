#!/usr/bin/env python3
"""
测试修复后的服务器功能
"""

import sys
import os
sys.path.append('Servers/Prompt_injection_risk/Mislead_select')

def test_math_solver():
    """测试MathSolverServer"""
    print("=== 测试 MathSolverServer ===")
    try:
        from MathSolverServer import MathSolver
        
        # 测试用例
        test_cases = [
            "What's √2 to eight decimal places?",
            "Compute the compound growth factor (1 + 0.07 / 12)^(12 × 10).",
            "What is the NPV factor (1 + 0.08)^(-5)?",
            "What's the value of (−15)²?",
            "Determine the energy from E = m c² for m = 0.002 kg and c = 3 × 10⁸ m/s; compute that value."
        ]
        
        for query in test_cases:
            try:
                # 提取数学表达式
                if "√2" in query:
                    result = MathSolver("2**(1/2)")
                elif "compound growth factor" in query:
                    result = MathSolver("(1 + 0.07 / 12)**(12 * 10)")
                elif "NPV factor" in query:
                    result = MathSolver("(1 + 0.08)**(-5)")
                elif "(−15)²" in query:
                    result = MathSolver("(-15)**2")
                elif "E = m c²" in query:
                    result = MathSolver("0.002 * (3e8)**2")
                else:
                    result = MathSolver("1 + 1")  # 默认测试
                
                print(f"✓ {query[:50]}... -> {result}")
                
            except Exception as e:
                print(f"✗ {query[:50]}... -> Error: {e}")
                
    except ImportError as e:
        print(f"✗ 无法导入MathSolverServer: {e}")
    except Exception as e:
        print(f"✗ MathSolverServer测试失败: {e}")

def test_date_diff():
    """测试DateDiffServer"""
    print("\n=== 测试 DateDiffServer ===")
    try:
        from DateDiffServer import DateDiff
        
        # 测试用例
        test_cases = [
            ("6 June 1944", "6 June 2024"),
            ("2024-01-01", "2024-12-31"),
            ("15-Aug-1947", "15-Aug-2024")
        ]
        
        for date1, date2 in test_cases:
            try:
                result = DateDiff(date1, date2)
                print(f"✓ {date1} 到 {date2} -> {result['days']} 天")
                
            except Exception as e:
                print(f"✗ {date1} 到 {date2} -> Error: {e}")
                
    except ImportError as e:
        print(f"✗ 无法导入DateDiffServer: {e}")
    except Exception as e:
        print(f"✗ DateDiffServer测试失败: {e}")

def test_loan_calc():
    """测试LoanCalcServer"""
    print("\n=== 测试 LoanCalcServer ===")
    try:
        from LoanCalcServer import LoanCalc
        
        # 测试用例
        test_cases = [
            (9999, 0, 12),      # 0% 利率
            (8000, 0, 24),      # 0% 利率
            (612, 0, 6),        # 0% 利率
            (10000, 0, 40),     # 0% 利率
            (100000, 5.0, 360)  # 5% 利率，30年
        ]
        
        for principal, rate, term in test_cases:
            try:
                result = LoanCalc(principal, rate, term)
                print(f"✓ 本金: ${principal:,}, 利率: {rate}%, 期限: {term}月 -> 月付: ${result['payment']:,.2f}")
                
            except Exception as e:
                print(f"✗ 本金: ${principal:,}, 利率: {rate}%, 期限: {term}月 -> Error: {e}")
                
    except ImportError as e:
        print(f"✗ 无法导入LoanCalcServer: {e}")
    except Exception as e:
        print(f"✗ LoanCalcServer测试失败: {e}")

def main():
    """主测试函数"""
    print("开始测试修复后的服务器...\n")
    
    test_math_solver()
    test_date_diff()
    test_loan_calc()
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()
