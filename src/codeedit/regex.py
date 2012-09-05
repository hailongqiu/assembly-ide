#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ini import Config

SYMBOL_TABLE_KEYWORD_TYPE   = 0 # 关键字
SYMBOL_TABLE_FUNCTION_TYPE  = 1 # 函数名
SYMBOL_TABLE_CLASS_TYPE     = 2 # 类名
SYMBOL_TABLE_STRING_TYPE    = 3 # 字符串
SYMBOL_TABLE_VARIABLE_TYPE  = 4 # 变量
SYMBOL_TABLE_SYMBOL_TYPE    = 5 # 符号
SYMBOL_TABLE_NUMBER_TYPE    = 6 # 数字
SYMBOL_TABLE_NOTES_TYPE     = 7 # 注释

class SymbolTable(object):
    def __init__(self):
        self.type = 0
        self.token = ""
        self.start_index = 0
        self.end_index   = 0
        self.row         = 0
        self.rgb         = "#000000"
        
class Scan(object):        
    def __init__(self, language_file, code_edit_file):
        self.symbol_table_list = []
        
        self.symbol = ["~", "`", "!", "@", "#", 
                       "$", "%", "^", "&", "*",                        
                       "(", ")", "+", "-", 
                       "=", "[", "{", "}", "]", 
                       "|", "\\", ":", ";", "'", 
                       "<", ",", ">", ".", "/", "?", '"', "_"]
        
        self.config = Config(language_file)
        self.code_edit_config = Config(code_edit_file)
        
        self.keyword = self.config.get_argvs("keyword").keys()
        '''Init value.'''
        self.index = 0
        self.start_index = 0
        self.end_index = 0
        self.next = 0
        self.pre  = 0
        self.row  = None
        
        self.text  = ""
        self.token = ""
        
        self.type           = SYMBOL_TABLE_VARIABLE_TYPE
        
        self.init_type_symbol()
        
    def init_type_symbol(self):        
        function_type_list = [""]
        class_type_list = [""]
        variable_type_list = [""]
        #################################
        config_function_type = self.code_edit_config.get("TEXT_BUFFER_VALUE", "function_type")
        if config_function_type:
            function_type_list = (config_function_type).split(",")
        config_class_type = self.code_edit_config.get("TEXT_BUFFER_VALUE", "class_type")    
        if config_class_type:
            class_type_list = config_class_type.split(",")
        config_variable_type = self.code_edit_config.get("TEXT_BUFFER_VALUE", "variable_type")
        if config_variable_type:
            variable_type_list = config_variable_type.split(",")
        #################################    
        self.function_type  = function_type_list
        self.class_type     = class_type_list
        self.variable_type  = variable_type_list
        
    def scan(self, text, row):    
        # Save text and row.
        self.text = text
        self.row  = row
        # Read token.
        self.temp_cn_next = 0
        if self.text:
            while True:
                ch = self.text[self.index]
                if ch not in [" "]:
                    if self.letter_bool(ch):
                        # print "======字母处理===="
                        self.letter_function()
                    elif self.number_bool(ch):
                        # print "======数字处理===="
                        self.number_function()
                    elif self.symbol_bool(ch):    
                        # print "======符号处理===="
                        self.symbol_function()  
                    else:    
                        # print "======中文处理===="
                        self.index += 1
                        self.temp_cn_next += 2
                else:    
                    self.index += 1
                
                if self.len_text() <= self.index:
                    break                
                
        ########################################
        ## return symbol table list.    
        return self.symbol_table_list
    
    def china_function(self):
        pass
    
    def china_save(self):    
        pass
    
    def letter_function(self):
        if self.keyword_bool(self.text[self.index]):
            self.keyword_function()
        else:    
            self.variable_function()
        
        self.index += 1
        
    def keyword_function(self):
        # print "关键字处理模块:"
        self.token = ""
        # save pre and next point.
        self.pre = self.index
        self.next = self.index
        # save start index.
        self.start_index = self.pre
        # get keyword list.
        # key_list = self.keyword_bool(self.text[self.index])
        ######################################        
        while True:
            try:
                keyword_ch = self.text[self.next]
            except:
                self.keyword_save()
                break                        
            
            if self.next > self.len_text() - 1:
                self.keyword_save()
                self.next += 1
                break
            
            if (not self.symbol_bool(keyword_ch)) and not keyword_ch in [" "]:
                self.token += keyword_ch
                self.next += 1
            else:
                self.keyword_save()
                break
            
        ######################################
        # print "======================"
        # print "token:", self.token
        # print "last next:", self.next
        # set index.            
        self.index     = self.next
        # save end index.
        self.end_index = self.next
            
    def keyword_save(self):    
        self.end_index = self.next
        symbol_table = SymbolTable()
        symbol_table.type  = SYMBOL_TABLE_NUMBER_TYPE
        symbol_table.token = self.token
        symbol_table.row   = self.row
        symbol_table.start_index = self.start_index + self.temp_cn_next
        symbol_table.end_index   = self.end_index - 1 + self.temp_cn_next
        config_rgb = self.config.get("keyword", self.token)
        
        if self.token in self.function_type:
            self.type = SYMBOL_TABLE_FUNCTION_TYPE
        elif self.token in self.class_type:    
            self.type = SYMBOL_TABLE_CLASS_TYPE
        elif self.token in self.variable_type:    
            self.type = SYMBOL_TABLE_VARIABLE_TYPE
            
            
        if not config_rgb:
            self.variable_save()
            # pass
        else:    
            symbol_table.rgb = config_rgb
            # print "================="
            # print "type:", symbol_table.type
            # print "token:", symbol_table.token
            # print "row:", symbol_table.row
            # print "start_index:", symbol_table.start_index
            # print "end_index:", symbol_table.end_index - 1
            # print "rgb:", symbol_table.rgb
            # print "==========="
            self.symbol_table_list.append(symbol_table)
        
    def variable_function(self):    
        # print "变量处理模块:"
        # clear token.
        self.token = ""
        # save pre and next point.
        self.pre = self.index
        self.next = self.index
        # save start index.
        self.start_index = self.pre
        
        #####################################################
        while True:
            try:
                variable_ch = self.text[self.next]
                if self.cn_bool(variable_ch):
                    self.temp_cn_next += 2
            except:    
                self.variable_save()
                break
            
            if self.next > self.len_text() - 1:
                self.variable_save()
                self.next += 1
                break
            
            if (not self.symbol_bool(variable_ch)) and not variable_ch in [" "]:
                self.token += variable_ch
                self.next += 1
            else:
                self.variable_save()
                break                       
        ##################################################    
        # print "======================"
        # print "token:", self.token
        # print "last next:", self.next
        # set index.            
        self.index     = self.next
        # save end index.
        self.end_index = self.next
                    
    def variable_save(self):
        self.end_index = self.next
        symbol_table = SymbolTable()        
        symbol_table.token = self.token
        symbol_table.row   = self.row
        symbol_table.start_index = self.start_index + self.temp_cn_next
        symbol_table.end_index   = self.end_index - 1 + self.temp_cn_next
                    
        # save color->rgb.
        if self.type ==   SYMBOL_TABLE_VARIABLE_TYPE:
            config_rgb = self.code_edit_config.get("TEXT_BUFFER_VALUE", "VARIABLE")
        elif self.type == SYMBOL_TABLE_FUNCTION_TYPE:    
            config_rgb = self.code_edit_config.get("TEXT_BUFFER_VALUE", "FUNCTION")
        elif self.type == SYMBOL_TABLE_CLASS_TYPE:
            config_rgb = self.code_edit_config.get("TEXT_BUFFER_VALUE", "CLASS")            
            
        self.type = SYMBOL_TABLE_VARIABLE_TYPE
        
        # save type.    
        symbol_table.type  = self.type
        
        if not config_rgb:
            config_rgb = "#000000"
            
        symbol_table.rgb = config_rgb
        
        # print "================="
        # print "type:", symbol_table.type
        # print "token:", symbol_table.token
        # print "row:", symbol_table.row
        # print "start_index:", symbol_table.start_index
        # print "end_index:", symbol_table.end_index - 1
        # print "rgb:", symbol_table.rgb
        # print "==========="
        self.symbol_table_list.append(symbol_table)
        
    def number_function(self):
        # print "数字处理模块:"
        # clear token.
        self.token = ""
        # save pre point.
        self.pre = self.index
        # save start index.
        self.start_index = self.pre
        # save next point.
        self.next = self.index
        
        # print "pre:", self.pre
        # print "next:", (self.next + self.index)
        # print "len:", self.len_text() - 1                
        ###################################            
        while True:
            try:
                number_ch = self.text[self.next]
            except:    
                break
            
            if self.next >= self.len_text()-1:                
                self.end_index = self.next
                if self.symbol_bool(number_ch):
                    self.end_index -= 1 
                    
                self.next += 1
                break
            
            if (not self.symbol_bool(number_ch)) and not number_ch in [" "]:
                self.token += number_ch
                self.next += 1
            else:
                self.end_index = self.next - 1                
                break
            
        ###################################
        # print "======================"   
        # print "token:", self.token
        # print "last next:", self.next            
        # set index.                        
        self.index     = self.next
        self.number_save()
        
    def number_save(self):            
        symbol_table = SymbolTable()
        symbol_table.type  = SYMBOL_TABLE_NUMBER_TYPE
        symbol_table.token = self.token
        symbol_table.row   = self.row
        symbol_table.start_index = self.start_index + self.temp_cn_next
        symbol_table.end_index   = self.end_index + self.temp_cn_next
        config_rgb = self.code_edit_config.get("TEXT_BUFFER_VALUE", "NUMBER")
        if not config_rgb:
            config_rgb = "#000000"
        symbol_table.rgb = config_rgb
        # print "================="
        # print "type:", symbol_table.type
        # print "token:", symbol_table.token
        # print "row:", symbol_table.row
        # print "start_index:", symbol_table.start_index
        # print "end_index:", symbol_table.end_index
        # print "rgb:", symbol_table.rgb
        # print "==========="
        self.symbol_table_list.append(symbol_table)

    def symbol_function(self):
        # print "符号处理模块:"
        # temp_list = list(self.config.get("keyword", "notes_symbol"))
        temp_list = list(self.code_edit_config.get("TEXT_BUFFER_VALUE", "notes_symbol"))
        
        if self.text[self.index] == '"':
            # print "字符串类型"
            self.string_function()            
        elif self.text[self.index] == temp_list[0]:
            # print "===注释处理..."      
            type_bool = False
            if len(self.text) >= len(temp_list):
                try:
                    for i in range(0, len(temp_list)):
                        type_bool = False                    
                        if self.text[self.index + i] == temp_list[i]:
                            type_bool = True                        
                except Exception, e:
                    print "symbol_function:-->", e
                    type_bool = False
                
            if type_bool:
                self.notes_function()
            else:
                self.index += 1
                
        self.index += 1        
        
    def string_function(self):    
        # clear token.
        self.token = ""
        # set pre and next point.
        self.pre  = self.index
        self.next = self.index
        # set start index.
        self.start_index = self.pre        
        
        string_bool = False        
        self.start_index += self.temp_cn_next
        ########################################
        while True:
            try:
                string_ch = self.text[self.next]
                self.token += string_ch
                if string_ch == '"' and string_bool:
                    self.next += 1
                    break
                string_bool = True
            except:    
                break
            
            if self.cn_bool(string_ch):
                self.temp_cn_next += 2                
            
            self.next += 1    
        ###################################
        # print "======================"   
        # print "token:", self.token
        # print "last next:", self.next
            
        # set index.            
        self.index     = self.next
        # save end index.
        self.end_index = self.next
        self.string_save()
        
    def string_save(self):    
        symbol_table = SymbolTable()
        symbol_table.type  = SYMBOL_TABLE_STRING_TYPE
        symbol_table.token = self.token
        symbol_table.row = self.row
        symbol_table.start_index = self.start_index 
        symbol_table.end_index   = self.end_index - 1  + self.temp_cn_next
        config_rgb = self.code_edit_config.get("TEXT_BUFFER_VALUE", "STRING")
        if not config_rgb:
            config_rgb = "#000000"
        symbol_table.rgb = config_rgb
        # print "================="
        # print "type:", symbol_table.type
        # print "token:", symbol_table.token
        # print "row:", symbol_table.row
        # print "start_index:", symbol_table.start_index
        # print "end_index:", symbol_table.end_index
        # print "rgb:", symbol_table.rgb
        # print "==========="        
        self.symbol_table_list.append(symbol_table)
        
    
    def notes_function(self):
        # clear token.
        self.token = ""
        # set pre and next point.
        self.pre = self.index
        self.next = self.index
        # set start index.
        self.start_index = self.pre
        notes_temp_cn_next = 0
        while True:
            try:
                notes_ch = self.text[self.next]
                self.token += notes_ch
            except:    
                self.index     = self.next
                self.end_index = self.next + notes_temp_cn_next
                self.notes_save()
                break
            
            if self.cn_bool(notes_ch):    
                notes_temp_cn_next += 2                

            self.next += 1
                
    
    def notes_save(self):
        symbol_table = SymbolTable()
        symbol_table.type  = SYMBOL_TABLE_NOTES_TYPE
        symbol_table.token = self.token
        symbol_table.row = self.row
        symbol_table.start_index = self.start_index  + self.temp_cn_next
        symbol_table.end_index   = self.end_index - 1  + self.temp_cn_next
        config_rgb = self.code_edit_config.get("TEXT_BUFFER_VALUE", "NOTES")
        if not config_rgb:
            config_rgb = "#000000"
        symbol_table.rgb = config_rgb
        # print "================="
        # print "type:", symbol_table.type
        # print "token:", symbol_table.token
        # print "row:", symbol_table.row
        # print "start_index:", symbol_table.start_index
        # print "end_index:", symbol_table.end_index
        # print "rgb:", symbol_table.rgb
        # print "==========="
        self.symbol_table_list.append(symbol_table)
        
    ###################################################3    
    ### bool function.            
    def keyword_bool(self, ch):
        key_list = []
        key_index = 0
        for key in self.keyword:
            if key[key_index] == ch:                
                key_list.append(key)
        return key_list
    
    def letter_bool(self, ch):    
        return (('a' <= ch <= 'z') or ('A' <= ch <= 'Z'))
    
    def number_bool(self, ch):    
        return ('0' <= ch <= '9')
        
    def symbol_bool(self, ch):    
        return (ch in self.symbol)
    
    def len_text(self):
        return len(self.text)
    
    def cn_bool(self, ch):
        if not (self.letter_bool(ch) or self.number_bool(ch) or self.symbol_bool(ch) or ch in [" "]):
            return True
        
##########################################################################

##########################################################################

class Regex(object):
    def __init__(self, String, Format):
        self.string = String
        self.format = Format
        
    def start_regex(self):                
        print self.format
        print self.string
                
        self.token_bool(self.format[0])
        start_index, end_index = 0,0
        return start_index, end_index
    
    def token_bool(self, token):                    
        if   token == "-":
            pass
        elif token == "*":   
            pass
        elif token == "":
            pass
        
        return token    
    
class Stack(object):
    def __init__(self):
        self.__stack = []
        self.__index = -1
    
    def pop(self):
        if self.__index > -1:
            element = self.__stack[self.__index]
            del self.__stack[self.__index]
            self.__index -= 1
            return element 
        else:
            return False
        
    def push(self, element):
        self.__stack.append(element)
        self.__index += 1
    
if __name__ == "__main__":
    # scan = Scan("language/python.ini")
    # print scan.scan("f", 10)
    
    #     # start_index, end_index = Regex("I love c and linux", "0-9").start_regex()
    #     # print "start_index:", start_index, "end_index:", end_index
    temp_stack = Stack()
    temp_stack.push('3')
    temp_stack.push('+')
    temp_stack.push('4')
    print temp_stack.pop()
    print temp_stack.pop()
    print temp_stack.pop()
    
    
    
    
