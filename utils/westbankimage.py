#!/usr/bin/env python3

import sys
import os
import argparse

SKOOLKIT_HOME = os.environ.get('SKOOLKIT_HOME')
if not SKOOLKIT_HOME:
    sys.stderr.write('SKOOLKIT_HOME is not set; aborting\n')
    sys.exit(1)
if not os.path.isdir(SKOOLKIT_HOME):
    sys.stderr.write('SKOOLKIT_HOME={}; directory not found\n'.format(SKOOLKIT_HOME))
    sys.exit(1)
sys.path.insert(0, SKOOLKIT_HOME)

WESTBANK_HOME = os.environ.get('WESTBANK_HOME')
if not WESTBANK_HOME:
    sys.stderr.write('WESTBANK_HOME is not set; aborting\n')
    sys.exit(1)
if not os.path.isdir(WESTBANK_HOME):
    sys.stderr.write('WESTBANK_HOME={}; directory not found\n'.format(WESTBANK_HOME))
    sys.exit(1)
sys.path.insert(0, '{}/sources'.format(WESTBANK_HOME))

from skoolkit.image import ImageWriter
from skoolkit.refparser import RefParser
from skoolkit.skoolhtml import Frame
from skoolkit.snapshot import get_snapshot
from westbank import WestBankHtmlWriter


class WestBank(WestBankHtmlWriter):
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.defaults = RefParser()
        self.ref_parser = RefParser()
        self.ref_parser.parse('{}/sources/westbank.ref'.format(WESTBANK_HOME))
        self.init()


def get_playarea(game):
    play_area_udgs = game.get_play_area_udgs(0, 0, 32, 24)
    return play_area_udgs


def _do_pokes(specs, snapshot):
    for spec in specs:
        addr, val = spec.split(',', 1)
        step = 1
        if '-' in addr:
            addr1, addr2 = addr.split('-', 1)
            addr1 = int(addr1)
            if '-' in addr2:
                addr2, step = [int(i) for i in addr2.split('-', 1)]
            else:
                addr2 = int(addr2)
        else:
            addr1 = int(addr)
            addr2 = addr1
        addr2 += 1
        value = int(val)
        for a in range(addr1, addr2, step):
            snapshot[a] = value


def run(imgfname, options):
    snapshot = get_snapshot('{}/WestBank.z80'.format(WESTBANK_HOME))
    _do_pokes(options.pokes, snapshot)
    game = WestBank(snapshot)
    udg_array = get_playarea(game)
    if options.geometry:
        wh, xy = options.geometry.split('+', 1)
        width, height = [int(n) for n in wh.split('x')]
        x, y = [int(n) for n in xy.split('+')]
        udg_array = [row[x:x + width] for row in udg_array[y:y + height]]
    frame = Frame(udg_array, options.scale)
    image_writer = ImageWriter()
    with open(imgfname, "wb") as f:
        image_writer.write_image([frame], f)


###############################################################################
# Begin
###############################################################################
parser = argparse.ArgumentParser(
    usage='westbankimage.py [options] FILE.png',
    description="Create an image of the background in West Bank.",
    formatter_class=argparse.RawTextHelpFormatter,
    add_help=False
)
parser.add_argument('imgfname', help=argparse.SUPPRESS, nargs='?')
group = parser.add_argument_group('Options')
group.add_argument('-g', dest='geometry', metavar='WxH+X+Y',
                   help='Create an image with this geometry')
group.add_argument('-p', dest='pokes', metavar='A[-B[-C]],V', action='append', default=[],
                   help="Do POKE N,V for N in {A, A+C, A+2C,...B} (this option may\n"
                        "be used multiple times)")
group.add_argument('-s', dest='scale', type=int, default=2,
                   help='Set the scale of the image (default: 2)')
namespace, unknown_args = parser.parse_known_args()
if unknown_args or not namespace.imgfname:
    parser.exit(2, parser.format_help())
run(namespace.imgfname, namespace)

