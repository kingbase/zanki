import os
import requests
import pandas as pd
from copy import deepcopy
import json
from zanki.gen_leetcode.gql_query import solutionDetailArticleQuery,\
    questionSolutionArticlesQuery, getQuestionDetailQuery
from zanki import conf

directory = os.path.dirname(os.path.realpath(__file__))
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
cookie = conf.LEETCODE_COOKIE
if len(cookie) == 0:
    print("Cookie is empty, if you want to crawl paid questions and answers, please specify cookie in zanki/zanki/conf.py#LEETCODE_COOKIE")

site = {
    "CN": "https://leetcode-cn.com/graphql",
    "EN": "https://leetcode.com/graphql"
}
headers = {
    'User-Agent': user_agent,
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Referer': 'https://leetcode-cn.com/problems/',
    'Cookie': cookie
}

def fetch(params, lang="CN"):
    url = site[lang]
    json_data = json.dumps(params).encode('utf-8')
    headers_ = deepcopy(headers)
    headers_["Referer"] = url
    req = requests.post(url, data=json_data, headers=headers, timeout=10)
    return req.text

def fetch_or_cache(fn, params, lang):
    if not os.path.exists(fn):
        print("Fetching %s" %(params['variables']))
        content = fetch(params, lang)
        open(fn, 'w', encoding="utf-8").write(content)
    else:
        print("Cached   %s" % (params['variables']))
        content = open(fn, encoding="utf-8").read()
    return json.loads(content)

url = "https://leetcode-cn.com/api/problems/all/"
req = requests.get(url)
js_ = req.json()

df  = pd.DataFrame(js_["stat_status_pairs"])
df["difficulty_level"] = df.pop("difficulty").map(lambda x: x["level"])
df_stat = df["stat"].apply(pd.Series)
df  = pd.concat([df_stat, df], axis=1)
df  = df.set_index("frontend_question_id").sort_values(by=["question_id"])
# 前200个题目中，有8道付费题目：156/156/158/159/161/163/170/186
# 开始时可以跳过这些题目
df  = df.head(150)

lang = "CN"
base_folder = os.path.join(directory, "..", "..", "output", "raw", "leetcode")
if not os.path.exists(base_folder):
    os.makedirs(base_folder)
df.to_pickle(os.path.join(base_folder, "index.pkl"))
question_slugs = df.question__title_slug.to_dict()

solution_articles = {}
question_describes = {}
for pid, problem_slug in question_slugs.items():
    describe_fn = os.path.join(base_folder, "json_describe", "%s-%s-%s.json" % (lang, pid, problem_slug))
    describe_html_fn = os.path.join(base_folder, "html_describe", "%s-%s-%s.html" % (lang, pid, problem_slug))
    solution_list_fn = os.path.join(base_folder, "json_solution_index", "%s-%s-%s.json" % (lang, pid, problem_slug))

    # 获取问题描述 (Step1)
    params = {
        'operationName': "getQuestionDetail",
        'variables': {'titleSlug': problem_slug},
        'query': getQuestionDetailQuery,
    }
    js1 = fetch_or_cache(describe_fn, params, lang)

    # 没有翻译的，值为null。这是由于有些题目比较新，没有翻译。
    if js1["data"]["question"]["translatedContent"]:
        describe_html = js1["data"]["question"]["translatedContent"]
    else:
        describe_html = js1["data"]["question"]["content"]
    open(describe_html_fn, 'w', encoding="utf-8").write(describe_html)

    # 获取解答列表，其中第一个通常是官方解答
    params = {
        'operationName': "questionSolutionArticles",
        'variables': {'questionSlug': problem_slug, "first": 10, "skip": 0, "orderBy": "DEFAULT"},
        'query': questionSolutionArticlesQuery
    }
    js2 = fetch_or_cache(solution_list_fn, params, lang)

    solution_slugs = {}
    df_edges = pd.DataFrame(js2["data"]["questionSolutionArticles"]["edges"])
    df_node = df_edges.pop("node").apply(pd.Series)
    df_solutions = pd.concat([df_edges, df_node], axis=1)
    df_official = df_solutions[(df_solutions.byLeetcode == True) | (df_solutions.isEditorsPick == True)]

    # 获取某个解答答案，我通常只关心官方解答
    # 如果不存在官方解答或者编辑选择，那么按数量取前3个，并且要在开头注明是来源于网友，还要加入分隔线
    df_top_voted = df_solutions.sort_values(by=["upvoteCount"], ascending=False).head(3)
    df_wanted = df_official.head(1) if len(df_official) > 0 else df_top_voted
    solution_slugs[problem_slug] = df_wanted.slug.tolist()

    solution_contents = []
    for solution_slug in solution_slugs[problem_slug]:
        solution_article_fn = os.path.join(base_folder, "json_solution_article",
                                           "%s-%s-%s.json" % (lang, pid, solution_slug))
        solution_md_fn = os.path.join(base_folder, "md_solution_article", "%s-%s-%s.md" % (lang, pid, solution_slug))
        params = {
            'operationName': "solutionDetailArticle",
            'variables': {'slug': solution_slug},
            'query': solutionDetailArticleQuery
        }
        js3 = fetch_or_cache(solution_article_fn, params, lang)
        article_content = js3["data"]["solutionArticle"]["content"]
        open(solution_md_fn, 'w', encoding="utf-8").write(article_content)
        solution_contents.append(article_content)
    solution_articles[problem_slug] = solution_contents
