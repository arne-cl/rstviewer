#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains pytest-based tests for the rstviewer library and
its commandline interface.
"""

import os
import tempfile
import pytest
import rstviewer
from rstviewer.main import cli


TESTDIR = os.path.dirname(__file__)
RS3_FILEPATH = os.path.join(TESTDIR, 'test.rs3')
EXPECTED_PNG = os.path.join(TESTDIR, 'result.png')
EXPECTED_HTML = """<div>
<div id="edu1" class="edu" title="1" style="left:0; top:120; width: 96px">
	<div id="wsk1" class="whisker" style="width:96px;"></div>
	<div class="edu_num_cont">
		<table class="btn_tb">
			<tr>
				<td rowspan="2"><span class="num_id">&nbsp;1&nbsp;</span></td>
</table>
</div>Although they didn't like it,</div>
<div id="lg3" class="group" style="left: 0; width: 196; top:60px; z-index:1">
	<div id="wsk3" class="whisker" style="width:196;"></div>
</div>
<div id="g3" class="num_cont" style="position: absolute; left:111px; top:64px; z-index:199">
	<table class="btn_tb">
		<tr>
			<td rowspan="2"><span class="num_id">1-2</span></td>
	</table>
</div>
<br/>"""


def test_rs3tohtml():
    """rs3 file is converted to HTML"""
    html_str = rstviewer.rs3tohtml(RS3_FILEPATH)
    assert EXPECTED_HTML in html_str


def test_rs3topng():
    """rs3 file is converted to PNG"""
    png_str = rstviewer.rs3topng(RS3_FILEPATH)

    temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp.close()

    rstviewer.rs3topng(RS3_FILEPATH, temp.name)
    with open(temp.name, 'r') as png_file:
        assert png_str == png_file.read()
        os.unlink(temp.name)

    with open(EXPECTED_PNG, 'r') as expected_png_file:
        assert png_str == expected_png_file.read()


def test_cli_rs3tohtml():
    """conversion to HTML on the commandline"""
    temp_html = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
    temp_html.close()

    cli([RS3_FILEPATH, temp_html.name])
    with open(temp_html.name, 'r') as html_file:
        assert EXPECTED_HTML in html_file.read()
        os.unlink(temp_html.name)


def test_cli_rs3topng():
    """conversion to PNG on the commandline"""
    temp_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_png.close()

    # calling `rstviewer -f png input.rs3 output.png` will end the program
    # with sys.exit(0), so we'll have to catch this here.
    with pytest.raises(SystemExit) as serr:
        cli(['-f', 'png', RS3_FILEPATH, temp_png.name])
        out, err = pytest.capsys.readouterr()
        assert err == 0

    with open(temp_png.name, 'r') as png_file, \
        open(EXPECTED_PNG, 'r') as expected_png_file:
            assert png_file.read() == expected_png_file.read()
