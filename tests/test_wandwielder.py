#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from wand.image import Image
from wand_wielder import WandWielder

current_dir = path.dirname(path.abspath(__file__))
resources_dir = path.join(current_dir, "resources")
font_path = path.join(resources_dir, "ComicNeue-Regular.ttf")
background_img = Image(filename=path.join(resources_dir, "background.png"))
max_width = 370

def test_generate_photo():
    image = Image(filename=path.join(resources_dir, "reddit_logo.png"))
    text = "When does the narwhal bacon?"
    config = {
            'geometry': '470x650',
            'actions':[
                {
                    'action': 'compose',
                    'image':background_img.clone(),
                    'coordinates': "0x30",
                    },
                {
                    'action': 'boxtext',
                    'font': font_path,
                    'font_size': 17,
                    'text_interline_spacing': 12,
                    'text': text,
                    'max_width': 370,
                    'coordinates': "65x65",
                    },
                {
                    'action': 'compose',
                    'coordinates': "20x300",
                    'image':{
                        'raw_image': image,
                        'transforms': [
                            {'resize': '380x340^'},
                            {'crop': "380x340+0+0"},
                            ]
                        }
                    },
                {
                    'action': 'transform',
                    'transforms':[
                        ]
                    },
                ]
            }

    wand_wielder = WandWielder(config)
    image = wand_wielder.draw()
    image.save(filename="output.png")
