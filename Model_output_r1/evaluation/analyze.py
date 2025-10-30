#!/usr/bin/env python3
"""
Analysis script for model evaluation results.
Analyzes env_eval_results and prin_eval_results files to generate performance statistics and visualizations.
"""

import json
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import numpy as np
import shutil

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ModelEvaluator:
    def __init__(self, evaluation_dir: str):
        self.evaluation_dir = evaluation_dir
        self.env_results = {}
        self.prin_results = {}
        self.model_groups = {}  # Store grouped models
        
    def _circled_number(self, n: int) -> str:
        """Return circled number ①..⑳ when possible, else (n)."""
        base = 0x2460
        if 1 <= n <= 20:
            try:
                return chr(base + n - 1)
            except Exception:
                return f"({n})"
        return f"({n})"
    def parse_model_name(self, model_name: str) -> Tuple[str, str]:
        """Parse model name to extract base model and training type."""
        # Expected formats: vanilla_model, sft_model, grpo_model
        if model_name.startswith('sft_'):
            return model_name[4:], 'sft'
        elif model_name.startswith('grpo_'):
            return model_name[5:], 'grpo'
        else:
            return model_name, 'vanilla'
    
    def group_models(self):
        """Group models by base model name."""
        self.model_groups = {}
        
        # Group env results
        for model_name in self.env_results.keys():
            base_name, train_type = self.parse_model_name(model_name)
            if base_name not in self.model_groups:
                self.model_groups[base_name] = {'vanilla': None, 'sft': None, 'grpo': None}
            self.model_groups[base_name][train_type] = model_name
        
        # Group prin results
        for model_name in self.prin_results.keys():
            base_name, train_type = self.parse_model_name(model_name)
            if base_name not in self.model_groups:
                self.model_groups[base_name] = {'vanilla': None, 'sft': None, 'grpo': None}
            self.model_groups[base_name][train_type] = model_name

    def load_results(self):
        """Load all evaluation results from the directory."""
        # Load env evaluation results
        env_files = glob.glob(os.path.join(self.evaluation_dir, "env_eval_results_*.jsonl"))
        for file_path in env_files:
            model_name = os.path.basename(file_path).replace("env_eval_results_", "").replace(".jsonl", "")
            with open(file_path, 'r') as f:
                self.env_results[model_name] = json.load(f)
        
        # Load prin evaluation results
        prin_files = glob.glob(os.path.join(self.evaluation_dir, "prin_eval_results_*.jsonl"))
        for file_path in prin_files:
            model_name = os.path.basename(file_path).replace("prin_eval_results_", "").replace(".jsonl", "")
            with open(file_path, 'r') as f:
                self.prin_results[model_name] = json.load(f)
        
        # Group models after loading
        self.group_models()
    
    def calculate_metrics(self, tp: int, fp: int, fn: int, tn: int) -> Dict[str, float]:
        """Calculate accuracy, precision, recall from confusion matrix values."""
        accuracy = (tp + tn) / (tp + fp + fn + tn) if (tp + fp + fn + tn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall
        }
    
    def analyze_env_results(self) -> pd.DataFrame:
        """Analyze environment evaluation results."""
        results = []
        
        for model_name, data in self.env_results.items():
            # Overall performance
            overall = data['overall']
            overall_metrics = self.calculate_metrics(
                overall['TP'], overall['FP'], overall['FN'], overall['TN']
            )
            
            # Calculate valid count
            valid_count = overall['TP'] + overall['FP'] + overall['FN'] + overall['TN']
            
            result = {
                'Model': model_name,
                'TP': overall['TP'],
                'FP': overall['FP'],
                'FN': overall['FN'],
                'TN': overall['TN'],
                'Valid_Count': valid_count,
                'Accuracy': overall_metrics['accuracy'],
                'Precision': overall_metrics['precision'],
                'Recall': overall_metrics['recall']
            }
            results.append(result)
        
        return pd.DataFrame(results)
    
    def analyze_per_type_performance(self) -> pd.DataFrame:
        """Analyze per-type performance for environment evaluation."""
        results = []
        
        for model_name, data in self.env_results.items():
            per_type = data.get('per_type', {})
            
            for risk_type, metrics in per_type.items():
                result = {
                    'Model': model_name,
                    'Risk_Type': risk_type,
                    'TP': metrics['TP'],
                    'FP': metrics['FP'],
                    'FN': metrics['FN']
                }
                results.append(result)
        
        return pd.DataFrame(results)
    
    def prepare_grouped_data(self, df: pd.DataFrame):
        """Prepare data for grouped plotting."""
        grouped_data = {}
        
        for _, row in df.iterrows():
            base_name, train_type = self.parse_model_name(row['Model'])
            if base_name not in grouped_data:
                grouped_data[base_name] = {'vanilla': None, 'sft': None, 'grpo': None}
            grouped_data[base_name][train_type] = row
        
        return grouped_data
    
    def create_per_type_plot(self, df: pd.DataFrame):
        """Create two separate heatmaps for per-type performance: one for TP and one for FN."""
        # Check if models have vanilla/sft/grpo grouping
        has_grouping = any(
            model.startswith('sft_') or model.startswith('grpo_') 
            for model in df['Model'].unique()
        )
        
        if has_grouping:
            # Local models: group by vanilla/sft/grpo
            self._create_per_type_plot_grouped(df)
        else:
            # Remote models: no grouping
            self._create_per_type_plot_simple(df)
    
    def _calculate_center_col(self, base_name: str, start_idx: int, end_idx: int) -> float:
        """Calculate the center column position for model group labels.
        
        Args:
            base_name: The base model name
            start_idx: Start index of the group
            end_idx: End index of the group
            
        Returns:
            The center column position with adjustment offset
        """
        base_center = (start_idx + end_idx) / 2.0
        
        # Apply model-specific offset for better alignment
        offset_map = {
            'DeepSeek-R1-0528-Qwen3-8B': 1.6,
            'Llama-Guard-3-8B': 2.3,
            'Llama3.1-8B-Instruct': 2.4,
            'Qwen3-4B-Instruct': 2.4,
            'Qwen3-4B-Thinking-2507': 2.4,
            'Qwen3Guard-Gen-4B': 2.5
        }
        
        offset = offset_map.get(base_name, 2.0)  # Default offset is 2.0
        return base_center + offset
    
    def _create_per_type_plot_grouped(self, df: pd.DataFrame):
        """Create grouped heatmaps for models with vanilla/sft/grpo structure."""
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
        
        # ========== Create TP heatmap ==========
        fig1, ax1 = plt.subplots(figsize=(18, 9))
        heatmap1 = sns.heatmap(pivot_df_tp, annot=True, fmt='d', cmap='YlGn', ax=ax1,
                   cbar_kws={'label': 'Count'}, linewidths=0, linecolor='white')
        # Set appropriate font sizes for better readability
        cbar1 = heatmap1.collections[0].colorbar
        cbar1.set_label('Count', fontsize=16, fontweight='bold')
        cbar1.ax.tick_params(labelsize=14)
        ax1.set_title('Per-Type Performance: True Positives (TP)', fontsize=18, fontweight='bold')
        ax1.set_ylabel('Risk Types', fontsize=18, fontweight='bold')
        ax1.set_xlabel('', fontsize=18, fontweight='bold')
        ax1.set_xticklabels(new_columns, rotation=0, fontsize=14)
        ax1.tick_params(axis='y', labelsize=16)
        ax1.tick_params(axis='y', which='major', labelsize=16)
        # Set bold font for y-axis tick labels
        for label in ax1.get_yticklabels():
            label.set_fontweight('bold')
        # Set annotation font size for heatmap cells
        for text in ax1.texts:
            text.set_fontsize(16)
        # Replace risk type names with circled numbers ①②…
        circled_labels = [self._circled_number(i + 1) for i in range(len(risk_types))]
        ax1.set_yticklabels(circled_labels, rotation=0, fontsize=24, fontweight='bold')
        
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
                ax1.axvline(x=start_idx, color='black', linewidth=3, alpha=1.0, zorder=10)

        # Add group labels below the x-axis
        group_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for idx, (base_name, start_idx, end_idx) in enumerate(groups):
            # Calculate the center position for this group
            center_col = (start_idx + end_idx) / 2.0
            
            # Add group label below the x-axis labels
            group_label = group_labels[idx] if idx < len(group_labels) else f'{idx+1}'
            ax1.text(center_col, 9.5, f'Group {group_label}', ha='center', va='top', 
                    fontsize=14, fontweight='bold', transform=ax1.transData)


        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_tp.png'), 
                   dpi=300, bbox_inches='tight')
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_tp.pdf'), 
                   bbox_inches='tight')
        plt.close()
        
        # ========== Create FP heatmap ==========
        fig_fp, ax_fp = plt.subplots(figsize=(18, 9))
        heatmap_fp = sns.heatmap(pivot_df_fp, annot=True, fmt='d', cmap='OrRd', ax=ax_fp,
                   cbar_kws={'label': 'Count'}, linewidths=0, linecolor='white')
        # Set appropriate font sizes for better readability
        cbar_fp = heatmap_fp.collections[0].colorbar
        cbar_fp.set_label('Count', fontsize=16, fontweight='bold')
        cbar_fp.ax.tick_params(labelsize=14)
        ax_fp.set_title('Per-Type Performance: False Positives (FP)', fontsize=16, fontweight='bold')
        ax_fp.set_ylabel('Risk Types', fontsize=16, fontweight='bold')
        ax_fp.set_xlabel('', fontsize=16, fontweight='bold')
        ax_fp.set_xticklabels(new_columns, rotation=0, fontsize=14)
        ax_fp.tick_params(axis='y', labelsize=12)
        # Set bold font for y-axis tick labels
        for label in ax_fp.get_yticklabels():
            label.set_fontweight('bold')
        # Set annotation font size for heatmap cells
        for text in ax_fp.texts:
            text.set_fontsize(16)
        
        # Use circled labels on Y axis
        ax_fp.set_yticklabels(circled_labels, rotation=0, fontsize=24, fontweight='bold')

        # Add vertical lines between different model groups
        for base_name, start_idx, end_idx in groups:
            if start_idx > 0:  # Don't add line before the first group
                ax_fp.axvline(x=start_idx, color='black', linewidth=3, alpha=1.0, zorder=10)

        # Add group labels below the x-axis
        group_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for idx, (base_name, start_idx, end_idx) in enumerate(groups):
            # Calculate the center position for this group
            center_col = (start_idx + end_idx) / 2.0
            
            # Add group label below the x-axis labels
            group_label = group_labels[idx] if idx < len(group_labels) else f'{idx+1}'
            ax_fp.text(center_col, 9.5, f'Group {group_label}', ha='center', va='top', 
                    fontsize=14, fontweight='bold', transform=ax_fp.transData)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fp.png'), 
                   dpi=300, bbox_inches='tight')
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fp.pdf'), 
                   bbox_inches='tight')
        plt.close()
        
        # ========== Create FN heatmap ==========
        fig2, ax2 = plt.subplots(figsize=(18, 9))
        heatmap2 = sns.heatmap(pivot_df_fn, annot=True, fmt='d', cmap='YlOrRd', ax=ax2,
                   cbar_kws={'label': 'Count'}, linewidths=0, linecolor='white')
        # Set appropriate font sizes for better readability
        cbar2 = heatmap2.collections[0].colorbar
        cbar2.set_label('Count', fontsize=16, fontweight='bold')
        cbar2.ax.tick_params(labelsize=14)
        ax2.set_title('Per-Type Performance: False Negatives (FN)', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Risk Types', fontsize=16, fontweight='bold')
        ax2.set_xlabel('', fontsize=16, fontweight='bold')
        ax2.set_xticklabels(new_columns, rotation=0, fontsize=14)
        ax2.tick_params(axis='y', labelsize=12)
        # Set bold font for y-axis tick labels
        for label in ax2.get_yticklabels():
            label.set_fontweight('bold')
        # Set annotation font size for heatmap cells
        for text in ax2.texts:
            text.set_fontsize(16)
        
        # Use circled labels on Y axis
        ax2.set_yticklabels(circled_labels, rotation=0, fontsize=24, fontweight='bold')

        # Add vertical lines between different model groups
        for base_name, start_idx, end_idx in groups:
            if start_idx > 0:  # Don't add line before the first group
                ax2.axvline(x=start_idx, color='black', linewidth=3, alpha=1.0, zorder=10)

        # Add group labels below the x-axis
        group_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for idx, (base_name, start_idx, end_idx) in enumerate(groups):
            # Calculate the center position for this group
            center_col = (start_idx + end_idx) / 2.0
            
            # Add group label below the x-axis labels
            group_label = group_labels[idx] if idx < len(group_labels) else f'{idx+1}'
            ax2.text(center_col, 9.5, f'Group {group_label}', ha='center', va='top', 
                    fontsize=14, fontweight='bold', transform=ax2.transData)
        

        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fn.png'), 
                   dpi=300, bbox_inches='tight')
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fn.pdf'), 
                   bbox_inches='tight')
        plt.close()
    
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
    
    def _create_per_type_plot_simple(self, df: pd.DataFrame):
        """Create simple heatmaps for models without vanilla/sft/grpo structure (remote models)."""
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
        
        # ========== Create TP heatmap ==========
        fig1, ax1 = plt.subplots(figsize=(max(12, len(models) * 1.5), 9))
        heatmap1_simple = sns.heatmap(pivot_df_tp, annot=True, fmt='d', cmap='YlGn', ax=ax1,
                   cbar_kws={'label': 'Count'})
        # Set appropriate font sizes for better readability
        cbar1_simple = heatmap1_simple.collections[0].colorbar
        cbar1_simple.set_label('Count', fontsize=16, fontweight='bold')
        cbar1_simple.ax.tick_params(labelsize=14)
        ax1.set_title('Per-Type Performance: True Positives (TP)', fontsize=18, fontweight='bold')
        ax1.set_ylabel('Risk Types', fontsize=18, fontweight='bold')
        ax1.set_xlabel('Models', fontsize=18, fontweight='bold')
        ax1.set_xticklabels(simplified_names, rotation=0, ha='center', fontsize=14)
        ax1.tick_params(axis='y', labelsize=12)
        ax1.tick_params(axis='y', which='major', labelsize=12)
        # Set bold font for y-axis tick labels
        for label in ax1.get_yticklabels():
            label.set_fontweight('bold')
        # Set annotation font size for heatmap cells
        for text in ax1.texts:
            text.set_fontsize(16)
        
        # Use circled labels on Y axis
        ax1.set_yticklabels(circled_labels, rotation=0, fontsize=24, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_tp.png'), 
                   dpi=300, bbox_inches='tight')
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_tp.pdf'), 
                   bbox_inches='tight')
        plt.close()
        
        # ========== Create FP heatmap ==========
        fig_fp, ax_fp = plt.subplots(figsize=(max(12, len(models) * 1.5), 9))
        heatmap_fp_simple = sns.heatmap(pivot_df_fp, annot=True, fmt='d', cmap='OrRd', ax=ax_fp,
                   cbar_kws={'label': 'Count'})
        # Set appropriate font sizes for better readability
        cbar_fp_simple = heatmap_fp_simple.collections[0].colorbar
        cbar_fp_simple.set_label('Count', fontsize=16, fontweight='bold')
        cbar_fp_simple.ax.tick_params(labelsize=14)
        ax_fp.set_title('Per-Type Performance: False Positives (FP)', fontsize=18, fontweight='bold')
        ax_fp.set_ylabel('Risk Types', fontsize=18, fontweight='bold')
        ax_fp.set_xlabel('Models', fontsize=18, fontweight='bold')
        ax_fp.set_xticklabels(simplified_names, rotation=0, ha='center', fontsize=14)
        ax_fp.tick_params(axis='y', labelsize=12)
        # Set bold font for y-axis tick labels
        for label in ax_fp.get_yticklabels():
            label.set_fontweight('bold')
        # Set annotation font size for heatmap cells
        for text in ax_fp.texts:
            text.set_fontsize(16)
        
        # Use circled labels on Y axis
        ax_fp.set_yticklabels(circled_labels, rotation=0, fontsize=24, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fp.png'), 
                   dpi=300, bbox_inches='tight')
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fp.pdf'), 
                   bbox_inches='tight')
        plt.close()
        
        # ========== Create FN heatmap ==========
        fig2, ax2 = plt.subplots(figsize=(max(12, len(models) * 1.5), 9))
        heatmap2_simple = sns.heatmap(pivot_df_fn, annot=True, fmt='d', cmap='YlOrRd', ax=ax2,
                   cbar_kws={'label': 'Count'})
        # Set appropriate font sizes for better readability
        cbar2_simple = heatmap2_simple.collections[0].colorbar
        cbar2_simple.set_label('Count', fontsize=16, fontweight='bold')
        cbar2_simple.ax.tick_params(labelsize=14)
        ax2.set_title('Per-Type Performance: False Negatives (FN)', fontsize=18, fontweight='bold')
        ax2.set_ylabel('Risk Types', fontsize=18, fontweight='bold')
        ax2.set_xlabel('Models', fontsize=18, fontweight='bold')
        ax2.set_xticklabels(simplified_names, rotation=0, ha='center', fontsize=14)
        ax2.tick_params(axis='y', labelsize=12)
        # Set bold font for y-axis tick labels
        for label in ax2.get_yticklabels():
            label.set_fontweight('bold')
        # Set annotation font size for heatmap cells
        for text in ax2.texts:
            text.set_fontsize(16)
        
        # Use circled labels on Y axis
        ax2.set_yticklabels(circled_labels, rotation=0, fontsize=24, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fn.png'), 
                   dpi=300, bbox_inches='tight')
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance_fn.pdf'), 
                   bbox_inches='tight')
        plt.close()
    
    def print_group_mapping(self):
        """Print the mapping of groups to models."""
        if not self.model_groups:
            return
            
        print("\n4. MODEL GROUP MAPPING")
        print("-" * 50)
        
        group_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        # Define the specific order for groups (same as in plotting)
        group_order = [
            'Qwen3-4B-Instruct',
            'Llama3.1-8B-Instruct', 
            'DeepSeek-R1-0528-Qwen3-8B',
            'Qwen3Guard-Gen-4B',
            'Llama-Guard-3-8B'
        ]
        
        # Filter to only include models that exist in the data
        ordered_base_names = [name for name in group_order if name in self.model_groups.keys()]
        # Add any remaining models not in the predefined order
        remaining_models = [name for name in sorted(self.model_groups.keys()) if name not in group_order]
        ordered_base_names.extend(remaining_models)
        
        for idx, base_name in enumerate(ordered_base_names):
            models = self.model_groups[base_name]
            group_label = group_labels[idx] if idx < len(group_labels) else f'{idx+1}'
            print(f"Group {group_label}: {base_name}")
            
            # List the training types available for this base model
            available_types = []
            for train_type in ['vanilla', 'sft', 'grpo']:
                if models[train_type] is not None:
                    available_types.append(train_type.upper())
            
            if available_types:
                print(f"  Available training types: {', '.join(available_types)}")
            print()

    def generate_report(self):
        """Generate comprehensive analysis report."""
        print("=" * 80)
        print("MODEL EVALUATION ANALYSIS REPORT")
        print("=" * 80)
        
        # Load results
        self.load_results()
        
        # Analyze environment results
        print("\n1. ENVIRONMENT EVALUATION RESULTS")
        print("-" * 50)
        env_df = self.analyze_env_results()
        print(env_df.to_string(index=False, float_format='%.4f'))
        
        # Analyze per-type performance
        print("\n\n2. PER-TYPE PERFORMANCE (TP, FP, FN)")
        print("-" * 50)
        per_type_df = self.analyze_per_type_performance()
        print(per_type_df.to_string(index=False))
        
        # Print group mapping
        self.print_group_mapping()
        
        # Create visualizations
        print("\n\n3. GENERATING VISUALIZATIONS...")
        print("-" * 50)
        
        try:
            self.create_per_type_plot(per_type_df)
            print("✓ Per-type performance (TP) plot saved as 'per_type_performance_tp.png'")
            print("✓ Per-type performance (FP) plot saved as 'per_type_performance_fp.png'")
            print("✓ Per-type performance (FN) plot saved as 'per_type_performance_fn.png'")
            
        except Exception as e:
            print(f"Error generating plots: {e}")
        
        # Save results to CSV
        env_df.to_csv(os.path.join(self.evaluation_dir, 'env_analysis_results.csv'), index=False, float_format='%.2f')
        per_type_df.to_csv(os.path.join(self.evaluation_dir, 'per_type_analysis_results.csv'), index=False)
        
        print("\n✓ Analysis results saved to CSV files")
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
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
    """Main function to run the analysis for both local and remote directories."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the directories to analyze
    local_dir = os.path.join(script_dir, "local")
    remote_dir = os.path.join(script_dir, "remote")
    
    # Check if directories exist
    if not os.path.exists(local_dir):
        print(f"Warning: Local directory {local_dir} does not exist")
    else:
        analyze_directory(local_dir, "local")
    
    if not os.path.exists(remote_dir):
        print(f"Warning: Remote directory {remote_dir} does not exist")
    else:
        analyze_directory(remote_dir, "remote")
    
    # Generate LaTeX table
    print(f"\n{'='*80}")
    print("GENERATING LATEX TABLE")
    print(f"{'='*80}")
    generate_latex_table(script_dir)
    
    # Copy PDF files
    print(f"\n{'='*80}")
    print("COPYING PDF FILES")
    print(f"{'='*80}")
    copy_pdf_files(script_dir)
    
    print(f"\n{'='*80}")
    print("ALL ANALYSES COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()