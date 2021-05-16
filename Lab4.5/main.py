import sys
import window5
import os
import time
import urllib.request
import matplotlib.pyplot as plt
from threading import Thread
from PyQt5 import QtWidgets

times = []
file_names = []
file_paths = []


class DownloadThread(Thread):

    def __init__(self, url, window, i):
        """Инициализация потока"""
        Thread.__init__(self)
        self.url = url
        self.time = time.time()
        self.endtime = 0
        self.mainwindow = window
        self.id = i

    def run(self):
        """Запуск потока"""
        handle = urllib.request.urlopen(self.url)
        file_name = self.url.split('/')[-1]
        fname = "D:\\" + file_name

        site = urllib.request.urlopen(self.url)
        out = site.length
        start = (4096 * 100) / out
        perc = (4096 * 100) / out
        arr = [self.mainwindow.progressBar, self.mainwindow.progressBar_2, self.mainwindow.progressBar_3]
        with open(fname, "wb") as f_handler:
            while True:
                chunk = handle.read(4096)
                if not chunk:
                    break
                f_handler.write(chunk)
                arr[self.id].setValue(start)
                start = start + perc

        self.endtime = time.time()
        mass = [self.mainwindow.label, self.mainwindow.label_2, self.mainwindow.label_3]
        mass[self.id].setText("Download finished")
        global times
        global file_names
        global file_paths
        file_paths.append(fname)
        times.append(round((self.endtime - self.time), 3))
        file_names.append("File {}".format(self.id))


def download_files(urls, window, ids):
    for i, url in enumerate(urls):
        thread = DownloadThread(url, window, ids[i])
        thread.start()


class ExampleApp(QtWidgets.QMainWindow, window5.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2.clicked.connect(self.showres)

    def download(self):
        global times, file_names, file_paths
        file_paths.clear()
        file_names.clear()
        times.clear()
        url = []
        ids = []
        self.label_3.setText("")
        self.label_2.setText("")
        self.label.setText("")
        for i, l in enumerate([self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()]):
            if l:
                url.append(l)
                ids.append(i)
        download_files(url, self, ids)

    def showres(self):
        global times, file_names, file_paths

        sizes = [os.path.getsize(s) for s in file_paths]

        labls = []
        for i, ff in enumerate(file_names):
            out = ff + '\n[' + str(round((sizes[i] / (1024 * 1024)), 2)) + ' mb]'
            labls.append(out)

        al1 = []
        for f in times:
            sp = str(f).split('.')
            out = sp[0] + 's ' + sp[1] + 'ms'
            al1.append(out)

        plt.subplot(121)
        plt.bar(file_names, times)

        for index, value in enumerate(times):
            plt.text(index - 0.3, value, al1[index])
        plt.grid()
        plt.title("Download time plot")
        plt.ylabel("Download time")

        plt.subplot(122)
        plt.pie(sizes, labels=labls, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')
        plt.title("File size")

        plt.show()



app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
app.exec_()