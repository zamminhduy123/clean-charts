"""Install Google Sans (OFL, from github.com/google/fonts) for matplotlib.

Downloads the variable font, writes static Regular/Medium/Bold instances (matplotlib cannot
select weights from a variable font), installs them in the user font dir, rebuilds the cache.
Needs: fonttools (pip install fonttools).
"""
import os, sys, tempfile, urllib.request, platform, glob

URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/googlesans/GoogleSans%5BGRAD%2Copsz%2Cwght%5D.ttf"
FONT_DIR = os.path.expanduser("~/Library/Fonts" if platform.system() == "Darwin" else "~/.local/share/fonts")

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

os.makedirs(FONT_DIR, exist_ok=True)
src = os.path.join(tempfile.mkdtemp(), "GoogleSans.ttf")
urllib.request.urlretrieve(URL, src)
for w, name in [(400, "Regular"), (500, "Medium"), (700, "Bold")]:
    f = instantiateVariableFont(TTFont(src), {"wght": w, "opsz": 18, "GRAD": 0}, updateFontNames=True)
    f["OS/2"].usWeightClass = w
    out = os.path.join(FONT_DIR, f"GoogleSans-{name}.ttf")
    f.save(out)
    print("installed", out)

import matplotlib
for c in glob.glob(os.path.join(matplotlib.get_cachedir(), "fontlist-*.json")):
    os.remove(c)  # next matplotlib import rebuilds the cache
print("done; matplotlib font cache cleared")
