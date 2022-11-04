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
        self.setMenuBar(self.getMenuBar())

        self.appview = MyAppView()

        self.appview.setSolveButton(self.solveMaze)
        self.appview.setLoadButton(self.loadMaze)

        self.setCentralWidget(self.appview)

        self.maze = None
        self.bfs_color, self.dfs_color = Qt.yellow, Qt.red
        self.translator = QTranslator(self)

        self.msg = QLabel(self.tr('Welcome to Ice Path Finder'))
        self.statusBar().addPermanentWidget(self.msg)

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
            self.maze = IceMaze(*dialog.values())
            self.appview.drawMaze(self.maze.get_map())

    def loadMaze(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text files (*.txt)')
        if dialog.exec():
            f = open(dialog.selectedFiles()[0])
            try:
                self.maze = IceMaze.read_maze(f.read())
                self.appview.drawMaze(self.maze.get_map())
            except (ValueError, IndexError):
                QMessageBox.critical(
                    self, self.tr('Error'),
                    self.tr('CANNOT READ MAZE\n'
                            'File is empty.'))

    def changeColor(self):
        dialog = PickColorDialog(self.bfs_color, self.dfs_color)
        if dialog.exec():
            self.bfs_color, self.dfs_color = dialog.values()

    def solveMaze(self):
        alg = ('BFS', 'DFS')
        option, ok = QInputDialog.getItem(self, self.tr('Solve maze'),
                                          self.tr('Choose algorithm:'), alg)
        if ok:
            start_time = time.time()
            if option == 'BFS':
                self.appview.drawSolution(self.maze.get_map(), self.maze.bfs(),
                                          self.bfs_color)
            elif option == 'DFS':
                self.appview.drawSolution(self.maze.get_map(), self.maze.dfs(),
                                          self.dfs_color)
            self.msg.setText(
                self.tr('Solved in ') + ('%s' % (time.time() - start_time)) +
                self.tr(' seconds.'))

    def changeLanguage(self):
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
        self.setMenuBar(self.getMenuBar())
        self.appview.setButtonsText()
        self.msg.setText(self.tr('Welcome to Ice Path Finder'))


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
