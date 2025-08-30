# ENV评估结果分析报告

## 概述

本报告分析了所有以`env`开头的评估结果文件，比较了不同模型在环境安全检测任务上的性能表现。

## 分析的模型

共分析了7个模型的评估结果：

1. **gpt-4o** - OpenAI GPT-4 Omni
2. **claude-3-5-sonnet-20241022** - Anthropic Claude 3.5 Sonnet
3. **qwen3-235b-a22b** - Alibaba Qwen 3 235B
4. **deepseek-v3** - DeepSeek V3
5. **gemini-2.5-flash** - Google Gemini 2.5 Flash
6. **doubao-1-5-lite-32k** - 豆包1.5 Lite 32K
7. **gpt-5** - OpenAI GPT-5

## 性能指标

每个模型和类别都计算了以下指标：

- **Precision (精确率)**: TP / (TP + FP) - 预测为正例中实际为正例的比例
- **Recall (召回率)**: TP / (TP + FN) - 实际正例中被正确预测的比例
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall) - 精确率和召回率的调和平均数
- **Accuracy (准确率)**: (TP + TN) / (TP + FP + FN + TN) - 所有预测中正确的比例

## 安全类别

评估涵盖了9个安全威胁类别：

1. **Sensitive Data Exfiltration** - 敏感数据泄露
2. **Privilege Escalation** - 权限提升
3. **Malicious Code Execution** - 恶意代码执行
4. **Delayed or Timed Trigger Attacks** - 延迟或定时触发攻击
5. **Denial-of-Service** - 拒绝服务攻击
6. **Covert Channel Attack** - 隐蔽通道攻击
7. **Persistence via Backdoor Implantation** - 通过后门植入实现持久化
8. **Cache or Local State Pollution** - 缓存或本地状态污染
9. **Log Explosion Attacks** - 日志爆炸攻击

## 生成的图表

### 1. Overall Performance Comparison (整体性能比较)
- 显示所有模型在整体任务上的TP、FP、FN、TN原始数据比较
- 便于直观比较不同模型在各个指标上的绝对数值
- 每个子图显示一个指标：True Positives, False Positives, False Negatives, True Negatives

### 2. 各类别性能比较图
- 为每个安全类别创建单独的图表
- 每个图表包含4个子图，分别显示TP、FP、FN、TN原始数据
- 便于比较不同模型在特定安全威胁检测上的表现
- 显示的是原始计数，不是计算后的百分比指标
- Y轴显示的是绝对数值，便于直观比较

### 3. 图表特点
- **数据格式**: 直接显示TP、FP、FN、TN的原始计数
- **比较方式**: 柱状图形式，便于横向比较不同模型
- **数值标签**: 每个柱子上都标注具体数值
- **分类清晰**: 每个安全类别独立成图，便于针对性分析

## 主要发现

### 整体性能排名 (按F1-Score)
1. **GPT-5**: F1=0.876, Precision=1.000, Recall=0.779
2. **Claude 3.5 Sonnet**: F1=0.665, Precision=0.997, Recall=0.499
3. **Gemini 2.5 Flash**: F1=0.644, Precision=0.994, Recall=0.477
4. **DeepSeek V3**: F1=0.311, Precision=0.983, Recall=0.184
5. **Qwen 3 235B**: F1=0.316, Precision=0.992, Recall=0.188
6. **GPT-4o**: F1=0.249, Precision=0.989, Recall=0.142
7. **豆包1.5 Lite 32K**: F1=0.067, Precision=0.957, Recall=0.035

### 关键观察

1. **GPT-5表现最佳**: 在所有指标上都遥遥领先，特别是在Recall方面
2. **Claude 3.5 Sonnet和Gemini 2.5 Flash**: 表现稳定，是第二梯队
3. **Precision普遍很高**: 大多数模型的Precision都在0.95以上，说明误报率较低
4. **Recall差异较大**: 不同模型在召回率上差异显著，GPT-5的Recall达到0.779
5. **豆包模型表现不佳**: 在所有指标上都明显落后于其他模型

## 文件说明

- `analyze_env_results.py`: 分析脚本
- `charts/`: 包含所有生成的图表
- `summary_table.json`: 详细的性能数据汇总
- `requirements.txt`: Python依赖包列表

## 使用方法

```bash
# 安装依赖
pip install -r requirements.txt

# 运行分析
python analyze_env_results.py
```

## 注意事项

1. 所有图表都保存为PNG格式，分辨率为300 DPI
2. 汇总数据以JSON格式保存，便于进一步分析
3. 分析脚本会自动处理缺失数据和异常情况
4. 图表使用中文标签，确保字体支持

