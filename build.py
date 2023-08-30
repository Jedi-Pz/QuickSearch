import PyInstaller.__main__

# 要打包的Python脚本
scripts = ['main.py', 'HandmadeEverything.py', 'OutputThread.py', 'SearchThread.py']

# 打包选项
options = [
    '--onefile',  # 打包成单个exe文件
    '--noconsole'  # 隐藏控制台窗口
]

args = options + scripts
PyInstaller.__main__.run(args)