import re
import os

from zanki import conf
from zanki.exceptions import QAParseError

def get_script_dir(f):
    return os.path.dirname(os.path.abspath(f))

def guess_is_valid(fn):
    content = open(fn, encoding="utf-8").read()
    line_count = content.count("\n")
    split_count = content.count("\n\n")
    print("Stat [%5d vs %5d] for %s" %(split_count, line_count, fn))

# 类似 Java 中的 hash
def java_string_hashcode(s):
    h = 0
    for c in s:
        h = int((((31 * h + ord(c)) ^ 0x80000000) & 0xFFFFFFFF) - 0x80000000)
    return h

# 为每条摘录生成一个短语，用作卡片正面
MIN_ITEM_LENGTH = 10
MAX_ITEM_LENGTH = 40
def get_head(item):
    def is_punctuation(sent):
        # 完全来自下面的 re.split 但 “、《这样的标点就不加了
        if sent in """,.，。： ？、》”-】【""":
            return True
        return False

    length = min(len(item), MAX_ITEM_LENGTH)
    the_head = item[:length]
    sents = re.split('(\,|\.|，|。|：| |？|、|\n|《|》|】|【|“|”|\—)', item)

    joined = ""
    for i, sent in enumerate(sents):
        if len(joined) + len(sent) <= length:
            joined += sent
        else:
            break

    # 如果后面的是标点符号，就把它补上，但最多补 5 个
    for j in range(3):
        if i+j > len(sents) - 1:
            break
        if is_punctuation(sents[i+j]):
            joined += sents[i+j]
        else:
            break

    if len(joined) < MIN_ITEM_LENGTH:
        return item[:MIN_ITEM_LENGTH]
    return joined

# 跳过某些行
def is_comment(item):
    for SYMBOL in conf.COMMENT_SYMBOLS:
        if item.strip().startswith(SYMBOL):
            return True
    return False

# col 中是否存在某 guid
def get_item_id(col, item_id):
    sql = "select id as item_id from notes where guid == '%s'" %(item_id)
    return col.db.scalar(sql) or 0

# col 中的所有 guid
def get_all_guid(did):
    sql = "select id as item_id from notes where guid == '%s'" %(item_id)
    return col.db.scalar(sql)

# 确保问题对的顺序是正常的
def check_content_inflict(content, qline_nos, aline_nos):
    for qnos, anos in zip(qline_nos, aline_nos):
        qstart_lineno, qend_lineno = qnos
        astart_lineno, aend_lineno = anos
        if qend_lineno > astart_lineno:
            raise QAParseError("Found Question End at %d but Answer Start at %d" %(qend_lineno, astart_lineno))

    if len(qline_nos) != len(aline_nos):
        min_len = min(len(qline_nos), len(aline_nos))
        if len(qline_nos) > min_len:
            raise QAParseError("Found More Questions in Following Postions: %s" %(repr(qline_nos[min_len:])))
        else:
            raise QAParseError("Found More Answers in Following Postions: %s" % (repr(aline_nos[min_len:])))

def is_empty(line):
    return len(line.strip()) == 0

# a: ~XXXX or q: ~XXXX
def is_multiline_mode(line):
    if line.startswith("#"):
        return False
    for start_sign in conf.MD_STOP_SPLITERS:
        if start_sign == "#":  continue
        line = line.lower().replace(start_sign, "")
    if line.strip().startswith(conf.MULTILINE_INDICATOR):
        return True
    return False

def startswith(s, begins):
    s = s[:5].lower()  # 取前5个字符够用了
    for begin in begins:
        if s.startswith(begin):
            return True
    return False

# 去掉行首标志，去掉多行标志
def extract_qa(lines, start, end):
    # 行尾加2个空格以期让 markdown 加入 <br>
    joined = "  \n".join(lines[start:end])
    assert startswith(joined, conf.MD_STOP_SPLITERS)
    striped = joined[2:].strip()
    if len(striped) == 0:
        raise Exception("Empty Line found at %s-%s-%s" %(lines, start, end))
    if striped[0] == conf.MULTILINE_INDICATOR:
        return striped[1:]
    return striped

def is_line_in_ranges(line_no, line_ranges):
    if line_ranges is None:
        return False
    for line_range in line_ranges:
        if line_no >= line_range[0] and line_no <= line_range[1]:
            return True
    return False

# 对于Q/A，多行情况下如何处理？
# 常见情况是
# 1. q、a各占一行，a结束后有一空行
# q: XXXX
# a: YYYY
# 2. q占多行时，寻找a:或#，遇到后q截断
# 3. a占多行时，寻找q:或#，遇到后a截断
# Param: mode == A or Q
def extract_lines_pos(lines, mode=None, extra_special_se=None):
    spliters = conf.MD_SPLITERS[mode]
    stop_spliters = conf.MD_STOP_SPLITERS

    start_line_no = None
    multiline_mode = False
    for line_no, line in enumerate(lines):
        if startswith(line, spliters):
            if start_line_no is None:
                start_line_no = line_no
                multiline_mode = is_multiline_mode(line)
                continue
            else:
                raise QAParseError("Question (%s) Not End But Found Another (%s)" %(lines[start_line_no], lines[line_no]))

        if start_line_no is None:
            continue

        if not multiline_mode:
            if is_empty(line) or startswith(line, stop_spliters):
                yield (start_line_no, line_no)
                start_line_no = None
                multiline_mode = False
        elif multiline_mode:
            if startswith(line, stop_spliters) or is_line_in_ranges(line_no, extra_special_se):
                yield (start_line_no, line_no)
                start_line_no = None
                multiline_mode = False

    if start_line_no is not None:
        yield (start_line_no, line_no+1)

# abc\n\n，第1个`\n`是第0行，第2个`\n`是第1行
def find_special_start_end(content):
    special_stopers = "\n{3,}|\n\#SpecialLine\n"
    content = content.replace("\r\n", "\n")
    m = re.finditer(special_stopers, content)
    match_list = list(m)
    match_count = len(match_list)
    if match_count == 0:
        return []

    match_index = 0
    match_object = match_list[match_index]
    matched_string = match_object.group()

    line_no = 0
    start_end_pairs = []
    for index, char in enumerate(content):
        if index == match_object.start():
            if char == "\n":
                start_line_no = line_no + 1
            else:
                start_line_no = line_no
            end_line_no = line_no + matched_string.count("\n") - 1
            start_end_pairs.append((start_line_no, end_line_no))

            if match_index >= match_count - 1:
                break
            match_index += 1
            match_object = match_list[match_index]
            matched_string = match_object.group()
        if char == "\n":
            line_no += 1

    return start_end_pairs

# 预留
def clean(input):
    input = input.strip()
    #input = input.replace("\n", "<br>")
    return input

# 对文本内容，将换行替换为 <br>
def clean_txt(input):
    input = input.strip()
    input = input.replace("\n", "<br>")
    return input
