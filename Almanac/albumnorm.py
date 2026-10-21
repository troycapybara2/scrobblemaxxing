import re
KW = r"(deluxe|expanded|remaster(ed)?|anniversary|bonus|special edition|complete edition|extended|super edition|platinum edition|edition|explicit|clean)"
PAREN = re.compile(r"\s*[\(\[][^\)\]]*" + KW + r"[^\)\]]*[\)\]].*$", re.I)       # "(Deluxe)" and anything after it
DASH = re.compile(r"\s+[-–]\s+[^-–]*" + KW + r"[^-–]*$", re.I)                       # " - Deluxe Edition" style suffix
def base(album):
    a = str(album)
    if re.search(r"taylor.?s version", a, re.I): return a.strip()   # re-recordings stay separate
    b = PAREN.sub("", a)
    b = DASH.sub("", b)
    return b.strip() or a.strip()
