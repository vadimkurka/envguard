"""EnvGuard CLI and checker regression tests."""

import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from click.testing import CliRunner
from envguard.checker import run_check
from envguard.cli import cli


class EnvGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = self.root / ".env"
        self.example = self.root / ".env.example"

    def write(self, env, example):
        self.env.write_text(env, encoding="utf-8")
        self.example.write_text(example, encoding="utf-8")

    def check(self):
        out = io.StringIO()
        passed = run_check(self.env, self.example, out=out)
        return passed, out.getvalue()

    def test_matching_files_pass(self):
        self.write("APP=ok\nNODE_ENV=production\n", "APP=sample\nNODE_ENV=dev\n")
        self.assertEqual(self.check()[0], True)

    def test_detects_missing_and_undocumented(self):
        self.write("EXTRA=yes\n", "REQUIRED=placeholder\n")
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertIn("REQUIRED", output)
        self.assertIn("EXTRA", output)

    def test_empty_and_quoted_empty(self):
        self.write('A=\nB=""\nC=  # comment\n', "A=1\nB=2\nC=3\n")
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertIn("A", output)
        self.assertIn("B", output)
        self.assertIn("C", output)

    def test_typo_suggestion(self):
        self.write("STRPE_SECRET_KEY=secret\n", "STRIPE_SECRET_KEY=sample\n")
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertIn("STRPE_SECRET_KEY -> STRIPE_SECRET_KEY", output)
        self.assertNotIn("secret\n", output)

    def test_ignores_comments_and_supports_export_and_quotes(self):
        self.write('# comment\nexport NAME="quoted # text"\nURL=https://example.com/#x\n',
                   "NAME=sample\nURL=sample\n")
        self.assertTrue(self.check()[0])

    def test_duplicate_key_is_failure(self):
        self.write("A=x\nA=y\n", "A=placeholder\n")
        self.assertIn("duplicate key A", self.check()[1])

    def test_invalid_key_without_echoing_value(self):
        self.write("BAD-NAME=private_value\n", "")
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertNotIn("private_value", output)

    def test_missing_file_is_failure(self):
        self.example.write_text("A=b\n", encoding="utf-8")
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertIn("Cannot read", output)

    def test_cli_exit_codes(self):
        self.write("NAME=ok\n", "NAME=sample\n")
        runner = CliRunner()
        args = ["check", "--env", str(self.env), "--example", str(self.example)]
        good = runner.invoke(cli, args)
        self.assertEqual(good.exit_code, 0, good.output)
        self.env.write_text("WRONG=value\n", encoding="utf-8")
        bad = runner.invoke(cli, args)
        self.assertEqual(bad.exit_code, 1, bad.output)

    def test_cli_help(self):
        result = CliRunner().invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("check", result.output)


if __name__ == "__main__":
    unittest.main()
