from PyQt6.QtWidgets import QApplication, QMainWindow
from src.diagram import generate_diagram
from src.firmware import generate_firmware
from main_window import Ui_MainWindow
from PyQt6.QtGui import QGuiApplication
from src.context import UI
from src.create_new import add_new_unit
from src.network import configure_nets, setup_nets
from src.ui import activate_unit, update_view

def show_main_window(ui, main_wnd, qapp):
    ui.setupUi(main_wnd)
    # Read actual data from unit source (like brigada)
    ui.units_combo.currentTextChanged.connect(activate_unit)
    # Create new unit
    ui.unit_create.clicked.connect(add_new_unit)
    # Functioanlity for working with radio network
    ui.channels_create.clicked.connect(setup_nets)
    ui.gen_diagram.clicked.connect(generate_diagram)
    #Generate or change config for network setting (channels and keys)
    ui.channels_setup.clicked.connect(configure_nets)
    ui.firmware_create.clicked.connect(generate_firmware)
    # center, show and update main window
    main_wnd.setWindowTitle('ZSUConnect')
    screen_center = QGuiApplication.primaryScreen().availableGeometry().center()
    main_wnd.move(screen_center - main_wnd.rect().center())
    update_view()
    main_wnd.show()
    qapp.exec()
    pass

UI.qapp = QApplication([])
UI.main_wnd = QMainWindow()
UI.ui = Ui_MainWindow() 

show_main_window(ui=UI.ui, main_wnd=UI.main_wnd, qapp=UI.qapp)