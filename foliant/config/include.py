import re
from pathlib import Path
from urllib.request import urlopen

from yaml import load, add_constructor, Loader

from foliant.config.base import BaseParser


class Parser(BaseParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_constructor('!include', self._resolve_include_tag)

        self.logger = self.logger.getChild('yaml_include')
        self.logger.debug(f'Extension inited: {self.__dict__}')

    def _resolve_include_tag(self, _, node) -> str:
        '''Replace value after ``!include`` with the content of the referenced file.'''

        self.logger.debug('Start resolving !include tag')

        parts = node.value.split('#')

        if len(parts) == 1:
            path_ = parts[0]

            include_content = self._get_file_or_url_content(path_)
            return load(include_content, Loader)

        elif len(parts) == 2:
            path_, section = parts[0], parts[1]

            include_content = self._get_file_or_url_content(path_)
            return load(include_content, Loader)[section]

        else:
            raise ValueError('Invalid include syntax')

    def _get_file_or_url_content(self, path_: str) -> str or bytes:
        """
        Determine whether path_ is a path to local file or url. And return its content.
        """

        link_pattern = re.compile(r'https?://\S+')
        if link_pattern.search(path_):  # path_ is a URL
            self.logger.debug(f'Getting included content from the link {path_}')
            result = urlopen(path_).read()
        else:
            included_file_path = self.project_path / Path(path_).expanduser()
            self.logger.debug(f'Getting included content from the file {included_file_path}')
            with open(included_file_path, encoding='utf8') as f:
                result = f.read()
        return result
