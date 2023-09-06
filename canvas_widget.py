from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from collections import defaultdict
from constants import FONT_PATH

font = FontProperties(fname=FONT_PATH)

class CanvasWidget(FigureCanvas):
    def __init__(self, table):
        self.figure = Figure()
        super().__init__(self.figure)
        self.table = table

    def update_pie_chart(self):
        self.figure.clear()
        data = defaultdict(int)
        total_expense = 0
        for row in range(self.table.rowCount()):
            category_widget = self.table.cellWidget(row, 3)
            if category_widget:
                category = category_widget.currentText()
                amount_item = self.table.item(row, 1)
                if amount_item:
                    try:
                        amount = float(amount_item.text())
                        data[category] += amount
                        total_expense += amount  # Add amount to total expense
                    except ValueError:
                        pass  # or you might want to handle this error in some way
        labels = [f'{key} ({value}镑)' for key, value in data.items()]
        sizes = data.values()

        ax = self.figure.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontproperties': font, 'fontsize': 30}, wedgeprops=dict(width=0.3, edgecolor='w'))
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display total expense at the top of the chart
        ax.text(0, 1.1, f'{total_expense}镑', ha='center', va='center', fontsize=50, fontproperties=font, fontweight='bold', color='red')

        self.draw()
