#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Hailong, Inc.
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
import gtk
import mmap
import cairo
import pango
import pangocairo

from codehintswindow import CodeHintsWindow
from ini   import Config, get_home_path
from regex import Scan

INIT_CONFIG_PATH = "codeedit/language/config.ini"
INIT_FONT_TYPE = "文泉驿等宽微米黑"
INIT_FONT_SIZE = 11

SELECT_MOVE_COPY_STATE_MID   = 0
SELECT_MOVE_COPY_STATE_LEFT  = 1
SELECT_MOVE_COPY_STATE_RIGHT = 2

class CodeEdit(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)                 
        self.init_code_edit_config() # init code edit config.
        self.init_language_config()  # init language config.        
        self.init_code_line_value()
        self.init_row_border()
        self.init_border_row_number()
        self.init_code_folding()        
        self.init_cursor()
        self.init_select_value()
        self.init_text_buffer_value()                
        self.init_font()   # init font-> type and size.    
        self.init_immultiontext()    # init immultiontext.
        self.init_text_source_view() # init text source view.
        self.init_scroll_window_connect() 
        self.init_code_hints_window()
        self.init_keymap() # init keymap.
        
        # scrolled window add text source view.
        self.add_with_viewport(self.text_source_view)
        gtk.timeout_add(self.cursor_time_second, self.show_and_hide_cursor)
                
    def show_and_hide_cursor(self):
        if self.cursor_time_bool:
            self.cursor_show_bool = not self.cursor_show_bool
            self.row_ch_queue_draw_area("|")
        return self.cursor_time_bool
    
    ###########################################################    
    ### Init value and connect.    
    def init_code_edit_config(self, config_path=INIT_CONFIG_PATH):        
        self.config_path_ini = Config("codeedit/language/assembly-ide-config.ini")
        temp_config_path = self.config_path_ini.get("CONFIG_PATH", "config_path")
        if temp_config_path and os.path.isfile(temp_config_path):
            config_path = temp_config_path
            
        self.code_edit_config_path = config_path
        self.code_edit_config = Config(self.code_edit_config_path)
        
    def init_language_config(self, language_path="codeedit/language/python.ini"):
        language_path = language_path
        # read config ini[language_path].
        config_language_path = self.code_edit_config.get("LANGUAGE", "language_path")
        if config_language_path:
            language_path = config_language_path
            
        self.language_path = language_path
        
    def init_code_line_value(self):        
        padding_x = 888
        color = "#000000"
        alpha = 0.1
        config_padding_x = self.code_edit_config.get("CODE_LINE_VALUE", "code_line_padding_x")
        if config_padding_x:
            padding_x = config_padding_x
        config_color = self.code_edit_config.get("CODE_LINE_VALUE", "code_line_color")    
        if config_color:
            color = config_color
        config_alpha = self.code_edit_config.get("CODE_LINE_VALUE", "code_line_alpha") 
        if config_alpha:
            alpha = config_alpha
            
        self.code_line_padding_x = int(padding_x)
        self.code_line_color = color
        self.code_line_alpha = float(alpha)

    def init_row_border(self):    
        color = "#F5F5F5"
        width = 45
        config_color = self.code_edit_config.get("ROW_BORDER", "row_border_color")
        config_width = self.code_edit_config.get("ROW_BORDER", "row_border_width")
        if config_color:
            color = config_color
        if config_width:    
            width = config_width
            
        self.row_border_color = color
        self.row_border_width = int(width)
        
    def init_border_row_number(self):    
        color = "#4169E1"
        alpha = 0.8
        padding_x = 15
        config_color = self.code_edit_config.get("ROW_BORDER", "row_number_color")
        config_alpha = self.code_edit_config.get("ROW_BORDER", "row_number_alpha")
        config_padding_x = self.code_edit_config.get("ROW_BORDER", "row_number_padding_x")
        if config_color:
            color = config_color
        if config_alpha:    
            alpha = config_alpha
        if config_padding_x:    
            padding_x = config_padding_x
            
        self.row_number_color = color
        self.row_number_alpha = float(alpha)
        self.row_number_padding_x = int(padding_x)
        
    def init_code_folding(self):                    
        self.code_folding_height = 0
        self.code_folding_width  = 15
        
        bg_alpha = 1
        bg_color = "#FFFFFF"
        line_alpha = 0.4
        line_color = "#000000"
        
        config_bg_alpha = self.code_edit_config.get("CODE_FOLDING", "code_folding_bg_alpha")
        if config_bg_alpha:
            bg_alpha = config_bg_alpha
        config_bg_color = self.code_edit_config.get("CODE_FOLDING", "code_folding_bg_color")
        if config_bg_color:
            bg_color = config_bg_color
        config_line_alpha = self.code_edit_config.get("CODE_FOLDING", "code_folding_line_alpha")
        if config_line_alpha:
            line_alpha = config_line_alpha
        config_line_color = self.code_edit_config.get("CODE_FOLDING", "code_folding_line_color")
        if config_line_color:
            line_color = config_line_color            
                
        self.code_folding_bg_alpha   = float(bg_alpha)
        self.code_folding_bg_color   = str(bg_color)
        self.code_folding_line_alpha = float(line_alpha)
        self.code_folding_line_color = str(line_color)
                
    def init_cursor(self):
        self.cursor_column = 0
        self.cursor_show_bool = True        
        self.cursor_padding_x = 0
        
        color = "#000000"
        width = 1
        time_bool = False
        time_second = 888
        config_color = self.code_edit_config.get("CURSOR", "cursor_color")
        config_width = self.code_edit_config.get("CURSOR", "cursor_width")
        config_time_bool = self.code_edit_config.get("CURSOR", "cursor_time_bool")
        config_time_second = self.code_edit_config.get("CURSOR", "cursor_time_second")
        
        if config_color:
            color = config_color
        if config_width:    
            width = config_width
        if config_time_bool and "true" == config_time_bool.lower():
                time_bool = True
        if config_time_second:    
            time_second = config_time_second
            
        self.cursor_color = color
        self.cursor_width = int(width)
        self.cursor_time_bool = int(time_bool)
        self.cursor_time_second = int(time_second)
        
        
    def init_select_value(self):
        self.select_start_to_end_state = SELECT_MOVE_COPY_STATE_MID
        self.select_copy_bool = False
        self.select_copy_draw_bool = False
        self.start_select_padding_x = 0
        self.end_select_padding_x   = 0
        self.start_select_row    = 0
        self.end_select_row      = 0
        self.start_select_column = 0
        self.end_select_column   = 0        
        
        color = "#000000"
        alpha = 0.5
        config_color = self.code_edit_config.get("SELECT_VALUE", "select_start_to_end_color")
        config_alpha = self.code_edit_config.get("SELECT_VALUE", "select_start_to_end_alpha")
        if config_color:
            color = config_color
        if config_alpha:    
            alpha = config_alpha
            
        self.select_start_to_end_color = color
        self.select_start_to_end_alpha = float(alpha)

    def init_text_buffer_value(self):
        notes_symbol = ";"
        self.tab_num = 4    
        view_bg_color = "#FFFFFF"
        ch_fg_color = "#000000"
        select_row_alpha = 0.1
        select_row_color = "#4169E1"
        # get notes symbol.
        config_notes_symbol = self.code_edit_config.get("TEXT_BUFFER_VALUE", "notes_symbol")
        if config_notes_symbol:
            notes_symbol = config_notes_symbol            
        # get tab num.
        config_tab_num = self.code_edit_config.get("TEXT_BUFFER_VALUE", "tab_num")
        if config_tab_num:
            self.tab_num = int(config_tab_num)
        # get view bg color.    
        config_view_bg_color = self.code_edit_config.get("TEXT_BUFFER_VALUE", "text_source_view_bg_color")
        if config_view_bg_color:
            view_bg_color = config_view_bg_color
        # get ch fg color.    
        config_ch_fg_color = self.code_edit_config.get("TEXT_BUFFER_VALUE", "VARIABLE")    
        if config_ch_fg_color:    
            ch_fg_color = config_ch_fg_color
        # get select row alpha.    
        config_select_row_alpha = self.code_edit_config.get("TEXT_BUFFER_VALUE", "select_row_alpha")    
        if config_select_row_alpha:
            select_row_alpha = config_select_row_alpha        
        # get select row color.    
        config_select_row_color = self.code_edit_config.get("TEXT_BUFFER_VALUE", "select_row_color")
        if config_select_row_color:    
            select_row_color = config_select_row_color
            
        self.text_buffer_list = [""]
        self.tab_string = ""
        for num in range(self.tab_num):
            self.tab_string += " "
        self.current_row = 1
        self.cursor_row  = 1        
        self.map_buffer = None
        #######################
        self.text_source_view_bg_color = str(view_bg_color) # 整个代码编辑器的背景:白色.
        self.ch_fg_color = str(ch_fg_color) # 显示文本中字符的初始化颜色值:黑色.        
        #####################
        self.select_row_alpha = float(select_row_alpha)
        self.select_row_color = str(select_row_color)
        self.scan_file_ini = self.language_path
        self.notes_symbol = notes_symbol
        
    def init_font(self, font_type=INIT_FONT_TYPE, font_size=INIT_FONT_SIZE):
        '''Init font type/size.'''
        config_font_type = self.code_edit_config.get("FONT", "font_type")
        config_font_size = self.code_edit_config.get("FONT", "font_size")
        
        if config_font_type:
            font_type = config_font_type
        if config_font_size:    
            font_size = config_font_size
            
        self.font_type  = font_type
        self.font_size  = int(font_size)
        self.column_font_width = self.get_ch_size(" ")[0]
        self.row_font_height = self.get_ch_size(" ")[1]
        
    def init_immultiontext(self):
        '''Init immulticontext.'''
        self.im = gtk.IMMulticontext()
        self.im_offset_x = 0
        self.im_offset_y = 0
        self.im.connect("commit", self.get_im_input_string)
        
    def get_im_input_string(self, IMMulticontext, text):    
        text_utf_8 = text.decode('utf-8')
        for ch in text_utf_8:
            start_string, end_string = self.start_to_end_string(
                self.cursor_row,
                0,
                self.cursor_column,
                self.cursor_column,
                len(self.text_buffer_list[self.cursor_row-1]) + 1
                )
            temp_string = start_string + ch + end_string
            self.text_buffer_list[self.cursor_row - 1] = temp_string
            self.cursor_padding_x += self.get_ch_size(ch)[0]
            self.cursor_column += 1            
            
        self.row_line_queue_draw_area()
        
    def init_text_source_view(self):    
        self.text_source_view = gtk.Button()
        init_width = 1500
        init_height = 1500
        self.text_source_view.set_size_request(init_width, init_height)
        self.text_source_view.set_can_focus(True)
        self.text_source_view.grab_focus()        
        '''Init text_source_view event.'''
        self.text_source_view.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.text_source_view.connect("expose-event",          
                                      self.text_source_view_expose_event)
        self.text_source_view.connect("button-press-event",    
                                      self.text_source_view_button_press_event)        
        self.text_source_view.connect("motion-notify-event", 
                                      self.text_source_view_motion_notify_event)        
        self.text_source_view.connect("button-release-event",  
                                      self.text_source_view_button_release_event)
        self.text_source_view.connect("key-press-event",       
                                      self.text_source_view_key_press_event)        
        self.text_source_view.connect("focus-out-event",       
                                      self.text_source_view_get_text_view_focus_out)
        self.text_source_view.connect("focus-in-event",        
                                      self.text_source_view_get_text_view_focus_in)
        
    def init_scroll_window_connect(self):    
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.get_hadjustment().connect("value-changed", 
                                       self.scrolled_window_hadjustment_value_changed)
        self.get_vadjustment().connect("value-changed", 
                                       self.scrolled_window_vadjustment_value_changed)
        
    def init_keymap(self):    
        self.keymap = {
            "BackSpace":self.key_delete_ch,
            ###############################
            "Return":self.key_enter,
            "Ctrl + l":self.key_enter_ctrl_l,
            ###############################
            "Ctrl + p":self.cursor_up,
            "Ctrl + n":self.cursor_down,            
            "Ctrl + f":self.cursor_right,
            "Ctrl + b":self.cursor_left,
            "Ctrl + L":self.cursor_copy_row_text,
            "Ctrl + a":self.cursor_row_start,
            "Ctrl + e":self.cursor_row_end,
            "Ctrl + s":self.save,
            "Ctrl + :":self.cursor_start_insert_ch,
            # "Ctrl + m":self.test_show_window,
            ###############################
            "F11":self.key_full_window,
            "Tab":self.key_tab_string
            }
        
    def init_code_hints_window(self):    
        self.code_hints_window = CodeHintsWindow()
        
    def test_show_window(self): # Error show window position. 相對座標
        self.code_hints_window.show_all()
        root_x, root_y = self.get_toplevel().window.get_root_origin()
        padding_height = 31
        padding_x = root_x + self.row_border_width + self.code_folding_width + self.cursor_padding_x - self.get_scrolled_window_width(self.cursor_row - 1)[0]
        padding_y = root_y + (self.cursor_row - self.get_scrolled_window_height()[0]) * self.row_font_height + padding_height
        
        self.code_hints_window.move(
            padding_x,
            padding_y
            )    
    
    ############################################################    
    ### scrolled window connect.
    def scrolled_window_hadjustment_value_changed(self, hadjustment):
        self.scrolled_window_queue_draw_area()
    
    def scrolled_window_vadjustment_value_changed(self, vadjustment):
        self.scrolled_window_queue_draw_area()
    
    ############################################################
    ### text source view connect.
        
    ###############    
    ''' expose function: background, border, row number, buffer text, hight... ...'''
    ###    
    def text_source_view_expose_event(self, widget, event):
        cr = widget.window.cairo_create() # create cairo.
        rect = widget.allocation # text source view allocation(x, y, width, height)        
        # Draw background.
        self.draw_text_source_view_background(cr, rect)
        # Draw code line.
        self.draw_text_source_view_code_line(cr, rect)
        # Draw buffer text.
        self.draw_text_source_view_buffer_text(cr, rect)
        # Draw select row color.
        self.draw_text_source_view_select_row(widget, cr, rect)
        # Draw select start to end row text color.
        self.draw_text_source_view_select_start_to_end_row(cr, rect)
        # Draw cursor.
        self.draw_text_source_view_cursor(cr, rect) 
        # Draw border.
        self.draw_text_source_view_border(widget, cr, rect)
        return True    
    ###
    # expose function.
    ###
    # draw_text_source_view_background.
    def draw_text_source_view_background(self, cr, rect):
        start_index = self.get_scrolled_window_height()[0]
        panent_rect = self.allocation
        self.draw_rectangle(
            cr,
            rect.x,
            rect.y + (start_index * self.row_font_height),
            rect.width,
            # rect.height,
            panent_rect.height,
            self.text_source_view_bg_color)

    # draw_text_source_view_code_line.
    def draw_text_source_view_code_line(self, cr, rect):
        self.draw_alpha_rectangle(
            cr,
            rect.x + self.code_line_padding_x,
            rect.y,
            1,
            rect.y + rect.height,
            self.code_line_color, 
            self.code_line_alpha
            )
        
    # draw_text_source_view_buffer_text.
    def draw_text_source_view_buffer_text(self, cr, rect):
        start_row, end_row, sum_row = self.get_scrolled_window_height()
        start_column, end_column, sum_column = self.get_scrolled_window_width()
        for text in self.get_buffer_row_start_to_end_text(start_row, sum_row):            
            # print "start_column:", start_column
            # print "end_column:", end_column
            # print "sum_column:", sum_column
            # get token color.
            pango_list = pango.AttrList()
            if text:                
                scan = Scan(self.scan_file_ini, self.code_edit_config_path)
                for table_color in scan.scan(text[:sum_column],
                                             start_row):
                    r, g, b = self.hex_color_to_65535_rgb(table_color.rgb)
                    # set pango list.
                    pango_list.insert(
                        pango.AttrForeground(
                            r, g, b, table_color.start_index, table_color.end_index+1))
                        
            # draw ch.
            x_padding = rect.x + self.row_border_width + self.code_folding_width
            y_padding = rect.y + (start_row) * self.row_font_height
            self.draw_text_source_view_buffer_text_ch(text,
                                                      cr,
                                                      x_padding,
                                                      y_padding, 
                                                      pango_list,
                                                      self.ch_fg_color
                                                      )
            start_row += 1
            
    def draw_text_source_view_buffer_text_ch(self, ch, cr, 
                                             offset_x, offset_y,                                              
                                             pango_list,
                                             init_fg_color
                                             ):    
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))         
        
        # Set font position.
        layout.set_text(ch)
        
        layout.set_attributes(pango_list)
        ch_width, ch_height = layout.get_pixel_size()
        cr.move_to(offset_x, 
                   offset_y)
        # Set font rgb.
        cr.set_source_rgb(*self.color_to_rgb(init_fg_color))
        # Show font.
        context.update_layout(layout)
        context.show_layout(layout)
        return ch_width
    
    def set_ch_background(self, cr, 
                          offset_x, offset_y, 
                          ch_width, ch_height, 
                          alpha, bg_rgb=None
                          ):    
        if bg_rgb:
            self.draw_alpha_rectangle(
                cr,
                offset_x, 
                offset_y, 
                ch_width, 
                ch_height,
                bg_rgb, 
                alpha
                )
            
    # draw_text_source_view_select_row        
    def draw_text_source_view_select_row(self, widget, cr, rect):
        paernt_rect = self.allocation        
        offset_x, offset_y = self.get_coordinates(widget, rect.x, rect.y)
        self.draw_alpha_rectangle(
            cr,
            -offset_x + rect.x + self.row_border_width + self.code_folding_width,
            rect.y + (self.cursor_row - 1) * self.row_font_height,
            paernt_rect.width,
            self.row_font_height,
            self.select_row_color,
            self.select_row_alpha
            )
        
    # draw_text_source_view_select_start_to_end_row    
    def draw_text_source_view_select_start_to_end_row(self, cr, rect):    # 123456
        if self.select_copy_draw_bool:
            start_select_row = self.start_select_row
            end_select_row   = self.end_select_row
            start_select_padding_width = self.start_select_padding_x
            end_select_padding_width = self.end_select_padding_x
            text_view_padding_width = self.row_border_width + self.code_folding_width
            start_padding_x = text_view_padding_width
            end_padding_x = text_view_padding_width
            paernt_rect = self.allocation
            ###################################
            if self.select_start_to_end_state == SELECT_MOVE_COPY_STATE_MID:
                if end_select_padding_width < start_select_padding_width: # sawp start and end.
                    start_select_padding_width, end_select_padding_width = (end_select_padding_width, start_select_padding_width)
                start_padding_x += start_select_padding_width
                start_select_padding_width = end_select_padding_width - start_select_padding_width
            elif self.select_start_to_end_state == SELECT_MOVE_COPY_STATE_LEFT:
                # swap start and end row.
                start_select_row, end_select_row = (end_select_row, start_select_row)
                # swap start and end width.                
                start_select_padding_width, end_select_padding_width = (end_select_padding_width, start_select_padding_width)
                # sawp start and end padding x.
                start_padding_x, end_padding_x = (end_padding_x, start_padding_x)
                # set value.
                start_padding_x += start_select_padding_width
                temp_text = self.text_buffer_list[self.start_select_row - 1]
                start_select_padding_width = self.get_ch_size(temp_text)[0] - start_select_padding_width
                start_select_padding_width = paernt_rect.width
            elif self.select_start_to_end_state == SELECT_MOVE_COPY_STATE_RIGHT:
                start_padding_x += start_select_padding_width
                temp_text = self.text_buffer_list[self.start_select_row - 1]
                start_select_padding_width = self.get_ch_size(temp_text)[0] - start_select_padding_width
                row_text_sum = len(self.text_buffer_list[self.start_select_row - 1])
                if (not row_text_sum) or (row_text_sum == self.start_select_column):
                    start_select_padding_width = paernt_rect.width
            ######################    
            self.draw_select_start_to_end_row_border_color(
                cr, rect,
                start_select_row, end_select_row,
                start_select_padding_width, end_select_padding_width,
                start_padding_x, end_padding_x
                )                                    
        
    def draw_select_start_to_end_row_border_color(self, cr, rect, 
                                                  start_row, end_row,
                                                  start_padding_width, end_padding_width,
                                                  start_padding_x, end_padding_x,
                                                  ):
        paernt_rect = self.allocation
        for row in range(start_row, end_row + 1):                        
            if row == start_row: # draw first row border.
                self.draw_alpha_rectangle(
                    cr,
                    rect.x + start_padding_x,
                    rect.y + (row - 1) * self.row_font_height,
                    start_padding_width,
                    self.row_font_height,
                    self.select_start_to_end_color,
                    self.select_start_to_end_alpha
                    )                
            elif row == end_row: # draw last row border.
                self.draw_alpha_rectangle(
                    cr,
                    rect.x + end_padding_x,
                    rect.y + (row - 1) * self.row_font_height,
                    end_padding_width,
                    self.row_font_height,
                    self.select_start_to_end_color,
                    self.select_start_to_end_alpha
                    )                
            else: # draw other row border.
                self.draw_alpha_rectangle(
                    cr,
                    rect.x + self.row_border_width + self.code_folding_width,
                    rect.y + (row - 1) * self.row_font_height,
                    paernt_rect.width,
                    self.row_font_height,
                    self.select_start_to_end_color,
                    self.select_start_to_end_alpha
                    )
        
    # draw_text_source_view_border.        
    def draw_text_source_view_border(self, widget, cr, rect):
        start_index = self.get_scrolled_window_height()[0]
        offset_x, offset_y = self.get_coordinates(widget, rect.x, rect.y)
        paernt_rect = self.allocation
        # Draw border.        
        self.draw_rectangle(
            cr,
            -offset_x,
            rect.y + (start_index * self.row_font_height),
            self.row_border_width,
            paernt_rect.height,
            self.row_border_color
            )
        # Draw code folding.
        self.draw_text_source_view_code_folding(cr, rect, -offset_x)        
        #Draw row number.
        self.draw_text_source_view_row_number(cr, rect, -offset_x)

        
    def draw_text_source_view_code_folding(self, cr, rect, offset_x):
        start_index = self.get_scrolled_window_height()[0]
        code_folding_x = rect.x + self.row_border_width
        paernt_rect = self.allocation
        # draw text source code folding background.
        self.draw_alpha_rectangle(
            cr,
            offset_x +  code_folding_x,
            rect.y + (start_index * self.row_font_height),
            self.code_folding_width,
            # rect.y + rect.height,
            paernt_rect.height,
            self.code_folding_bg_color,
            self.code_folding_bg_alpha
            )                
        # draw code folding line.
        self.draw_alpha_rectangle(
            cr,
            offset_x + code_folding_x + int(self.code_folding_width/2),
            rect.y + (start_index * self.row_font_height),
            1,
            paernt_rect.height,
            self.code_folding_line_color,
            self.code_folding_line_alpha
            )        
        
    def draw_text_source_view_row_number(self, cr, rect, offset_x): 
        cr.set_source_rgba(*self.color_to_rgba(self.row_number_color, self.row_number_alpha))
        start_position_row, end_position_row, temp_row = self.get_scrolled_window_height()
                
        if temp_row > self.current_row:
            temp_row = self.current_row
                            
        if self.current_row == 1:
            start_position_row = 0
            temp_row = 1
            
        for row_number in range(start_position_row+1, temp_row+1):
            self.text_buffer_list[row_number - 1] = self.text_buffer_list[row_number-1].replace("\t", self.tab_string)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            
            temp_font_size = self.font_size
            if row_number == self.cursor_row:
                temp_font_size += 1
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, temp_font_size)))
            (text_width, text_height) = layout.get_pixel_size()            
            
            x_padding = rect.x + offset_x + self.border_width + self.code_folding_width + self.row_number_padding_x
            y_padding = rect.y + (row_number - 1) * self.row_font_height
            layout.set_text(self.row_number_to_string(row_number))
            cr.move_to(
                x_padding,
                y_padding
                )
            context.update_layout(layout)
            context.show_layout(layout)
        
    # draw_text_source_view_cursor.
    def draw_text_source_view_cursor(self, cr, rect):
        if self.cursor_show_bool:
            x_padding = rect.x + self.row_border_width + self.code_folding_width + self.cursor_padding_x
            y_padding = rect.y + (self.cursor_row - 1) * self.row_font_height
            self.draw_rectangle(
                cr,
                x_padding,
                y_padding,
                self.cursor_width,
                self.row_font_height,
                self.cursor_color
                )

    #############################################
    def text_source_view_button_press_event(self, widget, event):
        move_row = int(event.y / self.row_font_height) + 1
        min_row = self.get_scrolled_window_height()[0]
        max_row = self.get_scrolled_window_height()[2]
        if min_row < move_row <= max_row:
            if 1 <= move_row <= self.current_row:
                token_all_width = self.get_press_cursor_position(widget, event, move_row - 1)
                self.cursor_row = move_row            
                self.cursor_padding_x = token_all_width
                self.cursor_show_bool = True
                self.scrolled_window_queue_draw_area()
                                
        self.select_init()        
        
    def select_init(self):    
        self.select_copy_bool = True
        temp_text = self.text_buffer_list[self.cursor_row - 1][:self.cursor_column]
        self.start_select_padding_x = self.get_ch_size(temp_text)[0]
        self.start_select_row    = self.cursor_row
        self.start_select_column = self.cursor_column
        
    # text_source_view_motion_notify_event.    
    def text_source_view_motion_notify_event(self, widget, event):
        if self.select_copy_bool:
            move_row = int(event.y / self.row_font_height) + 1
            move_padding_x = int(event.x)
                
            
            self.cursor_padding_x = self.select_motion_postion_function(move_padding_x)
            self.select_draw_function(max(move_row, 1))
            # print "===================================="
            # print "cursor_row:",   self.cursor_row
            # print "cusor_column:", self.cursor_column
            # print "cursor_padding_x:", self.cursor_padding_x        
            # print "start_row:", self.start_select_row
            # print "end_row:", self.end_select_row
            # print "start_column:", self.start_select_column
            # print "end_column:", self.end_select_column
            # print "start_select_padding_x:", self.start_select_padding_x
            # print "end_select_padding_x:", self.end_select_padding_x                        
            # print "state:", self.select_start_to_end_state
            # print "====================================@@"
            
            self.scrolled_window_queue_draw_area()
            
    def select_motion_postion_function(self, move_padding_x):
        token_all_width = 0
        self.cursor_column = 0
        rect = self.allocation
        temp_padding_x = self.row_border_width + self.code_folding_width
        if move_padding_x < temp_padding_x:
            return token_all_width
        
        for ch in self.text_buffer_list[self.cursor_row - 1]:
            ch_width = self.get_ch_size(ch)[0]
            max_padding_x = (rect.x + temp_padding_x + token_all_width + ch_width)
            min_padding_x = (rect.x + temp_padding_x + token_all_width)
            if  min_padding_x <= (move_padding_x) <= max_padding_x:
                break
            else:
                self.cursor_column += 1
                token_all_width += ch_width                
        self.end_select_column = self.cursor_column
        return token_all_width
        
        
    def select_draw_function(self, move_row):
        max_row =  self.get_scrolled_window_height()[2]
        # get select end row.
        self.end_select_row = min(min(move_row, max_row), self.current_row)
            
        if self.start_select_row == self.end_select_row:
            self.select_start_to_end_state = SELECT_MOVE_COPY_STATE_MID
        elif self.start_select_row > self.end_select_row:    
            self.select_start_to_end_state = SELECT_MOVE_COPY_STATE_LEFT
        elif self.start_select_row < self.end_select_row:    
            self.select_start_to_end_state = SELECT_MOVE_COPY_STATE_RIGHT
                
        temp_text = self.text_buffer_list[self.cursor_row - 1][:self.cursor_column]
        self.end_select_padding_x = self.get_ch_size(temp_text)[0]
            
        # Set cursor row.
        self.cursor_row = max(self.end_select_row, 1)
        # Set draw select flags.
        self.select_copy_draw_bool = True            
            
    def text_source_view_button_release_event(self, widget, event):
        self.select_copy_bool = False
    
    # text_source_view_key_press_event.
    def text_source_view_key_press_event(self, widget, event):
        self.handle_key_press(widget, event)
        widget.grab_focus()
        return True
        
    def handle_key_press(self, widget, event):
        input_method_filt = self.im.filter_keypress(event)
        if not input_method_filt:    
            self.handle_key_event(event)            
        return False        
    
    def handle_key_event(self, event):
        key_name = self.get_keyevent_name(event)        
        print "key_name:" , key_name
        if self.keymap.has_key(key_name):
            self.keymap[key_name]()
    
    # text_source_view_get_text_view_focus_out.        
    def text_source_view_get_text_view_focus_out(self, widget, event):
        self.im.focus_out()
    
    def text_source_view_get_text_view_focus_in(self, widget, event):
        self.im.set_client_window(widget.window)        
        self.im.focus_in()       
        
    ############################################################
    '''key map'''
    ###
    def key_delete_ch(self):
        if self.cursor_column > 0:
            start_string, end_string = self.start_to_end_string(
                self.cursor_row,
                0,
                self.cursor_column - 1,
                self.cursor_column,
                len(self.text_buffer_list[self.cursor_row - 1]) + 1
                )
            temp_text = start_string + end_string
            self.text_buffer_list[self.cursor_row - 1] = temp_text 
            
            self.cursor_column = max(self.cursor_column - 1, 0)
        
            if self.cursor_column > 0:
                self.cursor_padding_x = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1][:self.cursor_column])[0]
            else:    
                self.cursor_padding_x = 0                                    
                
            self.row_line_queue_draw_area()    
        else: # if column == 0
            if self.cursor_row > 1:
                temp_text = self.text_buffer_list[self.cursor_row - 1]
                # get cursor position.
                token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row - 2])[0]
                # set cursor_column.
                self.cursor_column = len(self.text_buffer_list[self.cursor_row - 2])
                # text_buffer_list connect temp_text.
                self.text_buffer_list[self.cursor_row - 2] += temp_text
                # delete current row text_buffer_list.
                del self.text_buffer_list[self.cursor_row - 1]                
                self.current_row -= 1                
                self.cursor_row  -= 1                
                # set cursor position.
                self.cursor_padding_x = token_all_width
                self.scrolled_window_queue_draw_area()
                
    def key_enter(self):
        temp_text_buffer = self.text_buffer_list[self.cursor_row - 1][:self.cursor_column]
        temp_insert_text = self.text_buffer_list[self.cursor_row - 1][self.cursor_column:] 
        self.text_buffer_list[self.cursor_row - 1] = temp_text_buffer
        self.text_buffer_list.insert(self.cursor_row, temp_insert_text)
        # self.text_buffer_list.insert(self.cursor_row, "")
        self.key_enter_init()
        self.cursor_down_vadjustment_set_value()
        # Set enter last height.
        # self.text_source_view.set_size_request(
        #     self.text_source_view.allocation.width,
        #     self.text_source_view.allocation.height + self.get_ch_size("龙")[1]*2 + 500
        #     )         

    def key_enter_ctrl_l(self):    
        '''Emacs key catl + l'''
        self.text_buffer_list.insert(self.cursor_row, "")
        self.key_enter_init()
        self.cursor_down_vadjustment_set_value()
        
    def key_enter_init(self):
        self.cursor_padding_x = 0
        self.cursor_column = 0
        self.cursor_row += 1
        self.current_row += 1
        temp_border_width = 45
        self.row_border_width = temp_border_width + self.get_ch_size(str(self.current_row))[0]
        self.text_source_view.set_size_request(
            self.text_source_view.allocation.width,
            self.text_source_view.allocation.height + self.row_font_height*2
            )         
        self.scrolled_window_queue_draw_area()

    def key_full_window(self):        
        if self.get_toplevel().window.get_state() == gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.get_toplevel().unfullscreen()
        else:    
            self.get_toplevel().fullscreen()
            
    def key_tab_string(self):        
        temp_buffer = self.text_buffer_list[self.cursor_row - 1]
        start_buffer = temp_buffer[:self.cursor_column]
        end_buffer = temp_buffer[self.cursor_column:]
        self.cursor_column += self.tab_num
        self.text_buffer_list[self.cursor_row - 1] = start_buffer + self.tab_string + end_buffer
        self.cursor_padding_x = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1][:self.cursor_column])[0]
        self.row_line_queue_draw_area()
        
    def cursor_down(self):    
        if self.cursor_row < self.current_row:
            token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row][:self.cursor_column])[0]
            self.cursor_row += 1
            self.cursor_padding_x = token_all_width
            self.cursor_column = len(self.text_buffer_list[self.cursor_row-1][:self.cursor_column])            
            self.scrolled_window_queue_draw_area()             
            self.cursor_down_vadjustment_set_value()
                
    def cursor_up(self):    
        if self.cursor_row > 1:
            token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row - 2][:self.cursor_column])[0]
            self.cursor_row = max(self.cursor_row - 1, 1)
            self.cursor_padding_x = token_all_width
            self.cursor_column = len(self.text_buffer_list[self.cursor_row-1][:self.cursor_column])
            self.scrolled_window_queue_draw_area()            
            self.cursor_up_vadjustment_set_value()
        else:                
            token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1][:self.cursor_column])[0]
            
    def cursor_right(self):
        if self.cursor_column < len(self.text_buffer_list[self.cursor_row - 1]):
            self.cursor_column += 1
            token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1][:self.cursor_column])[0]
            self.cursor_padding_x = token_all_width
            self.row_line_queue_draw_area()
            
            self.cursor_right_vadjustment_set_value()
            
    def cursor_left(self):        
        if self.cursor_column > 0:
            self.cursor_column -= 1
            token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1][:self.cursor_column])[0]
            self.cursor_padding_x = token_all_width
            self.row_line_queue_draw_area()
        
    def cursor_row_start(self):
        self.cursor_column = 0
        self.cursor_padding_x = 0
        self.row_line_queue_draw_area()
        
    def cursor_row_end(self):
        self.cursor_column = len(self.text_buffer_list[self.cursor_row - 1])
        self.cursor_padding_x = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1])[0]
        self.row_line_queue_draw_area()
        
    def cursor_copy_row_text(self):
        self.key_enter_ctrl_l()
        self.text_buffer_list[self.cursor_row - 1] = self.text_buffer_list[self.cursor_row - 2]
        
    def cursor_start_insert_ch(self):
        self.cursor_start_insert_ch_function()
    
    def cursor_start_insert_ch_function(self):    
        if self.text_buffer_list[self.cursor_row - 1] != "":            
            # if self.text_buffer_list[self.cursor_row - 1][0] != self.notes_symbol:
            if not self.text_buffer_list[self.cursor_row - 1].startswith(self.notes_symbol):
                self.text_buffer_list[self.cursor_row-1] = self.cursor_row_insert_text(0, self.notes_symbol)
                self.cursor_padding_x += self.get_ch_size(self.notes_symbol)[0]
                self.cursor_column += len(self.notes_symbol)
            else:
                self.text_buffer_list[self.cursor_row-1] = self.text_buffer_list[self.cursor_row-1][len(self.notes_symbol):]
                self.cursor_padding_x = max(self.cursor_padding_x - self.get_ch_size(self.notes_symbol)[0], 0)
                self.cursor_column = max(self.cursor_column - len(self.notes_symbol), 0)
            self.row_line_queue_draw_area()
        
    ############################################################
    '''Operation buffer text.'''    
    ###        
    def read(self, file_path):
        if os.path.exists(file_path):
            self.read_file(file_path)
        else:
            self.perror_input("Read File Error!!......")
            self.text_buffer_list = [""]
            self.current_row = 1
            self.text_source_view.set_size_request(
                self.text_source_view.allocation.width + 1500,
                self.text_source_view.allocation.height + 500,
                )
                
    def read_file(self, file_path):
        # save read file path.
        self.file_path = file_path
        try:
            self.read_file_function()
        except Exception, e:      
                print "read_file:--->", e
                self.current_row = 1          
                
    def read_file_function(self):          
        with open(self.file_path, "r") as f:
            self.map_buffer = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            
        # buffer list.
        temp_text_buffer_list = str(self.map_buffer[:]).decode("utf-8").split("\n")
        # sum row.
        sum_row = len(temp_text_buffer_list)
        # save max column.
        max_column = 0        
        # get text_buffer_list max colume.
        for row in xrange(0, sum_row-1):
            if len(temp_text_buffer_list[row]) > max_column:
                max_column = len(temp_text_buffer_list[row])                
        # set size.
        text_source_view_padding_height = 580
        text_source_view_padding_width  = 580
        self.text_source_view.set_size_request(
            max_column * self.column_font_width + text_source_view_padding_width,
            sum_row * self.row_font_height + text_source_view_padding_height
            ) 
        self.text_buffer_list = temp_text_buffer_list
        self.current_row = max(sum_row - 1, 1)
        
        self.row_border_width += self.get_ch_size(str(self.current_row))[0]
        
    def save(self):
        self.save_file(self.file_path)
        
    def save_file(self, file_path):    
        fp = open(file_path, "w")
        fp.write(self.buffer_to_text())
        fp.close()    
        
    def clear(self):  
        self.text_buffer_list = [""]
        self.current_row = 1
        self.cursor_row = 1
        self.cursor_padding_x = 0
        self.cursor_column = 0
        
    ############################################################    
    '''Tool function.'''
    ###
    def buffer_to_text(self):
        return '\n'.join(self.text_buffer_list)
        
    def perror_input(self, text):
        print text
        
    def get_buffer_row_start_to_end_text(self, start, end):
        return self.text_buffer_list[start:end]
    
    def get_buffer_column_start_to_end_text(self, text, start, end):
        return text[start:end]
    
    def color_to_rgb(self, color):
        if color[0] == '#': 
            try:
                gdk_color = gtk.gdk.color_parse(color)
                r = (gdk_color.red   / 65535.0)
                g = (gdk_color.green / 65535.0)
                b = (gdk_color.blue  / 65535.0)
                return (r, g, b)
            except Exception, e:
                self.perror_input("color_to_..[Error]:color %s error-->%s"%(color, e))
                return (0, 0, 0)
        else:    
            self.perror_input("color_to_..:color %s '#'"%(color))
            return (0, 0, 0)
            
    def color_to_rgba(self, color, alpha):    
        r,g,b = self.color_to_rgb(color)
        return r, g, b, alpha
    
    def hex_color_to_65535_rgb(self, color):
        gdk_color = gtk.gdk.color_parse(color)
        return (gdk_color.red, gdk_color.green, gdk_color.blue)
    
    def get_ch_size(self, ch):    
        if ch:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
            cr = cairo.Context(surface)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))
            layout.set_text(ch)
            return layout.get_pixel_size()
        return (0, 0)
    
    def get_scrolled_window_height(self):
        '''Get row of scrolled window current height.'''
        start_position_row = int(self.get_vadjustment().get_value() / self.row_font_height)
        end_position_row   = int(self.allocation.height / self.row_font_height)
        start_to_end_row   = end_position_row + start_position_row
        return start_position_row, end_position_row, start_to_end_row
    
    # get_scrolled_window_width
    def get_scrolled_window_width(self): # 123456
        '''Get column of scrolled window current width.'''
        # get start position column.
        start_position_column = int(self.get_hadjustment().get_value() / self.column_font_width)
        # get end position column.
        end_position_column = int(self.allocation.width / self.column_font_width)
        # end_position_column = int((self.allocation.width ) / self.column_font_width)
        start_to_end_column = start_position_column + end_position_column
        return start_position_column, end_position_column, start_to_end_column
    
    def get_scrolled_window_start_column(self, row):
        start_position_column = 0
        temp_all_ch_width = 0        
        if self.get_hadjustment().get_value() >= 1:
            temp_text = self.text_buffer_list[row]
            for ch in temp_text:
                ch_width = self.get_ch_size(ch)[0]
                # temp_width = self.get_hadjustment().get_value() - self.row_border_width - self.code_folding_width
                temp_width = self.get_hadjustment().get_value()
                if temp_width <= temp_all_ch_width:
                    break
                else:
                    temp_all_ch_width += ch_width
                    start_position_column += 1
            # print "temp_all_ch_width:", temp_all_ch_width
            # print "temp...width > dfdf:", 
        return start_position_column
    
    def get_scrolled_window_end_column(self, row, start_position_column):
        end_position_column = 0
        scrolled_toolbar_width = 25
        temp_all_ch_width = 0
        # temp_text = self.text_buffer_list[self.cursor_row - 1][start_position_column:]
        temp_text = self.text_buffer_list[row][start_position_column:]
        temp_padding_width = self.allocation.width - self.row_border_width - self.code_folding_width - scrolled_toolbar_width
        for ch in temp_text:
            ch_width = self.get_ch_size(ch)[0]
            temp_width = temp_padding_width
            if temp_width <= temp_all_ch_width:
                # print "get_scrolled_window_end_column...*************到了接觸到了..>>>>"
                break
            else:
                temp_all_ch_width   += ch_width
                end_position_column += 1
        return end_position_column
    
    # scrolled_window_queue_draw_area
    def scrolled_window_queue_draw_area(self):            
        # print "scrolled_window_queue_draw_area...---->>>"
        paernt_rect = self.allocation
        rect = self.text_source_view.allocation
        offset_x = self.get_text_source_view_coordinates()[0]
        start_row = self.get_scrolled_window_height()[0]
        self.text_source_view.queue_draw_area(
            -offset_x + rect.x,
             rect.y + start_row * self.row_font_height,
             paernt_rect.width,
             paernt_rect.height
            )
        
    def get_text_source_view_coordinates(self):    
        widget = self.text_source_view
        rect = self.text_source_view.allocation
        offset_x, offset_y = self.get_coordinates(widget, rect.x, rect.y)
        return (offset_x, offset_y)
    
    def get_coordinates(self, widget, x, y):
        return widget.translate_coordinates(self, x, y)
    
    def row_line_queue_draw_area(self):    
        # print "row_line_queue_draw_area-------->>>>"
        paernt_rect = self.allocation
        rect = self.text_source_view.allocation       
        offset_x = self.get_text_source_view_coordinates()[0]
        self.text_source_view.queue_draw_area(
            -offset_x + rect.x,
             rect.y + (self.cursor_row - 1) * self.row_font_height,
             paernt_rect.width,
             self.row_font_height
            )
        
    def row_ch_queue_draw_area(self, ch):    
        # print "row_ch_queue_draw_area--------->>>>"
        # paernt_rect = self.allocation
        rect = self.text_source_view.allocation
        x_padding = rect.x + self.row_border_width + self.code_folding_width +  self.cursor_padding_x
        y_padding = rect.y + (self.cursor_row - 1) * self.row_font_height
        offset_x = self.get_text_source_view_coordinates()[0]
        self.text_source_view.queue_draw_area(
            -offset_x + x_padding,
            y_padding,
            self.get_ch_size(ch)[0],
            self.row_font_height
            )
        
    def draw_rectangle(self, cr, x, y, w, h, rgb):
        cr.set_source_rgb(*self.color_to_rgb(rgb))
        cr.rectangle(x, y, w, h)
        cr.fill()
    
    def draw_alpha_rectangle(self, cr, x, y, w, h, rgb, alpha):
        cr.set_source_rgba(*self.color_to_rgba(rgb, alpha))
        cr.rectangle(x, y, w, h)
        cr.fill()
        
    def row_number_to_string(self, row):
        start_len = len(list(str(self.current_row)))
        end_len  = len(list(str(row)))
        num_len = start_len - end_len
        string_row = ""
        for i in xrange(1, num_len+1):
            string_row += "0"
        string_row += str(row)
        return string_row
        
    def get_press_cursor_position(self, widget, event, row):
        '''Get index at event.'''
        rect = widget.allocation
        cr = widget.window.cairo_create()
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_size, self.font_size)))
        
        token_all_width = 0
        rect = widget.allocation 
        temp_padding_x =  self.row_border_width + self.code_folding_width
        
        self.cursor_column = 0
        if event.x < temp_padding_x: 
            return 0                
        
        for ch in self.text_buffer_list[row]:
            min_padding_x = (rect.x +  temp_padding_x + token_all_width)
            max_padding_x = (rect.x + temp_padding_x + token_all_width + self.get_ch_size(ch)[0])
            if min_padding_x <= (event.x) <= max_padding_x:
                break
            else:
                self.cursor_column += 1
                token_all_width += self.get_ch_size(ch)[0]
                
        return token_all_width
    
    def get_key_name(self, keyval):    
        key_unicode = gtk.gdk.keyval_to_unicode(keyval)
        
        if key_unicode == 0:
            return gtk.gdk.keyval_name(keyval)
        else:
            return str(unichr(key_unicode))
            
        
    def get_key_event_modifiers(self, key_event): 
        modifiers = [] 
        if key_event.state & gtk.gdk.CONTROL_MASK:
            modifiers.append("Ctrl")            
            
        if key_event.state & gtk.gdk.MOD1_MASK:
            modifiers.append("Alt")
            
        if key_event.state & gtk.gdk.SHIFT_MASK and (len(self.get_key_name(key_event.keyval)) != 1 or not gtk.gdk.keyval_is_upper(key_event.keyval)):        

            modifiers.append("Shift")
    
        return modifiers
    
    def get_keyevent_name(self, key_event):
        if key_event.is_modifier:
            return ""
        else:
            key_modifiers = self.get_key_event_modifiers(key_event)
            key_name      = self.get_key_name(key_event.keyval)
            if key_modifiers == []:
                return key_name
            else:
                if key_name == " ":
                    key_name = "Space"
                return " + ".join(key_modifiers) + " + " + key_name
    
    def start_to_end_string(self, 
                            row, 
                            start_column_1, end_column_1, 
                            start_column_2, end_column_2
                            ):
        start_string = self.text_buffer_list[row - 1][start_column_1:end_column_1]
        end_string   = self.text_buffer_list[row - 1][start_column_2:]
        return start_string, end_string
            
    def cursor_row_insert_text(self, column, text):
        # print column,text
        # self.text_buffer_list[self.cursor_row]
        start_text, end_text = self.start_to_end_string(
            self.cursor_row,
            0, column,
            column, len(self.text_buffer_list[self.cursor_row - 1])
            )
        # print "start:", start_text
        # print "end:", end_text        
        return start_text + text + end_text
    
    def cursor_down_vadjustment_set_value(self):
        temp_padding_row = 2
        max_row = self.get_scrolled_window_height()[2]
        if self.cursor_row >= max_row - temp_padding_row:
            temp_value = self.cursor_row - max_row + temp_padding_row
            set_temp_value = self.get_vadjustment().get_value() + temp_value * self.row_font_height
            self.get_vadjustment().set_value(set_temp_value)
            
    def cursor_up_vadjustment_set_value(self):            
        temp_padding_row = 2
        min_row = self.get_scrolled_window_height()[0]
        
        if self.cursor_row <= min_row + temp_padding_row:
            temp_value = min_row - self.cursor_row + temp_padding_row
            self.get_vadjustment().set_value(self.get_vadjustment().get_value() - temp_value * self.row_font_height)
                    
    def cursor_left_vadjustment_set_value(self):    
        pass
    
    def cursor_right_vadjustment_set_value(self):
        # temp_padding_column = 1        
        # self.get_hadjustment().set_value(self.get_hadjustment().get_value() + 10)
        pass
                
    
class Buffers(object):
    '''Init buffer.'''
    def __init__(self):
        self.save_buffer = []
        self.index = -1
        self.__BUFFER_MAX_NUM = 5
        
    def save_temp_buffer(self, buffer_dict):        
        if len(self.save_buffer) <= self.__BUFFER_MAX_NUM:
            self.save_buffer.append(buffer_dict)
            self.index += 1
            print self.index
            
    def next(self): # ctrl + Z
        if self.index +1 <= len(self.save_buffer) - 1:
            self.index += 1
            temp_save_buffer = self.save_buffer[self.index]            
            return temp_save_buffer
        
    def pre(self): # Ctrl + z
        if self.index != -1:
            if self.index >= 0:
                temp_save_buffer = self.save_buffer[self.index]
                self.index -= 1
                return temp_save_buffer                
    
##########################################        
### Test.    
if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("visual python-代码编辑器")
    win.set_size_request(500, 500)
    win.connect("destroy", gtk.main_quit)
    code_edit = CodeEdit()
    # code_edit.read("/home/long/123.txt")
    # code_edit.read("/home/strom/123.py")
    win.add(code_edit)
    win.show_all()
    gtk.main()
