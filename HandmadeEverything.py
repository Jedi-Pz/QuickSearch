import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, \
    QFileDialog

from OutputThread import OutputThread
from SearchThread import SearchThread


class HandmadeEverything(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HandmadeEverything')
        self.setGeometry(200, 100, 400, 200)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.search_path = QLineEdit()  # 路径
        self.search_path.setPlaceholderText('路径')
        self.search_input = QLineEdit()  # 搜索内容
        self.search_input.setPlaceholderText('搜索内容')
        self.search_button = QPushButton('搜索')
        self.output_button = QPushButton('导出')
        self.result_list = QListWidget()  # 结果显示

        self.layout.addWidget(self.search_path)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.output_button)
        self.layout.addWidget(self.result_list)

        self.central_widget.setLayout(self.layout)

        self.search_button.clicked.connect(self.start_search_thread)
        self.output_button.clicked.connect(self.start_output_thread)
        self.result_list.itemDoubleClicked.connect(self.open_file)
        # 线程锁，对应search_files的TODO
        # self.lock = threading.Lock()

    def start_search_thread(self):
        """
        启动一个QThread线程来搜索文件
        线程定义在SearchThread类
        """
        search_thread = SearchThread(self.search_input, self.search_path)
        search_thread.search_finished.connect(self.display_search_results)
        search_thread.runThread()

    def display_search_results(self, result_paths):

        self.result_list.clear()
        self.result_list.addItems(result_paths)

    def start_output_thread(self):
        """

        :return:
        """
        search_results = [self.result_list.item(i).text() for i in range(self.result_list.count())]
        output_path, _ = QFileDialog.getSaveFileName(self, '选择导出路径', '',
                                                     'Markdown 文件 (*.md);;'
                                                     'Word 文件 (*.docx);;'
                                                     'PDF 文件 (*.pdf);;'
                                                     '所有文件 (*)')
        if self.result_list.count() == 0:
            QMessageBox.warning(self, "error", "no result can output!")
        if output_path:
            file_extension = output_path.split('.')[-1].lower()
            output_thread = OutputThread(search_results, output_path, file_extension)
            output_thread.output_finished.connect(self.output_message)
            output_thread.run_thread()

    def output_message(self):
        QMessageBox.information(self, "info", "output succeed")

    def open_file(self, item):
        """
        本函数实现双击列表内元素打开对应文件的功能
        双击搜索结果列表内元素可以打开对应的文件
        self.result_list.itemDoubleClicked.connect(self.open_file)
        """
        file_path = item.text()
        if os.path.exists(file_path):
            try:
                # with self.lock:
                os.startfile(file_path)
            except:
                # with self.lock:
                QMessageBox.warning(self, "error", "file can't open")
        else:
            with self.lock:
                QMessageBox.warning(self, "error", "file don't exist")
