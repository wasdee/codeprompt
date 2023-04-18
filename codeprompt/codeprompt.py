from pathlib import Path
from pydantic import BaseModel
import pyperclip
from codeprompt.techniques.count_token import count_token
import click

# 167 tokens
context_prompt = """You act as my tech lead in understanding and working with a Git repository represented as text. 

The repository's purpose is to provide context for various software development-related instructions. 

The repository structure consists of sections that begin with "----", followed by a single line containing 
the file path and file name, followed by a variable amount of lines containing the file contents. The text 
representing the repository ends when the symbols "--END--" are encountered. Meanwhile, 
Reply with "Aha" to allow me continue providing more context. 

Any further text beyond "--END--" should be interpreted as instructions using the aforementioned code as 
context. Instructions may include questions, requests to refactor, debug, find vulnerabilities, or make the 
code more robust. The programming language can be determined from the file extension in the file path.
"""

# highlight multiple files in vscode and click copy path\


class File(BaseModel):
    path: str
    content: str
    filesize: int
    num_tokens: int


from random import shuffle


class PromptGenerator:
    def __init__(self, len_function=count_token, max_length=8192 - 1000):
        self.len_function = len_function
        self.max_length = max_length

        self.chunks = [""]
        self.current_chunk = 0
        self.current_chunk_length = 0

        self.add_first_text(context_prompt)

    @property
    def left_length(self):
        return self.max_length - self.current_chunk_length

    def add_first_text(self, text):
        text_len = self.len_function(text)
        self.chunks[0] += text
        self.current_chunk_length += text_len

    def create_new_chunk(self):
        # add new chunk
        self.current_chunk += 1
        self.current_chunk_length = 0
        self.chunks.append("")

    def add_text(self, text, text_len=None):
        text_len = text_len or self.len_function(text)
        if text_len > self.left_length:
            self.create_new_chunk()

        self.chunks[self.current_chunk] += text
        self.current_chunk_length += text_len

    def add_files(self, files: list[File]):
        self.add_text(f"----\n")

        n = len(files)
        for i, file in enumerate(files):
            # prevent file content is not in the same chunk
            if file.num_tokens + 20 > self.left_length:
                self.create_new_chunk()
            self.add_text(f"{file.path}\n")
            self.add_text(f"```\n{file.content}\n```\n", text_len=file.num_tokens)
            if i != n - 1:
                self.add_text(f"----\n")
            else:
                self.add_text(f"--END--\n")


def main():
    # ask user to copy paths
    click.echo(
        "Open VSCode and Copy the paths (Shift + Alt + C) of the files you want to include in the prompt."
    )
    click.echo("Press Enter to continue.")
    click.getchar()

    clipboard_content = pyperclip.paste()
    absolute_files_and_dirs_str: list[str] = clipboard_content.splitlines()
    absolute_files_and_dirs: list[Path] = [
        Path(file) for file in absolute_files_and_dirs_str
    ]

    # replace directory with files inside directory
    files_and_dirs: list[Path] = []
    for file in absolute_files_and_dirs:
        if file.is_dir():
            files_and_dirs.extend(file.glob("**/*"))
        else:
            files_and_dirs.append(file)

    # remove directories
    files_objs = [file for file in files_and_dirs if file.is_file()]

    files: list[File] = []
    for file in files_objs:
        with open(file, "r") as f:
            content = f.read()
            filesize = len(content)
            num_tokens = count_token(content)
            files.append(
                File(
                    path=str(file.relative_to(Path.cwd())),
                    content=content,
                    filesize=filesize,
                    num_tokens=num_tokens,
                )
            )

    # shuffle files to make size distribution more even
    shuffle(files)

    click.echo(f"read {len(files)} files")
    n_token = sum([file.num_tokens for file in files])
    click.echo(f"total number of tokens: {n_token}")

    # continue (Y, n)
    if not click.confirm("Press Enter to continue (Y, n)", default=True):
        exit(0)

    prompt_generator = PromptGenerator()
    prompt_generator.add_files(files)

    user_instruction = click.prompt(
        "What do you waht to ask ChatGPT?", default="Explain this to me."
    )
    prompt_generator.add_text(user_instruction)

    click.echo("Prompt is ready to be copied to clipboard.\n")

    n_chunks = len(prompt_generator.chunks)
    for i, chunk in enumerate(prompt_generator.chunks):
        click.echo(f"Chunk {i + 1}/{n_chunks} is copied to clipboard.")
        click.echo(chunk, color="green")
        pyperclip.copy(chunk)
        if i != n_chunks - 1:
            click.confirm("Press Enter to continue (Y, n)", default=True)

    # write to file
    # with open("prompt.txt", "w") as f:
    #     f.write(prompt_generator.chunks[0])


if __name__ == "__main__":
    main()
