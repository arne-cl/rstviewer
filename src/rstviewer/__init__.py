# -*- coding: UTF-8 -*-
import os

from rstviewer import main, rstweb_classes, rstweb_reader, rstweb_sql
from rstviewer.main import embed_rs3_image, embed_rs3str_image, rs3tohtml, rs3topng

PACKAGE_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT_DIR = os.path.abspath(os.path.join(PACKAGE_ROOT_DIR, 'data'))
