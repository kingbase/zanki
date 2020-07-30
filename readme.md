本 repo 让你更方便的生成 Anki 卡片，且支持 Markdown 语法、代码高亮和 Latex 公式。

为方便 leetcode 刷题，可以生成 leetcode 刷题记忆库，库中包含了 leetcode 官方解法、网友高票答案，还能添加你的个人解答。

## 安装步骤

1. 下载本 repo: git clone git@github.com:kingbase/zanki.git
2. 在本 repo 根目录执行: git clone --depth 1 --branch 2.1.12 git@github.com:dae/anki.git
    - 最新的 anki 未经测试，且只支持 Python 3.7 及以上，因此使用旧版本。 
3. 安装依赖（zanki/requirements.txt），对于 Windows 用户如果安装 `mistune` 失败可以尝试使用 `conda install -c conda-forge misaka`

## 兼容性测试
  - Anki for Windows (2.1.15) (Tested)
  - Anki for Linux (2.1.15) (Tested)
  - Mac (Waiting for test)

## 使用步骤和说明（leetcode）

### 步骤

1. `python zanki/gen_leetcode/lc_dl.py eval/full`  # 爬问答，会下载到 `output/raw/leetcode` 目录。
   1. 若是收费用户，请在 `conf.py` 中补充 cookie 以便抓取收费题目。
   2. 参数 eval: 出于评估目的（看下本 repo 的效果），则仅抓取前 200 个问题（需要一两分钟）。
   3. 参数 full: 抓取所有可抓取的问题，耗时较长。对于付费用户是所有问题，对免费用户则是所有免费问题。
   4. 补充：下载时会默认缓存到 output 目录，若爬取速度过快导致程序中断，可以再次运行此时会跳过已下载的。
2. 可选，添加自己的做题笔记到 `output/raw/leetcode/my_solution` 目录，文件名为`[题号].md`，见 repo 中的 `5.md` 作为示例，md 文件支持代码高亮和 Latex 公式。
3. `python zanki/gen_leetcode/lc_gen.py file/desktop` 生成 Anki 的卡片文件，有 2 种方式可选：
   1. file: 生成独立文件，随后自行手动导入 Anki App 或桌面程序。
   2. desktop: 若您的桌面端已经安装 Anki，本程序会自动定位到默认 Anki 的 collection 文件并添加进去。您需要事先关闭 Anki 以更新，但随后您可以将其同步至其他安装 Anki 的设备（假如您已经登陆）。

### 说明

1. 为常见题目加了标签：[choice200](https://leetcode-cn.com/problemset/200/) / [highfreq70](https://blog.csdn.net/gongsai20141004277/article/details/105307217) / [hot100](https://leetcode-cn.com/problemset/hot-100/) / [database](https://leetcode-cn.com/problemset/database/) / [top](https://leetcode-cn.com/problemset/top/) / [fb](https://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=628098)，可以在 Anki 中建立筛选牌组：`deck:leetcode is:due tag:hot100` 则会找出[高频100题目](https://leetcode-cn.com/problemset/hot-100/)，方便高效复习。

## 使用（扫描目录）

Todo
