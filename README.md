### Install PyInstaller from PyPI:

- `pip install pyinstaller`
- Go to your program’s directory and run:`pyinstaller yourprogram.py`
This will generate the bundle in a subdirectory called dist.
- `pyinstaller -F yourprogram.py`
Adding -F (or --onefile) parameter will pack everything into single "exe".
- running into "ImportError" you might consider side-packages. `pip install pynput==1.6.8`
- still runing in Import-Erorr - try to downgrade pyinstaller - see Getting error when using pynput with pyinstaller