#!/usr/bin/env python3
"""
Copyright (c) 2023 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from transformers import pipeline
pipe = pipeline(model="facebook/roberta-hate-speech-dynabench-r4-target")
pipe("A time for Fox News, a time for Donald Trump.")
