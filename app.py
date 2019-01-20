import os
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox

import icon
from DirCopy import Ui_DirCopy


class DirCopy(QDialog):
    def __init__(self):
        super().__init__()
        self.DirCopy = Ui_DirCopy()
        self.DirCopy.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))
        self.show()
        #事件處理
        self.DirCopy.DirPathButton.clicked.connect(self.DirSelect)
        self.DirCopy.AimsDirPathButton.clicked.connect(self.AimsDirSelect)
        self.DirCopy.checkBox.clicked.connect(self.CheckBox)
        self.DirCopy.RunButton.clicked.connect(self.Run)

    def CheckBox(self):
        """CheckBox"""
        self.DirCopy.DirList.clear()
        DirSelect = self.DirCopy.DirPath.text()
        if not any(DirSelect):
            pass
        if self.DirCopy.checkBox.isChecked():
            DirList = self.IncludeSubfolder(DirSelect)
            self.DirCopy.DirList.addItems(DirList)
        else:
            DirList = self.DirList(DirSelect)
            self.DirCopy.DirList.addItems(DirList)

    def DirSelect(self):
        """DirSelect"""
        DirSelect = QFileDialog.getExistingDirectory(self,"選擇資料夾")
        if not DirSelect.endswith('/'):
            DirSelect = DirSelect+'/'
        if DirSelect==self.DirCopy.AimsDirPath.text():
            return QMessageBox.critical(self, '錯誤', '資料夾路徑與目的地路徑不可相同',QMessageBox.Ok, QMessageBox.Ok)
        self.DirCopy.DirPath.setText(DirSelect)
        self.DirCopy.DirList.clear()
        if any(DirSelect):
            if self.DirCopy.checkBox.isChecked():
                DirList = self.IncludeSubfolder(DirSelect)
                self.DirCopy.DirList.addItems(DirList)
            else:
                DirList = self.DirList(DirSelect)
                self.DirCopy.DirList.addItems(DirList)
                return 0

    def AimsDirSelect(self):
        """AimsDirSelect"""
        AimsDirSelect = QFileDialog.getExistingDirectory(self,"選擇資料夾")
        if not AimsDirSelect.endswith('/'):
            AimsDirSelect = AimsDirSelect+'/'
        if AimsDirSelect==self.DirCopy.DirPath.text():
            return QMessageBox.critical(self, '錯誤', '資料夾路徑與目的地路徑不可相同',QMessageBox.Ok, QMessageBox.Ok)
        self.DirCopy.AimsDirPath.setText(AimsDirSelect)

    def DirList(self,DirSelect):
        """DirList"""
        return [ f'{os.path.join(DirSelect,dirs)}' for dirs in os.listdir(DirSelect) if os.path.isdir(os.path.join(DirSelect,dirs)) ]

    def IncludeSubfolder(self,DirSelect):
        """IncludeSubfolder"""
        Dirs = []
        for root, dirs, files in os.walk(DirSelect):
            for Dir in dirs:
                Dirs.append(os.path.join(root,Dir).replace('\\','/'))
        return Dirs

    def Run(self):
        """Run"""
        DirPath = self.DirCopy.DirPath.text()
        AimsDirPath = self.DirCopy.AimsDirPath.text()

        if not any(DirPath) or not any(AimsDirPath):
            return QMessageBox.critical(self, '錯誤', '資料夾路徑或目的地路徑不可為空',QMessageBox.Ok, QMessageBox.Ok)
        try:
            if self.DirCopy.checkBox.isChecked():
                DirList = self.IncludeSubfolder(DirPath)
            else:
                DirList = self.DirList(DirPath)
            for index in range(len(DirList)):
                Dir = DirList[index].replace(DirPath,AimsDirPath)
                if not os.path.isdir(Dir):
                    os.makedirs(Dir)
                progress = '{:.0f}'.format((index+1)/len(DirList)*100)
                self.DirCopy.progressBar.setProperty("value", progress)
            return QMessageBox.about(self, '通知', '完成複製')
        except Exception as e:
            self.ErrorLog(str(e))


    def ErrorLog(self,Msg):
        """Error Log"""
        with open( f'{os.path.abspath(os.path.join(sys.argv[0],os.path.pardir))}/Error.log','a',encoding='UTF-8') as log:
            log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' - '+Msg+'\n')

if __name__=='__main__':
    app = QApplication(sys.argv)
    DirCopy = DirCopy()
    DirCopy.show()
    sys.exit(app.exec_())
