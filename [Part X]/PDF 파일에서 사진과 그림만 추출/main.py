"""
Author : Byunghyun Ban
Last Modification : 2020-11-18
Image with Drawing Markup Extraction
"""

import fitz
from PIL import Image
import sys
import os

fname = sys.argv[1]
outdir = sys.argv[2]
doc = fitz.open(fname)

if outdir not in os.listdir():
    os.mkdir(outdir)

for j in range(len(doc)):
    page = doc[j]
    d = page.getText("dict")
    blocks = d["blocks"]
    imgblocks = [b for b in blocks if b["type"] == 1]
    if not imgblocks:
        continue
    pix = page.getPixmap(alpha=False, matrix=fitz.Matrix(4.0, 4.0))
    pix.writePNG("temp.png")
    img = Image.open("temp.png")
    for i in range(len(imgblocks)):
        x0, y0, x1, y1 = imgblocks[i]["bbox"]
        x0 *= 4
        y0 *= 4
        x1 *= 4
        y1 *= 4
        cropped_img = img.crop((x0, y0, x1, y1))
        cropped_img.save(outdir + "/page_" + str(j) + "_image_" + str(i) + ".png")
    os.remove("temp.png")
