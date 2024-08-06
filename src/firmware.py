import json
import os
import shutil
import sys
from PyQt6.QtWidgets import QMessageBox
from src.utils import run as cpsRun
from src.context import UI,Context
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QProgressBar, QLabel, QSizePolicy

from src.ui import update_view

def generate_firmware():
    if not os.path.isfile('C:/Program Files (x86)/Motorola/MOTOTRBO CPS 2.0/CPSShell.exe'):
        QMessageBox.warning(UI.main_wnd, 'Увага', 'Не можу знайти програму MOTOTRBO CPS 2.0')
        return
    QMessageBox.warning(UI.main_wnd, 'Увага', 'Наразі робота нестабільна, залежить від розміру екрану. \n'
        'Якщо вікно програми MOTOTRBO CPS 2.0 не розгорнуте на весь екран, запустіть її вручну, розгорніть вікно і закрийте. \n'
        'Під час створення прошивки не можна чіпати клавіатуру або мишу, блокувати екран.')
    progress_bar = QProgressBar()
    progress_label = QLabel()
    progress_layout = UI.main_wnd.statusBar()
    progress_layout.addWidget(progress_bar, 1)
    progress_layout.addPermanentWidget(progress_label, 2)
    #progress_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    #main_wnd.statusBar().setSizeGripEnabled(False)
    progress_bar.setRange(0, len(Context.devs_config_db))
    #print('range - ' + str(len(devs_config_db)))
    for dev_i,dev in enumerate(Context.devs_config_db.values()):
        progress_label.setText('Створюється прошивка для ' + dev['dev_name'] + '...')
        progress_bar.setValue(dev_i)
        QApplication.processEvents() 
        #print('setting ' + str(dev_i))
        if dev['firmware_fname']: 
            #time.sleep(1)
            #progress_bar.setValue(dev_i+1)
            #progress_bar.repaint()
            continue
        dev_config = {}
        dev_config['RadioAlias'] = dev['dev_name']
        dev_config['RadioID'] = dev_i+1
        # should be set from nets_config_db
        dev_config['Channels'] = {}
        for net_name in dev['nets_names']:
            dev_config['Channels'][net_name] = Context.nets_config_db[net_name]
        #dev_config['SymmetricKeys'] = {}
        #for net in nets_config_db.values():
        #    dev_config['SymmetricKeys'][net['key_id']] = net['key_value']
        # save json config for ui script
        dev_config_fname = Context.active_unit + '/' + str(dev_i) + '_cps_settings.json'
        open(dev_config_fname, 'w', encoding='utf-8').write(json.dumps(dev_config, ensure_ascii=False))
        firmware_fname = ''
        if dev['model_name'] == 'DP 4800' or dev['model_name'] == 'DP 4400':
            if dev['model_name'] == 'DP 4800':
                firmware_fname = Context.active_unit + '/' + str(dev_i) + '_DP4800.ctb2'
                firmware_template_fname = os.path.join('src/mototrbo/DP4800_clean.ctb2')
                shutil.copyfile(firmware_template_fname, firmware_fname)
            elif dev['model_name'] == 'DP 4400':
                firmware_fname = Context.active_unit + '/' + str(dev_i) + '_DP4400.ctb2'
                firmware_template_fname = os.path.join('src/mototrbo/DP4400_clean.ctb2')
                shutil.copyfile(firmware_template_fname, firmware_fname)
            cmd = 'start "C:/Program Files (x86)/Motorola/MOTOTRBO CPS 2.0/CPSShell.exe" "' + firmware_fname + '"'
            print(cmd)
            os.system(cmd)
            cpsRun(dev_config_fname)
            print('Saved firmware ' + firmware_fname)
            dev['firmware_fname'] = firmware_fname
            update_view()
            #return
        #progress_bar.setValue(dev_i+1)
        #progress_bar.repaint()
    progress_layout.removeWidget(progress_bar)
    progress_layout.removeWidget(progress_label)