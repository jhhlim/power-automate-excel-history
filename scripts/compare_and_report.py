"""Main script to compare Excel files and generate reports."""

import os
import json
from pathlib import Path
from src.excel_comparator import ExcelComparator
from src.change_detector import ChangeDetector
from src.report_generator import ReportGenerator


def main():
    """
    Main function to compare Excel files and save report.
    """
    # Get environment variables
    old_file_path = os.getenv('OLD_FILE_PATH')
    new_file_path = os.getenv('NEW_FILE_PATH')
    file_name = os.getenv('FILE_NAME', 'Excel File')
    
    if not old_file_path or not new_file_path:
        print("Error: OLD_FILE_PATH and NEW_FILE_PATH environment variables required")
        exit(1)
    
    # Check if files exist
    if not os.path.exists(old_file_path):
        print(f"Error: Old file not found at {old_file_path}")
        exit(1)
    
    if not os.path.exists(new_file_path):
        print(f"Error: New file not found at {new_file_path}")
        exit(1)
    
    print(f"Comparing files:")
    print(f"  Old: {old_file_path}")
    print(f"  New: {new_file_path}")
    print(f"  File name: {file_name}")
    print()
    
    try:
        # Compare files
        comparator = ExcelComparator()
        comparison = comparator.compare_files(old_file_path, new_file_path)
        print(f"Comparison complete. Changes found in {len(comparison)} sheet(s).")
        
        # Detect changes
        detector = ChangeDetector()
        changes = detector.detect_changes(comparison)
        summary = detector.get_summary()
        
        print(f"\nChange Summary:")
        print(f"  Total changes: {summary['total_changes']}")
        print(f"  Sheets affected: {summary['sheets_affected']}")
        print(f"  By type: {summary['by_type']}")
        
        # Generate reports
        generator = ReportGenerator(file_name=file_name)
        text_report = generator.generate_text_report(changes)
        html_report = generator.generate_html_report(changes)
        
        # Save reports to files
        report_dir = Path('reports')
        report_dir.mkdir(exist_ok=True)
        
        text_report_path = report_dir / 'report.txt'
        html_report_path = report_dir / 'report.html'
        json_report_path = report_dir / 'report.json'
        
        with open(text_report_path, 'w') as f:
            f.write(text_report)
        
        with open(html_report_path, 'w') as f:
            f.write(html_report)
        
        # Save JSON report for Power Automate
        json_report = {
            'status': 'success',
            'summary': summary,
            'file_name': file_name,
            'changes_detected': len(changes) > 0,
            'text_report': text_report,
            'html_report': html_report
        }
        
        with open(json_report_path, 'w') as f:
            json.dump(json_report, f, indent=2)
        
        print(f"\nReports saved:")
        print(f"  Text: {text_report_path}")
        print(f"  HTML: {html_report_path}")
        print(f"  JSON: {json_report_path}")
        
        # Set GitHub output for next step
        with open(os.getenv('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write(f"report_json={json_report_path}\n")
        
        exit(0)
    
    except Exception as e:
        print(f"Error comparing files: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()
