# Name tilde checker
A GUI app made for checking if a name has a tilde ( ´ ) in it by checking with https://www.llevatilde.es and displaying the response.

## Found a way to build the app for Windows with pyinstaller
```{shell}
python -m PyInstaller main.py --onedir -w --collect-submodules beautifulsoup4 --collect-submodules requests --collect-submodules urllib3 --hidden-import beautifulsoup4 --hidden-import urllib3 --hidden-import requests
```

* Note that for this to work we had to add the `requests`, `urllib3` and `beautifulsoup4` modules (the folders) from the virtual environment site-packages' directory to the project folder (so a level above the venv folder)
