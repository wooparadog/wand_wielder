#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from hashlib import md5
from flask import Flask, request, abort, redirect, url_for
from wand_wielder import WandWielder

permdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

class StoreClient(object):
    def __init__(self, prefix='static/pics'):
        self.perm_dir = prefix
        self.prefix = os.path.join(permdir, self.perm_dir)

    def get_export_path(self, key):
        return os.path.join(self.perm_dir, *self.split_filename(key))

    def get_path(self, key):
        return os.path.join(self.prefix, *self.split_filename(key))

    def get_dir(self, key):
        return os.path.join(self.prefix, *self.split_filename(key)[:2])

    def split_filename(self, key):
        return key[:2], key[2:4], key

    def validate_key(self, key):
        if len(key) < 5:
            raise KeyError

    def get(self, key, default=None):
        self.validate_key(key)
        filepath = self.get_path(key)
        if os.path.exists(filepath):
            with open(filepath) as f:
                return f.read()

    def set(self, key, value):
        self.validate_key(key)
        filepath = self.get_path(key)
        dir_path = self.get_dir(key)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(filepath, 'wb') as f:
            f.write(value)


client = StoreClient()

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return redirect("https://github.com/wooparadog/wand_wielder")

@app.route("/wand/<format>", methods=["POST"])
def wand(format):
    if format not in ("jpg", "png"):
        abort(400, 'Wrong format')

    data = request.json
    if not data:
        abort(400, "No json data")

    key = "%s.%s" % (md5(repr(request.json)).hexdigest(), format)
    cached = client.get(key)

    if cached is None:
        wander = WandWielder(data)
        try:
            image = wander.draw()
        except Exception as e:
            return abort(400, e.message)
        image.format = format
        content = image.make_blob()
        client.set(key, content)

    return json.dumps({
        "key": key,
        "url": client.get_export_path(key)
        })
