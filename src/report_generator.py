"""Generates human-readable change summaries."""

from typing import List, Dict, Any
from datetime import datetime
from src.change_detector import Change, ChangeType


class ReportGenerator:
    """Generates formatted reports from detected changes."""

    def __init__(self, file_name: str = "Excel File"):
        self.file_name = file_name

    def generate_text_report(self, changes: List[Change]) -> str:
        """
        Generate a plain text report of changes.
        
        Args:
            changes: List of Change objects
            
        Returns:
            Formatted text report
        """
        report = []
        report.append(f"Excel File Change Summary Report")
        report.append(f"File: {self.file_name}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)
        report.append("")
        
        if not changes:
            report.append("No changes detected.")
            return "\n".join(report)
        
        # Group changes by sheet
        changes_by_sheet = {}
        for change in changes:
            if change.sheet_name not in changes_by_sheet:
                changes_by_sheet[change.sheet_name] = []
            changes_by_sheet[change.sheet_name].append(change)
        
        # Generate report per sheet
        for sheet_name, sheet_changes in changes_by_sheet.items():
            report.append(f"Sheet: {sheet_name}")
            report.append("-" * 60)
            
            for change in sheet_changes:
                if change.change_type == ChangeType.ROWS_ADDED:
                    report.append(f"\n✓ ROWS ADDED: {len(change.data)} row(s)")
                    for idx, row in enumerate(change.data[:5], 1):
                        report.append(f"  Row {idx}: {self._format_row(row)}")
                    if len(change.data) > 5:
                        report.append(f"  ... and {len(change.data) - 5} more row(s)")
                
                elif change.change_type == ChangeType.ROWS_DELETED:
                    report.append(f"\n✗ ROWS DELETED: {len(change.data)} row(s)")
                    for idx, row in enumerate(change.data[:5], 1):
                        report.append(f"  Row {idx}: {self._format_row(row)}")
                    if len(change.data) > 5:
                        report.append(f"  ... and {len(change.data) - 5} more row(s)")
                
                elif change.change_type == ChangeType.HEADERS_CHANGED:
                    report.append(f"\n⚠ HEADERS CHANGED")
            
            report.append("")
        
        return "\n".join(report)

    def generate_html_report(self, changes: List[Change]) -> str:
        """
        Generate an HTML report of changes.
        
        Args:
            changes: List of Change objects
            
        Returns:
            Formatted HTML report
        """
        html = []
        html.append("<html>")
        html.append("<head>")
        html.append("<style>")
        html.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        html.append("h1 { color: #333; }")
        html.append("h2 { color: #0066cc; border-bottom: 2px solid #0066cc; }")
        html.append(".added { color: green; }")
        html.append(".deleted { color: red; }")
        html.append(".modified { color: orange; }")
        html.append("table { border-collapse: collapse; width: 100%; margin: 10px 0; }")
        html.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
        html.append("th { background-color: #f2f2f2; }")
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        html.append(f"<h1>Excel File Change Summary</h1>")
        html.append(f"<p><strong>File:</strong> {self.file_name}</p>")
        html.append(f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        if not changes:
            html.append("<p>No changes detected.</p>")
        else:
            # Group changes by sheet
            changes_by_sheet = {}
            for change in changes:
                if change.sheet_name not in changes_by_sheet:
                    changes_by_sheet[change.sheet_name] = []
                changes_by_sheet[change.sheet_name].append(change)
            
            for sheet_name, sheet_changes in changes_by_sheet.items():
                html.append(f"<h2>Sheet: {sheet_name}</h2>")
                
                for change in sheet_changes:
                    if change.change_type == ChangeType.ROWS_ADDED:
                        html.append(f"<div class='added'><strong>✓ Rows Added:</strong> {len(change.data)} row(s)</div>")
                        html.append("<table>")
                        for idx, row in enumerate(change.data[:10], 1):
                            html.append(f"<tr><td>Row {idx}:</td><td>{self._format_row(row)}</td></tr>")
                        if len(change.data) > 10:
                            html.append(f"<tr><td colspan='2'>... and {len(change.data) - 10} more row(s)</td></tr>")
                        html.append("</table>")
                    
                    elif change.change_type == ChangeType.ROWS_DELETED:
                        html.append(f"<div class='deleted'><strong>✗ Rows Deleted:</strong> {len(change.data)} row(s)</div>")
                        html.append("<table>")
                        for idx, row in enumerate(change.data[:10], 1):
                            html.append(f"<tr><td>Row {idx}:</td><td>{self._format_row(row)}</td></tr>")
                        if len(change.data) > 10:
                            html.append(f"<tr><td colspan='2'>... and {len(change.data) - 10} more row(s)</td></tr>")
                        html.append("</table>")
                    
                    elif change.change_type == ChangeType.HEADERS_CHANGED:
                        html.append(f"<div class='modified'><strong>⚠ Headers Changed</strong></div>")
        
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)

    def _format_row(self, row: List[Any]) -> str:
        """
        Format a row for display.
        
        Args:
            row: Row data
            
        Returns:
            Formatted row string
        """
        # Filter out None values and format
        formatted = [str(cell) if cell is not None else "" for cell in row]
        return " | ".join(formatted)
