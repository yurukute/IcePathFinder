import time
from PySide6.QtCore import QSize, Qt, QTranslator, QEvent
from PySide6.QtWidgets import (QApplication, QFileDialog, QInputDialog, QLabel,
                               QMainWindow, QMessageBox)

from mywidgets import NewMazeDialog, PickColorDialog, MyMenuBar, MyAppView
from icemaze import IceMaze


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Path Finder')
        self.setFixedSize(QSize(800, 600))
        self.setMenuBar(self.get_menubar())

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

    def get_menubar(self):
        menu = MyMenuBar()

        menu.new_action.triggered.connect(self.init_maze)
        menu.load_action.triggered.connect(self.load_maze)
        menu.quit_action.triggered.connect(self.close)
        menu.change_color_action.triggered.connect(self.change_color)
        menu.english_action.triggered.connect(self.change_language)
        menu.vietnamese_action.triggered.connect(self.change_language)

        return menu

    def init_maze(self):
        dialog = NewMazeDialog()
        if dialog.exec():
            self.maze = IceMaze(*dialog.values())
            self.appview.draw_maze(self.maze.get_map())

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

    def change_language(self):
        lang = self.sender().data()
        if lang:
            self.translator.load(f'../translate/{lang}')
            QApplication.instance().installTranslator(self.translator)
        else:
            QApplication.instance().removeTranslator(self.translator)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

    def retranslateUi(self):
        self.setMenuBar(self.get_menubar())
        self.appview.reset_buttons()
        self.msg.setText(self.tr('Welcome to Ice Path Finder'))


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
