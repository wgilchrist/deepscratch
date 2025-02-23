import os, sys
import logging
from .utils.nbimport import NotebookFinder, DirectoryFinder

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.meta_path.append(NotebookFinder())
sys.meta_path.append(DirectoryFinder())

package_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(package_path)

if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

try:
    from IPython import get_ipython
    if get_ipython():
        notebook_dir = os.getcwd()
        if os.path.basename(notebook_dir) == os.path.basename(package_path):
            __package__ = os.path.basename(package_path)

except ImportError:
    pass

jaxmetal = logging.getLogger('jaxmetal')
jaxmetal.setLevel(logging.ERROR)