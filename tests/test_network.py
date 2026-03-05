# tests/test_network.py
# Unit tests for the Network module

import unittest
from recon.network import scan_port, scan_ports, grab_banner


class TestNetwork(unittest.TestCase):

    # --- Port Scanner Tests ---

    def test_open_port_returns_open(self):
        """Port 80 on scanme.nmap.org should be open."""
        result = scan_port("scanme.nmap.org", 80)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status"], "open")

    def test_closed_port_returns_closed(self):
        """Port 9999 should be closed on scanme.nmap.org."""
        result = scan_port("scanme.nmap.org", 9999)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status"], "closed")

    def test_scan_port_returns_dict(self):
        """scan_port should always return a dictionary."""
        result = scan_port("scanme.nmap.org", 80)
        self.assertIsInstance(result, dict)
        self.assertIn("port", result)
        self.assertIn("status", result)

    def test_scan_multiple_ports_returns_list(self):
        """scan_ports should return a list."""
        result = scan_ports("scanme.nmap.org", [80, 443, 9999])
        self.assertIsInstance(result, list)

    def test_scan_multiple_ports_only_open(self):
        """scan_ports should only return open ports."""
        result = scan_ports("scanme.nmap.org", [80, 9999, 9998])
        for port_info in result:
            self.assertEqual(port_info["status"], "open")

    # --- Banner Grabbing Tests ---

    def test_banner_grab_returns_string(self):
        """Banner grab should always return a string."""
        result = grab_banner("scanme.nmap.org", 80)
        self.assertIsInstance(result, str)

    def test_banner_grab_closed_port_returns_empty(self):
        """Banner grab on closed port should return empty string."""
        result = grab_banner("scanme.nmap.org", 9999)
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()