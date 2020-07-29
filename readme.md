## 安装步骤

1. 下载本 repo: git clone git@github.com:kingbase/zanki.git
2. 在本 repo 根目录执行: git clone --depth 1 --branch 2.1.12 git@github.com:dae/anki.git
    - 最新的 anki 未经测试，且只支持 Python 3.7 及以上，因此使用旧版本。 
3. 安装依赖（zanki/requirements.txt），对于 Windows 用户如果安装 `mistune` 失败可以尝试使用 `conda install -c conda-forge misaka`

## 兼容性测试
  - Anki for Windows (2.1.15)
  - Anki for Linux (2.1.15)

## 使用（leetcode）

请按照步骤进行

1. `python zanki/gen_leetcode/lc_dl.py eval/full`  # 爬问答，会下载到 `output/raw/leetcode` 目录。
   1. 若是收费用户，请在 `conf.py` 中补充 cookie 以便抓取收费题目。
   2. 参数 eval: 出于评估目的（看下本 repo 的效果），则仅抓取前 200 个问题（需要一两分钟）。
   3. 参数 full: 抓取所有可抓取的问题，耗时较长。对于付费用户是所有问题，对免费用户则是所有免费问题。
2. 可选，添加自己的做题笔记到 `output/raw/leetcode/my_solution` 目录，文件名为`[题号].md`，见 repo 中的 `5.md` 作为示例，md 文件支持代码高亮和 Latex 公式。
3. `python zanki/gen_leetcode/lc_gen.py file/desktop` 生成 Anki 的卡片文件，有 2 种方式可选：
   1. file: 生成独立文件，随后自行手动导入 Anki App 或桌面程序。
   2. desktop: 若您的桌面端已经安装 Anki，本程序会自动定位到默认 Anki 的 collection 文件并添加进去。您需要事先关闭 Anki 以更新，但随后您可以将其同步至其他安装 Anki 的设备（假如您已经登陆）。

## 使用（扫描目录）

Todo
