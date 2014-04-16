# Wand Wielder

Give me `dict` like config, and I'll give you an image

# Pens

## boxtext

    For draw text on canvas, and break line when lien width has reached `max_width` 

    Key: boxtext
    Parameters:
        action
        coordinates
        fill_color
        font
        font_size
        image
        max_width
        text
        text_interline_spacing
        transforms

## compose

    For composing another image upon a canvas 

    Key: compose
    Parameters:
        action
        coordinates
        image
        transforms

## text

    For draw one line text on canvas 

    Key: text
    Parameters:
        action
        coordinates
        fill_color
        font
        font_size
        image
        text
        text_interline_spacing
        transforms

## transform

    For cropping or resizing image 

    Key: transform
    Parameters:
        action
        transforms

# Usage

example:

```python

    image = Image("user.png")
    background_img = Image("backgrond.png")
    text = "test_text_wolalala"
    font_path = "wqy_zhenhei.ttf"
    config = {
            'geometry': '470x650',
            'actions':[
                {
                    'action': 'compose',
                    'image': background_img,
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
                        {'crop': '30x30'},
                        {'resize': '30x30'}
                        ]
                    },
                ]
            }

    wand_wielder = WandWielder(config)
    image = wand_wielder.draw()
    image.save(filename="wolalalalal.png")
```
