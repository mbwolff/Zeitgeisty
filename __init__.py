#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from flask import Flask, render_template, url_for
import os, re, datetime

enc = 'utf-8'

app = Flask(__name__)

package_dir = os.path.dirname(os.path.abspath(__file__))
aphor_dir = os.path.join(package_dir, "aphorisms")

def format_date(fname):
    date_time_str = fname.split("_")[0]
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    return '{0:%d} {0:%B} {0:%Y}'.format(date_time_obj, "day", "month", "year")

@app.route("/")
def list_days(days=None):
    days = list()
    files = os.listdir(aphor_dir)
    files.sort()
    for fname in files:
        if fname.endswith('txt'):
            days.append([fname, format_date(fname)])
    return render_template('days.html', days=days)

@app.route("/aphorisms/<fname>")
def display_aphorisms(fname):
    aphor_file = open(os.path.join(aphor_dir, fname), 'r', encoding=enc)
    stuff = aphor_file.readlines()
    aphorisms = list()
    for line in stuff:
        if not re.search('are the aphorisms', line) and re.search('\w', line):
            aphorisms.append(line)
    return render_template('aphorisms.html', aphorisms=[aphorisms, format_date(fname)])
