#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from config import pickled_doc_dir
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

doc_files = os.listdir(pickled_doc_dir)
doc_files.sort()
while len(doc_files) > 180: # last 90 days of data in docs
    f = doc_files.pop(0)
    os.remove(os.path.join(pickled_doc_dir, f))
