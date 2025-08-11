import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QStyleFactory, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class WeeklySchedule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weekly Schedule")
        self.setGeometry(100, 100, 800, 600)

        # Create a Treeview widget
        self.tree = QTreeView(self)
        self.tree.setHeaderHidden(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setIndentation(0)

        # Format the columns
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        header = self.tree.header()
        for day, heading in enumerate(days):
            header.resizeSection(day, 150)  # Set column width
            # header.setDefaultAlignment(day, Qt.AlignLeft)
            header.setText(day, heading)

        # Create a layout to center the treeview horizontally
        h_layout = QVBoxLayout()
        h_layout.addWidget(self.tree)
        h_layout.addStretch()

        # Create a layout to center the horizontal layout vertically
        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addLayout(h_layout)
        v_layout.addStretch()

        # Set the central layout
        central_widget = QWidget()
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeeklySchedule()
    window.show()
    sys.exit(app.exec_())
