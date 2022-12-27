"""
Test script to generate data augmented STR images.
"""
import argparse
import os

import PIL.ImageOps
import numpy as np
from PIL import Image

from straug.blur import GaussianBlur, DefocusBlur, MotionBlur, GlassBlur, ZoomBlur
from straug.camera import Contrast, Brightness, JpegCompression, Pixelate
from straug.geometry import Rotate, Perspective, Shrink, TranslateX, TranslateY
from straug.noise import GaussianNoise, ShotNoise, ImpulseNoise, SpeckleNoise
from straug.pattern import VGrid, HGrid, Grid, RectGrid, EllipseGrid
from straug.process import Posterize, Solarize, Invert, Equalize, AutoContrast, Sharpness, Color
from straug.warp import Curve, Distort, Stretch
from straug.weather import Fog, Snow, Frost, Rain, Shadow

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_folder', required=True, help='Load image folder')
    parser.add_argument('--results', default="results", help='Folder for augmented image files')
    parser.add_argument('--gray', action='store_true', help='Convert to grayscale 1st')
    #parser.add_argument('--width', default=100, type=int, help='Default image width')
    #parser.add_argument('--height', default=32, type=int, help='Default image height')
    parser.add_argument('--seed', default=0, type=int, help='Random number generator seed')
    opt = parser.parse_args()
    os.makedirs(opt.results, exist_ok=True)

    #img = Image.open(opt.image)
    #img = img.resize((opt.width, opt.height))
    rng = np.random.default_rng(opt.seed)
    ops = [Curve(rng=rng), Perspective(rng), Distort(rng), Stretch(rng) ]
    ops.extend([GaussianNoise(rng), SpeckleNoise(rng)])
    ops.extend([GaussianBlur(rng), MotionBlur(rng), ZoomBlur(rng)])
    ops.extend([Contrast(rng), Brightness(rng), JpegCompression(rng) ])
    ops.extend([Fog(rng), Frost(rng), Rain(rng), Shadow(rng)])
    ops.extend(
        [Posterize(rng), Invert(rng), Equalize(rng), AutoContrast(rng), Color(rng)])
    
    for image in os.listdir(opt.image_folder):
        img= Image.open(os.path.join(opt.image_folder, image))
        for op in ops:
            for mag in range(-1, 2):
                sub_dir_name = type(op).__name__ + "-" + str(mag) ##folder name basically
                sub_dir_path= os.path.join(opt.results, sub_dir_name)
                os.makedirs(sub_dir_path, exist_ok=True)
                file_name= os.path.splitext(image)[0]+os.path.splitext(image)[1]
                out_img = op(img, mag=mag)
                if opt.gray:
                    out_img = PIL.ImageOps.grayscale(out_img)
                out_img.save(os.path.join(sub_dir_path, file_name))

    print('Random token:', rng.integers(2 ** 16))
