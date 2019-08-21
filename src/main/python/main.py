import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from service import hello_mainWindow
from login import Ui_MainWindow


class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        MainWindow = QMainWindow()
        ui = Ui_MainWindow(self)
        self.ui_hello = hello_mainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()

        return self.app.exec_()                 # 3. End run() with this line
    
    @cached_property
    def icon_logo(self):
        return QIcon(self.get_resource('logo.png'))

    @cached_property
    def img_logbg(self):
        return QImage(self.get_resource('background.jpg'))

    
if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)