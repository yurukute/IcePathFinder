from itertools import pairwise
from PySide6.QtGui import QAction, QPen, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QColorDialog, QDialog,
                               QDialogButtonBox, QFormLayout, QGraphicsScene,
                               QGraphicsView, QGroupBox, QHBoxLayout, QLabel,
                               QMenuBar, QMessageBox, QPushButton, QSizePolicy,
                               QSpacerItem, QSpinBox, QVBoxLayout, QWidget)


class MyMenuBar(QMenuBar):

    def __init__(self):
        super(MyMenuBar, self).__init__()

        # File menu
        self.__new_action = QAction(self.tr('&New'), self)
        self.__load_action = QAction(self.tr('&Open...'), self)

        self.__new_action.setShortcut('Ctrl+N')
        self.__load_action.setShortcut('Ctrl+O')

        file_menu = self.addMenu(self.tr('&File'))
        file_menu.addAction(self.__new_action)
        file_menu.addAction(self.__load_action)
        file_menu.addSeparator()

        quit_action = QAction(self.tr('&Quit'), self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(QApplication.instance().quit)

        file_menu.addAction(quit_action)

        # Option menu
        self.__change_color_action = QAction(self.tr('&Change path\'s color'),
                                             self)
        self.__english_action = QAction(self.tr('&English'), self)
        self.__vietnamese_action = QAction(self.tr('&Vietnamese'), self)
        self.__vietnamese_action.setData('vi_VN')

        option_menu = self.addMenu(self.tr('&Option'))
        option_menu.addAction(self.__change_color_action)

        change_language_menu = option_menu.addMenu(self.tr('Change &language'))
        change_language_menu.addAction(self.__english_action)
        change_language_menu.addAction(self.__vietnamese_action)

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

    def setNewAction(self, function):
        self.__new_action.triggered.connect(function)

    def setLoadAction(self, function):
        self.__load_action.triggered.connect(function)

    def setChangeCorlorAction(self, function):
        self.__change_color_action.triggered.connect(function)

    def setChangeLanguageAction(self, function):
        self.__english_action.triggered.connect(function)
        self.__vietnamese_action.triggered.connect(function)


class MyDialog(QDialog):

    def __init__(self):
        super(MyDialog, self).__init__()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.createForm())
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
        form = QGroupBox(self.tr("Insert amount of"))
        self.__row_amt = QSpinBox()
        self.__col_amt = QSpinBox()
        self.__rock_amt = QSpinBox()
        self.__snow_amt = QSpinBox()

        self.__row_amt.setMinimum(2)
        self.__col_amt.setMinimum(2)

        self.__row_amt.valueChanged.connect(self.valueChange)
        self.__col_amt.valueChanged.connect(self.valueChange)
        self.__rock_amt.valueChanged.connect(self.valueChange)
        self.__snow_amt.valueChanged.connect(self.valueChange)

        layout = QFormLayout()
        layout.addRow(QLabel(self.tr("Rows:")), self.__row_amt)
        layout.addRow(QLabel(self.tr("Columns:")), self.__col_amt)
        layout.addRow(QLabel(self.tr("Rocks:")), self.__rock_amt)
        layout.addRow(QLabel(self.tr("Snows:")), self.__snow_amt)

        form.setLayout(layout)
        return form

    def valueChange(self):
        max = self.__row_amt.value() * self.__col_amt.value() - 2
        self.__rock_amt.setMaximum(max - self.__snow_amt.value())
        self.__snow_amt.setMaximum(max - self.__rock_amt.value())

    def values(self):
        row = self.__row_amt.value()
        col = self.__col_amt.value()
        rocks = self.__rock_amt.value()
        snows = self.__snow_amt.value()
        return [row, col, rocks, snows]


class PickColorDialog(MyDialog):

    def __init__(self, bfs_color, dfs_color):
        self.__bfs_color = bfs_color
        self.__dfs_color = dfs_color
        super(PickColorDialog, self).__init__()
        self.setWindowTitle(self.tr("Change path's color"))

    def createForm(self):
        form = QGroupBox(self.tr("Pick color for paths:"))
        layout = QFormLayout()
        self.__bfs_button = QPushButton()
        self.__dfs_button = QPushButton()

        self.__bfs_button.setPalette(self.__bfs_color)
        self.__dfs_button.setPalette(self.__dfs_color)

        self.__bfs_button.clicked.connect(self.bfsButtonClicked)
        self.__dfs_button.clicked.connect(self.dfsButtonClicked)

        layout.addRow(QLabel("BFS:"), self.__bfs_button)
        layout.addRow(QLabel("DFS:"), self.__dfs_button)

        form.setLayout(layout)
        return form

    def bfsButtonClicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.__bfs_color = color
            self.__bfs_button.setPalette(color)

    def dfsButtonClicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.__dfs_color = color
            self.__dfs_button.setPalette(color)

    def values(self):
        return [self.__bfs_color, self.__dfs_color]


class MyAppView(QWidget):

    def __init__(self):
        super(MyAppView, self).__init__()

        self.__view = QGraphicsView()
        self.__tileset = QPixmap('../imgs/tiles.png')
        self.__load_button = QPushButton()
        self.__solve_button = QPushButton()
        self.__solve_button.setEnabled(False)
        self.setButtonsText()

        buttons = QHBoxLayout()
        buttons.addItem(
            QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons.addWidget(self.__load_button)
        buttons.addItem(
            QSpacerItem(10, 1, QSizePolicy.Minimum, QSizePolicy.Minimum))
        buttons.addWidget(self.__solve_button)

        layout = QVBoxLayout()
        layout.addWidget(self.__view)
        layout.addItem(buttons)

        self.setLayout(layout)

    def setLoadButton(self, function):
        self.__load_button.clicked.connect(function)

    def setSolveButton(self, function):
        self.__solve_button.clicked.connect(function)

    def setButtonsText(self):
        self.__load_button.setText(self.tr('Import maze from file'))
        self.__solve_button.setText(self.tr('Solve'))

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
        scene = QGraphicsScene()
        self.__view.setScene(scene)
        row, col = len(maze), len(maze[0])
        for i in range(row):
            for j in range(col):
                tile_num = self.getTileNum(maze[i][j])
                tile = self.__tileset.copy(tile_num * 32, 0, 32, 32)
                pixmap = scene.addPixmap(tile)
                pixmap.setPos(j * 32, i * 32)
        self.__solve_button.setEnabled(True)
        self.__path = []
        print(scene.width(), scene.height())

    def drawSolution(self, maze, result, color):
        print(result)
        scene = self.__view.scene()
        if len(result) == 0:
            QMessageBox.information(
                self, self.tr('Notification'),
                self.tr('There is no solution for this maze.'))
            return
        for line in self.__path:
            scene.removeItem(line)
        col = len(maze[0])
        pen = QPen(color, 8, Qt.SolidLine, Qt.RoundCap)
        for curr, next in pairwise(result):
            from_row, from_col = curr // col, curr % col
            to_row, to_col = next // col, next % col
            line = scene.addLine(from_col * 32 + 16, from_row * 32 + 16,
                                 to_col * 32 + 16, to_row * 32 + 16, pen)
            self.__path.append(line)
        scene.update()
