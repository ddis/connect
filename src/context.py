import json

class Context ():
    active_unit = ''
    org_db = {}
    org_paths_list = []
    nets_design_db = {}
    nets_config_db = {}
    devs_config_db = {}
    widgets_db = {}
    
class UI ():
    qapp = object()
    main_wnd = object()
    ui = object()

class Globals():
    unitName = "brigada"
    organizational_design = json.loads(open('src/organizational_design.json', encoding='utf-8').read())