import time
from itertools import pairwise
from PySide6.QtCore import QSize, Qt, QTranslator, QEvent
from PySide6.QtGui import QAction, QPen, QPixmap
from PySide6.QtWidgets import (QApplication, QFileDialog, QGraphicsScene,
                               QGraphicsView, QHBoxLayout, QInputDialog,
                               QLabel, QMainWindow, QMessageBox, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from mywidgets import NewMazeDialog, PickColorDialog
from icemaze import IceMaze


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Path Finder')
        self.setFixedSize(QSize(800, 600))
        self.init_menubar()
        self.init_view()
        self.translator = QTranslator(self)
        self.exec_time = QLabel(self.tr('Welcome to Ice Path Finder'))
        self.statusBar().addPermanentWidget(self.exec_time)

    def init_menubar(self):
        menu = self.menuBar()

        # File menu
        new_action = QAction(self.tr('&New'), self)
        load_action = QAction(self.tr('&Open...'), self)
        quit_action = QAction(self.tr('&Quit'), self)

        new_action.setShortcut('Ctrl+N')
        load_action.setShortcut('Ctrl+O')
        quit_action.setShortcut('Ctrl+Q')

        new_action.triggered.connect(self.init_maze)
        load_action.triggered.connect(self.load_maze)
        quit_action.triggered.connect(self.close)

        file_menu = menu.addMenu(self.tr('&File'))
        file_menu.addAction(new_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        # Option menu
        change_color_action = QAction(self.tr('&Change path\'s color'), self)
        english_action = QAction(self.tr('&English'), self)
        vietnamese_action = QAction(self.tr('&Vietnamese'), self)

        change_color_action.triggered.connect(self.change_color)
        english_action.triggered.connect(self.change_language)
        vietnamese_action.triggered.connect(self.change_language)
        vietnamese_action.setData('vi_VN')

        option_menu = menu.addMenu(self.tr('&Option'))
        option_menu.addAction(change_color_action)

        change_language_menu = option_menu.addMenu(self.tr('Change &language'))
        change_language_menu.addAction(english_action)
        change_language_menu.addAction(vietnamese_action)

        # Help menu
        help_action = QAction(self.tr('&Help...'), self)
        about_action = QAction(self.tr('&About Ice Path Finder'), self)

        help_action.setShortcut('F1')

        help_action.triggered.connect(self.show_help)
        about_action.triggered.connect(self.show_about)

        help_menu = menu.addMenu(self.tr('&Help'))
        help_menu.addAction(help_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)

    def init_view(self):
        self.view = QGraphicsView()
        self.tileset = QPixmap('./imgs/tiles.png')
        self.maze = None
        self.bfs_color, self.dfs_color = Qt.yellow, Qt.red

        self.load_button = QPushButton(self.tr('Import maze from file'))
        self.load_button.clicked.connect(self.load_maze)
        self.solve_button = QPushButton(self.tr('Solve'))
        self.solve_button.clicked.connect(self.solve_maze)
        self.solve_button.setEnabled(False)

        footer = QHBoxLayout()
        footer.addItem(
            QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        footer.addWidget(self.load_button)
        footer.addItem(
            QSpacerItem(10, 1, QSizePolicy.Minimum, QSizePolicy.Minimum))
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
            try:
                self.maze = IceMaze.read_maze(f.read())
                self.draw_maze()
            except ValueError:
                QMessageBox.critical(
                    self, self.tr('Error'),
                    self.tr('CANNOT READ MAZE\n'
                            'File is empty.'))

    def change_color(self):
        dialog = PickColorDialog(self.bfs_color, self.dfs_color)
        if dialog.exec():
            self.bfs_color, self.dfs_color = dialog.values()

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
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        maze = self.maze.get_map()
        row, col = len(maze), len(maze[0])
        for i in range(row):
            for j in range(col):
                tile_num = self.get_tile_num(maze[i][j])
                tile = self.tileset.copy(tile_num * 32, 0, 32, 32)
                pixmap = self.scene.addPixmap(tile)
                pixmap.setPos(j * 32, i * 32)
        self.solve_button.setEnabled(True)
        self.path = []
        print(self.scene.width(), self.scene.height())

    def draw_solution(self, result, color):
        print(result)
        if len(result) == 0:
            QMessageBox.information(
                self, self.tr('Notification'),
                self.tr('There is no solution for this maze.'))
            return
        for line in self.path:
            self.scene.removeItem(line)
        col = len(self.maze.get_map()[0])
        pen = QPen(color, 8, Qt.SolidLine, Qt.RoundCap)
        for curr, next in pairwise(result):
            from_row, from_col = curr // col, curr % col
            to_row, to_col = next // col, next % col
            line = self.scene.addLine(from_col * 32 + 16, from_row * 32 + 16,
                                      to_col * 32 + 16, to_row * 32 + 16, pen)
            self.path.append(line)
        self.scene.update()

    def solve_maze(self):
        alg = ('BFS', 'DFS')
        option, ok = QInputDialog.getItem(self, 'Solve maze',
                                          'Choose algorithm:', alg)
        if ok:
            start_time = time.time()
            if option == 'BFS':
                self.draw_solution(self.maze.bfs(), self.bfs_color)
            elif option == 'DFS':
                self.draw_solution(self.maze.dfs(), self.dfs_color)
            self.exec_time.setText(
                self.tr('Solved in %s secconds' % (time.time() - start_time)))

    def show_about(self):
        QMessageBox.information(
            self, self.tr('About - Ice Path Finder'),
            self.tr('College Project - Basic Topics:\n'
                    'Apply blind search algorithms in solving ice maze\n'
                    'Develop by Nguyen Khanh Dung\n'
                    'Version: 1.0'))

    def show_help(self):
        print('help clicked')

    def change_language(self):
        lang = self.sender().data()
        if lang:
            self.translator.load(f'translate/{lang}')
            QApplication.instance().installTranslator(self.translator)
        else:
            QApplication.instance().removeTranslator(self.translator)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

    def retranslateUi(self):
        trans = QApplication.translate
        context = 'MainWindow'
        sources = [self.exec_time, self.load_button, self.solve_button]
        for menu in self.menuBar().actions():
            for submenu in menu.menu().actions():
                if submenu.menu():
                    for action in submenu.menu().actions():
                        sources.append(action)
                sources.append(submenu)
            sources.append(menu)
        for source in sources:
            source.setText(trans(context, source.text()))


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
