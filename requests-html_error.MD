In this file we will explain why requests-html not render js on some websites.
This due to the very old version of chromium on pyppeteer.
What we need to do is upgrade manually or by script.
Using script so far is not applicable on Windows, at least for me.
Manually upgrade chromium :
1. find suitable version here: https://chromium.cypress.io/
2. download and extract
3. find your local-chromium folder location. Mine was C:\Users\CORTANA\AppData\Local\pyppeteer\pyppeteer\local-chromium
4. Move new version to this folder with version number as folder name. In the end chrome.exe location looks like : C:\Users\CORTANA\AppData\Local\pyppeteer\pyppeteer\local-chromium\1223356\chrome-win\chrome
5. Open pyppeteer folder (in this case i am using venv) C:\Users\CORTANA\python_projects\ikea\Lib\site-packages\pyppeteer\__init__.py
6. Change the value of __chromium_revision__ to your version. Mine was __chromium_revision__ = '1223356'
7. save and we are ready to go

or simply using terminal by:
1. export PYPPETEER_CHROMIUM_REVISION=1204234
this is linux version for me
2. pyppeteer-install
done
pretty much easier huh?
but if you like to manually on linux, then goes here :
/home/asus/.local/share/pyppeteer/local-chromium/1204234
more or less is same like the top on windows