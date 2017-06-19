from PyQt4 import QtGui
import sys
import os

import card_client_handler as cch

def main():
    app = QtGui.QApplication(sys.argv)
    form = cch.ClientCard()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()