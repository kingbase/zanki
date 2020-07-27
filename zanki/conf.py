import os

def get_script_dir(f):
    return os.path.dirname(os.path.abspath(f))

LEETCODE_COOKIE = ""

COMMENT_SYMBOLS = ["!#", "#!"]
MD_SPLITERS = {
    "A": ["a:", "a："],
    "Q": ["q:", "q："],
}
MD_STOP_SPLITERS = ["q:", "q：", "a:", "a："] + COMMENT_SYMBOLS
MULTILINE_INDICATOR = "~"

# anki 默认会生成的 css
_DEFAULT_CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}"""

DEFAULT_CSS_N_ALIGN = """.card {
 font-family: arial;
 font-size: 20px;
 color: black;
 background-color: white;
 text-align: left;
}"""

script_dir = get_script_dir(__file__)
css_fn     = os.path.join(script_dir, "static/highlight.css")
js_fn      = os.path.join(script_dir, "static/math.js")

HIGHLIGHT_CSS = open(css_fn, encoding="utf-8").read()
MATH_JS       = open(js_fn, encoding="utf-8").read()
JS_TEMPLATE   = """<script type="text/javascript">%s</script>""" %(MATH_JS)
MATHJAX_JS_CDN_URL = "https://cdn.bootcss.com/mathjax/2.7.6/MathJax.js?config=TeX-MML-AM_SVG"
