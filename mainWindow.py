import sys, os
from ALPWindow import *
from alp_program import *



class mainALP(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # заполнение окна c файлами
        # lists = os.listdir(folder + 'Files\\')
        lists = os.listdir('Files\\')
        for x in lists:
            self.ui.listWidget.addItem(x)

        # кнопки pushButton
        self.ui.pushButton.clicked.connect(self.fopensingal)  # первая кнопка открывает сигнал
        self.ui.pushButton_2.clicked.connect(self.fopenresponce)  # вторая кнопка октрывает отклик
        self.ui.pushButton_3.clicked.connect(self.makedial)  # третья кнопка проводит расчет
        self.ui.pushButton_4.clicked.connect(self.save)     #сохраняет таблички
        self.ui.pushButton_5.clicked.connect(self.plotterf1) #строит графики
        self.ui.pushButton_6.clicked.connect(self.replotterf1)  #сохраняет графики
        self.ui.pushButton_7.clicked.connect(self.makesnr)  #проводит расчеты snr

    def fopensingal(self):  # функция кнопки открыть сигнал
        try:
            self.ui.lineEdit.setText(self.ui.listWidget.currentItem().text())
        except:
            print('Choice the signal_file')

    def fopenresponce(self):  # функция кнопки открыть отклик
        try:
            self.ui.lineEdit_2.setText(self.ui.listWidget.currentItem().text())
        except:
            print('Choice the responce_file')

    #функция отрисовать графики
    def plotterf1(self):
            plotter1(self.ui.figure1,self.ui.canvas1,self.ui.spinBox.value(),self.ui.spinBox_2.value())
            plotter2(self.ui.figure2, self.ui.canvas2,self.ui.spinBox.value(),self.ui.spinBox_2.value(),
                     self.ui.spinBox_3.value(),self.ui.spinBox_4.value())
            plotter3(self.ui.figure3, self.ui.canvas3)

    #функция сохранить рисунки
    def savePictures(self):
        self.ui.figure1.set_size_inches(8,2.5)
        self.ui.figure1.tight_layout()
        self.ui.figure1.subplots_adjust(left=0.166,right=0.936)
        self.ui.figure1.savefig(str(sys.argv)[2:-15] + 'signal.png',dpi=100, fmt='png')
        self.ui.figure2.set_size_inches(8,2.7)
        self.ui.figure2.tight_layout()
        self.ui.figure2.subplots_adjust(left=0.166,right=0.936)
        self.ui.figure2.savefig(str(sys.argv)[2:-15] + 'responce.png', dpi=100, fmt='png')
        self.ui.figure3.set_size_inches(8,2.7)
        self.ui.figure3.tight_layout()
        self.ui.figure3.subplots_adjust(left=0.166,right=0.936)
        self.ui.figure3.savefig(str(sys.argv)[2:-15] + 'redresponce.png', dpi=100, fmt='png')
        print('pictures save in :' + str(sys.argv)[2:-15])

    #функция для перерисовки графиков с осью x = time
    def replotterf1(self):
        replotter1(self.ui.spinBox.value())
        self.ui.canvas1.draw()
        replotter2(self.ui.spinBox.value())
        self.ui.canvas2.draw()
        replotter3()
        self.ui.canvas3.draw()
        self.savePictures()


    def makedial(self):  # функция для расчета по выбранному массиву
        global start, finish
        # аргументы для запуска функции raschet
        # доступ к файлами с помощью sys и lineEdit
        print(str(sys.argv))
        folder1 = str(sys.argv)[2:-15] + 'Files/' + self.ui.lineEdit.text()  # место файла сигнал
        folder2 = str(sys.argv)[2:-15] + 'Files/' + self.ui.lineEdit_2.text()  # место файла отклик
        # folder1 = r'C:\\Users\\groshkov\\Desktop\\work\\python\\programs\\ALP\\sd_copper_signal.csv'
        try:
            raschet(folder1, folder2, self.ui.label_6, self.ui.label_7)  # запуск функции raschet из файла alp_program.py
        # + формирование интервала отображения с помощью передачи self.ui.label_6
        except:
            print('Выберите файлы сигнала и отклика *csv')
            print('Error in raschet(folder1, folder2, self.ui.label_6, self.ui.label_7)')
        start = self.ui.spinBox_3.value()+self.ui.spinBox.value()  # начало
        finish = self.ui.spinBox_4.value()+self.ui.spinBox.value()  # конец

        #функция table для расчета значений обрезанного отклика
        # folderwrite = r'C:\Users\groshkov\Desktop\work\python\programs\ALP\table.txt'
        if start == finish:
            print('Input the interval start and end')
        else:
            try:
                table(start, finish)  # запуск функции table из файла alp_program.py
            except:
                print('ERROR in table(start,finish) :))')

    # функция сохранения таблицы через вызов save_table из alp_program.py
    def save(self):
        try:
            folderwrite = str(sys.argv)[2:-15] + 'table.txt'
            if self.ui.checkBox_1.checkState() == 2 and self.ui.checkBox_2.checkState() == 0:
                save_table(start, folderwrite, float(self.ui.lineEdit_3.text()), float(self.ui.lineEdit_4.text()),32)
            elif self.ui.checkBox_1.checkState() == 0 and self.ui.checkBox_2.checkState() == 2:
                save_table(start, folderwrite, float(self.ui.lineEdit_3.text()), float(self.ui.lineEdit_4.text()), 4)
            else:
                save_table(start, folderwrite, float(self.ui.lineEdit_3.text()), float(self.ui.lineEdit_4.text()), 1)
        except:
            print('Error in Save  :))')

    def makesnr(self):
        # аргументы для запуска функции snr и Fsnr
        # folderWmas = str(sys.argv)[2:-15] +'Wmas.txt'
        folderWmas = str(sys.argv)[2:str(sys.argv).rfind('/') + 1] + 'Wmas.txt'
        folderWf = str(sys.argv)[2:str(sys.argv).rfind('/') + 1] + 'Wf.txt'
        folderKa = str(sys.argv)[2:str(sys.argv).rfind('/') + 1] + 'Ka.txt'
        folderCkabs = str(sys.argv)[2:str(sys.argv).rfind('/') + 1] + 'Ckabs.txt'
        # try:
        Aconst = float(self.ui.lineEdit_3.text())
        Wconst = float(self.ui.lineEdit_4.text())
            #проверка на чекбоксы
        if self.ui.checkBox_1.checkState()==2 and self.ui.checkBox_2.checkState()==0:  #чекбокс=32
            self.ui.lineEdit_5.setText(str('%0.8e' % snr(Aconst, Wconst, razrqd=32)))
        elif self.ui.checkBox_1.checkState()==0 and self.ui.checkBox_2.checkState()==2: #чекбокс=4
            self.ui.lineEdit_5.setText(str('%0.8e' % snr(Aconst, Wconst, razrqd=4)))
        else:  #без чекбоксов
            self.ui.lineEdit_5.setText(str('%0.8e' % snr(Aconst, Wconst, razrqd=1)))

        # self.ui.lineEdit_6.setText(str('%0.8e' %Fsnr(Aconst, folderWmas,folderWf, folderKa, folderCkabs,razrqd=1)))
        # except:
        # print('ERROR in makesnr :))')


# Запуск mainALP

folder = (str(sys.argv))  # определение пути для отображения файлов в списке
print('folder = sys.argv -->> ', folder)

# запуск отрисовки GUI
app = QtWidgets.QApplication(sys.argv)
myapp = mainALP()
myapp.show()
sys.exit(app.exec_())
