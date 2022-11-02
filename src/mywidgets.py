from itertools import pairwise
from PySide6.QtGui import QAction, QPen, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QColorDialog, QDialog, QDialogButtonBox,
                               QFormLayout, QGraphicsView, QGroupBox,
                               QHBoxLayout, QLabel, QPushButton, QSpacerItem,
                               QSpinBox, QSizePolicy, QVBoxLayout, QWidget,
                               QGraphicsScene, QMessageBox, QMenuBar)


class MyMenuBar(QMenuBar):

    def __init__(self):
        super(MyMenuBar, self).__init__()

        # File menu
        self.new_action = QAction(self.tr('&New'), self)
        self.load_action = QAction(self.tr('&Open...'), self)
        self.quit_action = QAction(self.tr('&Quit'), self)

        self.new_action.setShortcut('Ctrl+N')
        self.load_action.setShortcut('Ctrl+O')
        self.quit_action.setShortcut('Ctrl+Q')

        file_menu = self.addMenu(self.tr('&File'))
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.load_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        # Option menu
        self.change_color_action = QAction(self.tr('&Change path\'s color'),
                                           self)
        self.english_action = QAction(self.tr('&English'), self)
        self.vietnamese_action = QAction(self.tr('&Vietnamese'), self)
        self.vietnamese_action.setData('vi_VN')

        option_menu = self.addMenu(self.tr('&Option'))
        option_menu.addAction(self.change_color_action)

        change_language_menu = option_menu.addMenu(self.tr('Change &language'))
        change_language_menu.addAction(self.english_action)
        change_language_menu.addAction(self.vietnamese_action)

        # Help menu
        help_action = QAction(self.tr('&Help...'), self)
        about_action = QAction(self.tr('&About Ice Path Finder'), self)

        help_action.setShortcut('F1')

        help_action.triggered.connect(self.showHelp)
        about_action.triggered.connect(self.showAbout)

        help_menu = self.addMenu(self.tr('&Help'))
        help_menu.addAction(help_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)

    def showHelp(self):
        print('help clicked')

    def showAbout(self):
        QMessageBox.information(
            self, self.tr('About - Ice Path Finder'),
            self.tr('College Project - Basic Topics:\n'
                    'Apply blind search algorithms in solving ice maze\n'
                    'Develop by Nguyen Khanh Dung\n'
                    'Version: 1.0'))


class MyDialog(QDialog):

    def __init__(self):
        super(MyDialog, self).__init__()
        self.createForm()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.form)
        mainLayout.addWidget(btns)
        self.setLayout(mainLayout)

    def createForm(self):
        return

    def values(self):
        return


class NewMazeDialog(MyDialog):

    def __init__(self):
        super(NewMazeDialog, self).__init__()
        self.setWindowTitle(self.tr("Create New Maze"))

    def createForm(self):
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

    def valueChange(self):
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


class PickColorDialog(MyDialog):

    def __init__(self, bfs_color, dfs_color):
        self.bfs_color = bfs_color
        self.dfs_color = dfs_color

        super(PickColorDialog, self).__init__()
        self.setWindowTitle(self.tr("Change path's color"))

    def createForm(self):
        self.form = QGroupBox(self.tr("Pick color for paths:"))
        layout = QFormLayout()
        self.bfs_button = QPushButton()
        self.dfs_button = QPushButton()

        self.bfs_button.setPalette(self.bfs_color)
        self.dfs_button.setPalette(self.dfs_color)

        self.bfs_button.clicked.connect(self.bfsButtonClicked)
        self.dfs_button.clicked.connect(self.dfsButtonClicked)

        layout.addRow(QLabel("BFS:"), self.bfs_button)
        layout.addRow(QLabel("DFS:"), self.dfs_button)
        self.form.setLayout(layout)

    def bfsButtonClicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bfs_color = color
            self.bfs_button.setPalette(color)

    def dfsButtonClicked(self):
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
        self.tileset = QPixmap('../imgs/tiles.png')
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

    def resetButtons(self):
        self.load_button.setText(self.tr('Import maze from file'))
        self.solve_button.setText(self.tr('Solve'))

    def getTileNum(self, tile):
        if tile == ' ':
            return 0
        if tile == '#':
            return 1
        if tile == 'S':
            return 2
        if tile == 'E':
            return 3
        else:
            return 4

    def drawMaze(self, maze):
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        row, col = len(maze), len(maze[0])
        for i in range(row):
            for j in range(col):
                tile_num = self.getTileNum(maze[i][j])
                tile = self.tileset.copy(tile_num * 32, 0, 32, 32)
                pixmap = self.scene.addPixmap(tile)
                pixmap.setPos(j * 32, i * 32)
        self.solve_button.setEnabled(True)
        self.path = []
        print(self.scene.width(), self.scene.height())

    def drawSolution(self, maze, result, color):
        print(result)
        if len(result) == 0:
            QMessageBox.information(
                self, self.tr('Notification'),
                self.tr('There is no solution for this maze.'))
            return
        for line in self.path:
            self.scene.removeItem(line)
        col = len(maze[0])
        pen = QPen(color, 8, Qt.SolidLine, Qt.RoundCap)
        for curr, next in pairwise(result):
            from_row, from_col = curr // col, curr % col
            to_row, to_col = next // col, next % col
            line = self.scene.addLine(from_col * 32 + 16, from_row * 32 + 16,
                                      to_col * 32 + 16, to_row * 32 + 16, pen)
            self.path.append(line)
        self.scene.update()
