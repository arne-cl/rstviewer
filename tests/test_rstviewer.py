#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains pytest-based tests for the rstviewer library and
its commandline interface.
"""

import os
import tempfile
import pytest

from PIL import Image
import imagehash

import rstviewer
from rstviewer.main import cli


TESTDIR = os.path.dirname(__file__)
RS3_FILEPATH = os.path.join(TESTDIR, 'test.rs3')
EXPECTED_PNG1 = os.path.join(TESTDIR, 'result1.png')
EXPECTED_PNG2 = os.path.join(TESTDIR, 'result2.png')

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

def image_matches(produced_file, expected_files=[EXPECTED_PNG1, EXPECTED_PNG2]):
    """Return True, iff the average hash of the produced image matches any of the
    expected images.
    """
    produced_hash = imagehash.average_hash(Image.open(produced_file))

    expected_hashes = [imagehash.average_hash(Image.open(ef)) for ef in expected_files]
    return any([produced_hash == expected_hash for expected_hash in expected_hashes])


def test_rs3tohtml():
    """rs3 file is converted to HTML"""
    html_str = rstviewer.rs3tohtml(RS3_FILEPATH)
    assert EXPECTED_HTML in html_str


def test_rs3topng():
    """rs3 file is converted to PNG"""
    temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp.close()

    rstviewer.rs3topng(RS3_FILEPATH, temp.name)
    match = image_matches(temp.name)
    os.unlink(temp.name)
    assert match is True


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

    match = image_matches(temp_png.name)
    os.unlink(temp_png.name)
    assert match is True
