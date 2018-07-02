"""
Tests for the Vagrant CLI.

This mostly provides error case coverage.
We rely mostly on manual testing.
This is because automated tests for this would be very slow.

For developing help texts, it is useful to add a breakpoint on failure and then
to capture what the help text actually is with:

  .. code: python

       import pyperclip; pyperclip.copy(result.output)
"""

import os
import uuid
from pathlib import Path
from tempfile import mkstemp
from textwrap import dedent
from typing import List

import pytest
from click.testing import CliRunner
# See https://github.com/PyCQA/pylint/issues/1536 for details on why the errors
# are disabled.
from py.path import local  # pylint: disable=no-name-in-module, import-error

from cli import dcos_vagrant


class TestDcosVagrant:
    """
    Tests for the top level `dcos-vagrant` command.
    """

    def test_version(self) -> None:
        """
        The CLI version is shown with ``dcos-vagrant --version``.
        """
        runner = CliRunner()
        result = runner.invoke(
            dcos_vagrant,
            ['--version'],
            catch_exceptions=False,
        )

        assert result.exit_code == 0
        expected = 'dcos-vagrant, version'
        assert expected in result.output

    @pytest.mark.parametrize('arguments', [
        [],
        ['--help'],
    ])
    def test_help(self, arguments: List[str]) -> None:
        """
        Help test is shown with `dcos-vagrant` and `dcos-vagrant --help`.
        """
        runner = CliRunner()
        result = runner.invoke(dcos_vagrant, arguments, catch_exceptions=False)
        assert result.exit_code == 0
        # yapf breaks multi-line noqa, see
        # https://github.com/google/yapf/issues/524.
        # yapf: disable
        expected_help = dedent(
            """\
            Usage: dcos-vagrant [OPTIONS] COMMAND [ARGS]...

              Manage DC/OS clusters on Vagrant.

            Options:
              --version      Show the version and exit.
              -v, --verbose
              --help         Show this message and exit.

            Commands:
              create  Create a DC/OS cluster.
            """,# noqa: E501,E261
        )
        # yapf: enable
        assert result.output == expected_help


class TestCreate:
    """
    Tests for the `create` subcommand.
    """

    def test_help(self) -> None:
        """
        Help text is shown with `dcos-vagrant create --help`.
        """
        runner = CliRunner()
        result = runner.invoke(
            dcos_vagrant,
            ['create', '--help'],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        # yapf breaks multi-line noqa, see
        # https://github.com/google/yapf/issues/524.
        # yapf: disable
        expected_help = dedent(
            """\
            Usage: dcos-vagrant create [OPTIONS] ARTIFACT

              Create a DC/OS cluster.

            Options:
              --help  Show this message and exit.
            """,# noqa: E501,E261
        )
        # yapf: enable
        assert result.output == expected_help