import os
from PyQt4 import QtCore, QtGui, uic
import sys
import requests
from bs4 import BeautifulSoup
from pytube import YouTube


qtCreatorFile1 = "untitled1.ui"  # Enter file here.
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)

qtCreatorFile2 = "untitled1.ui"  # Enter file here.
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

qtCreatorFile3 = "untitled3.ui"  # Enter file here.
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)


class MyApp(QtGui.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.save.clicked.connect(self.Check_connection_Url)
        self.actionAbout.triggered.connect(self.About)
        self.actionExit.triggered.connect(self.Quit_Win)
        self.url_video = ''
        self.url_playlist = []
        self.window2 = None
        self.window3 = None
        #self.ra_mp.setEnabled(False)
    def About(self):
        pass

    def Quit_Win(self):
        sys.exit()

    def Check_connection_Url(self):
        self.url_video = self.url_entered.text()
        if len(self.url_video) == 0:
            QtGui.QMessageBox.information(self, 'Information',
                                          "Enter URL or Check Internet Connection", )
        else:
            self.Quality()
            if self.ra_playlist.isChecked():
                if not (len(self.resolution)==0 and len(self.filetype)==0):
                    self.pre_download_playlist()
                else:
                    QtGui.QMessageBox.information(self, 'Information',
                                                  "Select Either playlist or video", )


            elif self.ra_video.isChecked():
                if not (len(self.resolution)==0 and len(self.filetype)==0):
                    self.pre_download_video()
                else:
                    QtGui.QMessageBox.information(self, 'Information',
                                                  "Select Either playlist or video", )

            else:
                QtGui.QMessageBox.information(self, 'Information',
                                          "Select Either playlist or video", )


    def Quality(self):
        self.resolution = ''
        self.filetype = ''
        if self.ra_mp4.isChecked():
            self.filetype = self.ra_mp4.text()
        if self.ra_flv.isChecked():
            self.filetype = self.ra_flv.text()
        if self.ra_3gp.isChecked():
            self.filetype = self.ra_3gp.text()
        if self.ra_144p.isChecked():
            self.resolution = self.ra_144p.text()
        if self.ra_240p.isChecked():
            self.resolution = self.ra_240p.text()
        if self.ra_360p.isChecked():
            self.resolution = self.ra_360p.text()
        if self.ra_480p.isChecked():
            self.resolution = self.ra_480p.text()
        if self.ra_720p.isChecked():
            self.resolution = self.ra_720p.text()
        if self.ra_1080p.isChecked():
            self.resolution = self.ra_1080p.text()


    def file_open(self):
        self.file_path = QtGui.QFileDialog.getExistingDirectory(None)

    def pre_download_video(self):
        '''self.window2 = MyApp2()
        self.window2.exec_()'''
        yt = YouTube(self.url_video)
        video = yt.get(self.filetype, self.resolution)
        self.file_open()
        video.download(self.file_path)
        print('done')

    def pre_download_playlist(self):
        '''self.window3 = MyApp3()
        self.window3.exec_()'''
        source_code = requests.get(self.url_video)
        code_text = source_code.text
        soup = BeautifulSoup(code_text, "html.parser")
        for links in soup.findAll('a', {'dir': 'ltr'}):
            href = 'https://www.youtube.com/' + links.get('href')
            self.url_playlist.append(href)
        self.downloading()
    def downloading(self):
        self.file_open()
        for i in range(1,len(self.url_playlist)-1):
            ytp = YouTube(self.url_playlist[i])
            print()
            video = ytp.get(self.filetype, self.resolution)
            video.download(self.file_path)
            print(str(i)+'done')
class thread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__()
        self.setupUi(self)

class MyApp2(QtGui.QWidget, Ui_MainWindow2):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)

class MyApp3(QtGui.QWidget, Ui_MainWindow3):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)



if __name__ == "__main__":
    file_name=''
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())