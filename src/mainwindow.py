import time
from os import path
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

        self.__menu = self.getMenuBar('en')

        self.__appview = MyAppView()
        self.__appview.setSolveButton(self.solveMaze)
        self.__appview.setLoadButton(self.loadMaze)

        self.setCentralWidget(self.__appview)

        self.__maze = None
        self.__bfs_color, self.__dfs_color = QColor("yellow"), QColor("red")
        self.__translator = QTranslator(self)

        self.__msg = QLabel(self.tr('Welcome to Ice Path Finder'))
        self.statusBar().addPermanentWidget(self.__msg)

    def getMenuBar(self, lang):
        menu = MyMenuBar(lang)

        menu.setNewAction(self.initMaze)
        menu.setLoadAction(self.loadMaze)
        menu.setSaveAction(self.saveMaze)
        menu.setChangeCorlorAction(self.changeColor)
        menu.setChangeLanguageAction(self.changeLanguage)

        self.setMenuBar(menu)
        return menu

    def initMaze(self):
        dialog = NewMazeDialog()
        if dialog.exec():
            self.__maze = IceMaze(*dialog.values())
            self.__appview.drawMaze(self.__maze.get_map())
            self.enableSave()

    def loadMaze(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text files (*.txt)')
        if dialog.exec():
            f = open(dialog.selectedFiles()[0])
            try:
                self.__maze = IceMaze.read_maze(f.read())
                self.__appview.drawMaze(self.__maze.get_map())
                self.enableSave()
            except (ValueError, IndexError):
                QMessageBox.critical(
                    self, self.tr('Error'),
                    self.tr('CANNOT READ MAZE\n'
                            'File is empty.'))

    def enableSave(self):
        file_menu = self.menuBar().actions()[0]
        save_action = file_menu.menu().actions()[2]
        save_action.setEnabled(True)

    def saveMaze(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save maze', '',
                                                  'Text files (*.txt)')
        if filename:
            map = self.__maze.get_map()
            f = open(filename, 'w')
            for i in range(len(map)):
                for j in range(len(map[0])):
                    f.write(map[i][j])
                f.write('\n')
            f.close()

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
            self.__translator.load(
                path.dirname(__file__) + f'/../translate/{lang}')
            QApplication.instance().installTranslator(self.__translator)
        else:
            QApplication.instance().removeTranslator(self.__translator)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

    def retranslateUi(self):
        lang = self.__translator.language()
        self.__menu = self.getMenuBar(lang[0:2])
        self.__appview.setButtonsText()
        self.__msg.setText(self.tr('Welcome to Ice Path Finder'))


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    app.exec()
