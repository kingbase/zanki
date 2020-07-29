import re
import html
from typing import List

import misaka
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

from zanki import util
from zanki import conf

class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(
                            html.escape(text.strip()))


# 对于 $f(x) = s_{ij}$ 这样形式的，
# 转换时会将 下划线 _ 转化为 markdown 语法中的 html标签 <em>
# 为此，我将 $ 中的 <em> 标签再转化回去
# 注意，$$ f(x) = s_{ij} $$ 这样的形式，不受影响
def md_mod(line):
    parts = []
    for part in re.split("(\$.*?\$)", line):
        if part.startswith("$") and part.endswith("$"):
            part = part.replace("<em>", "_")
            part = part.replace("</em>", "_")
            part = part.replace("&#39;", "'")
        parts.append(part)
    return "".join(parts)

# leetcode pre process
def md_convert(markdown):
    markdown = markdown.replace('{:align="center"}', '')
    markdown = markdown.replace('{:align=center}', '')
    markdown = markdown.replace("\r\n", "\n")

    # \n```xx``` will not work
    markdown = markdown.replace("\n```","\n\n```").replace("\n\n\n```","\n\n```")
    # TABLE，不确定在哪里处理时多加了2个空格
    markdown = markdown.replace("\nTABLE_START  \n", "\n\n").replace("\nTABLE_END  \n", "\n\n")
    markdown = markdown.replace("TABLE_START  \n", "\n")  # 可能出现在篇首
    markdown = markdown.replace("\nTABLE_END", "\n")  # 可能出现在篇尾
    markdown = md(markdown)

    lines = markdown.split("\n")
    lines = [md_mod(line) for line in lines]
    return "\n".join(lines)

renderer = HighlighterRenderer()
md = misaka.Markdown(renderer, extensions=('fenced-code','tables','math'))

def extract_qa_from_md(content: str):
    lines = content.split("\n")
    special_line_start_end = util.find_special_start_end(content)
    qline_nos = list(util.extract_lines_pos(lines, "Q", extra_special_se=special_line_start_end))
    aline_nos = list(util.extract_lines_pos(lines, "A", extra_special_se=special_line_start_end))
    util.check_content_inflict(content, qline_nos, aline_nos)

    result = []
    for qnos, anos in zip(qline_nos, aline_nos):
        qstart_lineno, qend_lineno = qnos
        astart_lineno, aend_lineno = anos
        question = util.extract_qa(lines, qstart_lineno, qend_lineno)
        answer   = util.extract_qa(lines, astart_lineno, aend_lineno)
        result.append((question, answer))
    return result

if __name__ == "__main__":
    bad_line = "在暴引 $i$ 到 $j - 1$ 之间的子字符串 $s_{ij}$ 已经被检查为没有重复字符。我们只需要检查 $s[j]$ 对应的字符是否已经存在于子字符串 $s_{ij}$ 中。"
    assert "<em>" not in md_convert(bad_line)

    raw_md_content = open("zanki/tests/static/code_math.md", encoding="utf-8").read()
    code_html = md(raw_md_content)

    css_template = open("zanki/static/highlight.css", encoding="utf-8").read()
    js_template = open("zanki/static/math.js", encoding="utf-8").read()

    html = """<script type="text/javascript" src="{js_cdn}"></script>
                <script type="text/javascript">{js}</script>
                <style type="text/css">{css}</style>
                {code}""".format(js=js_template, css=css_template, code=code_html,
                                 js_cdn=conf.MATHJAX_JS_CDN_URL
    )
    open("zanki/tests/demo.html", "w", encoding="utf-8").write(html)
