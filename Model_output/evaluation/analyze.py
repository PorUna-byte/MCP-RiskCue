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
        """Create bar plot for overall performance metrics."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Overall Performance Metrics by Model', fontsize=16, fontweight='bold')
        
        # Accuracy
        axes[0, 0].bar(df['Model'], df['Accuracy'], color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Accuracy', fontweight='bold')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].set_ylim(0, 1)
        
        # Precision
        axes[0, 1].bar(df['Model'], df['Precision'], color='lightgreen', alpha=0.7)
        axes[0, 1].set_title('Precision', fontweight='bold')
        axes[0, 1].set_ylabel('Precision')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].set_ylim(0, 1)
        
        # Recall
        axes[1, 0].bar(df['Model'], df['Recall'], color='lightcoral', alpha=0.7)
        axes[1, 0].set_title('Recall', fontweight='bold')
        axes[1, 0].set_ylabel('Recall')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].set_ylim(0, 1)
        
        # Confusion Matrix Heatmap
        confusion_data = df[['TP', 'FP', 'FN', 'TN']].T
        confusion_data.columns = df['Model']  # Set model names as column names
        sns.heatmap(confusion_data, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1])
        axes[1, 1].set_title('Confusion Matrix Values', fontweight='bold')
        axes[1, 1].set_xlabel('Models')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'overall_performance.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_cognitive_pollution_plot(self, df: pd.DataFrame):
        """Create plot for cognitive pollution metrics."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        fig.suptitle('Cognitive Pollution Analysis', fontsize=16, fontweight='bold')
        
        # Correct vs Missed Refusals
        x = np.arange(len(df))
        width = 0.35
        
        ax.bar(x - width/2, df['correct_refusals'], width, label='Correct Refusals', 
               color='lightgreen', alpha=0.7)
        ax.bar(x + width/2, df['missed_refusals'], width, label='Missed Refusals', 
               color='lightcoral', alpha=0.7)
        ax.set_xlabel('Models')
        ax.set_ylabel('Count')
        ax.set_title('Correct vs Missed Refusals')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Model'], rotation=45)
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'cognitive_pollution.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_mislead_select_plot(self, df: pd.DataFrame):
        """Create plot for mislead select metrics."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Stacked bar chart for tool call stats
        categories = ['baseline', 'desc', 'name', 'both', 'unknown']
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightgray']
        
        bottom = np.zeros(len(df))
        for i, category in enumerate(categories):
            ax.bar(df['Model'], df[category], bottom=bottom, label=category, 
                  color=colors[i], alpha=0.7)
            bottom += df[category]
        
        ax.set_xlabel('Models')
        ax.set_ylabel('Count')
        ax.set_title('Tool Call Statistics (Mislead Select)', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.evaluation_dir, 'mislead_select.png'), 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_per_type_plot(self, df: pd.DataFrame):
        """Create heatmap for per-type performance."""
        # Pivot the data for heatmap
        pivot_df = df.pivot(index='Risk_Type', columns='Model', values='TP')
        
        plt.figure(figsize=(12, 8))
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

def main():
    """Main function to run the analysis."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize evaluator
    evaluator = ModelEvaluator(script_dir)
    
    # Generate comprehensive report
    evaluator.generate_report()

if __name__ == "__main__":
    main()
