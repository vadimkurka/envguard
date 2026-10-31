"""Command-line interface for EnvGuard."""

import click
from .checker import run_check


@click.group()
@click.version_option("0.1.0", prog_name="EnvGuard")
def cli():
    """Catch missing, mistyped and empty environment variables."""


@cli.command()
@click.option("--env", "env_path", default=".env", show_default=True, type=click.Path(dir_okay=False))
@click.option("--example", "example_path", default=".env.example", show_default=True, type=click.Path(dir_okay=False))
def check(env_path, example_path):
    """Compare .env to .env.example without showing secret values."""
    if not run_check(env_path, example_path):
        raise SystemExit(1)
