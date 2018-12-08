from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path[0] = str(root_dir)+'/src/'

