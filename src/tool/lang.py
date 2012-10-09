#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
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


import os
from ini import Config

lang_path = ""

class Lang(object):
    def __init__(self):
        self.config = Config("cn.ini")
        
    def get_value(self, id):
        if self.config:
            return self.config.get("DEEPIN", str(id))
        else:    
            return "None"
        
    def set_lang(self, lang_path):
        if os.path.exists(lang_path):
            lang_path = lang_path
            self.config = Config(lang_path)
    
lang = Lang()
_ = lang.get_value

if __name__ == "__main__":            
    lang.set_lang("cn.ini")
    _ = lang.get_value
    print _(0)
    print _(1)
    print _(2)
    print _(3)
    lang.set_lang("en.ini")
    print _(0)
    print _(1)
    print _(2)
    print _(3)
