[![](https://img.shields.io/pypi/v/foliantcontrib.yaml_include.svg)](https://pypi.org/project/foliantcontrib.yaml_include/)  [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.yaml_include.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.yaml_include)

# YAMLInclude Extension

YAMLInclude is a configuration extension for Foliant to include parts of configuration from YAML-files.

It resolves `!include` YAML tags in the project config and inside XML-tags parameters.

## Installation

```bash
$ pip install foliantcontrib.include
```

## Usage

The syntax of the `!include` YAML tag is:

`!include <file>[#<key>]`

Where `file` may be

- path to local file in Foliant project root,
- direct link to a file on remote server.

An optional `#<key>` part is used to get a key from the mapping stored inside `<file>`.

**Including a local file**

Config example:

```yaml
chapters: !include chapters.yml
```

In this example the `chapters.yml` file should be placed in your Foliant project root.

if the contents of `chapters.yml` are as follows:

```yaml
# chapters.yml

- index.md
- description.md
```

then the resulting config after applying the extension will be:

```yaml
chapters:
    - index.md
    - description.md
```

**Including part of a local file**

Config example:

```yaml
chapters: !include chapters.yml#chapters_for_pdf
```

In this example the `chapters.yml` file should be placed in your Foliant project root. 

if the contents of `chapters.yml` are as follows:

```yaml
# chapters.yml

chapters_for_site:
    - index_site.md
    - description_site.md
chapters_for_pdf:
    - index.md
    - description.md
```

then the resulting config after applying the extension will be:

```yaml
chapters:
    - index.md
    - description.md
```

**Including a remote file**

Config example:

```yaml
chapters: !include http://example.com/chapters.yml
```

In this example the `chapters.yml` file is stored on the website `http://example.com/`.

if the contents of `chapters.yml` are as follows:

```yaml
# chapters.yml

- index.md
- description.md
```

then the resulting config after applying the extension will be:

```yaml
chapters:
    - index.md
    - description.md
```

**Including part of a remote file**

Config example:

```yaml
chapters: !include chapters.yml#chapters_for_pdf
```

In this example the `chapters.yml` file is stored on the website `http://example.com/`.

if the contents of `chapters.yml` are as follows:

```yaml
# chapters.yml

chapters_for_site:
    - index_site.md
    - description_site.md
chapters_for_pdf:
    - index.md
    - description.md
```

then the resulting config after applying the extension will be:

```yaml
chapters:
    - index.md
    - description.md
```
