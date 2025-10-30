## MCP-Guard

### 项目简介
MCP-Guard 是一个用于在“模型调用协议 (Model Context Protocol, MCP)”环境下评测与分析多种模型表现的实验框架。项目包含：
- 数据集与环境定义（Environment/）
- 客户端与模型管理（Client/）
- 评测脚本（Evaluator/）
- 可视化与统计生成脚本（Figures/）

支持对 Rewards 与 Response Length 等指标进行收集、聚合（多次实验取均值与总体标准差），并输出曲线与统计表。

### 目录结构（简要）
- `Client/`：模型客户端与模型管理器（如 `client.py`, `model_manager.py`）
- `Environment/`：实验环境与配置（如各模型的 `*_env_info.json`、`environment.py`）
- `Evaluator/`：评测逻辑（如 `env_risk_eval.py`）
- `Figures/`：绘图与统计脚本，以及输出图表与CSV
  - `plot_rewards_curve.py`：读取 `rewards_curve_{r1,r2,r3}.csv`，绘制各模型 Rewards 均值与标准差曲线
  - `plot_reslen_curve.py`：读取 `reslen_{r1,r2,r3}.csv`，绘制各模型 Response Length 均值与标准差曲线
  - `generate_rewards_stats.py`：对三次实验的 Rewards 逐 step 计算均值、总体标准差并输出 `rewards_curve.txt`
  - `generate_reslen_stats.py`：对三次实验的 Response Length 逐 step 计算均值、总体标准差并输出 `reslen_curve.txt`
  - 生成的图表：`MCPenv_rewards_curve.{pdf,png}`、`MCPenv_response_length_curve.{pdf,png}` 等
- `Model_output_r{1,2,3}/`：每次实验的输出与评测结果
- `Utils/`：通用工具函数（`utils.py`）

### 环境依赖
- Python 3.9+
- 推荐创建虚拟环境
- 依赖包（按需安装）：
  - pandas
  - numpy
  - matplotlib

安装示例：
```bash
pip install pandas numpy matplotlib
```

### 数据与输入
- 三次重复实验的聚合输入位于 `Figures/` 目录：
  - Rewards CSV：`rewards_curve_r1.csv`, `rewards_curve_r2.csv`, `rewards_curve_r3.csv`
  - Response Length CSV：`reslen_r1.csv`, `reslen_r2.csv`, `reslen_r3.csv`
- CSV 列命名约定：
  - `eval/step`：评估步数
  - `"<ModelName> - eval/MCPenv_rewards"`：各模型在 MCP 环境下的 rewards（0-1）
  - `"<ModelName> - eval/MCPenv_response_lengths"`：各模型响应长度
  - 同名列伴随 `__MIN/__MAX` 表示该统计量的区间（绘图与统计时会自动忽略带 `__` 的列）

### 可视化
在 `Figures/` 目录执行：
```bash
# 绘制 Rewards 曲线（均值+标准差阴影带）
python plot_rewards_curve.py
# 输出：MCPenv_rewards_curve.pdf / .png

# 绘制 Response Length 曲线（均值+标准差阴影带）
python plot_reslen_curve.py
# 输出：MCPenv_response_length_curve.pdf / .png
```
说明：
- 两个绘图脚本均会从三份 CSV 中逐 step 聚合，采用“可用数据点”的均值与总体标准差（np.std, ddof=0）。
- 若某一步骤缺失数据，则仅使用该步骤存在的数据点进行统计。

### 逐步统计（文本表）
在 `Figures/` 目录执行：
```bash
# 生成各模型在每个 step 的 Rewards 均值与总体标准差（以及样本数）
python generate_rewards_stats.py
# 输出：rewards_curve.txt

# 生成各模型在每个 step 的 Response Length 均值与总体标准差（以及样本数）
python generate_reslen_stats.py
# 输出：reslen_curve.txt
```
文本文件包含：
- Step：评估步数
- Mean：三次实验的均值（只基于有效数据点）
- Std：总体标准差（ddof=0）
- Count：该 step 的有效数据点个数
- Mean±Std：展示友好的均值±标准差格式

### 实验与评测（简要）
项目还包含完整的环境定义与多模型评测流程（详见 `Environment/`、`Client/`、`Evaluator/`）：
- 在 `Environment/` 中配置具体评测环境、系统提示与样例
- 通过 `Client/` 里的客户端与模型管理器接入不同模型
- 运行评测脚本（如 `Evaluator/env_risk_eval.py` 或各 `Model_output_r*/` 的 pipeline 脚本）生成原始输出与评测指标

### 结果解读建议
- 对于 Rewards（0-1）：
  - 越高越好；可关注曲线随 step 的提升与收敛情况
- 对于 Response Length：
  - 表征模型在任务中的输出长度；结合任务性质与质量指标共同分析
- 多次实验的标准差越小，表示稳定性越好

### 常见问题（FAQ）
- 问：某些 step 缺失数据怎么办？
  - 答：聚合时仅基于该 step 存在的数据点计算均值与总体标准差；Count 字段会显示该步的有效样本数。
- 问：标准差为何使用总体标准差？
  - 答：我们在描述当前三次实验的离散程度，因此默认使用 `np.std`（ddof=0）。如需样本标准差，可自行将脚本中的 `np.std(x)` 改为 `np.std(x, ddof=1)`。

### 许可
本仓库未附带许可证文件。如需开源分发或商用，请先补充或确认许可证策略。

### 联系方式
如有问题或建议，欢迎提交 Issue 或 PR。
