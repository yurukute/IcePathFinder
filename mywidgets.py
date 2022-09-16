from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout,
                               QGroupBox, QLabel, QSpinBox, QVBoxLayout)


class NewMazeDialog(QDialog):
    def __init__(self):
        super(NewMazeDialog, self).__init__()
        self.create_form()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.form)
        mainLayout.addWidget(btns)
        self.setLayout(mainLayout)
        self.setWindowTitle("Create New Maze")

    def create_form(self):
        self.form = QGroupBox("Insert amount of")
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
        layout.addRow(QLabel("Rows:"), self.row_amt)
        layout.addRow(QLabel("Columns:"), self.col_amt)
        layout.addRow(QLabel("Rocks:"), self.rock_amt)
        layout.addRow(QLabel("Snows:"), self.snow_amt)
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
