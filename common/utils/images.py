import os
from uuid import uuid4
from datetime import datetime

from PIL import Image

from common import LOG


def uuid_image_path(filename, sub_dir):
    ext = filename.split('.')[-1]
    fn = '%s.%s' % (uuid4().hex, ext)
    root_path = 'uploads/photos/%s' %  sub_dir
    return root_path + datetime.now().strftime('/%Y/%m/%d/') + fn

def uuid_vrzip_path(filename, sub_dir):
    ext = filename.split('.')[-1]
    fn = '%s.%s' % (uuid4().hex, ext)
    root_path = 'uploads/vrzip/'
    return root_path + fn

def get_image(image, width, height='', crop_type='middle', water_mark=True):
    size = (width, height)
    tmp_path, ext = os.path.splitext(image.path)
    new_path = tmp_path.replace('uploads', 'resize') + '_%dx%s' % size + ext
    
    if not os.path.exists(new_path):
        path_dir = os.path.dirname(new_path)
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        try:
            resize_and_crop(image.path, new_path, size, crop_type, water_mark)
        except Exception, e:
            # LOG.error('ERROR when resizing image [%s]', image.path)
            # LOG.exception(e)
            return ''
    
    tmp_url, ext = image.url.split('.')
    return tmp_url.replace('uploads', 'resize') + '_%dx%s.' % size + ext


def resize_and_crop(img_path, modified_path, size, crop_type='middle', water_mark=True):
    """
    Resize and crop an image to fit the specified size.

    args:
    img_path: path for the image to resize.
    modified_path: path to store the modified image.
    size: `(width, height)` tuple.
    crop_type: can be 'top', 'middle' or 'bottom', depending on this
    value, the image will cropped getting the 'top/left', 'middle' or
    'bottom/right' of the image to fit the size.
    raises:
    Exception: if can not open the file in img_path of there is problems
    to save the image.
    ValueError: if an invalid `crop_type` is provided.
    
    refs: https://gist.github.com/sigilioso/2957026
    """
    # If height is higher we resize vertically, if not we resize horizontally
    img = Image.open(img_path)
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    if size[1] in ('0', 0, 'x', ''):
        size1 = size[0]/img_ratio
        size = (size[0], int(round(size1)))
        ratio = img_ratio
    else:
        ratio = size[0] / float(size[1])
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
            Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                int(round((img.size[1] + size[1]) / 2)))
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
            Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = (int(round((img.size[0] - size[0]) / 2)), 0,
                int(round((img.size[0] + size[0]) / 2)), img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    else :
        img = img.resize((size[0], size[1]),
            Image.ANTIALIAS)
    
    if water_mark:
        img = add_water_mark(img)
    
    # If the scale is the same, we do not need to crop
    img.save(modified_path, quality=85, optimize=True)
    
    
def add_water_mark(src_image, margin_h=65):
    this_dir = os.path.dirname(os.path.dirname(__file__))
    water_mark = Image.open(os.path.join(this_dir, 'utils', 'water.png'))
    
    if src_image.mode != 'RGB':
        src_image = src_image.convert('RGB')
        
    layer = Image.new('RGBA', src_image.size, (0, 0, 0, 0))
    
    positions = []
    height = margin_h + water_mark.size[1]
    count = src_image.size[1] / height
    for i in range(1, count+1):
        y = height * i - water_mark.size[1]
        parts = 2 if i%2 else 3
        span = src_image.size[0]/parts
        if span > water_mark.size[0]:
            for j in range(parts):
                x = (span-water_mark.size[0])/2 + span*j
                positions.append((x, y))

    for position in positions:
        layer.paste(water_mark, position)
    
    return Image.composite(layer, src_image, layer)
