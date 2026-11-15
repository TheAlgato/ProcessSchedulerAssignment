import unittest
from unittest.mock import Mock, patch

import setup


class SetupTests(unittest.TestCase):
    def test_declining_environment_creation_stops_setup(self):
        with patch.object(setup, 'ENV_PYTHON', Mock(exists=Mock(return_value=False))), \
             patch.object(setup, 'ENV', Mock(exists=Mock(return_value=False))), \
             patch('builtins.input', return_value='n'), patch.object(setup.venv, 'create') as create:
            self.assertEqual(setup.main(), 0)
            create.assert_not_called()

    def test_declining_install_never_starts_dashboard(self):
        with patch.object(setup, 'ENV_PYTHON', Mock(exists=Mock(return_value=True))), \
             patch.object(setup.subprocess, 'run', return_value=Mock(returncode=1)), \
             patch.object(setup.subprocess, 'call') as start, patch('builtins.input', return_value='n'):
            self.assertEqual(setup.main(), 0)
            start.assert_not_called()


if __name__ == '__main__':
    unittest.main()
