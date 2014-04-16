#! /usr/bin/env python
# -*- coding: utf-8 -*-

from movie.libs.wand_wielder.pens import KNOWN_PENS

def print_pen_docs():
    for name, pen in sorted(KNOWN_PENS.iteritems()):
        print "# Pen: %s" % name
        print
        print pen.__doc__
        print

if __name__ == '__main__':
    print_pen_docs()
