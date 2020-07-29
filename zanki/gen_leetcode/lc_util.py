import os
import pandas as pd

from zanki.util import get_script_dir

def get_set(filename):
    return set([line.strip() for line in open(filename).readlines() if len(line) > 0])

cur = get_script_dir(__file__)
collection_folder = os.path.join(cur, "resources", "collections")
resource_folder = os.path.join(cur, "resources")

df_diff = pd.read_csv(os.path.join(resource_folder, "难度.csv"))
df_diff["frontend_question_id"] = df_diff.frontend_question_id.astype(str)
ser_diff = df_diff.set_index("frontend_question_id")["难度"]
diff_dict = ser_diff.to_dict()

problem_tag_dict = {
    # [力扣精选算法 200 题 - 力扣（LeetCode）](https://leetcode-cn.com/problemset/200/)
    "choice200": get_set(os.path.join(collection_folder, "choice200.txt")),
    # [Database - 力扣（LeetCode）](https://leetcode-cn.com/problemset/database/)
    "database": get_set(os.path.join(collection_folder, "database.txt")),
    # 高频70 - https://blog.csdn.net/gongsai20141004277/article/details/105307217
    "highfreq70": get_set(os.path.join(collection_folder, "highfreq70.txt")),
    # [🔥 热题 HOT 100 - 力扣（LeetCode）](https://leetcode-cn.com/problemset/hot-100/)
    "hot100": get_set(os.path.join(collection_folder, "hot100.txt")),
    # [👨‍💻 精选 TOP 面试题 - 力扣（LeetCode）](https://leetcode-cn.com/problemset/top/)
    "top": get_set(os.path.join(collection_folder, "top.txt")),
    # Amazon, Facebook, Microsoft近期高频题并集
    # https://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=628098
    "fb": get_set(os.path.join(collection_folder, "amzn_fb_ms.txt"))
}

def get_tags(frontend_question_id):
    tags = []
    for key,value in problem_tag_dict.items():
        if frontend_question_id in value:
            tags.append(key)
    return tags

def get_difficulty(frontend_question_id):
    return diff_dict.get(frontend_question_id, "未知")

if __name__ == "__main__":
    tags = get_tags("33")
    print(tags)
    tags = get_tags("1384")
    print(tags)
    tags = get_tags("256")
    print(tags)
    diff = get_difficulty("33")
    print(diff)
