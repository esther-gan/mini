import tkinter as tk
from tkinter import ttk
import functools
import ast
import datetime
from dateutil.parser import parse
import random
import tkcalendar
import time
from Fonts import *
from StallModule import Stall

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default='dog.ico')
        tk.Tk.wm_title(self, 'Mini Project')
        
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (MainMenu, ViewStalls, ShowMenu):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(MainMenu, 'load')
            
    def show_frame(self, container, string):
        if string == 'load':
            print('loading')
            frame = self.frames[container]
            frame.grid(row=0, column=0, sticky='nsew')
            frame.tkraise()
        
        if string == 'refresh':
            print('refreshing')
            frame = container(self.container, self)
            self.frames[container] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.tkraise()
        
        if string != 'load' and string != 'refresh':
            print('wrong string:', string, type(string))

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text='Welcome!', font=main_menu_heading_font)
        label.pack(pady=10, padx=10)
        
        style = ttk.Style()
        style.configure('general.TButton', font = ('Time News Roman','25'))
        
        button1 = ttk.Button(self, text='View Stalls', style='general.TButton',
                             command=lambda: controller.show_frame(ViewStalls, 'load'))
        
        button1.place(anchor='center', rely=0.5, relx=0.5, height=100, width=400)

class ViewStalls(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global date_selection
        global timerange_selection
        choices = []

        print('Initialized, date_selection = {}, timerange_selection = {}'.format(date_selection, timerange_selection))
        
        # config fonts
        style = ttk.Style()
        style.configure('stall_name.TButton', font = ('Helvetica','30'))
        #style.configure('back.TButton', font = ('Helvetica','30'), foreground='maroon')

        back_button = ttk.Button(self, text='Back', style='',
                                 command=lambda: controller.show_frame(MainMenu, 'load'))
        back_button.pack(anchor='nw')
        
        # check if date selected
        # if yes then create button with the date
        # if not then see else:
        if date_selection:
            # gen timeranges
            delta = datetime.timedelta(hours=1)
            gen_time = parse('00:00')
            for i in range(24):
                time_range = ('{}-{}'.format(gen_time.time(), '{}'))
                gen_time += delta
                choices.append(time_range.format(gen_time.time()))

            # add day to the button
            day = date_selection.weekday()
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            # refresh again
            select_date_button = ttk.Button(self, text=(days[day], date_selection),
                                            command=lambda: self.show_calendar(controller))
            select_date_button.pack(anchor='nw')
                
            # stuff to prepare for droplist
            self.variable = tk.StringVar(self)

            if not timerange_selection:
                print('Setting default value:', choices[8])
                self.variable.set(choices[8])
                timerange_selection = choices[8]
            
            else:
                print('Setting timerange_selection:', timerange_selection)
                self.variable.set(timerange_selection)
            
            # lambda *args: self.callback()
            self.variable.trace("w", lambda *args: self.callback(controller))

            # generate droplist
            options = tk.OptionMenu(self, self.variable, *choices)
            options.pack(anchor='nw')

        # run this if no date_selection
        # which will create a button to ask for date_selection
        else:
            calendar_button = ttk.Button(self, text='Select Date', style='',
                                         command=lambda: self.show_calendar(controller))
            calendar_button.pack(anchor='nw')

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
        
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)            
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # read data
        with open('stall.txt', 'r') as data:

            lines = data.readlines()

            for line in lines:
                line = line.split('/')
                line[4] = ast.literal_eval(line[4])
                stall = Stall(line[0], line[1], line[2], line[3], line[4])
                
                if not date_selection:
                    if stall.now_open():
                        # functools.partial takes in as args a method, a frame and the name of a stallInstance
                        # the method takes the last 2 args as its own args and runs only when clicked
                        # instead of running with every stall objects's name at initialization
                        button_x = ttk.Button(self.interior, text=stall.name, style='stall_name.TButton',
                                              command=functools.partial(self.show_menu, ShowMenu, controller, stall.name))
                        button_x.pack(anchor='center')
                else:
                    _open = parse(timerange_selection.split('-')[0]).time()
                    close = parse(timerange_selection.split('-')[1]).time()
                    if stall.is_open(_open, close, line[3]):
                        button_x = ttk.Button(self.interior, text=stall.name, style='stall_name.TButton',
                                              command=functools.partial(self.show_menu, ShowMenu, controller, stall.name))
                        button_x.pack(anchor='center')

    # store current timerange in global var, refresh ViewStalls
    def callback(self, controller, *args):
        global timerange_selection
        timerange_selection = self.variable.get()
        print('Running callback, timerange_selection = {}'.format(timerange_selection))
        controller.show_frame(ViewStalls, 'refresh')


    def show_calendar(self, controller):
        self.top = tk.Toplevel(self)
        self.top.geometry('{}x{}+{}+{}'.format(300, 250, 368, 132))
        self.cald = tkcalendar.Calendar(self.top)
        self.cald.pack(fill='both', expand=True)
        button = ttk.Button(self.top, text='Okay', style='',
                            command=lambda: self.print_sel(controller))
        button.pack(anchor='s')

    def print_sel(self, controller):
        global date_selection
        global timerange_selection
        date_selection = self.cald.selection_get()
        self.top.destroy()
        controller.show_frame(ViewStalls, 'refresh')

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())
            
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
            
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                                                  
    def show_menu(self, container, controller, name):
        controller.show_frame(container, 'refresh')
        
        frame = controller.frames[container]
        
        # read and store every line in variable lines
        with open('stall.txt', 'r') as data:
            
            lines = data.readlines()
            
            for line in lines:
                
                # split based on '/' which separates each piece of information when we saved it
                line = line.split('/')
                
                # dictionary was stored as string; this changes it to dictionary again
                line[4] = ast.literal_eval(line[4])
                
                # corresponds to Stall(name, _open, close, days, menu)
                stall = Stall(line[0], line[1], line[2], line[3], line[4])

                # if name of stall == name of stall when clicked, display items of menu
                if stall.name == name:
                    
                    # displaying items in menu
                    for key, value in stall.menu.items():
                        label_key = tk.Label(frame.interior, text=key, font=menu_font)
                        label_value = tk.Label(frame.interior, text=value, font=menu_font)
                        
                        label_key.pack()
                        label_value.pack()
        
        frame.tkraise()

class ShowMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        back_button = ttk.Button(self, text='Back', command=lambda: controller.show_frame(ViewStalls, 'load'))
        back_button.pack(anchor='nw')
        
        var = tk.StringVar(value='Enter number of people currently in queue.')
        self.waiting_field = tk.Entry(self, font=field_font, textvariable=var, width=36)
        self.waiting_field.config(fg = 'grey')
        self.waiting_field.pack(anchor='nw')
        
        self.waiting_field.bind('<FocusIn>', lambda *args: self.on_entry_click())
        self.waiting_field.bind('<FocusOut>', lambda *args: self.on_focusout())
        
        calculate_button = ttk.Button(self, text='Calculate', command=lambda: self.waiting_time(var.get()))
        calculate_button.pack(anchor='nw')
        
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        self.canvas.pack(anchor=tk.N, fill=tk.BOTH, expand=True)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
        
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)            
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())
            
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
            
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def on_entry_click(self):
        print('in')
        if self.waiting_field.get() == 'Enter number of people currently in queue.':
            self.waiting_field.delete(0, "end") # delete all the text in the entry
            self.waiting_field.insert(0, '') #Insert blank for user input
            self.waiting_field.config(fg = 'black')
    def on_focusout(self):
        print('out')
        if self.waiting_field.get() == '':
            self.waiting_field.insert(0, 'Enter number of people currently in queue.')
            self.waiting_field.config(fg = 'grey')
            
    def waiting_time(self, pax):
        print('calculating')
        total_time = 0
        
        try:
            pax = int(pax)
        
            # random float for time taken per pax
            for ppl in range(pax):
                time_taken = random.uniform(1, 3)
                total_time += time_taken

            self.top = tk.Toplevel(self)
            self.top.geometry('{}x{}+{}+{}'.format(200, 50, 368, 132))
            text = 'Estimated waiting time: {} minutes'.format(int(total_time))
            tk.Label(self.top, text=text).pack()
            ttk.Button(self.top, text='Okay', command=lambda: self.top.destroy()).pack()
            
        except:
            top = tk.Toplevel(self)
            top.geometry('{}x{}+{}+{}'.format(200, 50, 368, 132))
            tk.Label(top, text='Please enter a number.').pack()
            ttk.Button(top, text='Okay', command=lambda: top.destroy()).pack()

date_selection = False
timerange_selection = False
shrink_entry = False