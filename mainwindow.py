import time
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import (QApplication, QFileDialog, QGraphicsScene,
                               QGraphicsView, QHBoxLayout, QInputDialog,
                               QMainWindow, QMessageBox, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from mywidgets import NewMazeDialog
from icemaze import IceMaze


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Path Finder')
        self.setFixedSize(QSize(600, 600))
        self.init_menubar()
        self.init_view()

    def init_menubar(self):
        menu = self.menuBar()

        # File menu
        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.init_maze)
        load_action = QAction('&Load...', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.load_maze)
        quit_action = QAction('&Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)

        file_menu = menu.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        # Help menu
        help_action = QAction('&Help...', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.show_help)
        about_action = QAction('&About Ice Path Finder', self)
        about_action.triggered.connect(self.show_about)

        help_menu = menu.addMenu('&Help')
        help_menu.addAction(help_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)

    def init_view(self):
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.tileset = QPixmap('./imgs/tiles.png')
        self.maze = None

        self.load_button = QPushButton('Import maze from file')
        self.load_button.clicked.connect(self.load_maze)
        self.solve_button = QPushButton('Solve')
        self.solve_button.clicked.connect(self.solve_maze)
        self.solve_button.setEnabled(False)

        footer = QHBoxLayout()
        footer.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding,
                                   QSizePolicy.Minimum))
        footer.addWidget(self.load_button)
        footer.addItem(QSpacerItem(10, 1, QSizePolicy.Minimum,
                                   QSizePolicy.Minimum))
        footer.addWidget(self.solve_button)

        main = QVBoxLayout()
        main.addWidget(self.view)
        main.addItem(footer)

        self.wid = QWidget()
        self.wid.setLayout(main)
        self.setCentralWidget(self.wid)

    def init_maze(self):
        dialog = NewMazeDialog()
        if dialog.exec():
            self.maze = IceMaze(*dialog.values())
            self.draw_maze()

    def load_maze(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text files (*.txt)')
        if dialog.exec():
            f = open(dialog.selectedFiles()[0])
            self.maze = IceMaze.read_maze(f.read())
            self.draw_maze()

    def get_tile_num(self, tile):
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

    def draw_maze(self):
        self.scene.clear()
        maze = self.maze.get_map()
        col, row = len(maze), len(maze[0])
        for i in range(row):
            for j in range(col):
                tile_num = self.get_tile_num(maze[i][j])
                tile = self.tileset.copy(tile_num*32, 0, 32, 32)
                pixmap = self.scene.addPixmap(tile)
                pixmap.setPos(j*32, i*32)
        self.solve_button.setEnabled(True)

    def draw_solution(self):
        return

    def solve_maze(self):
        alg = ('BFS', 'DFS')
        option, ok = QInputDialog.getItem(
            self, 'Solve maze', 'Choose algorithm:', alg)
        if ok:
            start_time = time.time()
            if option == 'BFS':
                print(self.maze.bfs())
            elif option == 'DFS':
                print(self.maze.dfs())

    def show_about(self):
        QMessageBox.about(
            self,
            'About - Ice Path Finder',
            'College Project - Basic Topics: '
            'Apply blind search algorithms in solving ice maze\n'
            'Develop by Nguyen Khanh Dung\n'
            'Version: 1.0'
        )

    def show_help(self):
        print('help clicked')


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
