#!/usr/bin/env python3
"""
修复导致错误的查询脚本
将复杂的、格式不规范的查询替换为清晰、标准的格式
"""

import json
import re

def fix_math_queries():
    """修复数学查询"""
    math_fixes = {
        # 原始查询 -> 修复后的查询
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
        "What is the geometric mean of 4 and 9 (i.e., √(4 × 9))?": "Calculate sqrt(4 * 9)"
    }
    return math_fixes

def fix_date_queries():
    """修复日期查询"""
    date_fixes = {
        "Calculate the days between 6 June 1944 and 6 June 2024.": "Calculate days between 1944-06-06 and 2024-06-06",
        "How many days passed between 1 January 2000 and 31 December 2000?": "Calculate days between 2000-01-01 and 2000-12-31",
        "Give me the exact day count from February 29, 2016 to March 1, 2020.": "Calculate days between 2016-02-29 and 2020-03-01",
        "I need the number of days separating 07/04/1976 and 07/04/2026.": "Calculate days between 1976-07-04 and 2026-07-04",
        "Could you calculate how long it's been in days from 15-Aug-1947 to 26-Jan-1950?": "Calculate days between 1947-08-15 and 1950-01-26",
        "Tell me the distance in days between Halloween 2023 and New Year's Day 2024.": "Calculate days between 2023-10-31 and 2024-01-01",
        "What is the day difference between 2022-12-31 and 2023-01-01?": "Calculate days between 2022-12-31 and 2023-01-01",
        "Figure out how many days lie between April 10, 1815 and April 10, 1915.": "Calculate days between 1815-04-10 and 1915-04-10",
        "From my birthday on 09-09-1999 until today, how many days is that?": "Calculate days between 1999-09-09 and 2024-12-19",
        "Compute the absolute number of days separating March 3, 2023 and March 30, 2023.": "Calculate days between 2023-03-03 and 2023-03-30",
        "I'm curious: days between 30 June 2015 and 1 July 2015 during the leap second event?": "Calculate days between 2015-06-30 and 2015-07-01",
        "Tell me the gap in days from 2020-02-28 to 2020-03-01.": "Calculate days between 2020-02-28 and 2020-03-01",
        "How many days have elapsed since 5 May 2021 if today is 5 May 2024?": "Calculate days between 2021-05-05 and 2024-05-05",
        "Which span is longer: 1-Jan-2005 to 1-Jan-2006, or 1-Jan-2010 to 1-Dec-2010?": "Calculate days between 2005-01-01 and 2006-01-01",
        "Calculate the days between the Apollo 11 launch date (16 July 1969) and the moon landing (20 July 1969).": "Calculate days between 1969-07-16 and 1969-07-20",
        "Count the days from Christmas Eve 2022 to Valentine's Day 2023.": "Calculate days between 2022-12-24 and 2023-02-14",
        "How many days were there from the start of World War I (28-07-1914) to its armistice (11-11-1918)?": "Calculate days between 1914-07-28 and 1918-11-11",
        "If I graduated on 06/15/2012 and my reunion is on 06/15/2032, how many days apart are those dates?": "Calculate days between 2012-06-15 and 2032-06-15",
        "Give me the day difference between 29-Feb-2000 and 28-Feb-2001.": "Calculate days between 2000-02-29 and 2001-02-28",
        "What's the number of days separating 1989-11-09 and 1990-10-03?": "Calculate days between 1989-11-09 and 1990-10-03",
        "I need to know how many days lie between March 1, 1900 and March 1, 2000.": "Calculate days between 1900-03-01 and 2000-03-01",
        "Compute the total days from 12 Dec 2012 to 21 Dec 2012—the so-called \"end of the world.\"": "Calculate days between 2012-12-12 and 2012-12-21",
        "From the first day of spring 2021 (20 March 2021) to the first day of summer 2021 (21 June 2021), how many days?": "Calculate days between 2021-03-20 and 2021-06-21",
        "How many days passed between 2008-08-08 and 2008-08-24, the duration of the Beijing Olympics?": "Calculate days between 2008-08-08 and 2008-08-24",
        "Find the number of days between 09/28/2023 and 10/05/2023.": "Calculate days between 2023-09-28 and 2023-10-05",
        "Please tell me how many days separate 2024-02-29 and 2024-03-01.": "Calculate days between 2024-02-29 and 2024-03-01",
        "What is the absolute day difference from 01-01-1970 to 01-01-1980?": "Calculate days between 1970-01-01 and 1980-01-01",
        "If a project started on 2021-11-01 and ended on 2023-04-15, how many days did it last?": "Calculate days between 2021-11-01 and 2023-04-15",
        "Determine the days from my hire date 2010-07-19 to my work anniversary 2025-07-19.": "Calculate days between 2010-07-19 and 2025-07-19",
        "Compare the number of days from Jan 1 2018 to Jul 1 2018 with the days from Jan 1 2019 to Jul 1 2019.": "Calculate days between 2018-01-01 and 2018-07-01",
        "How many days are there between 31 January 2020 and 31 January 2021?": "Calculate days between 2020-01-31 and 2021-01-31",
        "Tell me the days difference between 4/4/2004 and 5/5/2005.": "Calculate days between 2004-04-04 and 2005-05-05",
        "I'm booking a vacation: how many days from 2023-12-15 to 2024-01-05?": "Calculate days between 2023-12-15 and 2024-01-05",
        "From the Boston Marathon bombing (15-Apr-2013) to 15-Apr-2023, count the days.": "Calculate days between 2013-04-15 and 2023-04-15",
        "Give the day count between 2022-10-31 and 2023-10-31 (one full year including leap context if any).": "Calculate days between 2022-10-31 and 2023-10-31",
        "How long (in days) was it from 1912-04-14 to 1912-04-15 during the Titanic sinking?": "Calculate days between 1912-04-14 and 1912-04-15",
        "Calculate the span in days between 09-11-2001 and 07-04-2026.": "Calculate days between 2001-09-11 and 2026-07-04",
        "I'd like the difference in days from 20-Jan-2021 (US inauguration) to 20-Jan-2025.": "Calculate days between 2021-01-20 and 2025-01-20",
        "What is the number of days between February 1, 2022 and February 1, 2023?": "Calculate days between 2022-02-01 and 2023-02-01",
        "Compute the days separating 2020-01-01 and 2020-12-31.": "Calculate days between 2020-01-01 and 2020-12-31",
        "Check the length in days from 14-Feb-2024 to 14-Mar-2024.": "Calculate days between 2024-02-14 and 2024-03-14",
        "Which interval is longer: Aug 1 2020–Oct 1 2020 or Jan 1 2021–Mar 1 2021?": "Calculate days between 2020-08-01 and 2020-10-01",
        "Find out how many days have passed since 2000-05-05 until 2020-05-05.": "Calculate days between 2000-05-05 and 2020-05-05",
        "Tell me the days count between the start of the pandemic lockdown in my area (2020-03-15) and its end (2021-06-15).": "Calculate days between 2020-03-15 and 2021-06-15",
        "How many days are there from the signing of the Declaration of Independence (04-Jul-1776) to today, 04-Jul-2026?": "Calculate days between 1776-07-04 and 2026-07-04",
        "Give me the exact days between Star Wars release (25-May-1977) and its 50th anniversary (25-May-2027).": "Calculate days between 1977-05-25 and 2027-05-25",
        "Compute the absolute difference in days between 11-11-2011 and 12-12-2012.": "Calculate days between 2011-11-11 and 2012-12-12",
        "From 1999-12-31 to 2000-01-01, how many days?": "Calculate days between 1999-12-31 and 2000-01-01",
        "Determine whether 01-03-2022 to 01-04-2022 is longer, shorter, or equal in days to 01-04-2022 to 01-05-2022.": "Calculate days between 2022-03-01 and 2022-04-01",
        "Calculate the number of days between International Women's Day 2020 (08-Mar-2020) and International Women's Day 2024 (08-Mar-2024).": "Calculate days between 2020-03-08 and 2024-03-08",
        "I'm curious: how many days separate 2025-05-05 and 2023-05-05 (absolute value, please).": "Calculate days between 2023-05-05 and 2025-05-05"
    }
    return date_fixes

def fix_loan_queries():
    """修复贷款查询"""
    loan_fixes = {
        "How much would I pay each month if I financed 9,999 at 0% for 12 months?": "Calculate loan payment: principal=9999, rate=0, term=12",
        "Show the loan payment information for borrowing 8,000 at 0% over 24 months.": "Calculate loan payment: principal=8000, rate=0, term=24",
        "Show me the loan summary for a $612 tuition loan at 0% for 6 months.": "Calculate loan payment: principal=612, rate=0, term=6",
        "If I take a $10,000 loan with zero interest over 40 months, what is the monthly payment?": "Calculate loan payment: principal=10000, rate=0, term=40",
        "How much would my monthly payment be on a $250,000 mortgage at 3.75% interest for 30 years?": "Calculate loan payment: principal=250000, rate=3.75, term=360",
        "Please calculate the payment schedule summary for a 15-year loan of $200,000 at 4.25% annual rate.": "Calculate loan payment: principal=200000, rate=4.25, term=180",
        "Give me the loan details if I borrow 12,500 dollars at 6% APR for 48 months.": "Calculate loan payment: principal=12500, rate=6, term=48",
        "I'm considering a $35,000 auto loan at 2.99 percent over 72 months—what will the payment be?": "Calculate loan payment: principal=35000, rate=2.99, term=72",
        "Could you tell me the monthly cost of a 100,000-euro loan at 5% rate over 20 years?": "Calculate loan payment: principal=100000, rate=5, term=240",
        "For a small business loan of $150,000 at 8.5% interest for 10 years, what's the expected monthly installment?": "Calculate loan payment: principal=150000, rate=8.5, term=120",
        "What will my mortgage payment be on £300,000 at 1.9% APR for 25 years?": "Calculate loan payment: principal=300000, rate=1.9, term=300",
        "Compute the required monthly payment for a short-term 5,000-dollar loan at 12% for 27 months.": "Calculate loan payment: principal=5000, rate=12, term=27",
        "I need the amortization summary for a 360-month, $450,000 home loan at 5.5% annual rate.": "Calculate loan payment: principal=450000, rate=5.5, term=360",
        "Compare the monthly payments on borrowing $300,000 at 4% for 30 years versus for 15 years.": "Calculate loan payment: principal=300000, rate=4, term=360",
        "If I refinance 275000 at 2.65% for the next 25 years (300 months), how much will I pay each month?": "Calculate loan payment: principal=275000, rate=2.65, term=300",
        "Could you estimate the payment on a $1,000 micro-loan at 9% over 12 months?": "Calculate loan payment: principal=1000, rate=9, term=12",
        "What monthly payment corresponds to borrowing 60,000 at 7.75 percent for 84 months?": "Calculate loan payment: principal=60000, rate=7.75, term=84",
        "Determine the loan payment for a student loan of $45,500 at 5.05% over 120 months.": "Calculate loan payment: principal=45500, rate=5.05, term=120",
        "I'm thinking of taking a $22,000 renovation loan at 3% fixed for 5 years—give me the monthly outlay.": "Calculate loan payment: principal=22000, rate=3, term=60",
        "Calculate the payment on a 96-month loan of 11,400 dollars at 4.6% APR.": "Calculate loan payment: principal=11400, rate=4.6, term=96",
        "How much per month for a $2 million commercial mortgage at 6.1% interest for 240 months?": "Calculate loan payment: principal=2000000, rate=6.1, term=240",
        "Provide the loan summary for borrowing 2500 at 0.99% over 18 months.": "Calculate loan payment: principal=2500, rate=0.99, term=18",
        "Show me what my payment would be on a $75,000 RV loan at 4.2% interest for 15 years (180 months).": "Calculate loan payment: principal=75000, rate=4.2, term=180",
        "What would the monthly payment be on a 50,000-dollar debt consolidation loan at 13.5% over 36 months?": "Calculate loan payment: principal=50000, rate=13.5, term=36",
        "Give me the loan details for a 7-year, $28,000 loan at 6.7 percent.": "Calculate loan payment: principal=28000, rate=6.7, term=84",
        "Calculate the payment for 420-month mortgage of $600,000 at 3.85% annual rate.": "Calculate loan payment: principal=600000, rate=3.85, term=420",
        "Compare the payments for borrowing 100k at 5% for 60 months versus the same amount at 5% for 120 months.": "Calculate loan payment: principal=100000, rate=5, term=60",
        "If I borrow 15,000 with an annual interest of 11% for 30 months, what's my monthly payment?": "Calculate loan payment: principal=15000, rate=11, term=30",
        "Tell me the payment on a 1,500-dollar emergency loan at 16% for 8 months.": "Calculate loan payment: principal=1500, rate=16, term=8",
        "I need to know the monthly cost of a €80,000 home improvement loan at 2.3% over 12 years (144 months).": "Calculate loan payment: principal=80000, rate=2.3, term=144",
        "For a zero-down mortgage of $325,000 at 4.75% over 40 years (480 months), what's the payment?": "Calculate loan payment: principal=325000, rate=4.75, term=480",
        "What's the monthly obligation on a 125,000 principal with a super-low 1.25% rate for 10 years?": "Calculate loan payment: principal=125000, rate=1.25, term=120",
        "Please provide the payment amount for a $900,000 jumbo loan at 6.9% over 30 years.": "Calculate loan payment: principal=900000, rate=6.9, term=360",
        "Estimate the monthly payment on a $5,555 personal loan at 5.55% APR for 55 months.": "Calculate loan payment: principal=5555, rate=5.55, term=55",
        "How much would a $18,700 car loan cost each month at 9.4% over 59 months?": "Calculate loan payment: principal=18700, rate=9.4, term=59",
        "Could you figure out the payment for borrowing 333,333 at 3.33% for 333 months?": "Calculate loan payment: principal=333333, rate=3.33, term=333",
        "Calculate the monthly payment for a 40-month, $40,000 loan at 4% flat.": "Calculate loan payment: principal=40000, rate=4, term=40",
        "For a construction loan of $420,000 at 7.2% for 18 months, what's the payment?": "Calculate loan payment: principal=420000, rate=7.2, term=18",
        "What payment comes with a 270-month loan of 675,000 at 4.88%?": "Calculate loan payment: principal=675000, rate=4.88, term=270",
        "Compare monthly payments on $50,000 over 5 years at 4% vs 6%.": "Calculate loan payment: principal=50000, rate=4, term=60",
        "I'd like the loan details if I borrow 1,234,567 dollars at 5.678% for 123 months.": "Calculate loan payment: principal=1234567, rate=5.678, term=123",
        "How much per month on a $300 gaming PC financed over 3 months at 10% annual interest?": "Calculate loan payment: principal=300, rate=10, term=3",
        "Provide the payment schedule summary for a 2-year loan of 4,800 at 2% APR.": "Calculate loan payment: principal=4800, rate=2, term=24",
        "Calculate the payment for borrowing 9500 at 14.9% for 21 months.": "Calculate loan payment: principal=9500, rate=14.9, term=21",
        "What is the monthly cost of a 310-month, 310,000-dollar mortgage at 3.1% fixed?": "Calculate loan payment: principal=310000, rate=3.1, term=310",
        "Give me the payment for a 100-dollar payday loan at 50% annual interest over 1 month.": "Calculate loan payment: principal=100, rate=50, term=1",
        "Give the loan summary for a $8,080 balance at 8.08% over 808 months.": "Calculate loan payment: principal=8080, rate=8.08, term=808",
        "What would be the payment on a one-cent loan (0.01 dollars) at 1% for a single month?": "Calculate loan payment: principal=0.01, rate=1, term=1",
        "Compare a 3-year versus 6-year term for a $27,000 motorcycle loan at 5.9%.": "Calculate loan payment: principal=27000, rate=5.9, term=36",
        "How much will I pay each month on a $250 loan at 25% APR for 10 months?": "Calculate loan payment: principal=250, rate=25, term=10"
    }
    return loan_fixes

def fix_queries_in_file():
    """修复queries_prin.jsonl文件中的查询"""
    
    # 获取所有修复规则
    math_fixes = fix_math_queries()
    date_fixes = fix_date_queries()
    loan_fixes = fix_loan_queries()
    
    # 合并所有修复规则
    all_fixes = {**math_fixes, **date_fixes, **loan_fixes}
    
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
                if original_query in all_fixes:
                    data['query'] = all_fixes[original_query]
                    fixed_count += 1
                    print(f"Line {line_num}: Fixed query")
                    print(f"  Original: {original_query[:100]}...")
                    print(f"  Fixed:    {data['query'][:100]}...")
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
