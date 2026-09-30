"""Unit tests for parser and stub commands."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src")
)
from main import parse_line, cmd_ls, cmd_cd, ParseError  # noqa: E402


class TestParser(unittest.TestCase):
    """Tests for parse_line function."""

    def test_simple_command(self):
        """Command without arguments."""
        cmd, args = parse_line("ls")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, [])

    def test_command_with_args(self):
        """Command with several arguments."""
        cmd, args = parse_line("ls -la /home")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["-la", "/home"])

    def test_quoted_argument(self):
        """Quoted argument stays one item."""
        cmd, args = parse_line('ls "hello world"')
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["hello world"])

    def test_single_quoted_argument(self):
        """Single-quoted argument stays one item."""
        cmd, args = parse_line("cd 'my folder'")
        self.assertEqual(cmd, "cd")
        self.assertEqual(args, ["my folder"])

    def test_unclosed_quote_raises(self):
        """Unclosed quotation raises ParseError."""
        with self.assertRaises(ParseError):
            parse_line('ls "hello')

    def test_empty_line(self):
        """Blank input returns empty command."""
        cmd, args = parse_line("   ")
        self.assertEqual(cmd, "")
        self.assertEqual(args, [])


class TestStubs(unittest.TestCase):
    """Tests for stub commands."""

    def test_ls_echoes_args(self):
        """ls returns its name and args."""
        result = cmd_ls(["-a"])
        self.assertIn("ls", result)
        self.assertIn("-a", result)

    def test_cd_echoes_args(self):
        """cd returns its name and args."""
        result = cmd_cd(["/tmp"])
        self.assertIn("cd", result)
        self.assertIn("/tmp", result)


if __name__ == "__main__":
    unittest.main()