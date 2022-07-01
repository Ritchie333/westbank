import art
import sys
import os

WESTBANK_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WB_SKOOL = '{}/sources/westbank.skool'.format(WESTBANK_HOME)

SKOOLKIT_HOME = os.environ.get('SKOOLKIT_HOME')
if SKOOLKIT_HOME:
    if not os.path.isdir(SKOOLKIT_HOME):
        sys.stderr.write('SKOOLKIT_HOME={}: directory not found\n'.format(SKOOLKIT_HOME))
        sys.exit(1)
    sys.path.insert(0, SKOOLKIT_HOME)
    from skoolkit import skool2asm, skool2html
else:
    try:
        from skoolkit import skool2asm, skool2html
    except ImportError:
        sys.stderr.write('Error: SKOOLKIT_HOME is not set, and SkoolKit is not installed\n')
        sys.exit(1)

sys.stderr.write("Found SkoolKit in {}\n".format(skool2html.PACKAGE_DIR))

def run_skool2asm():
    skool2asm.main(sys.argv[1:] + [WB_SKOOL])

def run_skool2html():
    options = '-c Config/InitModule=sources:bases -d {}/build/html'.format(WESTBANK_HOME)
    art.tprint("West Bank")
    hex = '-H -c Config/GameDir=westbank/hex'
    dec = '-D -c Config/GameDir=westbank/dec'
    skool2html.main(options.split() + hex.split() + sys.argv[1:] + [WB_SKOOL])
    skool2html.main(options.split() + dec.split() + sys.argv[1:] + [WB_SKOOL])
