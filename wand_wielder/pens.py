#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wand.drawing import Drawing
from wand.color import Color

from .parameters import PenImageParameter, PenParameter,\
        coordinates_validator, Coordinates

KNOWN_PENS = {}

class PenMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(PenMeta, cls).__new__(cls, name, bases, attrs)
        key = name.lower().replace("pen", '')
        KNOWN_PENS[name.lower().replace("pen", '')] = new_class
        super_parameters = getattr(new_class, 'known_parameter', dict())
        super_parameters.update(
                dict(
                    [(n, i) for n, i in attrs.iteritems()\
                        if isinstance(i, PenParameter)])
                )
        new_class.known_parameter = super_parameters

        if key:
            doc = []
            old_doc = new_class.__doc__ or ""

            if not old_doc:
                doc.append("# Pen: %s" % name)

            doc.extend([
                old_doc,
                '',
                "Key: %s" % key,
                "Parameters:",
                ])

            for name, parameter in sorted(new_class.known_parameter.iteritems()):
                doc.append("    %s" % name)

            doc = '\n'.join(doc)
            new_class.__doc__ = doc
        return new_class

class Pen(object):
    __metaclass__ = PenMeta
    action = PenParameter('action', validator=lambda x:x in KNOWN_PENS)

    def __init__(self, config):
        self.config = config
        self.parse_config()

    def parse_config(self):
        for parameter_name, parameter in self.known_parameter.iteritems():
            setattr(self, parameter_name,  self.config.get(parameter.name))

    def draw(self, canvas):
        raise NotImplementedError

def transform_validator(transforms):
    if not isinstance(transforms, (list, tuple)):
        raise TypeError("Transforms should be list/tuple")
    if not all([i.keys()[0] in TransformPen.ALLOWED_TRANSFORMS for i in transforms]):
        raise ValueError("Action Only support %s" % (TransformPen.ALLOWED_TRANSFORMS,))
    return True

class TransformPen(Pen):
    '''For cropping or resizing image '''
    ALLOWED_TRANSFORMS = ['crop', 'resize']
    transforms = PenParameter('transforms', validator=transform_validator)

    def draw(self, canvas):
        for t in self.transforms:
            canvas.image.transform(**t)

class ComposePen(Pen):
    '''For composing another image upon a canvas '''
    image = PenImageParameter('image')
    coordinates = PenParameter('coordinates', validator=coordinates_validator,
            export_filter=Coordinates)

    def draw(self, canvas):
        canvas.image.composite(
                image=self.image,
                left=self.coordinates.x,
                top=self.coordinates.y
                )

class TextPen(Pen):
    '''For draw one line text on canvas '''
    font = PenParameter("font")
    font_size = PenParameter("font_size")
    text_interline_spacing = PenParameter("text_interline_spacing")
    fill_color = PenParameter("fill_color", export_filter=lambda c:c and Color(c))

    coordinates = PenParameter(
            'coordinates',
            validator=coordinates_validator,
            export_filter=Coordinates
            )
    text = PenParameter(
            "text",
            validator=bool,
            export_filter=lambda text: text.decode('utf8') \
                    if isinstance(text, str) else text
            )

    def __init__(self, config):
        super(TextPen, self).__init__(config)
        self.drawer = Drawing()
        for name, parameter in self.known_parameter.iteritems():
            if name not in ("text", "coordinates"):
                value = getattr(self, name)
                if value:
                    setattr(self.drawer, name, value)

    def draw(self, canvas):
        self.drawer.text(
                self.coordinates.x,
                self.coordinates.y,
                self.text.encode('utf8')
                )
        self.drawer.draw(canvas.image)

class BoxTextPen(TextPen):
    '''For draw text on canvas, and break line when lien width has reached `max_width` '''
    max_width = PenParameter("max_width", validator=lambda x:isinstance(x, int))

    def draw(self, canvas):
        width = self.max_width

        lines = []
        line = []
        for pos, i in enumerate(self.text):
            i = i.encode('utf8')
            line_text = ''.join(line)
            metrics = self.drawer.get_font_metrics(
                    image=canvas.image,
                    text=line_text+i
                    )
            if metrics.text_width > width:
                if pos > 1 and \
                        self.text[pos-1].isalpha() and\
                        i.isalpha():
                    i = (line_text[-1] + i).strip()
                    line_text = line_text[:-1]
                    if self.text[pos-2].isalpha():
                        line_text += "-"
                lines.append(line_text)
                line = [] if i.isspace() else [i]
            else:
                line.append(i)
        lines.append(''.join(line))
        text = '\n'.join(lines)
        self.drawer.text(self.coordinates.x, self.coordinates.y, text)
        self.drawer.draw(canvas.image)
