"""Unit tests for the Excel comparator."""

import unittest
import os
from src.excel_comparator import ExcelComparator
from src.change_detector import ChangeDetector, ChangeType
from src.report_generator import ReportGenerator


class TestExcelComparator(unittest.TestCase):
    """Test cases for ExcelComparator."""

    def setUp(self):
        """Set up test fixtures."""
        self.comparator = ExcelComparator()

    def test_compare_sheets_with_added_rows(self):
        """Test detection of added rows."""
        old_data = [
            ['Name', 'Status'],
            ['Item A', 'Active'],
            ['Item B', 'Inactive']
        ]
        
        new_data = [
            ['Name', 'Status'],
            ['Item A', 'Active'],
            ['Item B', 'Inactive'],
            ['Item C', 'Active']
        ]
        
        result = self.comparator.compare_sheets(old_data, new_data)
        
        self.assertTrue(len(result['rows_added']) > 0)
        self.assertEqual(len(result['rows_deleted']), 0)

    def test_compare_sheets_with_deleted_rows(self):
        """Test detection of deleted rows."""
        old_data = [
            ['Name', 'Status'],
            ['Item A', 'Active'],
            ['Item B', 'Inactive'],
            ['Item C', 'Active']
        ]
        
        new_data = [
            ['Name', 'Status'],
            ['Item A', 'Active'],
            ['Item B', 'Inactive']
        ]
        
        result = self.comparator.compare_sheets(old_data, new_data)
        
        self.assertEqual(len(result['rows_added']), 0)
        self.assertTrue(len(result['rows_deleted']) > 0)

    def test_compare_sheets_no_changes(self):
        """Test when there are no changes."""
        data = [
            ['Name', 'Status'],
            ['Item A', 'Active'],
            ['Item B', 'Inactive']
        ]
        
        result = self.comparator.compare_sheets(data, data)
        
        self.assertEqual(len(result['rows_added']), 0)
        self.assertEqual(len(result['rows_deleted']), 0)
        self.assertFalse(result['headers_changed'])


class TestChangeDetector(unittest.TestCase):
    """Test cases for ChangeDetector."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = ChangeDetector()

    def test_detect_changes(self):
        """Test change detection."""
        comparison = {
            'Sheet1': {
                'rows_added': [['New', 'Row']],
                'rows_deleted': [],
                'rows_modified': 1,
                'headers_changed': False
            }
        }
        
        changes = self.detector.detect_changes(comparison)
        
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, ChangeType.ROWS_ADDED)

    def test_get_summary(self):
        """Test summary generation."""
        comparison = {
            'Sheet1': {
                'rows_added': [['New', 'Row']],
                'rows_deleted': [],
                'rows_modified': 1,
                'headers_changed': False
            }
        }
        
        self.detector.detect_changes(comparison)
        summary = self.detector.get_summary()
        
        self.assertEqual(summary['total_changes'], 1)
        self.assertEqual(summary['sheets_affected'], 1)


class TestReportGenerator(unittest.TestCase):
    """Test cases for ReportGenerator."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = ReportGenerator('Test File')

    def test_generate_text_report(self):
        """Test text report generation."""
        from src.change_detector import Change, ChangeType
        
        changes = [
            Change(
                change_type=ChangeType.ROWS_ADDED,
                sheet_name='Sheet1',
                details='1 row(s) added',
                data=[['New', 'Row']]
            )
        ]
        
        report = self.generator.generate_text_report(changes)
        
        self.assertIn('Test File', report)
        self.assertIn('Sheet1', report)
        self.assertIn('ROWS ADDED', report)

    def test_generate_html_report(self):
        """Test HTML report generation."""
        from src.change_detector import Change, ChangeType
        
        changes = [
            Change(
                change_type=ChangeType.ROWS_ADDED,
                sheet_name='Sheet1',
                details='1 row(s) added',
                data=[['New', 'Row']]
            )
        ]
        
        report = self.generator.generate_html_report(changes)
        
        self.assertIn('<html>', report)
        self.assertIn('Test File', report)
        self.assertIn('Sheet1', report)


if __name__ == '__main__':
    unittest.main()
