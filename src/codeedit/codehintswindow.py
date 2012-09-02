


import gtk

class CodeHintsWindow(gtk.Window):
    def __init__(self, width=150, height=100):
        gtk.Window.__init__(self)
        # alignment.
        self.win_ali = gtk.Alignment()
        # set window size.
        self.set_size_request(width, height)
        # Set window type.
        # self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_COMBO)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)
        # Taskbar hide taskbar.
        self.set_skip_taskbar_hint(True)
        self.set_decorated(False)
        # Set window keep above.
        # self.set_keep_above(True)        
        
        # Scrolledwindow init.
        self.scrol_win = gtk.ScrolledWindow()
        self.scrol_win.set_policy(
            gtk.POLICY_AUTOMATIC,
            # gtk.POLICY_AUTOMATIC
            gtk.POLICY_ALWAYS
            )
        
        # strings show.
        self.show_text_list = gtk.Button()
        self.show_text_list_bg_color = "#FFFFFF"        
        
        self.show_text_list_border_width = 20
        self.show_text_list_border_color = "#ADD8E6"
        
        self.scrol_win.add_with_viewport(self.show_text_list)

        self.win_ali.set(1, 1, 1, 1)
        self.win_ali.set_padding(2, 2, 2, 2)
        self.win_ali.add(self.scrol_win)
        self.add(self.win_ali)
                
        # Init window connect.
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("expose-event",     self.window_expose_event)
        # Init text list connect.
        self.show_text_list.connect("expose-event", self.show_text_list_expose_event)
        # self.show_text_list.connect("button-press-event", )                
                
    ######################################################3    
    ### show text list.    
    def show_text_list_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation                        
        # draw background.
        alpha = 1
        self.show_text_list_draw_background(cr,
                                            rect.x, rect.y, 
                                            rect.width, rect.height, 
                                            self.show_text_list_bg_color, alpha)
        # draw border.
        self.show_text_list_draw_border(cr,
                                        rect.x, rect.y,
                                        self.show_text_list_border_width, rect.height,
                                        self.show_text_list_border_color, alpha)        
        
        return True
    
    def show_text_list_draw_background(self,
                                       cr,
                                       x, y, w, h,
                                       color, alpha
                                       ):    
        self.draw_fill_rectangle(
            cr,
            x, y, w, h,
            color, alpha
            )
        
    def show_text_list_draw_border(self,
                                   cr,
                                   x, y, w, h,
                                   color, alpha):
        self.draw_fill_rectangle(
            cr,
            x, y, w, h,
            color, alpha)
    
    ##################################################################    
    ### window.    
    def window_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        
        # draw window background.
        self.draw_window_background(cr, rect)        
        
        if "get_child" in dir(widget) and widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
            
        return True
        
    def draw_window_background(self, cr, rect):        
        alpha = 1
        # draw background.
        self.draw_fill_rectangle(
            cr, rect.x, rect.y, 
            rect.width, rect.height,
            "#FFFFFF", alpha
            )
        # draw border.
        alpha = 1
        self.draw_stroke_rectangle(
            cr, rect.x, rect.y,
            rect.width, rect.height,
            "#000000", alpha            
            )
        alpha = 0.7
        self.draw_stroke_rectangle(
            cr, rect.x + 1, rect.y + 1, 
            rect.width - 2, rect.height - 2,
            "#A9A9A9", alpha
            )
        
    #############################################    
    ### Tool function.    
    def draw_fill_rectangle(self,
                            cr,
                            x, y,
                            w, h,
                            rgb, alpha
                            ):
        self.draw_rectangle(cr, x, y, w, h, rgb, alpha)
        cr.fill()
    
    def draw_stroke_rectangle(self, 
                              cr, 
                              x, y, 
                              w, h,
                              rgb, alpha
                              ):    
        self.draw_rectangle(cr, x, y, w, h, rgb, alpha)
        cr.stroke() 
        
    def draw_rectangle(self, 
                       cr, 
                       x, y, 
                       w, h, 
                       rgb, alpha
                       ):
        cr.set_source_rgba(*self.color_to_rgba(rgb, alpha))
        cr.rectangle(
            x, y, w, h
            )        
        
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
        
    
