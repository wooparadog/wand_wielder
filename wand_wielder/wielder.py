#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .canvas import Canvas
from .pens import KNOWN_PENS

class WandWielder(object):

    def __init__(self, config):
        self.config = config

    def create_canvas(self):
        background = self.config.get("background")
        geometry = self.config.get("geometry")

        if background and geometry:
            raise ValueError("background or geometry, choose 1")

        if background:
            canvas = Canvas.create_from_background(background)
        elif geometry:
            canvas = Canvas.create_from_geometry(geometry)
        else:
            raise ValueError("feed me background or geometry, plz")

        return canvas

    def draw(self):
        self.canvas = self.create_canvas()

        for action in self.config['actions']:
            pen_kls = KNOWN_PENS.get(action['action'])
            if not pen_kls:
                raise KeyError(
                    ("%s is not in available pens,"
                    " available pens are: %s") % (
                        action['action'],
                        KNOWN_PENS.keys(),
                        )
                    )
            pen = pen_kls(action)
            self.canvas.do_action(pen)
        return self.canvas.image
