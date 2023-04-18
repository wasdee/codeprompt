import click
from github import Github
from getpass import getpass


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--username",
    prompt="Your GitHub username",
    help="The GitHub username to authenticate with.",
)
@click.option(
    "--repo",
    prompt="Repository (format: owner/repo)",
    help="The GitHub repository to list files and directories from.",
)
@click.argument("path", default="", required=False)
def list(username, repo, path):
    """List the directories and files of a GitHub repository."""

    password = getpass("Enter your GitHub password: ")
    g = Github(username, password)

    try:
        repo_obj = g.get_repo(repo)
    except Exception as e:
        print(f"Error: {e}")
        return

    if path == "":
        contents = repo_obj.get_contents("")
    else:
        contents = repo_obj.get_contents(path)

    for content in contents:
        print(content.name)


@click.command()
@click.option(
    "--username",
    prompt="Your GitHub username",
    help="The GitHub username to authenticate with.",
)
@click.option(
    "--repo",
    prompt="Repository (format: owner/repo)",
    help="The GitHub repository to select a file or directory from.",
)
@click.argument("path", required=True)
def select(username, repo, path):
    """Select a file or directory from a GitHub repository."""

    password = getpass("Enter your GitHub password: ")
    g = Github(username, password)

    try:
        repo_obj = g.get_repo(repo)
    except Exception as e:
        print(f"Error: {e}")
        return

    try:
        content = repo_obj.get_contents(path)
        if content.type == "dir":
            print(f"Selected directory: {content.path}")
        elif content.type == "file":
            print(f"Selected file: {content.path}")
        else:
            print("Invalid path")
    except Exception as e:
        print(f"Error: {e}")


cli.add_command(list)
cli.add_command(select)

if __name__ == "__main__":
    cli()
