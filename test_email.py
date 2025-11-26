#!/usr/bin/env python3
"""
Test script for the SMTP email functionality.
This script verifies that the email sending function works correctly.
"""
import json
import os
import sys

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from submit import format_confirmation_email, format_form_data


def test_format_confirmation_email():
    """Test the confirmation email formatting."""
    print("Testing confirmation email formatting...")
    html = format_confirmation_email("John Doe")
    
    # Check that the HTML contains expected content
    assert "John Doe" in html
    assert "Workshop Registration Confirmation" in html
    assert "Thank you for registering" in html
    assert "confirmation" in html.lower()
    
    # Ensure it doesn't contain submission details
    assert "Submission Details" not in html
    
    print("✓ Confirmation email format test passed")
    return True


def test_format_form_data():
    """Test the form data formatting for admin email."""
    print("Testing form data formatting...")
    
    test_data = {
        "name": {"label": "Name", "value": "John Doe"},
        "email": {"label": "Email", "value": "john@example.com"},
        "gender": {"label": "Gender", "value": "Male"},
        "age": {"label": "Age", "value": "25-30"},
        "phone": {"label": "Phone", "value": "+1234567890"},
        "workshops1": {"label": "Workshop 1", "value": ["Workshop A", "Workshop B"]}
    }
    
    html = format_form_data(test_data)
    
    # Check that all data is present
    assert "John Doe" in html
    assert "john@example.com" in html
    assert "Male" in html
    assert "25-30" in html
    assert "+1234567890" in html
    assert "Workshop A, Workshop B" in html
    assert "Submission Details" in html
    
    print("✓ Form data format test passed")
    return True


def test_email_structure():
    """Test that emails have proper HTML structure."""
    print("Testing email HTML structure...")
    
    confirmation = format_confirmation_email("Test User")
    admin_email = format_form_data({"name": {"label": "Name", "value": "Test"}})
    
    # Check HTML structure for both emails
    for html in [confirmation, admin_email]:
        assert "<html>" in html
        assert "</html>" in html
        assert "<head>" in html
        assert "<style>" in html
        assert "<body>" in html
        assert ".container" in html
    
    print("✓ Email HTML structure test passed")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running Email Functionality Tests")
    print("="*50 + "\n")
    
    tests = [
        test_format_confirmation_email,
        test_format_form_data,
        test_email_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    # Note about SMTP credentials
    print("Note: To test actual email sending, configure SMTP credentials in .env")
    print("The email sending function requires:")
    print("  - SMTP_SERVER")
    print("  - SMTP_PORT")
    print("  - SMTP_USERNAME")
    print("  - SMTP_PASSWORD")
    print("  - EMAIL_SUBMISSIONS (optional, for admin emails)")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
