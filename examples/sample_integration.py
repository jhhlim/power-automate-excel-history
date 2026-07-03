"""Example: Integrate with Power Automate workflow.

This module shows how to use the Excel History Tracker with Power Automate.
Power Automate can call this as an Azure Function or HTTP endpoint.
"""

import json
import os
from src.excel_comparator import ExcelComparator
from src.change_detector import ChangeDetector
from src.report_generator import ReportGenerator


def process_excel_changes(old_file_path: str, new_file_path: str, file_name: str = "Homologation Report") -> dict:
    """
    Process Excel file changes and generate a report.
    
    This is the main function that Power Automate would call.
    
    Args:
        old_file_path: Path to the previous version of the file
        new_file_path: Path to the current version of the file
        file_name: Name of the file for the report
        
    Returns:
        Dictionary with report data suitable for Power Automate
    """
    try:
        # Compare files
        comparator = ExcelComparator()
        comparison = comparator.compare_files(old_file_path, new_file_path)
        
        # Detect changes
        detector = ChangeDetector()
        changes = detector.detect_changes(comparison)
        
        # Generate reports
        generator = ReportGenerator(file_name=file_name)
        text_report = generator.generate_text_report(changes)
        html_report = generator.generate_html_report(changes)
        
        # Get summary
        summary = detector.get_summary()
        
        return {
            'status': 'success',
            'summary': summary,
            'text_report': text_report,
            'html_report': html_report,
            'changes_detected': len(changes) > 0
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error_message': str(e),
            'changes_detected': False
        }


def format_for_email(result: dict) -> dict:
    """
    Format the result for sending via Power Automate email.
    
    Args:
        result: Output from process_excel_changes()
        
    Returns:
        Dictionary ready for Power Automate email action
    """
    if result['status'] == 'error':
        return {
            'subject': 'Error Processing Excel File Changes',
            'body': f"An error occurred: {result['error_message']}"
        }
    
    if not result['changes_detected']:
        return {
            'subject': 'No Changes Detected in Excel File',
            'body': 'The Excel file has not been modified.'
        }
    
    summary = result['summary']
    
    # Create email subject
    total = summary['total_changes']
    sheets = summary['sheets_affected']
    subject = f"Excel Update: {total} change(s) detected in {sheets} sheet(s)"
    
    # Create email body - can use either text or html_report
    body = result['text_report']
    
    return {
        'subject': subject,
        'body': body,
        'html_body': result['html_report']  # Use this if Power Automate supports HTML
    }


# Power Automate HTTP Trigger Example
# This would be called from Power Automate webhook
def azure_function_handler(req):
    """
    Azure Function handler for Power Automate HTTP trigger.
    
    Expected request body:
    {
        "old_file_path": "/path/to/old/file.xlsx",
        "new_file_path": "/path/to/new/file.xlsx",
        "file_name": "Homologation Report"
    }
    """
    try:
        req_body = req.get_json()
        
        old_file = req_body.get('old_file_path')
        new_file = req_body.get('new_file_path')
        file_name = req_body.get('file_name', 'Excel File')
        
        if not old_file or not new_file:
            return {
                'status': 400,
                'body': {'error': 'Missing file paths'}
            }
        
        result = process_excel_changes(old_file, new_file, file_name)
        email_data = format_for_email(result)
        
        return {
            'status': 200,
            'body': email_data
        }
    
    except Exception as e:
        return {
            'status': 500,
            'body': {'error': str(e)}
        }


if __name__ == '__main__':
    # Example usage
    print("Power Automate Excel History Tracker - Example")
    print("This module should be deployed as an Azure Function or HTTP endpoint.")
    print("\nFor local testing, you would call:")
    print("  result = process_excel_changes('old.xlsx', 'new.xlsx')")
    print("  email_data = format_for_email(result)")
