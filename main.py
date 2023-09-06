from PyQt5.QtWidgets import QApplication
from excel_app import ExcelApp
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelApp()
    ex.show()
    sys.exit(app.exec_())
