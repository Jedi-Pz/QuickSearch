import os

from PyQt5.QtCore import QThread, pyqtSignal


class SearchThread(QThread):
    """
        本类用来实现搜索文件的功能
        点击’搜索‘按钮后执行
        目前实现的功能：多线程，在限定的路径内的，比较小的范围内搜索。

        TODO: 同时匹配多个词语
            - 正则表达式实现分隔多个词语 search = re.split(r'\s+', text)
        TODO: 使用NTFS的USN日志匹配所有的文件
            - 目前可以获取这个文件，但是如何处理仍在探索
        TODO: 实现目标字符的高亮
        DONE: 多线程实现搜索文件的方法
            - threading库实现
            - 仅适用threading库造成了线程阻塞，包含GUI的主线程被阻塞了，
              没有实现多线程应有的搜索和显示独立运行的效果
            - 考虑使用Qthread实现
            - 发现是在搜索线程中操作result_list导致的线程阻塞
              实际上搜索线程也在使用这一共享资源，尝试把搜索结果保存在列表里来避免阻塞
            - 在display_search_results显示搜索结果
        """
    # 对于信号和槽的机制还需要理解
    # 线程结束时回传一个list，不声明返回类型的话会有报错如下
    # SearchThread.search_finished[] signal has 0 argument(s) but 1 provided
    search_finished = pyqtSignal(list)

    def __init__(self, search_input, search_path):
        super().__init__()
        self.search_input = search_input  # 搜索内容
        self.search_path = search_path  # 路径

    def runThread(self):
        search = self.search_input.text()
        path_lim = self.search_path.text()
        if search:
            result_paths = []
            for path, folders, files in os.walk(path_lim):
                for file in files:
                    file_path = os.path.join(path, file)
                    if search in file:
                        result_paths.append(file_path)
            """
            emit是触发信号的方法，用于在不同对象之间通信
            这里我对应的槽是display_search_results

            这是一种实现多线程间通信的方式，
            因为信号和槽函数机制允许你在不同线程间进行交互，
            而不需要直接进行线程间的数据共享或锁定。
            """
            self.search_finished.emit(result_paths)