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

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ModelEvaluator:
    def __init__(self, evaluation_dir: str):
        self.evaluation_dir = evaluation_dir
        self.env_results = {}
        self.prin_results = {}
        self.model_groups = {}  # Store grouped models
        
    def parse_model_name(self, model_name: str) -> Tuple[str, str]:
        """Parse model name to extract base model and training type."""
        # Expected formats: base_model, sft_model, grpo_model
        if model_name.startswith('sft_'):
            return model_name[4:], 'sft'
        elif model_name.startswith('grpo_'):
            return model_name[5:], 'grpo'
        else:
            return model_name, 'base'
    
    def group_models(self):
        """Group models by base model name."""
        self.model_groups = {}
        
        # Group env results
        for model_name in self.env_results.keys():
            base_name, train_type = self.parse_model_name(model_name)
            if base_name not in self.model_groups:
                self.model_groups[base_name] = {'base': None, 'sft': None, 'grpo': None}
            self.model_groups[base_name][train_type] = model_name
        
        # Group prin results
        for model_name in self.prin_results.keys():
            base_name, train_type = self.parse_model_name(model_name)
            if base_name not in self.model_groups:
                self.model_groups[base_name] = {'base': None, 'sft': None, 'grpo': None}
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
            
            result = {
                'Model': model_name,
                'TP': overall['TP'],
                'FP': overall['FP'],
                'FN': overall['FN'],
                'TN': overall['TN'],
                'Accuracy': overall_metrics['accuracy'],
                'Precision': overall_metrics['precision'],
                'Recall': overall_metrics['recall']
            }
            results.append(result)
        
        return pd.DataFrame(results)
    
    def analyze_prin_results(self) -> pd.DataFrame:
        """Analyze principle evaluation results."""
        results = []
        
        for model_name, data in self.prin_results.items():
            # Cognitive pollution metrics
            cognitive = data.get('cognitive_pollution', {})
            mislead = data.get('mislead_select', {})
            tool_stats = mislead.get('tool_call_stats', {})
            
            result = {
                'Model': model_name,
                'total_dialogs_cognitive': cognitive.get('total_dialogs', 0),
                'correct_refusals': cognitive.get('correct_refusals', 0),
                'missed_refusals': cognitive.get('missed_refusals', 0),
                'total_dialogs_mislead': mislead.get('total_dialogs', 0),
                'baseline': tool_stats.get('baseline', 0),
                'desc': tool_stats.get('desc', 0),
                'name': tool_stats.get('name', 0),
                'both': tool_stats.get('both', 0),
                'unknown': tool_stats.get('unknown', 0)
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
                    'FN': metrics['FN']
                }
                results.append(result)
        
        return pd.DataFrame(results)
    
    def create_overall_performance_plot(self, df: pd.DataFrame):
        """Create bar plot for overall performance metrics with grouped models."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Overall Performance Metrics by Model', fontsize=16, fontweight='bold')
        
        # Define colors for different training types
        colors = {'base': '#1f77b4', 'sft': '#ff7f0e', 'grpo': '#2ca02c'}
        
        # Prepare data for grouped plotting
        grouped_data = self.prepare_grouped_data(df)
        
        # Accuracy
        self.plot_grouped_bars(axes[0, 0], grouped_data, 'Accuracy', colors, 'Accuracy')
        axes[0, 0].set_ylim(0, 1)
        
        # Precision
        self.plot_grouped_bars(axes[0, 1], grouped_data, 'Precision', colors, 'Precision')
        axes[0, 1].set_ylim(0, 1)
        
        # Recall
        self.plot_grouped_bars(axes[1, 0], grouped_data, 'Recall', colors, 'Recall')
        axes[1, 0].set_ylim(0, 1)
        
        # Confusion Matrix Heatmap - reorganize columns by groups
        confusion_data = self.prepare_grouped_confusion_matrix(df)
        sns.heatmap(confusion_data, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1])
        axes[1, 1].set_title('Confusion Matrix Values', fontweight='bold')
        axes[1, 1].set_xlabel('Models')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'overall_performance.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def prepare_grouped_data(self, df: pd.DataFrame):
        """Prepare data for grouped plotting."""
        grouped_data = {}
        
        for _, row in df.iterrows():
            base_name, train_type = self.parse_model_name(row['Model'])
            if base_name not in grouped_data:
                grouped_data[base_name] = {'base': None, 'sft': None, 'grpo': None}
            grouped_data[base_name][train_type] = row
        
        return grouped_data
    
    def prepare_grouped_confusion_matrix(self, df: pd.DataFrame):
        """Prepare confusion matrix data with grouped columns."""
        grouped_data = self.prepare_grouped_data(df)
        
        # Create new DataFrame with reordered columns
        new_columns = []
        new_data = {'TP': [], 'FP': [], 'FN': [], 'TN': []}
        
        for base_name in sorted(grouped_data.keys()):
            group = grouped_data[base_name]
            for train_type in ['base', 'sft', 'grpo']:
                if group[train_type] is not None:
                    model_name = group[train_type]['Model']
                    new_columns.append(f"{base_name}\n({train_type})")
                    new_data['TP'].append(group[train_type]['TP'])
                    new_data['FP'].append(group[train_type]['FP'])
                    new_data['FN'].append(group[train_type]['FN'])
                    new_data['TN'].append(group[train_type]['TN'])
        
        confusion_df = pd.DataFrame(new_data, index=new_columns).T
        return confusion_df
    
    def plot_grouped_bars(self, ax, grouped_data, metric, colors, title):
        """Plot grouped bars for a specific metric."""
        x_pos = 0
        x_labels = []
        x_positions = []
        
        for base_name in sorted(grouped_data.keys()):
            group = grouped_data[base_name]
            group_x_positions = []
            
            for train_type in ['base', 'sft', 'grpo']:
                if group[train_type] is not None:
                    value = group[train_type][metric]
                    ax.bar(x_pos, value, color=colors[train_type], alpha=0.7, 
                          width=0.8, label=f'{train_type.upper()}' if x_pos == 0 else "")
                    group_x_positions.append(x_pos)
                    x_pos += 1
            
            # Add group label at the center of the group
            if group_x_positions:
                center_pos = (min(group_x_positions) + max(group_x_positions)) / 2
                x_labels.append(base_name)
                x_positions.append(center_pos)
                x_pos += 0.5  # Add space between groups
        
        # Set x-axis labels
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
        ax.set_title(title, fontweight='bold')
        ax.set_ylabel(title)
        
        # Add legend only for the first subplot
        if 'Accuracy' in title:
            ax.legend(loc='upper right')
    
    def create_cognitive_pollution_plot(self, df: pd.DataFrame):
        """Create plot for cognitive pollution metrics with grouped models."""
        fig, ax = plt.subplots(1, 1, figsize=(14, 6))
        fig.suptitle('Cognitive Pollution Analysis', fontsize=16, fontweight='bold')
        
        # Define colors for different training types
        colors = {'base': '#1f77b4', 'sft': '#ff7f0e', 'grpo': '#2ca02c'}
        
        # Prepare grouped data
        grouped_data = self.prepare_grouped_data(df)
        
        # Plot grouped bars for correct and missed refusals
        x_pos = 0
        x_labels = []
        x_positions = []
        
        for base_name in sorted(grouped_data.keys()):
            group = grouped_data[base_name]
            group_x_positions = []
            
            for train_type in ['base', 'sft', 'grpo']:
                if group[train_type] is not None:
                    correct_refusals = group[train_type]['correct_refusals']
                    missed_refusals = group[train_type]['missed_refusals']
                    
                    # Plot correct refusals
                    ax.bar(x_pos - 0.2, correct_refusals, width=0.35, 
                          color=colors[train_type], alpha=0.7, 
                          label=f'Correct ({train_type.upper()})' if x_pos == 0 else "")
                    # Plot missed refusals
                    ax.bar(x_pos + 0.2, missed_refusals, width=0.35, 
                          color=colors[train_type], alpha=0.5,
                          label=f'Missed ({train_type.upper()})' if x_pos == 0 else "")
                    
                    group_x_positions.append(x_pos)
                    x_pos += 1
            
            # Add group label at the center of the group
            if group_x_positions:
                center_pos = (min(group_x_positions) + max(group_x_positions)) / 2
                x_labels.append(base_name)
                x_positions.append(center_pos)
                x_pos += 0.5  # Add space between groups
        
        ax.set_xlabel('Models')
        ax.set_ylabel('Count')
        ax.set_title('Correct vs Missed Refusals')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'cognitive_pollution.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_mislead_select_plot(self, df: pd.DataFrame):
        """Create plot for mislead select metrics with grouped models."""
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Define colors for different training types
        train_colors = {'base': '#1f77b4', 'sft': '#ff7f0e', 'grpo': '#2ca02c'}
        
        # Stacked bar chart for tool call stats
        categories = ['baseline', 'desc', 'name', 'both', 'unknown']
        category_colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightgray']
        
        # Prepare grouped data
        grouped_data = self.prepare_grouped_data(df)
        
        # Plot grouped stacked bars
        x_pos = 0
        x_labels = []
        x_positions = []
        
        for base_name in sorted(grouped_data.keys()):
            group = grouped_data[base_name]
            group_x_positions = []
            
            for train_type in ['base', 'sft', 'grpo']:
                if group[train_type] is not None:
                    bottom = 0
                    for i, category in enumerate(categories):
                        value = group[train_type][category]
                        # Use training type color with category-specific alpha
                        alpha_values = [0.9, 0.7, 0.5, 0.3, 0.1]
                        color = train_colors[train_type]
                        ax.bar(x_pos, value, bottom=bottom, width=0.8,
                              color=color, alpha=alpha_values[i],
                              label=f'{category} ({train_type.upper()})' if x_pos == 0 and i == 0 else "")
                        bottom += value
                    
                    group_x_positions.append(x_pos)
                    x_pos += 1
            
            # Add group label at the center of the group
            if group_x_positions:
                center_pos = (min(group_x_positions) + max(group_x_positions)) / 2
                x_labels.append(base_name)
                x_positions.append(center_pos)
                x_pos += 0.5  # Add space between groups
        
        ax.set_xlabel('Models')
        ax.set_ylabel('Count')
        ax.set_title('Tool Call Statistics (Mislead Select)', fontweight='bold')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'mislead_select.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_per_type_plot(self, df: pd.DataFrame):
        """Create heatmap for per-type performance with grouped models."""
        # Prepare grouped data for heatmap
        grouped_data = {}
        
        for _, row in df.iterrows():
            base_name, train_type = self.parse_model_name(row['Model'])
            if base_name not in grouped_data:
                grouped_data[base_name] = {'base': {}, 'sft': {}, 'grpo': {}}
            grouped_data[base_name][train_type][row['Risk_Type']] = row['TP']
        
        # Create new DataFrame with reordered columns
        new_columns = []
        new_data = {}
        
        # Get all risk types
        risk_types = sorted(df['Risk_Type'].unique())
        
        for base_name in sorted(grouped_data.keys()):
            group = grouped_data[base_name]
            for train_type in ['base', 'sft', 'grpo']:
                if group[train_type]:  # If this training type exists
                    col_name = f"{base_name}\n({train_type})"
                    new_columns.append(col_name)
                    for risk_type in risk_types:
                        if risk_type not in new_data:
                            new_data[risk_type] = []
                        new_data[risk_type].append(group[train_type].get(risk_type, 0))
        
        # Create the pivot DataFrame
        pivot_df = pd.DataFrame(new_data, index=new_columns).T
        
        plt.figure(figsize=(16, 8))
        sns.heatmap(pivot_df, annot=True, fmt='d', cmap='YlOrRd', 
                   cbar_kws={'label': 'True Positives'})
        plt.title('Per-Type Performance (True Positives)', fontsize=16, fontweight='bold')
        plt.xlabel('Models')
        plt.ylabel('Risk Types')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'per_type_performance.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
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
        
        # Analyze principle results
        print("\n\n2. PRINCIPLE EVALUATION RESULTS")
        print("-" * 50)
        prin_df = self.analyze_prin_results()
        print(prin_df.to_string(index=False))
        
        # Analyze per-type performance
        print("\n\n3. PER-TYPE PERFORMANCE (TP, FN)")
        print("-" * 50)
        per_type_df = self.analyze_per_type_performance()
        print(per_type_df.to_string(index=False))
        
        # Create visualizations
        print("\n\n4. GENERATING VISUALIZATIONS...")
        print("-" * 50)
        
        try:
            self.create_overall_performance_plot(env_df)
            print("✓ Overall performance plot saved as 'overall_performance.png'")
            
            self.create_cognitive_pollution_plot(prin_df)
            print("✓ Cognitive pollution plot saved as 'cognitive_pollution.png'")
            
            self.create_mislead_select_plot(prin_df)
            print("✓ Mislead select plot saved as 'mislead_select.png'")
            
            self.create_per_type_plot(per_type_df)
            print("✓ Per-type performance plot saved as 'per_type_performance.png'")
            
        except Exception as e:
            print(f"Error generating plots: {e}")
        
        # Save results to CSV
        env_df.to_csv(os.path.join(self.evaluation_dir, 'env_analysis_results.csv'), index=False)
        prin_df.to_csv(os.path.join(self.evaluation_dir, 'prin_analysis_results.csv'), index=False)
        per_type_df.to_csv(os.path.join(self.evaluation_dir, 'per_type_analysis_results.csv'), index=False)
        
        print("\n✓ Analysis results saved to CSV files")
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)

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
    
    print(f"\n{'='*80}")
    print("ALL ANALYSES COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()