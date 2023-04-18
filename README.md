# codeprompt
An improvement from [chunrapeepat/codeprompt](https://github.com/chunrapeepat/codeprompt) with auto chunking 📚
- Use as CLI 🖥️
- Read selected from VSCode 🆚
- copy and paste to clipboard, directly 🪄

## Install 📥
```bash
pip install codeprompt
pipx install codeprompt
```

## Usage 🛠️
```bash
$ codeprompt
Open VSCode and Copy the paths (Shift + Alt + C) of the files you want to include in the prompt.
Press Enter to continue.

read 1 files
total number of tokens: 917


$ Press Enter to continue (Y, n) [Y/n]:  

$ What do you waht to ask ChatGPT? [Explain this to me.]:


Prompt is ready to be copied to clipboard.

Chunk 1/1 is copied to clipboard.
You act as my tech lead in understanding and working with a Git repository represented as text.

The repository's purpose is to provide context for various software development-related instructions.

The repository structure consists of sections that begin with "----", followed by a single line containing
the file path and file name, followed by a variable amount of lines containing the file contents. The text
representing the repository ends when the symbols "--END--" are encountered. Meanwhile,
Reply with "Aha" to allow me continue providing more context.

Any further text beyond "--END--" should be interpreted as instructions using the aforementioned code as
context. Instructions may include questions, requests to refactor, debug, find vulnerabilities, or make the
code more robust. The programming language can be determined from the file extension in the file path.
----
codeprompt\template.py
```
```python
import os
from pathlib import Path
from loguru import logger

import pyperclip
import frontmatter

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound, meta


def paste_from_clipboard():
    value = pyperclip.paste()
    return value


class TemplateManager:
    """
    Manage templates.
    """

    def __init__(self, template_dirs: list[Path]):
        self.log = logger
        self.template_dirs = template_dirs
        self.templates = []
        self.templates_env = None

    def template_builtin_variables(self):
        return {
            "clipboard": paste_from_clipboard,
        }


```
```
--END--
create add docstring to the function
```

## Special Thanks 🙏
1. <https://github.com/mmabrouk/chatgpt-wrapper> - good template idea, learn token count here, plus interactive TUI interface
2. <https://github.com/chunrapeepat/codeprompt> - original codeprompt
3. <https://github.com/Significant-Gravitas/Auto-GPT> - auto chunking, inject memory, and more
