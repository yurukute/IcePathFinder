import time
from PySide6.QtCore import QSize, QTranslator, QEvent
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QFileDialog, QInputDialog, QLabel,
                               QMainWindow, QMessageBox)

from mywidgets import NewMazeDialog, PickColorDialog, MyMenuBar, MyAppView
from icemaze import IceMaze


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Path Finder')
        self.setFixedSize(QSize(800, 600))
        self.setMenuBar(self.getMenuBar())

        self.__appview = MyAppView()

        self.__appview.setSolveButton(self.solveMaze)
        self.__appview.setLoadButton(self.loadMaze)

        self.setCentralWidget(self.__appview)

        self.__maze = None
        self.__bfs_color, self.__dfs_color = QColor("yellow"), QColor("red")
        self.__translator = QTranslator(self)

        self.__msg = QLabel(self.tr('Welcome to Ice Path Finder'))
        self.statusBar().addPermanentWidget(self.__msg)

    def getMenuBar(self):
        menu = MyMenuBar()

        menu.setNewAction(self.initMaze)
        menu.setLoadAction(self.loadMaze)
        menu.setChangeCorlorAction(self.changeColor)
        menu.setChangeLanguageAction(self.changeLanguage)

        return menu

    def initMaze(self):
        dialog = NewMazeDialog()
        if dialog.exec():
            self.__maze = IceMaze(*dialog.values())
            self.__appview.drawMaze(self.__maze.get_map())

    def loadMaze(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text files (*.txt)')
        if dialog.exec():
            f = open(dialog.selectedFiles()[0])
            try:
                self.__maze = IceMaze.read_maze(f.read())
                self.__appview.drawMaze(self.__maze.get_map())
            except (ValueError, IndexError):
                QMessageBox.critical(
                    self, self.tr('Error'),
                    self.tr('CANNOT READ MAZE\n'
                            'File is empty.'))

    def changeColor(self):
        dialog = PickColorDialog(self.__bfs_color, self.__dfs_color)
        if dialog.exec():
            self.__bfs_color, self.__dfs_color = dialog.values()

    def solveMaze(self):
        alg = ('BFS', 'DFS')
        option, ok = QInputDialog.getItem(self, self.tr('Solve maze'),
                                          self.tr('Choose algorithm:'), alg)
        if ok:
            start_time = time.time()
            if option == 'BFS':
                self.__appview.drawSolution(self.__maze.get_map(),
                                            self.__maze.bfs(),
                                            self.__bfs_color)
            elif option == 'DFS':
                self.__appview.drawSolution(self.__maze.get_map(),
                                            self.__maze.dfs(),
                                            self.__dfs_color)
            self.__msg.setText(
                self.tr('Solved in ') + ('%s' % (time.time() - start_time)) +
                self.tr(' seconds.'))

    def changeLanguage(self):
        lang = self.sender().data()
        if lang:
            self.__translator.load(f'../translate/{lang}')
            QApplication.instance().installTranslator(self.__translator)
        else:
            QApplication.instance().removeTranslator(self.__translator)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

    def retranslateUi(self):
        self.setMenuBar(self.getMenuBar())
        self.__appview.setButtonsText()
        self.__msg.setText(self.tr('Welcome to Ice Path Finder'))


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
