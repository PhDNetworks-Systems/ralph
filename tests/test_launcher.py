"""Offline launcher contract checks: no real model, subscription or network use."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LauncherTests(unittest.TestCase):
    def run_launcher(self, tool, *, code=0, output='<promise>COMPLETE</promise>', extra=(), large=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy2(ROOT / 'ralph.sh', root / 'ralph.sh')
            for name in ('prompt.md', 'CLAUDE.md'):
                (root / name).write_text('synthetic ' + name + '\n')
            bindir = root / 'bin'
            bindir.mkdir()
            # One harmless executable supplies both CLIs and records each call.
            mock = '#!/bin/bash\nprintf "%s\\n" "$*" >> "$MOCK_CALLS"\ncat > "$MOCK_INPUT"\nprintf "%s\\n" "$MOCK_OUTPUT"\nif [[ "$MOCK_LARGE" == 1 ]]; then head -c 2000000 /dev/zero | tr "\\0" x; fi\nexit "$MOCK_CODE"\n'
            for name in ('amp', 'claude'):
                path = bindir / name
                path.write_text(mock)
                path.chmod(0o700)
            env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.defpath,
                       MOCK_CALLS=str(root / 'calls'), MOCK_INPUT=str(root / 'input'),
                       MOCK_OUTPUT=output, MOCK_CODE=str(code), MOCK_LARGE=str(int(large)))
            result = subprocess.run(['bash', str(root / 'ralph.sh'), '--tool', tool,
                                     '3', *extra], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=5)
            calls = (root / 'calls').read_text().splitlines() if (root / 'calls').exists() else []
            received = (root / 'input').read_text() if (root / 'input').exists() else ''
            return result, calls, received

    def test_amp_keeps_default_permissions_and_prompt(self):
        result, calls, received = self.run_launcher('amp')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(calls, [''])
        self.assertEqual(received, 'synthetic prompt.md\n')

    def test_claude_keeps_default_permissions_and_single_story_prompt(self):
        result, calls, received = self.run_launcher('claude')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(calls, ['--print'])
        self.assertEqual(received, 'synthetic CLAUDE.md\n')

    def test_failed_invocation_stops_without_retry_or_false_completion(self):
        for tool in ('amp', 'claude'):
            with self.subTest(tool=tool):
                result, calls, _ = self.run_launcher(tool, code=42)
                self.assertEqual(result.returncode, 42)
                self.assertEqual(len(calls), 1)
                self.assertNotIn('completed all tasks', result.stdout)

    def test_large_successful_response_does_not_lose_completion_on_sigpipe(self):
        for tool in ('amp', 'claude'):
            with self.subTest(tool=tool):
                result, calls, _ = self.run_launcher(tool, large=True)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(len(calls), 1)
                self.assertIn('completed all tasks', result.stdout)

    def test_invalid_tool_never_invokes_cli(self):
        result, calls, _ = self.run_launcher('invalid')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(calls, [])

    def test_missing_tool_argument_is_rejected(self):
        result = subprocess.run(['bash', str(ROOT / 'ralph.sh'), '--tool'],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn('--tool requires', result.stderr)


if __name__ == '__main__':
    unittest.main()
