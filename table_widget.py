from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
from datetime import datetime

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initTable()

    def initTable(self):
        self.setRowCount(0)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["支出项目", "支出金额/£", "支出日期", "类型"])
        header = self.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def add_row(self):
        row_position = self.rowCount()
        self.insertRow(row_position)
        date_item = QTableWidgetItem(datetime.now().strftime('%Y-%m-%d'))
        self.setItem(row_position, 2, date_item)
        combo = QComboBox()
        for item in ["交通", "日用品", "学习", "日常饮食", "社交活动", "赠送", "娱乐"]:
            combo.addItem(item)
        self.setCellWidget(row_position, 3, combo)

    def remove_row(self):
        selected_indexes = self.selectedIndexes()
        if selected_indexes:
            rows_to_remove = set(index.row() for index in selected_indexes)
            for row in sorted(rows_to_remove, reverse=True):
                self.removeRow(row)
