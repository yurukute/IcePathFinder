from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import (QApplication, QFileDialog, QGraphicsScene,
                               QGraphicsView, QHBoxLayout,
                               QMainWindow, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget)
from icemaze import IceMaze
from mywidgets import NewMazeDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Path Finder')
        self.setFixedSize(QSize(800, 600))
        self.init_menubar()
        self.init_client()

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
        about_action = QAction('&About', self)
        about_action.setShortcut('F1')

        help_menu = menu.addMenu('&Help')
        help_menu.addAction(about_action)

    def init_client(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.tileset = QPixmap('./imgs/tiles.png')
        self.maze = None

        load_button = QPushButton('Import maze from file')
        load_button.clicked.connect(self.load_maze)
        solve_button = QPushButton('Solve')

        footer = QHBoxLayout()
        footer.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding,
                                   QSizePolicy.Minimum))
        footer.addWidget(load_button)
        footer.addItem(QSpacerItem(10, 1, QSizePolicy.Minimum,
                                   QSizePolicy.Minimum))
        footer.addWidget(solve_button)

        main = QVBoxLayout()
        main.addWidget(self.view)
        main.addItem(footer)

        self.wid = QWidget()
        self.wid.setLayout(main)
        self.setCentralWidget(self.wid)

    def load_maze(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text files (*.txt)')
        if dialog.exec():
            f = open(dialog.selectedFiles()[0])
            self.maze = IceMaze.read_maze(f.read())
            self.draw_maze()

    def init_maze(self):
        dialog = NewMazeDialog()
        if dialog.exec():
            self.maze = IceMaze(*dialog.values())
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
        self.maze.print()
        maze = self.maze.get_map()
        for i in range(len(maze)):
            tile_num = self.get_tile_num(maze[i])
            tile = self.tileset.copy(tile_num*32, 0,
                                     32, 32)
            pixmap = self.scene.addPixmap(tile)
            pixmap.setPos(tile_num*32, 0)


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
