#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from wand.image import Image

class PenParameter(object):
    def __repr__(self):
        return "<%s name=%s>" % (self.__class__.__name__, self.name)

    def __init__(self, name, validator=None, export_filter=None, default=None):
        self.name = name
        self.validator = validator
        self.export_filter = export_filter
        self.default = default

    def __get__(self, obj, objtype):
        if obj is None:
            return self.default
        value = getattr(obj, "__" + self.name, self.default)
        if self.export_filter is not None:
            value = self.export_filter(value)
        return value

    def __set__(self, obj, value):
        if not self.validate(value):
            raise ValueError("Validation Error")
        setattr(obj, "__" + self.name, value)

    def validate(self, value):
        if self.validator is not None:
            return self.validator(value)
        return True

class PenImageParameter(PenParameter):
    '''Image Parameter

    Valid values:
        1. `wand.image.Image`
        2. dict config like:
            {
                'raw_image': `wand.image.Image`,
                'transforms': [
                    {'resize': '380x340^'},
                    {'crop': "380x340+0+0"},
                ],
            }
        3. `uri`, file path or url.(will be read by `urllib.urlopen`)
    '''
    def _create_image(self, image_argument):
        image = None

        if isinstance(image_argument, Image):
            image = image_argument

        if isinstance(image_argument, (str, unicode)):
            image_file = urllib.urlopen(image_argument)
            image = Image(blob=image_file.read())

        elif isinstance(image_argument, dict):
            config = image_argument
            if 'raw_image' not in config:
                raise KeyError("Should have image in config")

            if not isinstance(config['raw_image'], Image):
                raise TypeError("config['raw_image'] should be Image")

            image = config['raw_image']
            transforms = config.get('transforms', [])

            for t in transforms:
                image.transform(**t)

        if image is None:
            raise ValueError("Generate Fail")

        return image

    def validate(self, value):
        if isinstance(value, Image):
            return True

        if isinstance(value, (str, unicode)):
            return True

        if not isinstance(value, dict):
            raise ValueError('image parameter should be dict or `wand.image.Image`')

        if not isinstance(value['raw_image'], Image):
            raise ValueError("raw_iamge should be `wand.image.Image`")

        transforms = value['transforms']
        ALLOWED_TRANSFORMS = ['crop', 'resize']

        if not super(PenImageParameter, self).validate(transforms):
            raise ValueError("Validation fails")

        if not isinstance(transforms, (list, tuple)):
            raise TypeError("Transforms should be list/tuple")

        if not all([i.keys()[0] in ALLOWED_TRANSFORMS for i in transforms]):
            raise ValueError("Action Only support %s" % (ALLOWED_TRANSFORMS,))

        return True

    def __set__(self, obj, value):
        if not self.validate(value):
            raise ValueError("Generate Fail")
        image = self._create_image(value)
        setattr(obj, "__" + self.name, image)

def coordinates_validator(coordinates):
    return map(lambda x:x.isdigit(), coordinates.split('x')) == [True, True]

class Coordinates(object):
    def __init__(self, coordinates):
        self.x, self.y = map(int, coordinates.split('x'))

