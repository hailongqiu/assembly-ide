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

import subprocess
import commands

def run_elf(souce_file):
    return commands.getoutput(souce_file)
    
def input_elf(souce_file, dec_file):
    '''
    nasm 生成LINUX可执行文件.
    '''
    print souce_file, dec_file
    getoutput_str = commands.getoutput(
        "sh ./tool/compile.sh %s %s %s" % ("elf", souce_file, dec_file))
    if not getoutput_str:
        getoutput_str = "True"
    return getoutput_str

def input_link(souce_file, dec_file, OS_BIT_TYPE=32):
    '''
    链接NASM的.asm代码. 
    'link' -> 发送sh脚本的参数命令
    souce_file: 源代码文件
    dec_file: 目标文件
    OS_BIT_TYPE: 当前系统类型(32/64)
    '''
    print souce_file, dec_file
    getoutput_str = commands.getoutput(
        "sh ./tool/compile.sh %s %s %s %s" % ("link", souce_file, dec_file, OS_BIT_TYPE))
    return getoutput_str
    
def input_bin(souce_file, dec_file):
    getoutput_str = commands.getoutput(
        "sh compile.sh %s %s %s" % ("bin", souce_file, dec_file))
    return getoutput_str
    
def open_gcalctool():
    '''调用计算器.'''
    subprocess.Popen("gcalctool")
        
    
if __name__ == "__main__":
    import gtk    
    
    def button_clicked_event(widget):
        # open_gcalctool()
        widget.set_label(
            # str(input_link("/home/long/Desktop/test-obj/a.asm",
            #           "/home/long/Desktop/test-obj/a.o"))
            str(input_bin("/home/long", "fdjskfd"))
            )
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.connect("destroy", lambda w:gtk.main_quit())
    btn = gtk.Button("打开计算器")
    btn.connect("clicked", button_clicked_event)
    win.add(btn)
    win.show_all()
    gtk.main()
