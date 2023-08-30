from PyQt5.QtWidgets import QMessageBox
from docx import Document
from markdown import markdown

from PyQt5.QtCore import QThread, pyqtSignal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class OutputThread(QThread):
    """
    
    """
    output_finished = pyqtSignal()

    def __init__(self, search_results, output_path, file_extension):
        super().__init__()

        self.search_results = search_results
        self.output_path = output_path
        self.file_extension = file_extension

    def run_thread(self):
        if self.file_extension == 'pdf':
            self.output_pdf()
        elif self.file_extension == 'docx':
            self.output_docx()
        elif self.file_extension == 'md':
            self.output_md()

    def output_pdf(self):
        c = canvas.Canvas(self.output_path, pagesize=letter)
        y_position = 750
        for result in self.search_results:
            lines = self.text_line_split(result, 100)
            for line in lines:
                c.drawString(15, y_position, line)
                y_position -= 15
                if y_position < 50:
                    y_position = 750
                    c.showPage()
        try:
            c.save()
        except:
            QMessageBox.warning('error', 'save failed!\nplease check if the file is currently in use')

        self.output_finished.emit()

    def text_line_split(self, text, width):
        lines = []
        words = text.split('\\')
        tmp = words[0]

        for word in words[1:]:
            if len(tmp + '\\' + word) <= width:
                # or (len(tmp + '-' + word) <= width)
                # or (len(tmp + '_' + word) <= width)):
                tmp += '\\'
                tmp += word
            else:
                lines.append(tmp)
                tmp = '\\' + word
        lines.append(tmp)
        return lines

    def output_docx(self):
        document = Document()
        for result in self.search_results:
            document.add_paragraph(result)
        document.save(self.output_path)

        self.output_finished.emit()

    def output_md(self):
        markdown_content = '\n'.join(self.search_results)
        markdown_content = markdown(markdown_content)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        self.output_finished.emit()
