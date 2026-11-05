"""Access checks for opening swipe review from a phone on the same Wi-Fi."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from swipe_review_server import COOKIE_NAME, access_allowed, redact_access_key


TOKEN = "phone-key-example"


class PhoneAccessTests(unittest.TestCase):
    def test_computer_loopback_does_not_need_the_key(self):
        self.assertTrue(access_allowed("127.0.0.1", TOKEN, "", "", ""))
        self.assertTrue(access_allowed("::1", "", "", "", ""))

    def test_phone_needs_the_key_from_the_link_header_or_cookie(self):
        self.assertFalse(access_allowed("192.168.1.20", TOKEN, "", "", ""))
        self.assertFalse(access_allowed("192.168.1.20", TOKEN, "wrong-key", "", ""))
        self.assertTrue(access_allowed("192.168.1.20", TOKEN, TOKEN, "", ""))
        self.assertTrue(access_allowed("192.168.1.20", TOKEN, "", TOKEN, ""))
        self.assertTrue(access_allowed("192.168.1.20", TOKEN, "", "", f"other=1; {COOKIE_NAME}={TOKEN}"))

    def test_open_lan_without_a_key_stays_closed(self):
        self.assertFalse(access_allowed("10.0.0.8", "", "", "", ""))

    def test_request_log_hides_the_key(self):
        line = redact_access_key(f'"GET /?k={TOKEN} HTTP/1.1"')
        self.assertNotIn(TOKEN, line)
        self.assertIn("k=redacted", line)


if __name__ == "__main__":
    unittest.main()
