# EasyCopy
- 仅用于交流和个人测试，请勿用于重要数据及生产环境
- 需要环境
1. Python3.7及以上
2. Windows系统已安装dd，并设置为环境变量；Linux系包含dd无需安装
```
pip install poetry
poetry install
# 直接运行
poetry run python main.py
# 打包成可执行文件
poetry run pyinstaller -w -F main.py
```
