from datetime import datetime
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox
from matplotlib import dates
from parser_rate import ParserRate


# class window
class MyWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        # interface loading and window setting
        uic.loadUi('window.ui', self)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

        try:
            # connecting with data server
            self.data = ParserRate('https://charts.finance.ua/ua/currency/data-archive?for=order&source=1&indicator=usd')
        except ConnectionError:
            # if fail to connect to the server, we terminate the program
            QMessageBox.critical(None, 'Помилка', 'Не вдалось під\'єднатись до сервера', QMessageBox.Cancel)
            raise SystemExit

        #  setting for window elements
        date_first, date_last, date_next_last, date_next_first = self.data.return_first_end_data()

        self.data1_description.setText(datetime.strftime(date_first, '%d.%m.%Y'))
        self.data2_description.setText(datetime.strftime(date_last, '%d.%m.%Y'))
        self.dateEdit1.setDate(date_first)
        self.dateEdit2.setDate(date_last)
        self.dateEdit1.setCalendarPopup(True)
        self.dateEdit2.setCalendarPopup(True)
        self.dateEdit1.setDateRange(date_first, date_next_last)
        self.dateEdit2.setDateRange(date_next_first, date_last)

        # connect with slot for build graphic
        self.buttonStart.clicked.connect(self.view_graphics)

    # slot for build graphic
    @pyqtSlot()
    def view_graphics(self):
        try:
            # get data
            result = self.data.return_data(self.dateEdit1.date().toString('dd.MM.yyyy'),
                                           self.dateEdit2.date().toString('dd.MM.yyyy'))

            # build graphic
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.set_title('Курс долара', fontsize=20, color='b')
            self.MplWidget.canvas.axes.set_ylabel('У гривні', fontsize=20, color='b')
            self.MplWidget.canvas.axes.set_xlabel('Дата', fontsize=20, color='b')
            self.MplWidget.canvas.axes.plot([datetime.strptime(x[0], '%m/%d/%Y') for x in result],
                                            [float(y[2]) for y in result])
            self.MplWidget.canvas.axes.xaxis.set_major_formatter(dates.DateFormatter('%d.%m.%y'))
            self.MplWidget.canvas.axes.grid(color="grey", which="major", axis='x', linestyle='-', linewidth=0.5)
            self.MplWidget.canvas.axes.grid(color="grey", which="major", axis='y', linestyle='-', linewidth=0.5)
            self.MplWidget.canvas.draw()
        except ValueError:
            # if date format is wrong showing message about error
            QMessageBox.warning(None, 'Помилка', 'Не вірний діапазон дати', QMessageBox.Ok)
