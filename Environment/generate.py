#!/usr/bin/env python3
"""
Generate system logs for all risks
"""

import os
import json
import time
import threading
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
import random

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Available models for processing
MODELS = [
    "claude-3-7-sonnet-20250219",  
    "doubao-1-5-pro-32k-250115",
    "gemini-2.5-pro", 
    "glm-4.5v", 
    "grok-4", 
    "gpt-4o",
    "gpt-5-2025-08-07",
    "deepseek-r1",
    "kimi-k2-0711-preview",
    "o3-2025-04-16"
]

# Thread lock for safe operations
print_lock = threading.Lock()
file_lock = threading.Lock()

@dataclass
class ProcessingTask:
    """Represents a single processing task for generating content based on risk_type."""
    risk_type: str
    model_name: str
    task_id: str
    generation_index: int  # Index for this specific risk_type + model combination

@dataclass
class ProcessingResult:
    """Represents the result of processing a task."""
    task_id: str
    success: bool
    observation: Optional[str] = None  # OBSERVATION (risky)
    safe_twin: Optional[str] = None    # SAFE TWIN (safe but similar)
    explanation: Optional[str] = None  # EXPLANATION
    error_message: Optional[str] = None
    processing_time: float = 0.0

class CheckpointManager:
    """Manages checkpoint saving and loading for resumable processing."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.checkpoint_file = f"{model_name.replace('-', '_')}_env_info.json"
        self.processed_tasks = set()
        self.all_results = []  # Store all results for JSON format
        self.load_checkpoint()
    
    def load_checkpoint(self):
        """Load existing checkpoint to resume processing."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.all_results = data
                        for item in data:
                            if 'task_id' in item:
                                self.processed_tasks.add(item['task_id'])
                    else:
                        # Handle old JSONL format for backward compatibility
                        safe_print(f"Converting old JSONL format to JSON for {self.model_name}")
                        self.all_results = []
                safe_print(f"Loaded checkpoint for {self.model_name}: {len(self.processed_tasks)} tasks completed")
            except Exception as e:
                safe_print(f"Error loading checkpoint for {self.model_name}: {e}")
                self.all_results = []
    
    def is_task_completed(self, task_id: str) -> bool:
        """Check if a task has already been completed."""
        return task_id in self.processed_tasks
    
    def save_result(self, result: ProcessingResult, enhanced_data: Dict[str, Any]):
        """Save a completed task result to checkpoint."""
        with file_lock:
            try:
                # Add metadata to the result
                result_data = {
                    'task_id': result.task_id,
                    'success': result.success,
                    'processing_time': result.processing_time,
                    'timestamp': time.time(),
                    'enhanced_data': enhanced_data
                }
                
                # Clean newlines in text fields
                cleaned_data = self._clean_json_data(result_data)
                
                # Add to in-memory results
                self.all_results.append(cleaned_data)
                self.processed_tasks.add(result.task_id)
                
                # Save entire results array to JSON file
                with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                    json.dump(self.all_results, f, ensure_ascii=False, indent=2)
                
            except Exception as e:
                safe_print(f"Error saving checkpoint for {self.model_name}: {e}")
    
    def _clean_json_data(self, data):
        """Clean JSON data for better formatting."""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                if key == 'enhanced_data' and isinstance(value, dict):
                    cleaned[key] = self._clean_enhanced_data(value)
                else:
                    cleaned[key] = self._clean_json_data(value)
            return cleaned
        elif isinstance(data, list):
            return [self._clean_json_data(item) for item in data]
        elif isinstance(data, str):
            # Keep original formatting for JSON output
            return data
        else:
            return data
    
    def _clean_enhanced_data(self, enhanced_data):
        """Clean enhanced data fields specifically."""
        cleaned = {}
        for key, value in enhanced_data.items():
            if key in ['observation', 'safe_twin', 'explanation']:
                # Keep original formatting for JSON output
                cleaned[key] = str(value)
            else:
                cleaned[key] = value
        return cleaned

def safe_print(*args, **kwargs):
    """Thread-safe print function."""
    with print_lock:
        print(*args, **kwargs)

def generate_task_id(risk_type: str, model_name: str, generation_index: int) -> str:
    """Generate a unique task ID for tracking."""
    content = f"{risk_type}:{model_name}:{generation_index}"
    return hashlib.md5(content.encode()).hexdigest()

class DifficultyEnhancer:
    """Handles the difficulty enhancement of descriptions using AI models."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
    
    def enhance_description(self, task: ProcessingTask) -> ProcessingResult:
        """Enhance a single description, generating both OBSERVATION and SAFE TWIN in one call."""
        start_time = time.time()
        
        try:
            # Generate observation, safe twin, and explanation in one call
            result = self._generate_observation_safe_twin_explanation(task)
            if not result['success']:
                return ProcessingResult(
                    task_id=task.task_id,
                    success=False,
                    error_message=f"Failed to generate descriptions: {result['error']}",
                    processing_time=time.time() - start_time
                )
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                task_id=task.task_id,
                success=True,
                observation=result['observation'],
                safe_twin=result['safe_twin'],
                explanation=result['explanation'],
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                task_id=task.task_id,
                success=False,
                error_message=str(e),
                processing_time=processing_time
            )
    
    
    def _parse_response(self, content: str) -> Tuple[str, str, str]:
        """Parse the model response to extract OBSERVATION, SAFE TWIN, and EXPLANATION with improved parsing."""
        try:
            # Clean the content first
            content = content.strip()
            
            # Define possible section headers with variations
            observation_headers = ['OBSERVATION:', 'OBSERVATION', 'Observation:', 'Observation']
            safe_twin_headers = ['SAFE TWIN:', 'SAFE TWIN', 'Safe Twin:', 'Safe Twin', 'SAFE_TWIN:', 'SAFE_TWIN']
            explanation_headers = ['EXPLANATION:', 'EXPLANATION', 'Explanation:', 'Explanation']
            
            observation = ""
            safe_twin = ""
            explanation = ""
            
            # Method 1: Try to find sections using regex-like approach
            import re
            
            # Look for section patterns with flexible matching
            obs_pattern = r'(?:OBSERVATION|Observation)[:\s]*(.*?)(?=SAFE TWIN|Safe Twin|EXPLANATION|Explanation|$)'
            safe_pattern = r'(?:SAFE TWIN|Safe Twin|SAFE_TWIN)[:\s]*(.*?)(?=EXPLANATION|Explanation|$)'
            exp_pattern = r'(?:EXPLANATION|Explanation)[:\s]*(.*?)$'
            
            obs_match = re.search(obs_pattern, content, re.DOTALL | re.IGNORECASE)
            safe_match = re.search(safe_pattern, content, re.DOTALL | re.IGNORECASE)
            exp_match = re.search(exp_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if obs_match:
                observation = obs_match.group(1).strip()
            if safe_match:
                safe_twin = safe_match.group(1).strip()
            if exp_match:
                explanation = exp_match.group(1).strip()
            
            # Method 2: If regex didn't work well, try line-by-line parsing
            if not observation and not safe_twin and not explanation:
                lines = content.split('\n')
                current_section = None
                current_content = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        if current_section and current_content:
                            if current_section == 'observation':
                                observation = '\n'.join(current_content).strip()
                            elif current_section == 'safe_twin':
                                safe_twin = '\n'.join(current_content).strip()
                            elif current_section == 'explanation':
                                explanation = '\n'.join(current_content).strip()
                        current_content = []
                        continue
                    
                    # Check for section headers
                    line_upper = line.upper()
                    if any(header.upper() in line_upper for header in observation_headers):
                        if current_section and current_content:
                            if current_section == 'observation':
                                observation = '\n'.join(current_content).strip()
                            elif current_section == 'safe_twin':
                                safe_twin = '\n'.join(current_content).strip()
                            elif current_section == 'explanation':
                                explanation = '\n'.join(current_content).strip()
                        current_section = 'observation'
                        current_content = []
                        # Remove the header from the line
                        for header in observation_headers:
                            if header.upper() in line_upper:
                                line = line.replace(header, '').strip()
                                break
                        if line:
                            current_content.append(line)
                    elif any(header.upper() in line_upper for header in safe_twin_headers):
                        if current_section and current_content:
                            if current_section == 'observation':
                                observation = '\n'.join(current_content).strip()
                            elif current_section == 'safe_twin':
                                safe_twin = '\n'.join(current_content).strip()
                            elif current_section == 'explanation':
                                explanation = '\n'.join(current_content).strip()
                        current_section = 'safe_twin'
                        current_content = []
                        # Remove the header from the line
                        for header in safe_twin_headers:
                            if header.upper() in line_upper:
                                line = line.replace(header, '').strip()
                                break
                        if line:
                            current_content.append(line)
                    elif any(header.upper() in line_upper for header in explanation_headers):
                        if current_section and current_content:
                            if current_section == 'observation':
                                observation = '\n'.join(current_content).strip()
                            elif current_section == 'safe_twin':
                                safe_twin = '\n'.join(current_content).strip()
                            elif current_section == 'explanation':
                                explanation = '\n'.join(current_content).strip()
                        current_section = 'explanation'
                        current_content = []
                        # Remove the header from the line
                        for header in explanation_headers:
                            if header.upper() in line_upper:
                                line = line.replace(header, '').strip()
                                break
                        if line:
                            current_content.append(line)
                    else:
                        # Regular content line
                        if current_section:
                            current_content.append(line)
                
                # Handle the last section
                if current_section and current_content:
                    if current_section == 'observation':
                        observation = '\n'.join(current_content).strip()
                    elif current_section == 'safe_twin':
                        safe_twin = '\n'.join(current_content).strip()
                    elif current_section == 'explanation':
                        explanation = '\n'.join(current_content).strip()
            
            # Method 3: Fallback - try simple string splitting
            if not observation and not safe_twin and not explanation:
                # Try to find the sections using simple string operations
                content_upper = content.upper()
                obs_keywords = ['OBSERVATION', 'OBSERVATION:']
                safe_keywords = ['SAFE TWIN', 'SAFE TWIN:', 'SAFE_TWIN']
                exp_keywords = ['EXPLANATION', 'EXPLANATION:']
                
                obs_start = -1
                safe_start = -1
                exp_start = -1
                
                for keyword in obs_keywords:
                    pos = content_upper.find(keyword.upper())
                    if pos != -1:
                        obs_start = pos + len(keyword)
                        break
                
                for keyword in safe_keywords:
                    pos = content_upper.find(keyword.upper())
                    if pos != -1:
                        safe_start = pos + len(keyword)
                        break
                
                for keyword in exp_keywords:
                    pos = content_upper.find(keyword.upper())
                    if pos != -1:
                        exp_start = pos + len(keyword)
                        break
                
                if obs_start != -1 and safe_start != -1 and exp_start != -1:
                    observation = content[obs_start:safe_start].strip()
                    safe_twin = content[safe_start:exp_start].strip()
                    explanation = content[exp_start:].strip()
                elif obs_start != -1 and safe_start != -1:
                    observation = content[obs_start:safe_start].strip()
                    safe_twin = content[safe_start:].strip()
                elif obs_start != -1:
                    observation = content[obs_start:].strip()
            
            # Clean up the results
            observation = observation.strip() if observation else ""
            safe_twin = safe_twin.strip() if safe_twin else ""
            explanation = explanation.strip() if explanation else ""
            
            # If still no content found, use the entire content as observation
            if not observation and not safe_twin and not explanation:
                observation = content
                safe_twin = ""
                explanation = ""
            
            return observation, safe_twin, explanation
            
        except Exception as e:
            safe_print(f"Error parsing response: {e}")
            return content, "", ""
    
    def _generate_observation_safe_twin_explanation(self, task: ProcessingTask) -> Dict[str, Any]:
        """Generate OBSERVATION, SAFE TWIN, and EXPLANATION in one call."""
        try:
            # Load system prompt from file
            with open('system_prompt.txt', 'r', encoding='utf-8') as f:
                system_prompt = f.read().format(risk_type=task.risk_type)
            response = self.client.chat.completions.create(
                model=task.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": "Begin to generate the observation, safe twin, and explanation:\n"
                    }
                ],
                temperature=1.0
            )
            content = response.choices[0].message.content.strip()
            observation, safe_twin, explanation = self._parse_response(content)
            
            return {
                'success': True,
                'observation': observation,
                'safe_twin': safe_twin,
                'explanation': explanation
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    
    

class EnvironmentProcessor:
    """Main processor for handling environment information generation."""
    
    def __init__(self, risk_types: List[str], generations_per_risk_type: int = 10):
        self.risk_types = risk_types
        self.generations_per_risk_type = generations_per_risk_type
        self.enhancer = DifficultyEnhancer()
        self.results = {}
    
    def create_processing_tasks(self) -> List[ProcessingTask]:
        """Create processing tasks for generating content based on risk_types."""
        tasks = []
        
        for risk_type in self.risk_types:
            for generation_index in range(self.generations_per_risk_type):
                for model_name in MODELS:
                    task_id = generate_task_id(risk_type, model_name, generation_index)
                    
                    task = ProcessingTask(
                        risk_type=risk_type,
                        model_name=model_name,
                        task_id=task_id,
                        generation_index=generation_index
                    )
                    tasks.append(task)
        
        return tasks
    
    def process_single_task(self, task: ProcessingTask, checkpoint_manager: CheckpointManager) -> ProcessingResult:
        """Process a single task with checkpoint support."""
        
        # Check if task already completed
        if checkpoint_manager.is_task_completed(task.task_id):
            safe_print(f"Skipping completed task: {task.task_id}")
            return ProcessingResult(
                task_id=task.task_id,
                success=True,
                observation="[ALREADY_COMPLETED]",
                processing_time=0.0
            )
        
        safe_print(f"Processing {task.risk_type} - {task.model_name} - Task {task.task_id[:8]}...")
        
        # Enhance the description
        result = self.enhancer.enhance_description(task)
        
        # Save result to checkpoint
        if result.success:
            enhanced_data = {
                'risk_type': task.risk_type,
                'model_name': task.model_name,
                'observation': result.observation,
                'safe_twin': result.safe_twin,
                'explanation': result.explanation
            }
            checkpoint_manager.save_result(result, enhanced_data)
        
        return result
    
    def process_model_tasks(self, model_name: str, tasks: List[ProcessingTask]) -> Dict[str, Any]:
        """Process all tasks for a specific model."""
        safe_print(f"\n{'='*60}")
        safe_print(f"Processing tasks for model: {model_name}")
        safe_print(f"{'='*60}")
        
        # Filter tasks for this model
        model_tasks = [task for task in tasks if task.model_name == model_name]
        safe_print(f"Found {len(model_tasks)} tasks for {model_name}")
        
        # Initialize checkpoint manager for this model
        checkpoint_manager = CheckpointManager(model_name)
        
        # Process tasks
        model_results = {
            'model_name': model_name,
            'total_tasks': len(model_tasks),
            'completed_tasks': 0,
            'failed_tasks': 0,
            'skipped_tasks': 0,
            'enhanced_descriptions': {},
            'processing_times': []
        }
        
        for task in model_tasks:
            result = self.process_single_task(task, checkpoint_manager)
            
            if result.success:
                if result.observation == "[ALREADY_COMPLETED]":
                    model_results['skipped_tasks'] += 1
                else:
                    model_results['completed_tasks'] += 1
                    if task.risk_type not in model_results['enhanced_descriptions']:
                        model_results['enhanced_descriptions'][task.risk_type] = []
                    model_results['enhanced_descriptions'][task.risk_type].append({
                        'observation': result.observation,
                        'safe_twin': result.safe_twin,
                        'explanation': result.explanation,
                        'generation_index': task.generation_index
                    })
            else:
                model_results['failed_tasks'] += 1
                safe_print(f"Failed to process task {task.task_id[:8]}: {result.error_message}")
            
            model_results['processing_times'].append(result.processing_time)
        
        # Calculate statistics
        total_time = sum(model_results['processing_times'])
        avg_time = total_time / len(model_results['processing_times']) if model_results['processing_times'] else 0
        
        safe_print(f"\nModel {model_name} processing complete:")
        safe_print(f"  Completed: {model_results['completed_tasks']}")
        safe_print(f"  Skipped: {model_results['skipped_tasks']}")
        safe_print(f"  Failed: {model_results['failed_tasks']}")
        safe_print(f"  Total time: {total_time:.2f}s")
        safe_print(f"  Average time per task: {avg_time:.2f}s")
        
        return model_results
    
    def run_parallel_processing(self, max_workers: int = 3):
        """Run parallel processing across multiple models."""
        safe_print("Starting parallel processing of environment descriptions...")
        
        # Create all processing tasks
        all_tasks = self.create_processing_tasks()
        safe_print(f"Created {len(all_tasks)} total processing tasks")
        
        # Group tasks by model
        model_tasks = {}
        for task in all_tasks:
            if task.model_name not in model_tasks:
                model_tasks[task.model_name] = []
            model_tasks[task.model_name].append(task)
        
        # Process models in parallel
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all model processing tasks
            future_to_model = {
                executor.submit(self.process_model_tasks, model_name, tasks): model_name 
                for model_name, tasks in model_tasks.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_model):
                model_name = future_to_model[future]
                try:
                    result = future.result()
                    results.append(result)
                    safe_print(f"✓ Completed processing for {model_name}")
                except Exception as e:
                    safe_print(f"✗ Error processing {model_name}: {e}")
                    results.append({
                        'model_name': model_name,
                        'error': str(e),
                        'completed_tasks': 0,
                        'failed_tasks': 0
                    })
        
        return results
    
    def generate_summary_report(self, results: List[Dict[str, Any]]):
        """Generate a summary report of the processing results."""
        safe_print(f"\n{'='*80}")
        safe_print("PROCESSING SUMMARY REPORT")
        safe_print(f"{'='*80}")
        
        total_completed = 0
        total_failed = 0
        total_skipped = 0
        
        for result in results:
            if 'error' in result:
                safe_print(f"✗ {result['model_name']}: ERROR - {result['error']}")
                continue
            
            completed = result.get('completed_tasks', 0)
            failed = result.get('failed_tasks', 0)
            skipped = result.get('skipped_tasks', 0)
            
            total_completed += completed
            total_failed += failed
            total_skipped += skipped
            
            safe_print(f"✓ {result['model_name']}: {completed} completed, {skipped} skipped, {failed} failed")
        
        safe_print(f"\nTOTAL STATISTICS:")
        safe_print(f"  Completed: {total_completed}")
        safe_print(f"  Skipped: {total_skipped}")
        safe_print(f"  Failed: {total_failed}")
        safe_print(f"  Success Rate: {total_completed/(total_completed+total_failed)*100:.1f}%" if (total_completed+total_failed) > 0 else "N/A")

def main():    
    """Main execution function."""
    if not os.getenv("API_KEY"):
        print("Error: API_KEY environment variable not set. Please set it in your .env file or environment.")
        return
    
    if not os.getenv("BASE_URL"):
        print("Error: BASE_URL environment variable not set. Please set it in your .env file or environment.")
        return
    
    # Define risk types to generate content for
    risk_types = [
        "Sensitive Data Exfiltration",
        "Covert Channel Attack", 
        "Malicious Code Execution",
        "Privilege Escalation",
        "Persistence via Backdoor Implantation",
        "Cache or Local State Pollution",
        "Delayed or Timed Trigger Attacks",
        "Denial-of-Service",
        "Log Explosion Attacks",
    ]
    
    print(f"Using models: {MODELS}")
    print(f"Risk types: {risk_types}")
    print(f"Starting environment content generation...")
    
    # Initialize processor with risk types and generations per type
    processor = EnvironmentProcessor(risk_types=risk_types, generations_per_risk_type=10)
    
    # Run parallel processing
    results = processor.run_parallel_processing(max_workers=10)
    
    # Generate summary report
    processor.generate_summary_report(results)
    
    
    print(f"\nProcessing complete! Check individual model checkpoint files for detailed results.")
    print(f"Checkpoint files: {[f'{model.replace('-', '_')}_env_info.json' for model in MODELS]}")

if __name__ == "__main__":
    main()