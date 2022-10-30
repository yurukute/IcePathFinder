from PySide6.QtWidgets import (QColorDialog, QDialog, QDialogButtonBox,
                               QFormLayout, QGraphicsView, QGroupBox,
                               QHBoxLayout, QLabel, QPushButton, QSpacerItem,
                               QSpinBox, QSizePolicy, QVBoxLayout, QWidget,
                               QMenuBar, QMainWindow)


class MyDialog(QDialog):

    def __init__(self):
        super(MyDialog, self).__init__()
        self.create_form()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.form)
        mainLayout.addWidget(btns)
        self.setLayout(mainLayout)

    def create_form(self):
        return

    def values(self):
        return


class NewMazeDialog(MyDialog):

    def __init__(self):
        super(NewMazeDialog, self).__init__()
        self.setWindowTitle(self.tr("Create New Maze"))

    def create_form(self):
        self.form = QGroupBox(self.tr("Insert amount of"))
        self.row_amt = QSpinBox()
        self.col_amt = QSpinBox()
        self.rock_amt = QSpinBox()
        self.snow_amt = QSpinBox()

        self.row_amt.setMinimum(3)
        self.col_amt.setMinimum(3)

        self.row_amt.valueChanged.connect(self.value_change)
        self.col_amt.valueChanged.connect(self.value_change)
        self.rock_amt.valueChanged.connect(self.value_change)
        self.snow_amt.valueChanged.connect(self.value_change)

        layout = QFormLayout()
        layout.addRow(QLabel(self.tr("Rows:")), self.row_amt)
        layout.addRow(QLabel(self.tr("Columns:")), self.col_amt)
        layout.addRow(QLabel(self.tr("Rocks:")), self.rock_amt)
        layout.addRow(QLabel(self.tr("Snows:")), self.snow_amt)
        self.form.setLayout(layout)

    def value_change(self):
        max = self.row_amt.value() * self.col_amt.value()
        if max >= 2:
            max -= 2
        self.rock_amt.setMaximum(max - self.snow_amt.value())
        self.snow_amt.setMaximum(max - self.rock_amt.value())

    def values(self):
        row = self.row_amt.value()
        col = self.col_amt.value()
        rocks = self.rock_amt.value()
        snows = self.snow_amt.value()
        return [row, col, rocks, snows]


class PickColorDialog(NewMazeDialog):

    def __init__(self, bfs_color, dfs_color):
        self.bfs_color = bfs_color
        self.dfs_color = dfs_color

        super(PickColorDialog, self).__init__()
        self.setWindowTitle(self.tr("Change path's color"))

    def create_form(self):
        self.form = QGroupBox(self.tr("Pick color for paths:"))
        layout = QFormLayout()
        self.bfs_button = QPushButton()
        self.dfs_button = QPushButton()

        self.bfs_button.setPalette(self.bfs_color)
        self.dfs_button.setPalette(self.dfs_color)

        self.bfs_button.clicked.connect(self.bfs_button_clicked)
        self.dfs_button.clicked.connect(self.dfs_button_clicked)

        layout.addRow(QLabel("BFS:"), self.bfs_button)
        layout.addRow(QLabel("DFS:"), self.dfs_button)
        self.form.setLayout(layout)

    def bfs_button_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bfs_color = color
            self.bfs_button.setPalette(color)

    def dfs_button_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.dfs_color = color
            self.dfs_button.setPalette(color)

    def values(self):
        return [self.bfs_color, self.dfs_color]


class MyAppView(QWidget):

    def __init__(self):
        super(MyAppView, self).__init__()

        self.view = QGraphicsView()
        self.load_button = QPushButton(self.tr('Import maze from file'))
        self.solve_button = QPushButton(self.tr('Solve'))

        buttons = QHBoxLayout()
        buttons.addItem(
            QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons.addWidget(self.load_button)
        buttons.addItem(
            QSpacerItem(10, 1, QSizePolicy.Minimum, QSizePolicy.Minimum))
        buttons.addWidget(self.solve_button)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addItem(buttons)

        self.setLayout(layout)

    def reset_buttons(self):
        self.load_button.setText(self.tr('Import maze from file'))
        self.solve_button.setText(self.tr('Solve'))
