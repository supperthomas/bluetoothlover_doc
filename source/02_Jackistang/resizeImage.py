#! python3
# resizeImage.py - Resizes all images in current working directory to fit
# in a 100x100 square.

# 此方案会导致图片文字太小，无法查看。
import os
from PIL import Image

SQUARE_FIT_SIZE = 200

# Loop over all files in the working directory.
for foldername, subfolders, filenames in os.walk('../../'):
    print('Enter %s \tfolder' % (foldername))

    for filename in filenames:
        if not (filename.endswith('.png') or filename.endswith('.jpg')):
            continue # skip non-image files

        im = Image.open(os.path.join(foldername, filename))
        
        if im.mode == 'P' or im.mode == 'RGBA':
            im = im.convert('RGB')
        width, height = im.size

        # Check if image needs to be resized.
        if width > SQUARE_FIT_SIZE and height > SQUARE_FIT_SIZE:
            # Calculate the new width and height to resize to.
            if width > height:
                height = int((SQUARE_FIT_SIZE / width) * height)
                width = SQUARE_FIT_SIZE
            else:
                width = int((SQUARE_FIT_SIZE / height) * width)
                height = SQUARE_FIT_SIZE

            # Resize the image.
            print('Resizing %s...' % (filename))
            im = im.resize((width, height))

        # Save changes.
        im.save(os.path.join(foldername, filename))
