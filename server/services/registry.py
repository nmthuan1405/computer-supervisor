import winreg as reg
from tempfile import NamedTemporaryFile
import subprocess
import os

def getHKEY(name):
    if name == "HKEY_CLASSES_ROOT":
        return reg.HKEY_CLASSES_ROOT
    elif name == "HKEY_CURRENT_USER":
        return reg.HKEY_CURRENT_USER
    elif name == "HKEY_LOCAL_MACHINE":
        return reg.HKEY_LOCAL_MACHINE
    elif name == "HKEY_USERS":
        return reg.HKEY_USERS
    elif name == 'HKEY_PERFORMANCE_DATA':
        return reg.HKEY_PERFORMANCE_DATA
    elif name == 'HKEY_CURRENT_CONFIG':
        return reg.HKEY_CURRENT_CONFIG
    elif name == 'HKEY_DYN_DATA':
        return reg.HKEY_DYN_DATA

def getType(type):
    if type == 'String':
        return reg.REG_SZ
    elif type == 'Binary':
        return reg.REG_BINARY
    elif type == 'DWORD':
        return reg.REG_DWORD
    elif type == 'QWORD':
        return reg.REG_QWORD
    elif type == 'Multi-String':
        return reg.REG_MULTI_SZ
    elif type == 'Expandable String':
        return reg.REG_EXPAND_SZ 

def returnType(type):
    if type == reg.REG_SZ:
        return 'String'
    elif type == reg.REG_BINARY:
        return 'Binary'
    elif type == reg.REG_DWORD:
        return 'DWORD'
    elif type == reg.REG_QWORD:
        return 'QWORD'
    elif type == reg.REG_MULTI_SZ:
        return 'Multi-String'
    elif type == reg.REG_EXPAND_SZ:
        return 'Expandable String' 

def merge_reg_file(file_data):
    try:
        f = NamedTemporaryFile(mode = 'w', encoding = 'utf-16', delete = False)
        f.write(file_data)
        f.close()

        res = subprocess.run(f'reg import \"{f.name}\"', capture_output = True)
        if res.stderr.decode().rstrip().find('ERROR') != -1:
            raise Exception
    except:
        state = False
    else:
        state = True
    finally:
        os.remove(f.name)
        return state

def query_value(path, value):
    try:
        hkey, key = path.split('\\', 1)
        value, type  = reg.QueryValueEx(reg.OpenKeyEx(getHKEY(hkey), key, 0, reg.KEY_QUERY_VALUE), value)

        return value, returnType(type)
    except:
        return None, None

def set_value(path, value, type, data):
    try:
        hkey, key = path.split('\\', 1)
        reg.SetValueEx(reg.OpenKeyEx(getHKEY(hkey), key, 0, reg.KEY_SET_VALUE), value, 0, getType(type), data)

        return True
    except:
        return False

def delete_value(path, value):
    try:
        hkey, key = path.split('\\', 1)
        reg.DeleteValue(reg.OpenKeyEx(getHKEY(hkey), key, 0, reg.KEY_SET_VALUE), value)

        return True
    except:
        return False

def create_key(path):
    try:
        hkey, key = path.split('\\', 1)
        reg.CreateKeyEx(getHKEY(hkey), key, 0, reg.KEY_CREATE_SUB_KEY)

        return True
    except:
        return False

def delete_key(path):
    try:
        hkey, key = path.split('\\', 1)
        reg.DeleteKeyEx(getHKEY(hkey), key)

        return True
    except:
        return False
