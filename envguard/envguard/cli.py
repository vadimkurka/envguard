import sys
import click
from .checker import run_check

@click.group()
@click.version_option("0.1.0", prog_name="EnvGuard")
def cli():
    """EnvGuard — catch broken .env files before they break your app."""
    pass

@cli.command()
@click.option("--env", default=".env", show_default=True, help="Path to .env file")
@click.option("--example", default=".env.example", show_default=True, help="Path to .env.example file")
def check(env, example):
    """Compare .env against .env.example and catch common issues."""
    success = run_check(env, example)
    sys.exit(0 if success else 1)
