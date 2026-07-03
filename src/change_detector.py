"""Detects and categorizes Excel file changes."""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class ChangeType(Enum):
    """Types of changes detected in Excel files."""
    ROWS_ADDED = "rows_added"
    ROWS_DELETED = "rows_deleted"
    ROWS_MODIFIED = "rows_modified"
    HEADERS_CHANGED = "headers_changed"
    NEW_SHEET = "new_sheet"
    SHEET_DELETED = "sheet_deleted"


@dataclass
class Change:
    """Represents a single change in an Excel file."""
    change_type: ChangeType
    sheet_name: str
    details: str
    data: Any = None


class ChangeDetector:
    """Detects and categorizes changes in Excel files."""

    def __init__(self):
        self.changes: List[Change] = []

    def detect_changes(self, comparison_result: Dict[str, Dict[str, Any]]) -> List[Change]:
        """
        Detect and categorize changes from comparison result.
        
        Args:
            comparison_result: Output from ExcelComparator.compare_files()
            
        Returns:
            List of Change objects
        """
        self.changes = []
        
        for sheet_name, changes in comparison_result.items():
            # Check for added rows
            if changes['rows_added']:
                self.changes.append(
                    Change(
                        change_type=ChangeType.ROWS_ADDED,
                        sheet_name=sheet_name,
                        details=f"{len(changes['rows_added'])} row(s) added",
                        data=changes['rows_added']
                    )
                )
            
            # Check for deleted rows
            if changes['rows_deleted']:
                self.changes.append(
                    Change(
                        change_type=ChangeType.ROWS_DELETED,
                        sheet_name=sheet_name,
                        details=f"{len(changes['rows_deleted'])} row(s) deleted",
                        data=changes['rows_deleted']
                    )
                )
            
            # Check for header changes
            if changes['headers_changed']:
                self.changes.append(
                    Change(
                        change_type=ChangeType.HEADERS_CHANGED,
                        sheet_name=sheet_name,
                        details="Column headers changed",
                        data=None
                    )
                )
        
        return self.changes

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all detected changes.
        
        Returns:
            Dictionary with change counts and types
        """
        summary = {
            'total_changes': len(self.changes),
            'sheets_affected': len(set(c.sheet_name for c in self.changes)),
            'by_type': {}
        }
        
        for change in self.changes:
            change_type = change.change_type.value
            if change_type not in summary['by_type']:
                summary['by_type'][change_type] = 0
            summary['by_type'][change_type] += 1
        
        return summary
