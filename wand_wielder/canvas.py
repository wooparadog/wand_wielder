#! /usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlopen
from wand.image import Image

class Canvas(object):
    def __init__(self, image):
        self.image = image

    @classmethod
    def create_from_geometry(cls, geometry):
        width, height = map(int, geometry.split("x"))
        return cls(Image(width=width, height=height))

    @classmethod
    def create_from_background(cls, background):
        if isinstance(background, Image):
            image = background
        elif isinstance(background, (str, unicode)):
            image = Image(file=urlopen(background))
        else:
            raise ValueError("Wrong backgrong")
        return cls(image)

    def do_action(self, pen):
        pen.draw(self)
