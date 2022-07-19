import sys
import traceback

from PyQt5 import QtWidgets

from file_operation import LoadingPanel
app = QtWidgets.QApplication(sys.argv)

if __name__ == "__main__":
    try:
        ex = LoadingPanel()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        traceback.print_exc()
        sys.exit(-1)
