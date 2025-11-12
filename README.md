## MCP-RiskCue

### Project Overview
MCP-RiskCue accompanies the paper “Evaluating LLMs for Risk Inference from System Logs” (https://arxiv.org/pdf/2511.05867). The repository packages everything needed to reproduce our benchmark and experiments.

Key components:
- `Environment/`: curated pools of system logs.
- `Client/`: the MCP client used to query servers and collect responses.
- `Evaluator/`: scoring scripts for quantitative evaluation.
- `Figures/`: plotting utilities for visualizing metrics.
- `Data/`: training and test splits (`train.jsonl`, `test.jsonl`) plus generation scripts.
- `Servers/`: minimal MCP servers for simulation.
- `Prompts/`: prompt templates used throughout the pipeline.

### Setup
- Use Python 3.9 or newer.
- Create and activate a virtual environment.
- Install dependencies such as `pandas`, `numpy`, and `matplotlib` as required by individual modules.
- Populate the `.env` file with the necessary API keys and secrets.

### Evaluating a Model
Inside `Model_output_rx/`, run either `python pipeline_local.py` for locally hosted models or `python pipeline_remote.py` for remote endpoints. See the script docstrings for optional flags.

### Training Guidance
We recommend applying a reinforcement-learning framework to the training split in `Data/` and reusing the provided scripts for logging and evaluation. In our project, we use the slime framework: https://github.com/PorUna-byte/slime

### Benchmark Construction (already completed)
The benchmark artifacts in this repository are pre-built. If you need to regenerate them:
1. From `Servers/`, run `collate.py` to assemble server descriptions.
2. From `Data/`, run `query_generator.py` to create per-server queries.
3. From `Data/`, run `history_generator.py` to synthesize dialogue histories.
4. From `Data/`, run `curate_train_test.py` to split the histories into train/test sets.
5. From `Data/`, run `data_format.py` to finalize the dataset layout.

