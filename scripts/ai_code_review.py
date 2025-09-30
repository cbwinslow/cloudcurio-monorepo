#!/usr/bin/env python3
"""
CloudCurio AI Code Review Script

This script uses local AI models (Ollama) to review code and provide feedback.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any
import requests


class AICodeReviewer:
    """AI-powered code reviewer using local Ollama models"""
    
    def __init__(self, model: str = "llama3", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.api_url = f"{host}/api/generate"
    
    def check_ollama_availability(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def pull_model(self, model: str = None) -> bool:
        """Pull the required model if not available"""
        model = model or self.model
        try:
            # This will trigger the model download if not available
            response = requests.post(self.api_url, json={
                "model": model,
                "prompt": "Hello",
                "stream": False
            })
            return response.status_code == 200
        except:
            return False
    
    def review_code_file(self, file_path: str) -> Dict[str, Any]:
        """Review a single code file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Skip very large files
            if len(content) > 100000:  # 100KB limit
                return {
                    "file": file_path,
                    "status": "skipped",
                    "reason": "File too large for review",
                    "issues": []
                }
            
            # Create a prompt for the AI to review the code
            prompt = f"""
You are an experienced Python code reviewer. Please review the following Python code and provide feedback on:

1. Code quality and best practices
2. Potential bugs or issues
3. Performance improvements
4. Security concerns
5. Readability and maintainability
6. Documentation and comments

Focus on concrete, actionable feedback. For each issue, provide:
- Location (line numbers if possible)
- Description of the issue
- Suggestion for improvement

Code to review:
```python
{content}
```

Please format your response as a JSON object with the following structure:
{{
  "overall_rating": "A-F grade",
  "summary": "Brief summary of the review",
  "issues": [
    {{
      "type": "bug|performance|security|style|documentation",
      "line_start": 10,
      "line_end": 15,
      "description": "Description of the issue",
      "suggestion": "How to fix it"
    }}
  ]
}}
"""
            
            # Send request to Ollama
            response = requests.post(self.api_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "stop": ["```json"]
                }
            })
            
            if response.status_code == 200:
                result = response.json()
                # Try to parse the JSON response
                try:
                    # Extract JSON from the response
                    response_text = result.get('response', '')
                    # Try to find JSON in the response
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        review_data = json.loads(json_str)
                        review_data['file'] = file_path
                        review_data['status'] = 'success'
                        return review_data
                    else:
                        return {
                            "file": file_path,
                            "status": "error",
                            "error": "Could not parse AI response as JSON",
                            "issues": []
                        }
                except json.JSONDecodeError:
                    return {
                        "file": file_path,
                        "status": "error",
                        "error": "Invalid JSON response from AI",
                        "issues": []
                    }
            else:
                return {
                    "file": file_path,
                    "status": "error",
                    "error": f"Ollama API error: {response.status_code}",
                    "issues": []
                }
                
        except Exception as e:
            return {
                "file": file_path,
                "status": "error",
                "error": str(e),
                "issues": []
            }
    
    def review_changed_files(self, base_ref: str = "HEAD~1") -> List[Dict[str, Any]]:
        """Review files that have changed compared to a base reference"""
        try:
            # Get list of changed files
            result = subprocess.run([
                'git', 'diff', '--name-only', base_ref
            ], capture_output=True, text=True, check=True)
            
            changed_files = result.stdout.strip().split('\n')
            python_files = [f for f in changed_files if f.endswith('.py') and os.path.exists(f)]
            
            reviews = []
            for file_path in python_files:
                print(f"Reviewing {file_path}...")
                review = self.review_code_file(file_path)
                reviews.append(review)
            
            return reviews
            
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files: {e}")
            return []
    
    def generate_markdown_report(self, reviews: List[Dict[str, Any]]) -> str:
        """Generate a markdown report from the reviews"""
        report = "# AI Code Review Report\n\n"
        report += f"Generated on {self._get_current_timestamp()}\n\n"
        
        # Overall statistics
        total_files = len(reviews)
        successful_reviews = len([r for r in reviews if r.get('status') == 'success'])
        skipped_files = len([r for r in reviews if r.get('status') == 'skipped'])
        errored_files = len([r for r in reviews if r.get('status') == 'error'])
        
        report += "## Summary\n\n"
        report += f"- Total files reviewed: {total_files}\n"
        report += f"- Successful reviews: {successful_reviews}\n"
        report += f"- Skipped files: {skipped_files}\n"
        report += f"- Errored files: {errored_files}\n\n"
        
        # Detailed reviews
        for review in reviews:
            file_path = review.get('file', 'Unknown')
            status = review.get('status', 'unknown')
            
            report += f"## File: `{file_path}`\n\n"
            report += f"**Status**: {status}\n\n"
            
            if status == 'success':
                overall_rating = review.get('overall_rating', 'N/A')
                summary = review.get('summary', 'No summary provided')
                
                report += f"**Overall Rating**: {overall_rating}\n\n"
                report += f"**Summary**: {summary}\n\n"
                
                issues = review.get('issues', [])
                if issues:
                    report += "### Issues Found\n\n"
                    for i, issue in enumerate(issues, 1):
                        issue_type = issue.get('type', 'unknown')
                        line_start = issue.get('line_start', 'N/A')
                        line_end = issue.get('line_end', 'N/A')
                        description = issue.get('description', 'No description')
                        suggestion = issue.get('suggestion', 'No suggestion')
                        
                        report += f"{i}. **{issue_type.title()} Issue** (Lines {line_start}-{line_end})\n"
                        report += f"   - **Description**: {description}\n"
                        report += f"   - **Suggestion**: {suggestion}\n\n"
                else:
                    report += "✅ No issues found\n\n"
                    
            elif status == 'skipped':
                reason = review.get('reason', 'Unknown reason')
                report += f"⏭️ Skipped: {reason}\n\n"
                
            elif status == 'error':
                error = review.get('error', 'Unknown error')
                report += f"❌ Error: {error}\n\n"
        
        return report
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="CloudCurio AI Code Review")
    parser.add_argument('--model', default='llama3', help='Ollama model to use')
    parser.add_argument('--host', default='http://localhost:11434', help='Ollama host')
    parser.add_argument('--file', help='Specific file to review')
    parser.add_argument('--output', default='ai_code_review_report.md', help='Output report file')
    parser.add_argument('--pre-commit', action='store_true', help='Run as pre-commit hook')
    parser.add_argument('--base-ref', default='HEAD~1', help='Base reference for git diff')
    
    args = parser.parse_args()
    
    print("Starting CloudCurio AI Code Review...")
    
    # Initialize the reviewer
    reviewer = AICodeReviewer(model=args.model, host=args.host)
    
    # Check if Ollama is available
    if not reviewer.check_ollama_availability():
        print("❌ Ollama is not available. Please start Ollama service.")
        if not args.pre_commit:
            sys.exit(1)
        else:
            # For pre-commit, just exit silently
            sys.exit(0)
    
    # Pull the model if needed
    print(f"Ensuring model {args.model} is available...")
    if not reviewer.pull_model():
        print(f"❌ Could not pull model {args.model}")
        if not args.pre_commit:
            sys.exit(1)
        else:
            sys.exit(0)
    
    # Perform reviews
    reviews = []
    
    if args.file:
        # Review specific file
        if os.path.exists(args.file) and args.file.endswith('.py'):
            print(f"Reviewing {args.file}...")
            review = reviewer.review_code_file(args.file)
            reviews.append(review)
        else:
            print(f"❌ File {args.file} does not exist or is not a Python file")
            if not args.pre_commit:
                sys.exit(1)
            else:
                sys.exit(0)
    else:
        # Review changed files
        print("Reviewing changed files...")
        reviews = reviewer.review_changed_files(base_ref=args.base_ref)
    
    # Generate report
    if reviews:
        report = reviewer.generate_markdown_report(reviews)
        
        # Write report to file
        with open(args.output, 'w') as f:
            f.write(report)
        
        print(f"✅ AI code review report generated: {args.output}")
        
        # Print summary to console
        successful = len([r for r in reviews if r.get('status') == 'success'])
        print(f"Reviewed {len(reviews)} files, {successful} successful reviews")
        
        # For pre-commit, exit with error code if issues found
        if args.pre_commit and successful > 0:
            # Check if any reviews found serious issues
            issues_found = False
            for review in reviews:
                if review.get('status') == 'success':
                    issues = review.get('issues', [])
                    serious_issues = [i for i in issues if i.get('type') in ['bug', 'security']]
                    if serious_issues:
                        issues_found = True
                        print(f"⚠️  Serious issues found in {review.get('file')}:")
                        for issue in serious_issues:
                            print(f"   - {issue.get('description')}")
            
            if issues_found:
                print("❌ Pre-commit failed due to serious issues found")
                sys.exit(1)
    
    print("AI code review completed!")


if __name__ == "__main__":
    main()