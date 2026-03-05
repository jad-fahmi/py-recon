# tests/test_scanner.py
# Unit tests for utility and validation functions

import unittest
import os
import json
from recon.utils import (
    validate_domain,
    validate_ip,
    create_output_folder,
    save_json,
    format_timestamp
)


class TestUtils(unittest.TestCase):

    # --- Validation Tests ---

    def test_valid_domain(self):
        """Valid domains should pass validation."""
        self.assertTrue(validate_domain("google.com"))
        self.assertTrue(validate_domain("sub.example.com"))
        self.assertTrue(validate_domain("my-site.co.uk"))

    def test_invalid_domain(self):
        """Invalid domains should fail validation."""
        self.assertFalse(validate_domain("notadomain"))
        self.assertFalse(validate_domain("192.168.1.1"))
        self.assertFalse(validate_domain(""))

    def test_valid_ip(self):
        """Valid IPs should pass validation."""
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("8.8.8.8"))
        self.assertTrue(validate_ip("0.0.0.0"))

    def test_invalid_ip(self):
        """Invalid IPs should fail validation."""
        self.assertFalse(validate_ip("999.999.999.999"))
        self.assertFalse(validate_ip("google.com"))
        self.assertFalse(validate_ip("192.168.1"))

    # --- Output Tests ---

    def test_create_output_folder(self):
        """Output folder should be created and exist."""
        folder = create_output_folder("test-target")
        self.assertTrue(os.path.exists(folder))

    def test_save_json(self):
        """JSON file should be created with correct content."""
        folder = create_output_folder("test-json")
        data = {"test": "value", "number": 42}
        filepath = save_json(data, folder, "test.json")
        self.assertTrue(os.path.exists(filepath))

        with open(filepath) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["test"], "value")
        self.assertEqual(loaded["number"], 42)

    def test_format_timestamp(self):
        """Timestamp should be a non-empty string."""
        ts = format_timestamp()
        self.assertIsInstance(ts, str)
        self.assertGreater(len(ts), 0)


if __name__ == "__main__":
    unittest.main()