from unittest import TestCase
from unittest.mock import patch, mock_open, Mock
from foliant_test.config_extension import ConfigExtensionTestFramework


class TestInclude(TestCase):
    def setUp(self):
        self.ctf = ConfigExtensionTestFramework('yaml_include')

    def test_include_simple(self):
        source = 'param: !include part.yml'
        part_yml = 'key: [val1, val2, val3]\n'
        expected = {
            'param': {
                'key': ['val1', 'val2', 'val3']
            }
        }
        self.ctf.config_path = self.ctf.config_path.resolve()

        with patch("foliant.config.yaml_include.open", mock_open(read_data=part_yml)):
            self.ctf.test_extension(input_config=source, expected_config=expected, keep=True)

    def test_include_get(self):
        source = 'param: !include part.yml#key'
        part_yml = 'key: [val1, val2, val3]\nanother_key: ignored\n'
        expected = {
            'param': ['val1', 'val2', 'val3']
        }
        self.ctf.config_path = self.ctf.config_path.resolve()

        with patch("foliant.config.yaml_include.open", mock_open(read_data=part_yml)):
            self.ctf.test_extension(input_config=source, expected_config=expected, keep=True)

    def test_include_remote(self):
        source = 'param: !include http://example.com/part.yml'
        part_yml = 'key: [val1, val2, val3]\n'
        expected = {
            'param': {
                'key': ['val1', 'val2', 'val3']
            }
        }
        self.ctf.config_path = self.ctf.config_path.resolve()

        with patch('foliant.config.yaml_include.urlopen') as mock_urlopen:
            mock_read = Mock()
            mock_read.read.return_value = part_yml
            mock_urlopen.return_value = mock_read
            self.ctf.test_extension(input_config=source, expected_config=expected, keep=True)

    def test_include_remote_get(self):
        source = 'param: !include http://example.com/part.yml#key'
        part_yml = 'key: [val1, val2, val3]\nanother_key: ignored\n'
        expected = {
            'param': ['val1', 'val2', 'val3']
        }
        self.ctf.config_path = self.ctf.config_path.resolve()

        with patch('foliant.config.yaml_include.urlopen') as mock_urlopen:
            mock_read = Mock()
            mock_read.read.return_value = part_yml
            mock_urlopen.return_value = mock_read
            self.ctf.test_extension(input_config=source, expected_config=expected, keep=True)
