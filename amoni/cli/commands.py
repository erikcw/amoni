# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Amoni project team members listed at
# https://github.com/anvilistas/amoni/graphs/contributors
#
# This software is published at https://github.com/anvilistas/amoni
import typer
from cookiecutter.main import cookiecutter
from python_on_whales import docker

__version__ = "0.0.1"

amoni = typer.Typer()


@amoni.callback()
def main():
    pass


@amoni.command()
def init(
    project: str = typer.Option("", help="Project Name", prompt=True),
    app_folder_name: str = typer.Option(
        "hello_world", help="App Folder Name", prompt=True
    ),
):
    """Initialise an amoni project

    Parameters
    ----------
    project
        The name of the amoni project folder to create
    app_folder_name
        The name of folder within the 'app' folder which contains the app to be run
    """
    cookiecutter(
        "https://github.com/anvilistas/amoni-cookiecutter.git",
        no_input=True,
        extra_context={"project_name": project, "app_folder_name": app_folder_name},
    )
    typer.echo(f"amoni project created in {project} directory")


@amoni.command()
def start():
    """Start the anvil app and db servers"""
    typer.echo("Checking for newer images")
    docker.compose.pull(["app"])
    typer.echo("Starting anvil app and database servers")
    docker.compose.up(["app"], detach=True)
    typer.echo("Your app is available at http://localhost:3030")


@amoni.command()
def stop():
    """Stop the anvil app and db servers"""
    typer.echo("Stopping the anvil app and database servers...")
    docker.compose.down()
    typer.echo("Done")


@amoni.command()
def test():
    """Run the test suite"""
    typer.echo("Checking for newer images")
    docker.compose.pull(["test_runner"])
    docker.compose.run("test_runner")
