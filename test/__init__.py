import os.path
import pathlib
import sys

parent_dir = str(pathlib.Path(__file__).parent.parent)
src = os.path.join(parent_dir, "api")
sys.path.append(src)
