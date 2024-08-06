import os

from src.context import UI, Globals, Context
from PyQt6.QtWidgets import QMessageBox
from src.helper import collect_tree_keys
from src.ui import update_view

def add_new_unit():
    if os.path.isdir(Globals.unitName):
        QMessageBox.warning(UI.main_wnd, 'Увага', 'Наразі можливо створити тільки одну частину')
        return
    all_keys = {}
    collect_tree_keys(Globals.organizational_design, all_keys)
    for u in all_keys.keys():
        Context.org_db[u] = {}
        Context.org_db[u]['user_name'] = u
        Context.org_db[u]['org_path'] = '/'.join(all_keys[u]['units'])
    try:
        os.mkdir(Globals.unitName)
    except:
        pass
    update_view()