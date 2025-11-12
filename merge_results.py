#!/usr/bin/env python3
"""
Analysis script for model evaluation results.
Analyzes env_eval_results and prin_eval_results files to generate performance statistics and visualizations.
Modified to merge results from two experimental runs (Model_output_r1 and Model_output_r2).
"""

import json
import os
import glob
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from typing import Dict, List, Tuple
import numpy as np
import shutil

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configure matplotlib to use a font that supports Unicode circled characters
# This prevents warnings about missing glyphs when saving PDFs
matplotlib.rcParams['pdf.fonttype'] = 42  # Use TrueType fonts (supports Unicode)
matplotlib.rcParams['ps.fonttype'] = 42   # Use TrueType fonts for PostScript too
# Try to use DejaVu Sans which supports circled Unicode characters
try:
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
except:
    # If DejaVu Sans is not available, matplotlib will use the default
    pass

# Suppress warnings about missing glyphs when saving PDFs
# The font configuration above should handle this, but this is a fallback
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*missing from current font.*')


class ExperimentMerger:
    """Class to merge and analyze results from two experimental runs."""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.r1_dir = os.path.join(base_dir, "Model_output_r1", "evaluation")
        self.r2_dir = os.path.join(base_dir, "Model_output_r2", "evaluation")
        self.r3_dir = os.path.join(base_dir, "Model_output_r3", "evaluation")
        self.figures_dir = os.path.join(base_dir, "Figures")
        
        # Create Figures directory if it doesn't exist
        os.makedirs(self.figures_dir, exist_ok=True)
    
    def load_csv_data(self, run_dir: str, subdir: str, filename: str) -> pd.DataFrame:
        """Load CSV data from a specific run and subdirectory."""
        file_path = os.path.join(run_dir, subdir, filename)
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            print(f"Warning: File {file_path} does not exist")
            return pd.DataFrame()
    
    def merge_env_results(self) -> pd.DataFrame:
        """Merge environment analysis results from three runs."""
        # Load data from all three runs
        r1_local = self.load_csv_data(self.r1_dir, "local", "env_analysis_results.csv")
        r1_remote = self.load_csv_data(self.r1_dir, "remote", "env_analysis_results.csv")
        r2_local = self.load_csv_data(self.r2_dir, "local", "env_analysis_results.csv")
        r2_remote = self.load_csv_data(self.r2_dir, "remote", "env_analysis_results.csv")
        r3_local = self.load_csv_data(self.r3_dir, "local", "env_analysis_results.csv")
        r3_remote = self.load_csv_data(self.r3_dir, "remote", "env_analysis_results.csv")
        
        # Add source identifier to distinguish local vs remote
        r1_local['Source'] = 'local'
        r1_remote['Source'] = 'remote'
        r2_local['Source'] = 'local'
        r2_remote['Source'] = 'remote'
        r3_local['Source'] = 'local'
        r3_remote['Source'] = 'remote'
        
        # Combine local and remote data for each run
        r1_data = pd.concat([r1_local, r1_remote], ignore_index=True)
        r2_data = pd.concat([r2_local, r2_remote], ignore_index=True)
        r3_data = pd.concat([r3_local, r3_remote], ignore_index=True)
        
        # Add run identifier
        r1_data['Run'] = 'r1'
        r2_data['Run'] = 'r2'
        r3_data['Run'] = 'r3'
        
        # Combine all runs
        combined_data = pd.concat([r1_data, r2_data, r3_data], ignore_index=True)
        
        # Calculate statistics
        merged_results = []
        
        for (model, source) in combined_data[['Model', 'Source']].drop_duplicates().values:
            model_data = combined_data[
                (combined_data['Model'] == model) & 
                (combined_data['Source'] == source)
            ]
            
            if len(model_data) == 3:  # All three runs have data for this model-source combination
                # Calculate mean and std for each metric
                metrics = ['TP', 'FP', 'FN', 'TN', 'Valid_Count', 'Accuracy', 'Precision', 'Recall']
                result = {'Model': model, 'Source': source}
                
                for metric in metrics:
                    values = model_data[metric].values
                    mean_val = np.mean(values)
                    std_val = np.std(values, ddof=0) if len(values) > 1 else 0
                    result[f'{metric}_mean'] = mean_val
                    result[f'{metric}_std'] = std_val
                
                merged_results.append(result)
        
        return pd.DataFrame(merged_results)
    
    def merge_per_type_results(self) -> pd.DataFrame:
        """Merge per-type analysis results from three runs."""
        # Load data from all three runs
        r1_local = self.load_csv_data(self.r1_dir, "local", "per_type_analysis_results.csv")
        r1_remote = self.load_csv_data(self.r1_dir, "remote", "per_type_analysis_results.csv")
        r2_local = self.load_csv_data(self.r2_dir, "local", "per_type_analysis_results.csv")
        r2_remote = self.load_csv_data(self.r2_dir, "remote", "per_type_analysis_results.csv")
        r3_local = self.load_csv_data(self.r3_dir, "local", "per_type_analysis_results.csv")
        r3_remote = self.load_csv_data(self.r3_dir, "remote", "per_type_analysis_results.csv")
        
        # Add source identifier to distinguish local vs remote
        r1_local['Source'] = 'local'
        r1_remote['Source'] = 'remote'
        r2_local['Source'] = 'local'
        r2_remote['Source'] = 'remote'
        r3_local['Source'] = 'local'
        r3_remote['Source'] = 'remote'
        
        # Add run identifier
        r1_local['Run'] = 'r1'
        r1_remote['Run'] = 'r1'
        r2_local['Run'] = 'r2'
        r2_remote['Run'] = 'r2'
        r3_local['Run'] = 'r3'
        r3_remote['Run'] = 'r3'
        
        # Combine all data
        combined_data = pd.concat([r1_local, r1_remote, r2_local, r2_remote, r3_local, r3_remote], ignore_index=True)
        
        # Calculate statistics
        merged_results = []
        
        for (model, risk_type, source) in combined_data[['Model', 'Risk_Type', 'Source']].drop_duplicates().values:
            model_risk_data = combined_data[
                (combined_data['Model'] == model) & 
                (combined_data['Risk_Type'] == risk_type) &
                (combined_data['Source'] == source)
            ]
            
            if len(model_risk_data) == 3:  # All three runs have data for this model-risk-source combination
                # Calculate mean and std for each metric
                metrics = ['TP', 'FP', 'FN']
                result = {
                    'Model': model,
                    'Risk_Type': risk_type,
                    'Source': source
                }
                
                for metric in metrics:
                    values = model_risk_data[metric].values
                    mean_val = np.mean(values)
                    # Always use population std (ddof=0) regardless of number of data points
                    if len(values) > 1:
                        std_val = np.std(values, ddof=0)
                    else:
                        std_val = 0
                    result[f'{metric}_mean'] = mean_val
                    result[f'{metric}_std'] = std_val
                
                merged_results.append(result)
        
        return pd.DataFrame(merged_results)
    
    def parse_model_name(self, model_name: str) -> Tuple[str, str]:
        """Parse model name to extract base model and training type."""
        # Expected formats: vanilla_model, sft_model, grpo_model
        if model_name.startswith('sft_'):
            return model_name[4:], 'sft'
        elif model_name.startswith('grpo_'):
            return model_name[5:], 'grpo'
        else:
            return model_name, 'vanilla'
    
    def _circled_number(self, n: int) -> str:
        """Return circled number ①..⑳ when possible, else (n)."""
        base = 0x2460
        if 1 <= n <= 20:
            try:
                return chr(base + n - 1)
            except Exception:
                return f"({n})"
        return f"({n})"
    
    def _simplify_model_name(self, model_name: str) -> str:
        """Simplify model name for remote models.
        - For GPT series: take first two parts after splitting by '-'
        - For others: take only the first part
        """
        parts = model_name.split('-')
        if len(parts) == 0:
            return model_name
        
        # Check if it's a GPT model (starts with 'gpt')
        if parts[0].lower().startswith('gpt'):
            # Take first two parts
            return '-'.join(parts[:2]) if len(parts) >= 2 else parts[0]
        else:
            # Take only first part
            return parts[0]
    
    def generate_level1_table(self, env_results: pd.DataFrame):
        """Generate level1_table.txt with mean values and standard deviations."""
        # Function to format model name for LaTeX
        def format_model_name(name):
            """Replace hyphens and underscores with LaTeX-safe versions."""
            return name.replace('-', '\\textendash ').replace('_', '\\textendash ')
        
        # Function to parse model name
        def parse_model_name(model_name):
            if model_name.startswith('sft_'):
                return model_name[4:], 'sft'
            elif model_name.startswith('grpo_'):
                return model_name[5:], 'grpo'
            else:
                return model_name, 'vanilla'
        
        # Group models by source (local vs remote)
        local_groups = {}
        remote_models = []
        
        for _, row in env_results.iterrows():
            base_name, train_type = parse_model_name(row['Model'])
            source = row['Source']
            
            if source == 'local':
                if base_name not in local_groups:
                    local_groups[base_name] = {}
                local_groups[base_name][train_type] = row
            else:  # source == 'remote'
                remote_models.append(row)
        
        # Start building LaTeX table
        latex_lines = []
        latex_lines.append(r"\begin{table}")
        latex_lines.append(r"\caption{Performance of local and remote models on Level-1 risk detection (mean ± std).}")
        latex_lines.append(r"\label{tab:level1}")
        latex_lines.append(r"  \centering")
        latex_lines.append(r"  \small")
        latex_lines.append(r"  \begin{tabular}{")
        latex_lines.append(r"    l l")
        latex_lines.append(r"    S[table-format=3] % TP")
        latex_lines.append(r"    S[table-format=3] % FP")
        latex_lines.append(r"    S[table-format=3] % FN")
        latex_lines.append(r"    S[table-format=3] % TN")
        latex_lines.append(r"    S[table-format=1.2] % Acc")
        latex_lines.append(r"    S[table-format=1.2] % Prec")
        latex_lines.append(r"    S[table-format=1.2] % Rec")
        latex_lines.append(r"  }")
        latex_lines.append(r"    \toprule")
        latex_lines.append(r"    \multicolumn{1}{c}{Models} & \multicolumn{1}{c}{} &")
        latex_lines.append(r"    \multicolumn{1}{c}{TP~($\uparrow$)} &")
        latex_lines.append(r"    \multicolumn{1}{c}{FP~($\downarrow$)} &")
        latex_lines.append(r"    \multicolumn{1}{c}{FN~($\downarrow$)} &")
        latex_lines.append(r"    \multicolumn{1}{c}{TN~($\uparrow$)} &")
        latex_lines.append(r"    \multicolumn{1}{c}{Acc.~($\uparrow$)} &")
        latex_lines.append(r"    \multicolumn{1}{c}{Prec.~($\uparrow$)} &")
        latex_lines.append(r"    \multicolumn{1}{c}{Rec.~($\uparrow$)} \\")
        latex_lines.append(r"    \midrule")
        latex_lines.append("")
        latex_lines.append(r"    % ===== Local =====")
        
        # Order of local models
        local_order = [
            'Qwen3-4B-Instruct',
            'Llama3.1-8B-Instruct',
            'DeepSeek-R1-0528-Qwen3-8B',
            'Qwen3Guard-Gen-4B',
            'Llama-Guard-3-8B'
        ]
        
        # Add local models
        for base_name in local_order:
            if base_name not in local_groups:
                continue
            
            group = local_groups[base_name]
            train_types = ['vanilla', 'sft', 'grpo']
            available_types = [t for t in train_types if t in group]
            
            if not available_types:
                continue
            
            # Format model name for LaTeX
            latex_model_name = format_model_name(base_name)
            
            latex_lines.append(f"    % ===== {base_name} =====")
            latex_lines.append(f"    \\multirow{{{len(available_types)}}}{{*}}{{{latex_model_name}}}")
            
            # Find best accuracy for this group
            best_acc = max(group[t]['Accuracy_mean'] for t in available_types)
            
            for i, train_type in enumerate(available_types):
                row = group[train_type]
                acc_mean = row['Accuracy_mean']
                acc_std = row['Accuracy_std']
                acc_str = f"\\textbf{{\\num{{{acc_mean:.2f} \\pm {acc_std:.2f}}}}}" if acc_mean == best_acc else f"\\num{{{acc_mean:.2f} \\pm {acc_std:.2f}}}"
                prec_str = f"\\num{{{row['Precision_mean']:.2f} \\pm {row['Precision_std']:.2f}}}"
                rec_str = f"\\num{{{row['Recall_mean']:.2f} \\pm {row['Recall_std']:.2f}}}"
                
                if i == 0:
                    line = f"      & {train_type} & \\num{{{row['TP_mean']:.0f} \\pm {row['TP_std']:.0f}}}  & \\num{{{row['FP_mean']:.0f} \\pm {row['FP_std']:.0f}}}   & \\num{{{row['FN_mean']:.0f} \\pm {row['FN_std']:.0f}}}   & \\num{{{row['TN_mean']:.0f} \\pm {row['TN_std']:.0f}}}  & {acc_str} & {prec_str} & {rec_str} \\\\"
                else:
                    line = f"      & {train_type}  & \\num{{{row['TP_mean']:.0f} \\pm {row['TP_std']:.0f}}} & \\num{{{row['FP_mean']:.0f} \\pm {row['FP_std']:.0f}}} & \\num{{{row['FN_mean']:.0f} \\pm {row['FN_std']:.0f}}}   & \\num{{{row['TN_mean']:.0f} \\pm {row['TN_std']:.0f}}}  & {acc_str} & {prec_str} & {rec_str} \\\\"
                latex_lines.append(line)
            
            latex_lines.append(r"    \midrule")
            latex_lines.append("")
        
        # Add remote models section
        latex_lines.append(r"    % ===== Remote (API) =====")
        latex_lines.append("")
        
        # Find best accuracy for remote models
        if remote_models:
            remote_best_acc = max(row['Accuracy_mean'] for row in remote_models)
            
            # Add remote models
            for row in remote_models:
                model_name = format_model_name(row['Model'])
                acc_mean = row['Accuracy_mean']
                acc_std = row['Accuracy_std']
                acc_str = f"\\textbf{{\\num{{{acc_mean:.2f} \\pm {acc_std:.2f}}}}}" if acc_mean == remote_best_acc else f"\\num{{{acc_mean:.2f} \\pm {acc_std:.2f}}}"
                prec_str = f"\\num{{{row['Precision_mean']:.2f} \\pm {row['Precision_std']:.2f}}}"
                rec_str = f"\\num{{{row['Recall_mean']:.2f} \\pm {row['Recall_std']:.2f}}}"
                
                line = f"    {model_name} & --- & \\num{{{row['TP_mean']:.0f} \\pm {row['TP_std']:.0f}}}  & \\num{{{row['FP_mean']:.0f} \\pm {row['FP_std']:.0f}}}  & \\num{{{row['FN_mean']:.0f} \\pm {row['FN_std']:.0f}}}  & \\num{{{row['TN_mean']:.0f} \\pm {row['TN_std']:.0f}}}  & {acc_str} & {prec_str} & {rec_str} \\\\"
                latex_lines.append(line)
        
        latex_lines.append(r"    \bottomrule")
        latex_lines.append(r"  \end{tabular}")
        latex_lines.append("")
        latex_lines.append(r"\end{table}")
        
        # Write to file
        output_file = os.path.join(self.figures_dir, "level1_table.txt")
        with open(output_file, 'w') as f:
            f.write('\n'.join(latex_lines))
        
        print(f"\n✓ LaTeX table saved to {output_file}")
    
    def generate_per_type_plots(self, per_type_results: pd.DataFrame):
        """Generate per-type performance plots with mean values and standard deviations."""
        # Generate plots for both local and remote models based on Source column
        for source in ['local', 'remote']:
            # Filter data for this source
            source_data = per_type_results[per_type_results['Source'] == source]
            
            if source_data.empty:
                continue
            
            # Convert mean data back to original format for plotting
            plot_data = self._convert_to_plot_format(source_data)
            
            # Use original plotting logic
            self._create_per_type_plots_original(plot_data, source)
    
    def _convert_to_plot_format(self, data: pd.DataFrame) -> pd.DataFrame:
        """Convert mean/std data back to original format for plotting."""
        plot_data = []
        
        for _, row in data.iterrows():
            # Create rows for TP, FP, FN using mean values
            plot_data.append({
                'Model': row['Model'],
                'Risk_Type': row['Risk_Type'],
                'TP': row['TP_mean'],
                'FP': row['FP_mean'],
                'FN': row['FN_mean'],
                'TP_std': row['TP_std'],
                'FP_std': row['FP_std'],
                'FN_std': row['FN_std']
            })
        
        return pd.DataFrame(plot_data)
    
    def _create_per_type_plots_original(self, df: pd.DataFrame, model_type: str):
        """Create per-type performance plots using original logic."""
        # Check if models have vanilla/sft/grpo grouping
        has_grouping = any(
            model.startswith('sft_') or model.startswith('grpo_') 
            for model in df['Model'].unique()
        )
        
        if has_grouping:
            # Local models: group by vanilla/sft/grpo
            self._create_per_type_plot_grouped_original(df, model_type)
        else:
            # Remote models: no grouping
            self._create_per_type_plot_simple_original(df, model_type)
    
    def _create_per_type_plot_grouped_original(self, df: pd.DataFrame, model_type: str):
        """Create grouped heatmaps for models with vanilla/sft/grpo structure using original logic."""
        # Prepare grouped data for heatmap
        grouped_data_tp = {}
        grouped_data_fp = {}
        grouped_data_fn = {}
        
        for _, row in df.iterrows():
            base_name, train_type = self.parse_model_name(row['Model'])
            if base_name not in grouped_data_tp:
                grouped_data_tp[base_name] = {'vanilla': {}, 'sft': {}, 'grpo': {}}
                grouped_data_fp[base_name] = {'vanilla': {}, 'sft': {}, 'grpo': {}}
                grouped_data_fn[base_name] = {'vanilla': {}, 'sft': {}, 'grpo': {}}
            grouped_data_tp[base_name][train_type][row['Risk_Type']] = row['TP']
            grouped_data_fp[base_name][train_type][row['Risk_Type']] = row['FP']
            grouped_data_fn[base_name][train_type][row['Risk_Type']] = row['FN']
        
        # Get all risk types
        risk_types = sorted(df['Risk_Type'].unique())
        
        # Prepare data for all heatmaps
        new_columns = []
        tp_data = {}
        fp_data = {}
        fn_data = {}
        col_labels = []
        
        # Define the specific order for groups
        group_order = [
            'Qwen3-4B-Instruct',
            'Llama3.1-8B-Instruct', 
            'DeepSeek-R1-0528-Qwen3-8B',
            'Qwen3Guard-Gen-4B',
            'Llama-Guard-3-8B'
        ]
        
        # Filter to only include models that exist in the data
        ordered_base_names = [name for name in group_order if name in grouped_data_tp.keys()]
        # Add any remaining models not in the predefined order
        remaining_models = [name for name in sorted(grouped_data_tp.keys()) if name not in group_order]
        ordered_base_names.extend(remaining_models)
        
        for base_name in ordered_base_names:
            group_tp = grouped_data_tp[base_name]
            group_fp = grouped_data_fp[base_name]
            group_fn = grouped_data_fn[base_name]
            for train_type in ['vanilla', 'sft', 'grpo']:
                if group_tp[train_type]:  # If this training type exists
                    new_columns.append(train_type.upper())
                    col_labels.append((base_name, train_type))
                    for risk_type in risk_types:
                        if risk_type not in tp_data:
                            tp_data[risk_type] = []
                            fp_data[risk_type] = []
                            fn_data[risk_type] = []
                        tp_data[risk_type].append(group_tp[train_type].get(risk_type, 0))
                        fp_data[risk_type].append(group_fp[train_type].get(risk_type, 0))
                        fn_data[risk_type].append(group_fn[train_type].get(risk_type, 0))
        
        # Create the pivot DataFrames
        pivot_df_tp = pd.DataFrame(tp_data, index=new_columns).T
        pivot_df_fp = pd.DataFrame(fp_data, index=new_columns).T
        pivot_df_fn = pd.DataFrame(fn_data, index=new_columns).T
        
        # Create FN and FP heatmaps (as requested)
        for metric, pivot_df, cmap in [('FN', pivot_df_fn, 'YlOrRd'), ('FP', pivot_df_fp, 'OrRd')]:
            fig, ax = plt.subplots(figsize=(18, 9))
            
            # Create custom annotations with mean ± std (smaller font for std)
            annotations = []
            for i in range(len(risk_types)):
                row_annotations = []
                for j in range(len(new_columns)):
                    model = col_labels[j][0]
                    train_type = col_labels[j][1]
                    risk_type = risk_types[i]
                    
                    # Find the data for this combination
                    # Build full model name based on training type
                    if train_type == 'vanilla':
                        full_model_name = model
                    elif train_type == 'sft':
                        full_model_name = f'sft_{model}'
                    elif train_type == 'grpo':
                        full_model_name = f'grpo_{model}'
                    else:
                        full_model_name = model
                    
                    model_data = df[(df['Model'] == full_model_name) & (df['Risk_Type'] == risk_type)]
                    if len(model_data) > 0:
                        mean_val = model_data.iloc[0][f'{metric}']
                        std_val = model_data.iloc[0][f'{metric}_std']
                        # Format with smaller font for std part
                        row_annotations.append(f'{mean_val:.1f}±{std_val:.1f}')
                    else:
                        row_annotations.append('0.0±0.0')
                annotations.append(row_annotations)
            
            heatmap = sns.heatmap(pivot_df, annot=annotations, fmt='', cmap=cmap, ax=ax,
                       cbar_kws={'label': 'Count'}, linewidths=0, linecolor='white')
            
            # Modify annotation positions - mean on top, std at bottom
            for text in ax.texts:
                text_str = text.get_text()
                if '±' in text_str:
                    # Split the text and reposition
                    parts = text_str.split('±')
                    if len(parts) == 2:
                        # Get the original position
                        x, y = text.get_position()
                        # Hide the original text
                        text.set_text('')
                        # Add mean at the top (above center)
                        ax.text(x, y-0.2, parts[0], ha='center', va='center', 
                               fontsize=28, color=text.get_color())
                        # Add std at the bottom (below center)
                        ax.text(x, y+0.3, f'±{parts[1]}', ha='center', va='center', 
                               fontsize=24, color=text.get_color())
            
            # Set appropriate font sizes for better readability
            cbar = heatmap.collections[0].colorbar
            cbar.set_label('Count', fontsize=20, fontweight='bold')
            cbar.ax.tick_params(labelsize=20)
            ax.set_title(f'Per-Type Performance: {metric} ({model_type.title()})', fontsize=20, fontweight='bold')
            ax.set_ylabel('Risk Types', fontsize=20, fontweight='bold')
            ax.set_xlabel('', fontsize=20, fontweight='bold')
            ax.set_xticklabels(new_columns, rotation=0, fontsize=18)
            ax.tick_params(axis='y', labelsize=20)
            ax.tick_params(axis='y', which='major', labelsize=20)
            
            # Set bold font for y-axis tick labels
            for label in ax.get_yticklabels():
                label.set_fontweight('bold')
            
            # Replace risk type names with circled numbers ①②…
            circled_labels = [self._circled_number(i + 1) for i in range(len(risk_types))]
            ax.set_yticklabels(circled_labels, rotation=0, fontsize=30, fontweight='bold')
            
            # Calculate positions for model group labels and add vertical separators
            # Group consecutive columns by base model name
            groups = []
            current_base = None
            start_idx = 0
            
            for j, (base_name, train_type) in enumerate(col_labels):
                if base_name != current_base:
                    if current_base is not None:
                        groups.append((current_base, start_idx, j))
                    current_base = base_name
                    start_idx = j
            
            # Add the last group
            if current_base is not None:
                groups.append((current_base, start_idx, len(col_labels)))
            
            # Add vertical lines between different model groups
            for base_name, start_idx, end_idx in groups:
                if start_idx > 0:  # Don't add line before the first group
                    ax.axvline(x=start_idx, color='black', linewidth=3, alpha=1.0, zorder=10)

            # Add group labels below the x-axis
            group_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            for idx, (base_name, start_idx, end_idx) in enumerate(groups):
                # Calculate the center position for this group
                center_col = (start_idx + end_idx) / 2.0
                
                # Add group label below the x-axis labels
                group_label = group_labels[idx] if idx < len(group_labels) else f'{idx+1}'
                ax.text(center_col, 9.5, f'Group {group_label}', ha='center', va='top', 
                        fontsize=20, fontweight='bold', transform=ax.transData)

            plt.tight_layout()
            
            # Save plots
            output_file = os.path.join(self.figures_dir, f'per_type_performance_{metric.lower()}_{model_type}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            
            output_file_pdf = os.path.join(self.figures_dir, f'per_type_performance_{metric.lower()}_{model_type}.pdf')
            plt.savefig(output_file_pdf, bbox_inches='tight')
            
            plt.close()
            
            print(f"✓ {metric} plot for {model_type} saved as {output_file}")
    
    def _create_per_type_plot_simple_original(self, df: pd.DataFrame, model_type: str):
        """Create simple heatmaps for models without vanilla/sft/grpo structure using original logic."""
        # Get all models and risk types
        models = sorted(df['Model'].unique())
        risk_types = sorted(df['Risk_Type'].unique())
        
        # Create simplified model names for display
        simplified_names = [self._simplify_model_name(model) for model in models]
        
        # Create circled number labels for y-axis (risk types)
        circled_labels = [self._circled_number(i+1) for i in range(len(risk_types))]
        
        # Prepare data for all heatmaps
        tp_data = {risk_type: [] for risk_type in risk_types}
        fp_data = {risk_type: [] for risk_type in risk_types}
        fn_data = {risk_type: [] for risk_type in risk_types}
        
        # Collect data for each model
        for model in models:
            model_df = df[df['Model'] == model]
            for risk_type in risk_types:
                risk_row = model_df[model_df['Risk_Type'] == risk_type]
                if len(risk_row) > 0:
                    tp_data[risk_type].append(risk_row.iloc[0]['TP'])
                    fp_data[risk_type].append(risk_row.iloc[0]['FP'])
                    fn_data[risk_type].append(risk_row.iloc[0]['FN'])
                else:
                    tp_data[risk_type].append(0)
                    fp_data[risk_type].append(0)
                    fn_data[risk_type].append(0)
        
        # Create the pivot DataFrames
        pivot_df_tp = pd.DataFrame(tp_data, index=models).T
        pivot_df_fp = pd.DataFrame(fp_data, index=models).T
        pivot_df_fn = pd.DataFrame(fn_data, index=models).T
        
        # Create FN and FP heatmaps (as requested)
        for metric, pivot_df, cmap in [('FN', pivot_df_fn, 'YlOrRd'), ('FP', pivot_df_fp, 'OrRd')]:
            fig, ax = plt.subplots(figsize=(max(12, len(models) * 1.5), 9))
            
            # Create custom annotations with mean ± std (smaller font for std)
            annotations = []
            for i in range(len(risk_types)):
                row_annotations = []
                for j in range(len(models)):
                    model = models[j]
                    risk_type = risk_types[i]
                    
                    # Find the data for this combination
                    model_data = df[(df['Model'] == model) & (df['Risk_Type'] == risk_type)]
                    if len(model_data) > 0:
                        mean_val = model_data.iloc[0][f'{metric}']
                        std_val = model_data.iloc[0][f'{metric}_std']
                        row_annotations.append(f'{mean_val:.1f}±{std_val:.1f}')
                    else:
                        row_annotations.append('0.0±0.0')
                annotations.append(row_annotations)
            
            heatmap = sns.heatmap(pivot_df, annot=annotations, fmt='', cmap=cmap, ax=ax,
                       cbar_kws={'label': 'Count'})
            
            # Modify annotation positions - mean on top, std at bottom
            for text in ax.texts:
                text_str = text.get_text()
                if '±' in text_str:
                    # Split the text and reposition
                    parts = text_str.split('±')
                    if len(parts) == 2:
                        # Get the original position
                        x, y = text.get_position()
                        # Hide the original text
                        text.set_text('')
                        # Add mean at the top (above center)
                        ax.text(x, y-0.2, parts[0], ha='center', va='center', 
                               fontsize=28, color=text.get_color())
                        # Add std at the bottom (below center)
                        ax.text(x, y+0.3, f'±{parts[1]}', ha='center', va='center', 
                               fontsize=24, color=text.get_color())
            
            # Set appropriate font sizes for better readability
            cbar = heatmap.collections[0].colorbar
            cbar.set_label('Count', fontsize=20, fontweight='bold')
            cbar.ax.tick_params(labelsize=20)
            ax.set_title(f'Per-Type Performance: {metric} ({model_type.title()})', fontsize=20, fontweight='bold')
            ax.set_ylabel('Risk Types', fontsize=20, fontweight='bold')
            ax.set_xlabel('Models', fontsize=20, fontweight='bold')
            ax.set_xticklabels(simplified_names, rotation=0, ha='center', fontsize=18)
            ax.tick_params(axis='y', labelsize=20)
            ax.tick_params(axis='y', which='major', labelsize=20)
            
            # Set bold font for y-axis tick labels
            for label in ax.get_yticklabels():
                label.set_fontweight('bold')
            
            # Use circled labels on Y axis
            ax.set_yticklabels(circled_labels, rotation=0, fontsize=30, fontweight='bold')
            
            plt.tight_layout()
            
            # Save plots
            output_file = os.path.join(self.figures_dir, f'per_type_performance_{metric.lower()}_{model_type}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            
            output_file_pdf = os.path.join(self.figures_dir, f'per_type_performance_{metric.lower()}_{model_type}.pdf')
            plt.savefig(output_file_pdf, bbox_inches='tight')
            
            plt.close()
            
            print(f"✓ {metric} plot for {model_type} saved as {output_file}")
    
    
    def run_analysis(self):
        """Run the complete analysis."""
        print("=" * 80)
        print("MERGING RESULTS FROM THREE EXPERIMENTAL RUNS")
        print("=" * 80)
        
        # Merge environment results
        print("\n1. MERGING ENVIRONMENT RESULTS...")
        print("-" * 50)
        env_results = self.merge_env_results()
        print(f"✓ Merged results for {len(env_results)} models")
        
        # Merge per-type results
        print("\n2. MERGING PER-TYPE RESULTS...")
        print("-" * 50)
        per_type_results = self.merge_per_type_results()
        print(f"✓ Merged results for {len(per_type_results)} model-risk combinations")
        
        # Generate level1 table
        print("\n3. GENERATING LEVEL1 TABLE...")
        print("-" * 50)
        self.generate_level1_table(env_results)
        
        # Generate per-type plots
        print("\n4. GENERATING PER-TYPE PLOTS...")
        print("-" * 50)
        self.generate_per_type_plots(per_type_results)
        
        print("\n" + "=" * 80)
        print("MERGE ANALYSIS COMPLETE")
        print("=" * 80)

def generate_latex_table(script_dir: str):
    """Generate LaTeX table from local and remote CSV files."""
    # Read CSV files
    local_csv = os.path.join(script_dir, "local", "env_analysis_results.csv")
    remote_csv = os.path.join(script_dir, "remote", "env_analysis_results.csv")
    
    if not os.path.exists(local_csv):
        print(f"Warning: Local CSV {local_csv} does not exist")
        return
    if not os.path.exists(remote_csv):
        print(f"Warning: Remote CSV {remote_csv} does not exist")
        return
    
    local_df = pd.read_csv(local_csv)
    remote_df = pd.read_csv(remote_csv)
    
    # Function to format model name for LaTeX
    def format_model_name(name):
        """Replace hyphens and underscores with LaTeX-safe versions."""
        return name.replace('-', '\\textendash ').replace('_', '\\textendash ')
    
    # Function to parse model name
    def parse_model_name(model_name):
        if model_name.startswith('sft_'):
            return model_name[4:], 'sft'
        elif model_name.startswith('grpo_'):
            return model_name[5:], 'grpo'
        else:
            return model_name, 'vanilla'
    
    # Group local models
    local_groups = {}
    for _, row in local_df.iterrows():
        base_name, train_type = parse_model_name(row['Model'])
        if base_name not in local_groups:
            local_groups[base_name] = {}
        local_groups[base_name][train_type] = row
    
    # Order of local models
    local_order = [
        'Qwen3-4B-Instruct',
        'Llama3.1-8B-Instruct',
        'DeepSeek-R1-0528-Qwen3-8B',
        'Qwen3Guard-Gen-4B',
        'Llama-Guard-3-8B'
    ]
    
    # Start building LaTeX table
    latex_lines = []
    latex_lines.append(r"\begin{table}")
    latex_lines.append(r"\caption{Performance of local and remote models on Level-1 risk detection.}")
    latex_lines.append(r"\label{tab:level1}")
    latex_lines.append(r"  \centering")
    latex_lines.append(r"  \small")
    latex_lines.append(r"  \begin{tabular}{")
    latex_lines.append(r"    l l")
    latex_lines.append(r"    S[table-format=3] % Valid")
    latex_lines.append(r"    S[table-format=3] % TP")
    latex_lines.append(r"    S[table-format=3] % FP")
    latex_lines.append(r"    S[table-format=3] % FN")
    latex_lines.append(r"    S[table-format=3] % TN")
    latex_lines.append(r"    S[table-format=1.2] % Acc")
    latex_lines.append(r"    S[table-format=1.2] % Prec")
    latex_lines.append(r"    S[table-format=1.2] % Rec")
    latex_lines.append(r"  }")
    latex_lines.append(r"    \toprule")
    latex_lines.append(r"    \multicolumn{1}{c}{Models} & \multicolumn{1}{c}{} &")
    latex_lines.append(r"    \multicolumn{1}{c}{Valid} &")
    latex_lines.append(r"    \multicolumn{1}{c}{TP~($\uparrow$)} &")
    latex_lines.append(r"    \multicolumn{1}{c}{FP~($\downarrow$)} &")
    latex_lines.append(r"    \multicolumn{1}{c}{FN~($\downarrow$)} &")
    latex_lines.append(r"    \multicolumn{1}{c}{TN~($\uparrow$)} &")
    latex_lines.append(r"    \multicolumn{1}{c}{Acc.~($\uparrow$)} &")
    latex_lines.append(r"    \multicolumn{1}{c}{Prec.~($\uparrow$)} &")
    latex_lines.append(r"    \multicolumn{1}{c}{Rec.~($\uparrow$)} \\")
    latex_lines.append(r"    \midrule")
    latex_lines.append("")
    latex_lines.append(r"    % ===== Local =====")
    
    # Add local models
    for base_name in local_order:
        if base_name not in local_groups:
            continue
        
        group = local_groups[base_name]
        train_types = ['vanilla', 'sft', 'grpo']
        available_types = [t for t in train_types if t in group]
        
        if not available_types:
            continue
        
        # Format model name for LaTeX
        latex_model_name = format_model_name(base_name)
        
        latex_lines.append(f"    % ===== {base_name} =====")
        latex_lines.append(f"    \\multirow{{{len(available_types)}}}{{*}}{{{latex_model_name}}}")
        
        # Find best accuracy for this group
        best_acc = max(group[t]['Accuracy'] for t in available_types)
        
        for i, train_type in enumerate(available_types):
            row = group[train_type]
            acc = row['Accuracy']
            acc_str = f"\\textbf{{{acc:.2f}}}" if acc == best_acc else f"{acc:.2f}"
            
            if i == 0:
                line = f"      & {train_type} & {int(row['Valid_Count'])} & {int(row['TP'])}  & {int(row['FP'])}   & {int(row['FN'])}   & {int(row['TN'])}  & {acc_str} & {row['Precision']:.2f} & {row['Recall']:.2f} \\\\"
            else:
                line = f"      & {train_type}  & {int(row['Valid_Count'])} & {int(row['TP'])} & {int(row['FP'])} & {int(row['FN'])}   & {int(row['TN'])}  & {acc_str} & {row['Precision']:.2f} & {row['Recall']:.2f} \\\\"
            latex_lines.append(line)
        
        latex_lines.append(r"    \midrule")
        latex_lines.append("")
    
    # Add remote models section
    latex_lines.append(r"    % ===== Remote (API) =====")
    latex_lines.append("")
    
    # Find best accuracy for remote models
    remote_best_acc = remote_df['Accuracy'].max()
    
    # Add remote models
    for _, row in remote_df.iterrows():
        model_name = format_model_name(row['Model'])
        acc = row['Accuracy']
        acc_str = f"\\textbf{{{acc:.2f}}}" if acc == remote_best_acc else f"{acc:.2f}"
        
        line = f"    {model_name} & --- & {int(row['Valid_Count'])} & {int(row['TP'])}  & {int(row['FP'])}  & {int(row['FN'])}  & {int(row['TN'])}  & {acc_str} & {row['Precision']:.2f} & {row['Recall']:.2f} \\\\"
        latex_lines.append(line)
    
    latex_lines.append(r"    \bottomrule")
    latex_lines.append(r"  \end{tabular}")
    latex_lines.append("")
    latex_lines.append(r"\end{table}")
    
    # Write to file
    output_file = os.path.join(script_dir, "level1_table.txt")
    with open(output_file, 'w') as f:
        f.write('\n'.join(latex_lines))
    
    print(f"\n✓ LaTeX table saved to {output_file}")

def copy_pdf_files(script_dir: str):
    """Copy PDF files from local and remote directories to evaluation directory."""
    files_to_copy = [
        ("local/per_type_performance_fn.pdf", "per_type_performance_fn_local.pdf"),
        ("local/per_type_performance_fp.pdf", "per_type_performance_fp_local.pdf"),
        ("remote/per_type_performance_fn.pdf", "per_type_performance_fn_remote.pdf"),
        ("remote/per_type_performance_fp.pdf", "per_type_performance_fp_remote.pdf"),
    ]
    
    for src_rel, dst_name in files_to_copy:
        src_path = os.path.join(script_dir, src_rel)
        dst_path = os.path.join(script_dir, dst_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"✓ Copied {src_rel} to {dst_name}")
        else:
            print(f"⚠ Warning: {src_path} does not exist")

def analyze_directory(evaluation_dir: str, dir_name: str):
    """Analyze a specific evaluation directory."""
    print(f"\n{'='*80}")
    print(f"ANALYZING {dir_name.upper()} DIRECTORY")
    print(f"{'='*80}")
    
    # Initialize evaluator for this directory
    evaluator = ModelEvaluator(evaluation_dir)
    
    # Generate comprehensive report
    evaluator.generate_report()

def main():
    """Main function to run the analysis for local and remote directories."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if Model_output_r1, Model_output_r2, and Model_output_r3 directories exist
    r1_dir = os.path.join(script_dir, "Model_output_r1")
    r2_dir = os.path.join(script_dir, "Model_output_r2")
    r3_dir = os.path.join(script_dir, "Model_output_r3")
    
    if not os.path.exists(r1_dir):
        print(f"Error: Model_output_r1 directory {r1_dir} does not exist")
        return
    
    if not os.path.exists(r2_dir):
        print(f"Error: Model_output_r2 directory {r2_dir} does not exist")
        return
    
    if not os.path.exists(r3_dir):
        print(f"Error: Model_output_r3 directory {r3_dir} does not exist")
        return
    
    # Use the new ExperimentMerger class
    merger = ExperimentMerger(script_dir)
    merger.run_analysis()
    
    print(f"\n{'='*80}")
    print("ALL ANALYSES COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()