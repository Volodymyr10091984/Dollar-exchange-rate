import sys
from PyQt5.QtWidgets import QApplication
from my_window import MyWindow

# create window
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
