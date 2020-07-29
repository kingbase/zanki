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

1. `python zanki/gen_leetcode/lc_dl.py`  # 爬问答，会下载到 `output/raw/leetcode` 目录。
2. Todo

## 使用（扫描目录）

Todo
