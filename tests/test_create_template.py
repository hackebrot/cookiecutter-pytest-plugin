# -*- coding: utf-8 -*-

"""
test_create_template
--------------------
"""


import os
import pytest
import subprocess


def run_tox(plugin):
    """Run the tox suite of the newly created plugin."""
    try:
        subprocess.check_call([
            'tox',
            plugin,
            '-c', os.path.join(plugin, 'tox.ini'),
            '-e', 'py'
        ])
    except subprocess.CalledProcessError as e:
        pytest.fail(str(e))


def test_run_cookiecutter_and_plugin_tests(cookies):
    """Create a new plugin via cookiecutter and run its tests."""
    result = cookies.bake(extra_context={'plugin_name': 'foo-bar', 'module_name': 'mymodule'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'pytest-foo-bar'
    assert result.project.isdir()
    assert result.project.join('mymodule', 'plugin.py').isfile()
    assert result.project.join('tests', 'test_mymodule.py').isfile()

    run_tox(str(result.project))
