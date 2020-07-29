#coding: utf-8
import time
from copy import deepcopy
import argparse
import tqdm

import pandas as pd
import glob
import sys, os

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "..", "..", "anki"))
from anki.storage import Collection
from anki.exporting import AnkiCollectionPackageExporter
from anki.notes import Note
from anki.stdmodels import addBasicModel

from zanki import conf
from zanki import util
from zanki import md_util
from zanki.gen_leetcode import lc_util
from zanki import util_anki

def usage():
    print("Location of output: desktop or file\n"
          "desktop: Write to default user of anki desktop app, "
          "so you can use it in your desktop app or sync from desktop app to other devices like iOS and Android app.\n"
          "file: Write to folder output/leetcode and you can distribute it online or import it to your anki app manually.")

parser = argparse.ArgumentParser()
parser.add_argument("output", help="Location of output: desktop or file")
args = parser.parse_args()
if args.output not in ["desktop", "file"]:
    usage()
    sys.exit()

if args.output == "file":
    collection_fn = os.path.join(directory, "..", "..", "output", "leetcode", "leetcode.anki2")
    collection_fn = os.path.abspath(collection_fn)
elif args.output == "desktop":
    collection_fn = util_anki.get_default_collection()
col = Collection(collection_fn, log=True)
my_sol_folder = os.path.join(directory, "..", "..", "output", "raw", "leetcode", "my_solution")

modelBasic = col.models.byName('Basic')
if modelBasic is None:
    # 新安装的 Anki 桌面端会存在为空的情况
    modelBasic = addBasicModel(col)
modelBasic["css"] = conf.DEFAULT_CSS_N_ALIGN + "\n" + conf.HIGHLIGHT_CSS
modelBasic["tmpls"][0]["qfmt"] = "{{Front}}" + conf.JS_TEMPLATE
modelBasic["tmpls"][0]["afmt"] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}" + conf.JS_TEMPLATE
col.models.save(modelBasic)

# 建立新 deck
deck_name = "leetcode"
did = col.decks.id(deck_name)
col.decks.select(did)
col.decks.current()['mid'] = modelBasic['id']
deck = col.decks.byName(deck_name)

base_folder = os.path.join(directory, "..", "..", "output", "raw", "leetcode")
lang = "CN"
df = pd.read_pickle(os.path.join(base_folder, "index.pkl"))
question_slugs = df.question__title_slug.to_dict()

for pid, problem_slug in tqdm.tqdm(question_slugs.items()):
    difficulty = lc_util.get_difficulty(pid)
    tags = lc_util.get_tags(pid)
    describe_html_fn = os.path.join(base_folder, "html_describe", "%s-%s-%s.html" % (lang, pid, problem_slug))
    question = "%s: %s (%s)" % (pid, problem_slug, difficulty) + \
               "<br>" + open(describe_html_fn, encoding="utf-8").read()

    solution_article_fn_pattern = os.path.join(base_folder, "md_solution_article", "%s-%s-*.md" % (lang, pid))
    solution_article_fns = glob.glob(solution_article_fn_pattern)
    official_answer_list = [open(fn, encoding="utf-8").read() for fn in solution_article_fns]
    my_sol_fn = os.path.join(my_sol_folder, "%s.md" %(pid))
    if os.path.exists(my_sol_fn):
        is_my_sol = True
        my_sol_raw    = open(my_sol_fn, encoding="utf-8").read()
        my_sol_html = "自己答案<br>" + my_sol_raw
        answer_list = [my_sol_html] + official_answer_list
    else:
        is_my_sol = False
        answer_list = official_answer_list
    answer = md_util.md_convert("\r\n<hr>答案分隔线<hr>\r\n".join(answer_list))

    # 答案可能会变化，但文件名和问题会相对固定，所以以这两者取 guid
    guid = util.java_string_hashcode(deck_name + "|" + problem_slug)
    item_id = util.get_item_id(col, guid)
    fields0 = question
    fields1 = answer

    if item_id > 0:
        note = Note(col, id=item_id)
        old_tags = deepcopy(note.tags)
        if is_my_sol:
            note.addTag("mysol")
        for tag in tags:
            note.addTag(tag)
        if old_tags != note.tags:
            note.flush()
        if not (note.fields[0] == fields0 and note.fields[1] == fields1):
            note.guid = guid
            note.model()['did'] = deck['id']
            note.fields[0] = fields0
            note.fields[1] = fields1
            note.flush(int(time.time()))
    # 如果没有此 item 则建立新的 item
    else:
        note = col.newNote()
        note.guid = guid
        note.model()["did"] = deck["id"]
        note.fields[0] = fields0
        note.fields[1] = fields1
        if is_my_sol:
            note.addTag("mysol")
        for tag in tags:
            note.addTag(tag)
        col.addNote(note)

col.save()

output_fn = collection_fn.replace(".anki2", ".apkg")
print("Saving to %s ..." %(output_fn))
acpe = AnkiCollectionPackageExporter(col)
acpe.exportInto(output_fn)
print("Generated at %s" %(output_fn))
