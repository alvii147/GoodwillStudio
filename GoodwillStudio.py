import sys
from scipy.io import wavfile
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtGui import QIcon, QColor, QPixmap, QBrush
from PyQt5.QtCore import QSize, QThread, pyqtSignal
import pyqtgraph as pg
from QSharpTools import SharpButton
from record import Recorder
from gcspeech import speech2text
from better_profanity import profanity

s2t = []
transcripts = []
fs = 0
data = []

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 600
        screenSizeX = 1920
        screenSizeY = 1080
        self.xPos = int((screenSizeX/2) - (self.width/2))
        self.xPos -= 2000
        self.yPos = int((screenSizeY/2) - (self.height/2))
        self.recordButtonOn = True
        self.stopButtonOn = False
        self.recThread = recordThread()
        self.procThread = processThread()
        self.procThread.procDone.connect(self.processDone)
        self.initUI()

    def initUI(self):
        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Goodwill Studio")
        self.acceptDrops()

        bgColor = "rgb(14, 14, 37);"
        graphBgColor = (28, 28, 74)
        self.setStyleSheet(f"background-color: {bgColor};")
        primColor = "rgb(45, 45, 134)"
        secColor = "rgb(217, 217, 242)"
        self.recButtonLength = 50

        self.recordButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.recordButton.move(13, 13)
        self.recordButton.resize(self.recButtonLength, self.recButtonLength)
        self.recordButton.setIcon(QIcon("img/rec_icon.png"))
        self.recordButton.setIconSize(QSize(int(self.recButtonLength * 0.75), int(self.recButtonLength * 0.75)))
        self.recordButton.clicked.connect(self.startRecording)

        self.stopButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.stopButton.move(73, 13)
        self.stopButton.resize(self.recButtonLength, self.recButtonLength)
        self.stopButton.setIcon(QIcon("img/stop_icon.png"))
        self.stopButton.setIconSize(QSize(int(self.recButtonLength * 0.73), int(self.recButtonLength * 0.73)))
        self.stopButton.clicked.connect(self.stopRecording)

        self.playButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.playButton.move(133, 13)
        self.playButton.resize(self.recButtonLength, self.recButtonLength)
        self.playButton.setIcon(QIcon("img/playbutton_icon.png"))
        self.playButton.setIconSize(QSize(int(self.recButtonLength * 1.05), int(self.recButtonLength * 1.05)))

        self.cutButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.cutButton.move(193, 13)
        self.cutButton.resize(self.recButtonLength, self.recButtonLength)
        self.cutButton.setIcon(QIcon("img/scissors_icon.png"))
        self.cutButton.setIconSize(QSize(int(self.recButtonLength * 0.80), int(self.recButtonLength * 0.80)))

        self.fileButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.fileButton.move(253, 13)
        self.fileButton.resize(self.recButtonLength, self.recButtonLength)
        self.fileButton.setIcon(QIcon("img/audiofile_icon.png"))
        self.fileButton.setIconSize(QSize(int(self.recButtonLength * 0.70), int(self.recButtonLength * 0.70)))

        self.titleLabel = QLabel(self)
        self.titleLabel.move(620, -10)
        self.titleLabel.resize(self.width - 620 - 10, 90)
        self.pixmap = QPixmap("img/logo.png").scaledToHeight(75)
        self.titleLabel.setPixmap(self.pixmap)

        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.move(10, 80)
        self.graphWidget.resize(self.width - 20, 150)
        self.graphWidget.hideAxis("left")
        self.graphWidget.hideAxis("bottom")
        self.graphWidget.setBackground(QColor(graphBgColor[0], graphBgColor[1], graphBgColor[2]))

        self.transcriptBox = QListWidget(self)
        self.transcriptBox.move(10, 250)
        self.transcriptBox.resize(self.width - 20, 300)
        self.transcriptBox.setStyleSheet("QListWidget{color: rgb(179, 179, 204); background-color: rgb(41, 41, 61); selection-color: rgb(41, 41, 61); selection-background-color: rgb(179, 179, 204); font-size: 15px;}")

        self.exportButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.exportButton.move(10, self.height - 28 - 10)
        self.exportButton.resize(165, 28)
        self.exportButton.setText("Export Censored Audio")

        self.copyButton = SharpButton(self, primaryColor = primColor, secondaryColor = secColor, pressed_border_color = bgColor, border_radius = "25px")
        self.copyButton.move(185, self.height - 28 - 10)
        self.copyButton.resize(150, 28)
        self.copyButton.setText("Copy Transcript")

        self.show()

    def startRecording(self):
        if self.recordButtonOn:
            self.recordButtonOn = False
            self.stopButtonOn = True
            self.recThread.start()

    def stopRecording(self):
        if self.stopButtonOn:
            self.stopButtonOn = False
            self.recThread.rec.RECORDING = False
            while not self.recThread.rec.PROCESSED:
                pass
            self.procThread.start()

    def processDone(self):
        global transcripts
        global s2t
        global fs
        global data
        wavlength = len(data) / float(fs)
        ydata = [i[0] for i in data]
        xdata = range(len(ydata))
        graphLineColor = (200, 200, 234)
        graphCriticalLineColor = (255, 128, 128)
        timeCount = 0
        for i in s2t:
            dataPointLeft = int((timeCount / wavlength) * len(ydata))
            dataPointRight = int((i[1] / wavlength) * len(ydata))
            color = graphCriticalLineColor if profanity.contains_profanity(i[0]) else graphLineColor
            self.graphWidget.plot(xdata[dataPointLeft:dataPointRight], ydata[dataPointLeft:dataPointRight], pen = pg.mkPen(color = color))
            timeCount = i[1]
        self.transcriptBox.clear()
        criticalBrush = QBrush(QColor(41, 41, 61))
        for tr in transcripts:
            item = QListWidgetItem(str(profanity.censor(tr)).capitalize())
            if profanity.contains_profanity(tr):
                item.setForeground(criticalBrush)
                item.setBackground(QColor(255, 128, 128))
            self.transcriptBox.addItem(item)
        self.recordButtonOn = True

class recordThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.rec = Recorder()
        self.rec.start()

class processThread(QThread):
    procDone = pyqtSignal(int)
    def __init__(self):
        super().__init__()

    def run(self):
        global s2t
        global transcripts
        global fs
        global data
        fs, data = wavfile.read("output.wav")
        transcripts, s2t = speech2text()
        self.procDone.emit(int)


if __name__ == "__main__":
    profanity.add_censor_words(["hackathon"])
    app = QApplication(sys.argv)
    myWin = Window()
    sys.exit(app.exec_())