import os
import glob

def clear_directory():
    files = glob.glob('afisha/*')
    for f in files:
        os.remove(f)

    files = glob.glob('backgrounds/*')
    for f in files:
        os.remove(f)

    files = glob.glob('baner/*')
    for f in files:
        os.remove(f)

    print('[CLEAR] Directory clean!')

