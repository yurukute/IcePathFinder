import time
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt, QTranslator, QEvent
from PySide6.QtWidgets import (QApplication, QFileDialog, QInputDialog, QLabel,
                               QMainWindow, QMessageBox)

from mywidgets import NewMazeDialog, PickColorDialog, MyAppView
from icemaze import IceMaze


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Path Finder')
        self.setFixedSize(QSize(800, 600))
        self.init_menubar()

        self.appview = MyAppView()

        self.appview.solve_button.clicked.connect(self.solve_maze)
        self.appview.load_button.clicked.connect(self.load_maze)
        self.appview.solve_button.setEnabled(False)

        self.setCentralWidget(self.appview)

        self.maze = None
        self.bfs_color, self.dfs_color = Qt.yellow, Qt.red
        self.translator = QTranslator(self)

        self.msg = QLabel(self.tr('Welcome to Ice Path Finder'))
        self.statusBar().addPermanentWidget(self.msg)

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

    def init_maze(self):
        dialog = NewMazeDialog()
        if dialog.exec():
            self.maze = IceMaze(*dialog.values())
            self.appview.draw_maze()

    def load_maze(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text files (*.txt)')
        if dialog.exec():
            f = open(dialog.selectedFiles()[0])
            try:
                self.maze = IceMaze.read_maze(f.read())
                self.appview.draw_maze(self.maze.get_map())
            except (ValueError, IndexError):
                QMessageBox.critical(
                    self, self.tr('Error'),
                    self.tr('CANNOT READ MAZE\n'
                            'File is empty.'))

    def change_color(self):
        dialog = PickColorDialog(self.bfs_color, self.dfs_color)
        if dialog.exec():
            self.bfs_color, self.dfs_color = dialog.values()

    def solve_maze(self):
        alg = ('BFS', 'DFS')
        option, ok = QInputDialog.getItem(self, self.tr('Solve maze'),
                                          self.tr('Choose algorithm:'), alg)
        if ok:
            start_time = time.time()
            if option == 'BFS':
                self.appview.draw_solution(self.maze.get_map(),
                                           self.maze.bfs(), self.bfs_color)
            elif option == 'DFS':
                self.appview.draw_solution(self.maze.get_map(),
                                           self.maze.dfs(), self.dfs_color)
            self.msg.setText(
                self.tr('Solved in ') + ('%s' % (time.time() - start_time)) +
                self.tr(' seconds.'))

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
        self.menuBar().clear()
        self.init_menubar()
        self.appview.reset_buttons()
        self.msg.setText(self.tr('Welcome to Ice Path Finder'))


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
