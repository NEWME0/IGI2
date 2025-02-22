import os

from utils import fs
from format import tex
from format import tga


def func(args):
    count = 0

    for srcpath in fs.walkdir(args.src, ('*.tex', '*.spr', '*.pic')):
        texfile = tex.fromfile(srcpath)

        dstpath = srcpath.replace(args.src, args.dst, 1)

        print(dstpath)

        os.makedirs(os.path.dirname(dstpath), exist_ok=True)

        for i in range(len(texfile.bitmaps)):
            fxt = srcpath[-4:]
            ext = '.tga'
            wid = texfile.width
            hei = texfile.height

            if texfile.version in (7, 9) and len(texfile.bitmaps) > 1:
                ext = '.#{0:0>2}.tga'.format(i)

            elif texfile.version == 11 and i > 0:
                ext = '.%{0:0>2}.tga'.format(i)
                wid = texfile.width // (1 << i)
                hei = texfile.height // (1 << i)

            tgafile = tga.TGA()
            tgafile.setImageType(2)
            tgafile.setTGALines(
                texfile.bitmaps[i],
                wid,
                hei,
                tex.DEPTH[texfile.mode] * 8)
            tgafile.setImageDescriptor(True, True, tex.ALPHA[texfile.mode])

            tga.tofile(tgafile, dstpath.replace(fxt, ext))

        count += 1

    print('Converted: {0}'.format(count))
