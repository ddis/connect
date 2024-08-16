import pywinauto
import time
import json

target_settings = {}
cps = None
cps_w = None
cps_controls = None


def get_control(pos, direction=1, title=None, auto_id=None, control_type=None, is_visible=True):
    global cps_controls
    last_j = len(cps_controls)
    if direction < 0:
        last_j = 0
    j = pos
    while not j == last_j:
        #print(cps_controls[j].window_text() + ' --- ' + cps_controls[j].automation_id() + ' --- ' + cps_controls[j].friendly_class_name())
        if (title == None or cps_controls[j].window_text() == title) and (not auto_id or cps_controls[j].automation_id() == auto_id) and (not control_type or cps_controls[j].friendly_class_name() == control_type) and (is_visible == None or cps_controls[j].is_visible() == is_visible):
            print(cps_controls[j].window_text() + ' --- ' + cps_controls[j].automation_id() + ' --- ' + cps_controls[j].friendly_class_name() + ' --- ' + str(cps_controls[j].is_visible()))
            return j, cps_controls[j]
        j = j + direction
    return None,None


def adjust_pos_for_general_edit(pos):
    return pos + 2

def set_general_settings():
    global cps_controls
    pos, w = get_control(0,title='General Settings')
    if not w:
        get_control(0, auto_id='dtrTopCategories')[1].scroll('up', 'page')
        cps_controls = cps_w.descendants()
        pos, w = get_control(0,title='General')
        w.click_input()
        cps_controls = cps_w.descendants()
    pos, w = get_control(pos,title='General Settings')
    w.click_input()
    cps_controls = cps_w.descendants()

    pos, w = get_control(0,title='Radio Alias')
    pos = adjust_pos_for_general_edit(pos)
    w = cps_controls[pos]
    w.type_keys('^a' + target_settings['RadioAlias'])

    pos, w = get_control(pos,title='Radio ID')
    pos = adjust_pos_for_general_edit(pos)
    w = cps_controls[pos]
    w.type_keys('^a' + str(target_settings['RadioID']))

def set_security():
    global cps_controls
    pos, w = get_control(0,title='Security')
    if not w:
        pos, w = get_control(0,title='General')
        w.click_input()
        cps_controls = cps_w.descendants()
    pos, w = get_control(pos,title='Security')
    w.click_input()
    cps_controls = cps_w.descendants()

    pos, w = get_control(0,title='Symmetric')
    pos, w = get_control(pos+1,title='Symmetric')
    pos, w = get_control(pos+1,title='Symmetric')
    pos, btn_add = get_control(pos+1,auto_id='btnAdd')
    pos, ui_keys_list = get_control(pos,title='Records', control_type='ListView')
    #print(len(ui_keys_list.get_items()))
    #print(ui_keys_list)
    #target_keys = target_settings['SymmetricKeys']
    target_keys_count = len(target_settings['Channels'])
    while target_keys_count > len(ui_keys_list.get_items()) - 1:
        btn_add.click()
    for k,channel in enumerate(target_settings['Channels'].values()):
        item = ui_keys_list.get_item(k).descendants()
        ui_key_id = item[8]
        ui_key_name = item[11]
        ui_key_value = item[14]
        key_id = str(channel['key_id'])
        ui_key_id.type_keys('{VK_F2}' + key_id + '{ENTER}')
        ui_key_name.type_keys('{VK_F2}SymmetricKey' + key_id + '{ENTER}')
        v = channel['key_value'].upper()
        print(v)
        ui_key_value.type_keys('{VK_F2}' + str(v) + '{ENTER}')
    while target_keys_count < len(ui_keys_list.get_items()) - 1:
        item = ui_keys_list.get_item(target_keys_count)
        #print(item)
        item.select()
        item.type_keys('{VK_DELETE}{ENTER}')

def set_caller_ids_and_groups():
    global cps_controls    

    # Contacts
    
    #pos, w = get_control(0, control_type='TreeItem')
    #while w:
    #    print(pos)
    #    w.draw_outline()
    #    time.sleep(1)
    #    pos, w = get_control(pos+1, control_type='TreeItem')
    #exit()
    
    pos_grdContacts, contacts_list = get_control(0, auto_id='grdContacts')
    w_tree_item_contacts = None
    if not contacts_list or not contacts_list.is_visible():
        pos, w_top_contacts = get_control(0, auto_id='Contacts', control_type='TreeItem')
        pos, w_tree_item_contacts = get_control(pos+1, auto_id='Contacts', control_type='TreeItem')
        if not w_tree_item_contacts or not w_tree_item_contacts.is_visible():
            w_top_contacts.click_input()
            cps_controls = cps_w.descendants()
        pos, w_top_contacts = get_control(0, auto_id='Contacts', control_type='TreeItem')
        pos, w_tree_item_contacts = get_control(pos+1, auto_id='Contacts', control_type='TreeItem')
        w_tree_item_contacts.click_input()
        cps_controls = cps_w.descendants()
        pos_grdContacts, contacts_list = get_control(0, auto_id='grdContacts')
        
    print('grdContacts found: ' + str(bool(contacts_list)) + '; has ' + str(len(contacts_list.get_items())) + ' items')
    pos, btn_edit = get_control(pos_grdContacts, direction=-1, auto_id='btnEdit')
    pos, btn_add = get_control(pos_grdContacts, direction=-1, auto_id='btnAdd')
    pos, btn_del = get_control(pos_grdContacts, direction=-1, auto_id='btnDelete')
    #if len(contacts_list.get_items()) > 1:
    #    print('grdContacts removing items')
    #    
    #    #pos, btn_aux = get_control(pos_grdContacts, direction=-1, auto_id='btnAdditional')
    #    #btn_aux.click()
    #    #time.sleep(0.5)
    #    #print(pywinauto.Desktop(backend='uia')['Menu'].wrapper_object())
    #    #return
    #    #pos, menu = get_control(0, control_type='MenuItem')
    #    #while menu: pos, menu = get_control(pos+1, control_type='MenuItem')
    #    #print(menu)
    #    #return
    #    #for i in range(0,5): pywinauto.keyboard.send_keys('{DOWN}')
    #    #pywinauto.keyboard.send_keys('{ENTER}{ENTER}')
    #    
    #    #pos, w = get_control(0, title='Delete All')
    #    #print(cps_w.Menu)
    #    #return
    #    while len(contacts_list.get_items()) > 1:
    #        pos, w = get_control(0, title='Contact Name', control_type='DataItem')
    #        print(w.rectangle())
    #        #w.draw_outline()
    #        #time.sleep(1)
    #        w.click_input()
    #        #w.click_input()
    #        if btn_del.is_enabled():
    #            btn_del.click()
    #        w.type_keys('{ENTER}')
    #        cps_controls = cps_w.descendants()
    
    target_channels = target_settings['Channels']
    #target_keys_count = len(target_keys)
    #pos, w = get_control(0, title='Contact Name', control_type='DataItem')
    #if w:
    #    w.click_input()
    for i,channel in enumerate(target_channels.values()):
        #if i == 0 and btn_edit.is_enabled():
        #    pos, w = get_control(0, title='Contact Name', control_type='DataItem')
        #    btn_edit.click()
        #else:
        #    btn_add.click()
        
        btn_add.click()
        cps_controls = cps_w.descendants()
        pos,w = get_control(0, title='Contact', control_type='Static')
        pos,w = get_control(0, title='Digital', control_type='Static')
        pos,w = get_control(pos, direction=-1, auto_id='btnAdd')
        w.click_input()
        pywinauto.keyboard.send_keys('{ENTER}')        
        cps_controls = cps_w.descendants()
        
        pos,w = get_control(0, title='Contact', control_type='Static')
        pos,w = get_control(pos+1, control_type='Edit')
        w.set_text(channel['net_name'])
        pos,w = get_control(pos+1, title='Call ID', control_type='Static')
        pos,w = get_control(pos+1, control_type='Edit')
        w.set_text(channel['caller_id'])
        #return

    
    # Groups
    
    pos, w_tree_item_digital_groups = get_control(0, title='Digital RX Group List')
    if not w_tree_item_digital_groups:
        pos, w = get_control(0, title='RX Group Lists')
        w.click_input()
        cps_controls = cps_w.descendants()
        pos, w_tree_item_digital_groups = get_control(pos+1, title='Digital RX Group List')
    w_tree_item_digital_groups.click_input()
    cps_controls = cps_w.descendants()
    
    pos, w = get_control(0, title='Digital Name')
    _,btn_add = get_control(pos, direction=-1, auto_id='btnAdd')
    _,btn_del = get_control(pos, direction=-1, auto_id='btnDelete')
    _, w_dataitem = get_control(pos+1, title='', control_type='DataItem')
    while w_dataitem:
        w_dataitem.click_input()
        if not btn_del.is_enabled():
            break
        btn_del.click()
        time.sleep(0.5)
        pywinauto.keyboard.send_keys('{ENTER}')
        time.sleep(0.5)
        cps_controls = cps_w.descendants()
        _, w_dataitem = get_control(pos+1, title='', control_type='DataItem')
        #time.sleep(0.5)
        #w.draw_outline()
    if w_dataitem:
        _,btn_edit = get_control(pos, direction=-1, auto_id='btnEdit')
        btn_edit.click()
    else:
        btn_add.click()
    target_channels = target_settings['Channels']
    for channel in target_channels.values():
        if not w_dataitem:
            btn_add.click()
        cps_controls = cps_w.descendants()
        pos, w = get_control(0, title='Digital Name')
        pos, w = get_control(pos+1, control_type='Edit')
        w.set_text('Гр ' + channel['net_name'])
        _, w = get_control(pos+1, auto_id='lbSelectedItems')
        w.type_keys('^a')
        _, w = get_control(pos+1, auto_id='btnRemove')
        # if there are items
        if w.is_enabled():
            w.click()
        _, w = get_control(pos+1, auto_id='lbItems')
        w.item(channel['net_name']).select()
        #w.type_keys('^a')
        _, w = get_control(pos+1, auto_id='btnAdd')
        w.click()
        w_dataitem = None

    pass

def set_channels():
    global cps_controls    

    pos_zone_name, w = get_control(0, title='Zone Name')
    #pos, w = get_control(pos_zone_name, control_type='Edit')
    pos, w_zona_main_tree = get_control(0, title='ЗонаОсн')
    if not w or not w.is_visible():
        if not w_zona_main_tree:
            get_control(0, auto_id='dtrTopCategories')[1].scroll('down', 'page')
            cps_controls = cps_w.descendants()
            #time.sleep(0.5)
            pos, w_zona_tree = get_control(0, title='Zone')
            if not w_zona_tree:
                pos, w_zona_channel = get_control(0, title='Zone/Channel Assignment')
                w_zona_channel.click_input()
                cps_controls = cps_w.descendants()
            pos, w_zona_tree = get_control(0, title='Zone')
            w_zona_tree.click_input()
            cps_controls = cps_w.descendants()
            get_control(0, auto_id='dtrTopCategories')[1].scroll('down', 'page')
            cps_controls = cps_w.descendants()
            time.sleep(1)
        pos, w_zona_main_tree = get_control(0, title='ЗонаОсн')
        w_zona_main_tree.click_input()
        cps_controls = cps_w.descendants()
        time.sleep(1)
    pos_zone_name, w = get_control(0, title='Zone Name')
    
    pos, btn_edit = get_control(pos_zone_name, auto_id='btnEdit')
    pos, btn_add = get_control(pos_zone_name, auto_id='btnAdd')
    pos, btn_del = get_control(pos_zone_name, auto_id='btnDelete')
    pos, channels_list = get_control(pos_zone_name, title='Records', control_type='ListView')
    w_stub_item = None
    if len(channels_list.items()) > 1:
        w_stub_item = channels_list.item(1)
        w_stub_item.select()
        btn_edit.click()
    else:
        btn_add.click()
    for i,channel in enumerate(target_settings['Channels'].values()):
        if not w_stub_item:
            pos, w_zona_main_tree = get_control(0, title='ЗонаОсн')
            w_zona_main_tree.click_input()
            cps_controls = cps_w.descendants()
            time.sleep(1)
            pos_zone_name, w = get_control(0, title='Zone Name')            
            pos, btn_add = get_control(pos_zone_name, auto_id='btnAdd')
            btn_add.click()            
            
            time.sleep(0.5)
            pywinauto.keyboard.send_keys('Digital{ENTER}')
            cps_controls = cps_w.descendants()
            pos, channels_list = get_control(pos_zone_name, title='Records', control_type='ListView')
            channels_list.item(-1).select()
            pos, btn_edit = get_control(pos_zone_name, auto_id='btnEdit')
            btn_edit.click()
            
        cps_controls = cps_w.descendants()
        time.sleep(2)
        
        pos,w = get_control(0, title='Channel Name')
        pos,w = get_control(pos+1, control_type='Edit')
        w.set_text(channel['net_name'])
        
        pos,w = get_control(pos+1, title='Scan/Roam List')
        pos,w = get_control(pos+1, control_type='ComboBox')
        w.select('None')
        
        pos,w = get_control(pos+1, title='Color Code')
        pos,w = get_control(pos+1, control_type='Edit')
        w.type_keys('^a' + str(channel['ColorCode']))
        
        pos,w = get_control(pos+1, title='Symmetric Alias')
        pos,w = get_control(pos+1, control_type='ComboBox')
        w.select('SymmetricKey' + str(channel['key_id']))
        
        pos,w = get_control(pos+1, title='RX')
        #for i in range(0,20): pos,w = get_control(pos+1)
        #return
        pos,w = get_control(pos+1, auto_id='PART_InputTextBox')
        w.type_keys('^a' + str(channel['Rx']))
        
        pos,w = get_control(pos+1, title='Group List')
        #for i in range(0,20): pos,w = get_control(pos+1)
        #return
        pos,w = get_control(pos+1, control_type='ComboBox')
        #w.type_keys('DigitalRXGroupList/Гр ' + list(target_settings['Contacts'].values())[i])
        print('DigitalRXGroupList/Гр ' + channel['net_name'])
        w.select('DigitalRXGroupList/Гр ' + channel['net_name'])
        
        pos,w = get_control(pos+1, title='TX')
        #for i in range(0,20): pos,w = get_control(pos+1)
        #return
        pos,w = get_control(pos+1, auto_id='PART_InputTextBox')
        w.type_keys('^a' + str(channel['Tx']))
        
        pos,w = get_control(pos+1, title='Contact Name')
        #for i in range(0,20): pos,w = get_control(pos+1)
        #return
        pos,w = get_control(pos+1, control_type='ComboBox')
        w.select(channel['net_name'])
        
        w_stub_item = None
    pass


def load_controls():
    global target_settings, cps, cps_w, cps_controls
    d = pywinauto.Desktop(backend='uia')
    cps = d.window(title_re='.*MOTOTRBO *.')
    
    cps['Password'].wait('exists', timeout=100).set_focus()
    cps['Password'].type_keys('1111{ENTER}{ENTER}')
    cps['General Settings'].wait('exists', timeout=100).set_focus()
    
    cps_w = cps.wrapper_object()
    cps_controls = cps_w.descendants()
    #exit()

def run(config_name):
    global target_settings, cps, cps_w, cps_controls
    
    target_settings = json.loads(open(config_name, encoding='utf-8').read())
    load_controls()
    
    #pos,w = get_control(0, title='Set Categories')
    #pos,w = get_control(0, auto_id='dtrTopCategories')
    #for i in range(0,20): pos,w = get_control(pos+1)
    #w.scroll('down', 'page')
    #print(w)
    #exit()
    
    set_general_settings()
    set_security()
    set_caller_ids_and_groups()
    set_channels()
    
    # save and close, wait for termination
    print('Saving firmware...')
    cps.type_keys('^S')
    print('Closing CPS window...')
    cps['Close'].click()
    #cps.type_keys('%{F4}')
    #cps.type_keys('%{F4}{ENTER}')
    print('Waiting for window to be closed...')
    cps.wait_not('exists', timeout=100)
    #time.sleep(3)
    print('CPS window closed')

#run('бат1 мбр1/0_cps_settings.json')

#target_settings = json.loads(open('cps_settings.json', encoding='utf-8').read())
#load_controls()
#set_caller_ids_and_groups()
#set_channels()
