# coding:utf-8
from __future__ import print_function
from __future__ import absolute_import

import os,sys,re,traceback
if sys.version[0]=='2':
    import  _winreg as winreg
else:
    import winreg

class CustomRegistryKey:
    def __init__(self, hkey, path,reserved=0,access=winreg.KEY_READ):
        self.hkey = hkey
        self.path = path
        self.reg_key = None
        self.reserved=reserved
        self.access=access
        self.open()


    def open(self,):
        # winreg.QueryValueEx(key, 'MyApp'): 
        try: 
            self.reg_key = winreg.OpenKey(self.hkey, self.path,
                                    self.reserved, self.access)
            if  self.reg_key:
                return self.reg_key
        except:
            pass
        
    def close(self):
        if self.reg_key:
            winreg.CloseKey(self.reg_key)
            self.reg_key = None

    def get_value(self, value_name):
        if self.reg_key:
            try:
                value, value_type = winreg.QueryValueEx(self.reg_key, value_name)
                return value, value_type
            except:
                pass

    def enum_keys(self, index):
        if self.reg_key:
            key_name = winreg.EnumKey(self.reg_key, index)
            return key_name

    def serialize(self):
        if self.reg_key:
            return self.hkey, self.path

    @classmethod
    def deserialize(cls, data):
        hkey, path = data
        instance = cls(hkey, path)
        instance.open()
        return instance

    def getallSubitem(self):
        subItems=[]
        try:
            i = 0
            while True:
                try:
                    if not self.reg_key:
                        break
                    sub_key_name =  self.enum_keys(i)
                    subItems.append(sub_key_name)
                    i += 1
                except WindowsError:
                    break
        except:
            print (traceback.format_exc())
        return subItems