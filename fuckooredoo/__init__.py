#fuckooredoo/__init__.py

__version__ = "1.0.2"
__author__ = "Mohamed Aziz Bahloul"
__email__ = "azizbahloul3@gmail.com"  

from .torrent_client import TorrentClient
 
# Import GUI lazily and handle missing GUI dependencies (tkinter) gracefully.
# When the package is imported in an environment without tkinter, importing
# `fuckooredoo` should not raise a ModuleNotFoundError. We attempt to import
# the GUI and capture the ImportError so the CLI entrypoint can show a
# friendly message instead of crashing.
TorrentGUI = None
GUI_IMPORT_ERROR = None
try:
	from .gui import TorrentGUI  # type: ignore
except Exception as _err:  # catch broad exceptions to avoid breaking import
	# Save the import error so the caller can present a helpful message.
	GUI_IMPORT_ERROR = _err
 
__all__ = ["TorrentClient", "TorrentGUI", "GUI_IMPORT_ERROR"]
