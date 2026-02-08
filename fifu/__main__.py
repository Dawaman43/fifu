"""CLI entry point for Fifu."""

import click

from fifu.app import FifuApp


@click.command()
def main():
    """Fifu - YouTube Channel Video Downloader TUI"""
    app = FifuApp()
    app.run()


if __name__ == "__main__":
    main()
