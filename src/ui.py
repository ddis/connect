from functools import reduce
import json
import os
from src.context import UI, Context, Globals


def update_view():
    print('update_view')
    users_total = len(Context.org_db)
    #radio_users = reduce(lambda ur,u: ur + 1 if u in nets_design_db.keys() and nets_design_db[u] else ur, org_db.keys(), 0)
    radio_users = len(Context.nets_design_db)
    nets_total = len(Context.nets_config_db)
    nets_configured = 0
    for net_config in Context.nets_config_db.values():
        # if there are empty values, skip it
        #if not net_config['Rx']: continue
        #if not net_config['Tx']: continue
        if False in list(map(lambda v: bool(v), net_config.values())): continue
        nets_configured = nets_configured + 1
    devs_total = len(Context.devs_config_db)
    devs_DP_4400 = reduce(lambda s,d: s + 1 if d['model_name'] == 'DP 4400' else s, Context.devs_config_db.values(), 0)
    devs_DP_4400_configured = reduce(lambda s,d: s + 1 if d['model_name'] == 'DP 4400' and d['firmware_fname'] else s, Context.devs_config_db.values(), 0)
    devs_DP_4800 = reduce(lambda s,d: s + 1 if d['model_name'] == 'DP 4800' else s, Context.devs_config_db.values(), 0)
    devs_DP_4800_configured = reduce(lambda s,d: s + 1 if d['model_name'] == 'DP 4800' and d['firmware_fname'] else s, Context.devs_config_db.values(), 0)
    devs_DM_4600 = reduce(lambda s,d: s + 1 if d['model_name'] == 'DM 4600' else s, Context.devs_config_db.values(), 0)
    devs_DM_4600_configured = reduce(lambda s,d: s + 1 if d['model_name'] == 'DM 4600' and d['firmware_fname'] else s, Context.devs_config_db.values(), 0)
    devs_configured = reduce(lambda s,d: s + 1 if d['firmware_fname'] else s, Context.devs_config_db.values(), 0)
    
    UI.ui.users_total.setText(str(users_total))
    UI.ui.radio_users.setText(str(radio_users))
    UI.ui.nets_total.setText(str(nets_total))
    UI.ui.nets_configured.setText(str(nets_configured))
    UI.ui.devs_total_configured.setText(str(devs_total) + ' / ' + str(devs_configured))
    UI.ui.devs_4400.setText(str(devs_DP_4400) + ' / ' + str(devs_DP_4400_configured))
    UI.ui.devs_4800.setText(str(devs_DP_4800) + ' / ' + str(devs_DP_4800_configured))
    UI.ui.devs_4600.setText(str(devs_DM_4600) + ' / ' + str(devs_DM_4600_configured))
    # folders names
    units = reduce(lambda d,f: d+[f] if os.path.isdir(f) and f.startswith(Globals.unitName) else d, os.listdir(), [])
    UI.ui.units_combo.blockSignals(True)
    prev_cur = UI.ui.units_combo.currentText()
    UI.ui.units_combo.clear()
    UI.ui.units_combo.addItems(units)
    #ui.units_combo.adjustSize()
    if not prev_cur:
        UI.ui.units_combo.setCurrentText(prev_cur)
    UI.ui.units_combo.blockSignals(False)
    # Select current unit (now we have only one unit)
    if not prev_cur == UI.ui.units_combo.currentText():
        activate_unit(UI.ui.units_combo.currentText())
    
    if Context.active_unit:
        print('saving to ' + Context.active_unit)
        open(Context.active_unit + '/org_db.json', 'w', encoding='utf-8').write(json.dumps(Context.org_db, ensure_ascii=False))
        open(Context.active_unit + '/org_paths_list.json', 'w', encoding='utf-8').write(json.dumps(Context.org_paths_list, ensure_ascii=False))
        open(Context.active_unit + '/nets_design_db.json', 'w', encoding='utf-8').write(json.dumps(Context.nets_design_db, ensure_ascii=False))
        open(Context.active_unit + '/nets_config_db.json', 'w', encoding='utf-8').write(json.dumps(Context.nets_config_db, ensure_ascii=False))
        open(Context.active_unit + '/devs_config_db.json', 'w', encoding='utf-8').write(json.dumps(Context.devs_config_db, ensure_ascii=False))
        open(Context.active_unit + '/widgets_db.json', 'w', encoding='utf-8').write(json.dumps(Context.widgets_db, ensure_ascii=False))

    UI.main_wnd.adjustSize()
    pass

def activate_unit(unit_name):
    if Context.active_unit == unit_name:
        return
    print('activate_unit: ' + unit_name)
    Context.active_unit = unit_name
    try:
        print('reading from ' + Context.active_unit)
        Context.org_db = json.loads(open(Context.active_unit + '/org_db.json', encoding='utf-8').read())
        Context.org_paths_list = json.loads(open(Context.active_unit + '/org_paths_list.json', encoding='utf-8').read())
        Context.nets_design_db = json.loads(open(Context.active_unit + '/nets_design_db.json', encoding='utf-8').read())
        Context.nets_config_db = json.loads(open(Context.active_unit + '/nets_config_db.json', encoding='utf-8').read())
        Context.devs_config_db = json.loads(open(Context.active_unit + '/devs_config_db.json', encoding='utf-8').read())
        Context.widgets_db = json.loads(open(Context.active_unit + '/widgets_db.json', encoding='utf-8').read())
    except:
        print('not read')
    update_view()