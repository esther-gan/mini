import tkinter as tk
from tkinter import ttk
import functools
import ast
from Stall import *
from Fonts import *

# inherit from tk.Tk
class Window(tk.Tk):
    
    # *args, **kwargs represent infinite number of arguments and 
    # keywords/named arguments that can be taken in
    def __init__(self, *args, **kwargs):
        
        # init the tk.Tk class to be inherited
        # set icon of GUI
        # set title of GUI
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default='dog.ico')
        tk.Tk.wm_title(self, 'Mini Project')
        
        # create instance variable to store instance of tk.Frame
        # scale this frame to the current window size
        # best to set weight
        # best to set weight
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # init empty dictionary
        self.frames = {}
        
        # for every frame
        for F in (MainMenu, ViewStalls, ShowMenu, AddStalls):
            
            # each frame/page takes in (tk.Frame(WindowInstance), WindowInstance)
            # which are parent and controller respectively
            frame = F(self.container, self)
            
            # creates dictionary {F: frame, F: frame, F: frame} for every F and its instance
            self.frames[F] = frame
            
            # scale to fill screen
            frame.grid(row=0, column=0, sticky='nsew')

        # calls the class method to show the MainMenu frame
        self.show_frame(MainMenu)
        
    # brings the specified frame to the top
    def show_frame(self, container):
        
        # retrieves value tagged to the container in the dictionary
        # {container: frame, container: frame, container: frame}
        frame = self.frames[container]
        frame.tkraise()
        
            
    # same as show_frame but also takes in name of the current stallInstance
    def show_menu(self, container, name):
        frame = self.frames[container]
        frame.tkraise()
        
        for label in frame.labels:
            label.destroy()
        
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
                        label_key = tk.Label(frame, text=key, font=label_font)
                        label_value = tk.Label(frame, text=value, font=label_font)
                        
                        label_key.grid(row=frame.row, column=frame.column)
                        
                        frame.column += 1
                        
                        label_value.grid(row=frame.row, column=frame.column)
                        
                        frame.row +=1
                        frame.column = 0
                        
                        frame.labels.append(label_key)
                        frame.labels.append(label_value)
                        
    def popup(self, msg):
        popup = tk.Tk()
        
        popup.wm_title('test')
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        win_width = 100
        win_height = 60

        start_x = int((screen_width/2) - (win_width/2))
        start_y = int((screen_height/2) - (win_height/2))

        popup.geometry('{}x{}+{}+{}'.format(win_width, win_height, start_x, start_y))
        
        label = ttk.Label(popup, text=msg)
        label.pack(side='top', fill='x', pady=10)
        button = ttk.Button(popup, text='Okay', command=popup.destroy)
        button.pack()
                        

        
# main page that inherits from tk.Frame that was init in Window
class MainMenu(tk.Frame):
    
    # recall (parent, controller) is (tk.Frame(WindowInstance), WindowInstance)
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text='Welcome!', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        style = ttk.Style()
        style.configure('general.TButton', font = ('Time News Roman','25'))
        
        # when clicked, runs lambda command which runs show_frame method
        # lambda is used so as to run the method only when clicked
        # if no lambda, method runs at runtime
        # lambda is an anonymous function as compared to functools.partial later in the code
        # the latter is preferred as its not anonymous and allows preloading a function
        # and freezing preloaded args, allowing for more args if needed
        button1 = ttk.Button(self, text='View Stalls', style='general.TButton',
                             command=lambda: controller.show_frame(ViewStalls))
        
        # fix button to middle even if window is scaled
        button1.place(anchor='center', rely=0.4, relx=0.5, height=100, width=400)
        
        button2 = ttk.Button(self, text='Add Stalls', style='general.TButton',
                             command=lambda: controller.show_frame(AddStalls))
        
        button2.place(anchor='center', rely=0.6, relx=0.5, height=100, width=400)
        
        
class ViewStalls(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        style = ttk.Style()
        style.configure('stall.TButton', font = ('Time News Roman','20'))
        
        back_button = ttk.Button(self, text='Back', command=lambda: controller.show_frame(MainMenu))
        back_button.pack(anchor='nw')
        
        
        with open('stall.txt', 'r') as data:
    
            lines = data.readlines()

            for line in lines:
                line = line.split('/')
                line[4] = ast.literal_eval(line[4])
                stall = Stall(line[0], line[1], line[2], line[3], line[4])
                
                # functools.partial takes in as args a method, a frame and the name of a stallInstance
                # the method takes the last 2 args as its own args and runs only when clicked
                # instead of running with every stall objects's name at initialization
                button_x = ttk.Button(self, text=stall.name, style='stall.TButton',
                                      command=functools.partial(controller.show_menu, ShowMenu, stall.name))
                button_x.pack(anchor='center')
                
                
        
class ShowMenu(tk.Frame):
    
    row = 1
    column = 0
    labels = []
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        back_button = ttk.Button(self, text='Back', command=lambda: controller.show_frame(ViewStalls))
        back_button.grid_rowconfigure(0, weight=1)
        back_button.grid_columnconfigure(0, weight=1)
        back_button.grid(row=0, column=0, sticky='nw')
         
        
                        
class AddStalls(tk.Frame):
    
    text = ['Stall Name', 'Opening Time', 'Closing Time', 'Item Name', 'Item Cost']
    row = 1
    column = 0
    entries = []
    states = []
    index = 0
    days = ''
    last = None
    menu = {}
    cost = ''
    item_name  = ''
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        back_button = ttk.Button(self, text='Back', command=lambda: controller.show_frame(MainMenu))
        back_button.grid(row=0, column=0, sticky='nw')
        
        for index in range(len(self.text)):
            label = tk.Label(self, text=self.text[index], font=label_font)
            label.grid(row=self.row, column=self.column)
            
            self.column += 1
            
            entry = ttk.Entry(self, font=field_font)
            entry.grid(row=self.row, column=self.column)
            
            self.entries.append(entry)
            
            self.row += 1
            self.column = 0
            
        add_button = tk.Button(self, text='Add', command=lambda: add(self), height=2)
        
        self.row -= 1
        self.column += 2
        
        add_button.grid(row=self.row, column=self.column)
        
        remove_button = tk.Button(self, text='Undo', command=lambda: undo(self, 'menu'), height=2)
        
        self.column += 1
        
        remove_button.grid(row=self.row, column=self.column)
        
        self.row += 1
        self.column = 0
        
        # create Check buttons for days open
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            variable = tk.IntVar()
            checkbutton = tk.Checkbutton(self, text=day, variable=variable, onvalue=1, offvalue=0)
            checkbutton.grid(row=self.row, column=self.column)
            
            self.states.append(variable)
            
            self.row += 1
            self.column = 0
        
        self.row += 1
        self.column = 0
        save_button = ttk.Button(self, text='Save', command=lambda: verify_save(self))
        save_button.grid(row=self.row, column=self.column)
        
        self.row += 1
        
        undo_button = ttk.Button(self, text='Undo', command=lambda: undo(self, 'stall'))
        undo_button.grid(row=self.row)
        
        # verifies entries are acceptable then saves
        def verify_save(self):
            
            # verify block
            try:
                name = self.entries[0].get()
                _open = self.entries[1].get()
                close = self.entries[2].get()

                # checks if all are letters
                for letter in name:
                    if letter.lower() not in alphabets:
                        raise EOFError

                # check if ':' in in the times
                if ':' not in _open or ':' not in close:
                    raise EOFError

                # check if all are numbers
                for number in _open:
                    if number not in numbers:
                        raise EOFError

                for number in close:
                    if number not in numbers:
                        raise EOFError

                # check for 5 characters which guarantees HH:MM format at this point
                if len(_open) != len(close) or len(_open) != 5:
                    raise EOFError

                # get the state of the Checkbuttons
                # if checked, add corresponding number to self.days string
                # 0 for mon and so on
                for thing in self.states:
                    state = thing.get()
                    selected = 1
                    if state == selected:
                        self.days += str(self.index)

                    self.index += 1

                # append all the details in one line
                with open('stall_tmp.txt', 'a') as f:
                    seperator = '/'
                    self.menu = str(self.menu)
                    self.last = seperator.join((name, _open, close, self.days, self.menu))
                    f.write(self.last)

            except:
                controller.popup('Error')
                    
        def undo(self, string):
                        
            if string == 'stall':
            
                with open('stall_tmp.txt', 'r') as read:
                    lines = read.readlines()

                with open('stall_tmp.txt', 'w') as write:
                    for line in lines:
                        if line != self.last:
                            write.write(line)
                            
            if string == 'menu':
                
                del self.menu[self.last]
                        
        def add(self):
            
            self.item_name = self.entries[3].get()
            self.cost = self.entries[4].get()
            
            try:
                
                for letter in self.item_name:
                    if letter.lower() not in alphabets:
                        raise EOFError

                for number in self.cost:
                    if number not in money:
                        raise EOFError

                if '.' not in self.cost:
                    raise EOFError

                if len(self.cost.split('.')[1]) != 2:
                    raise EOFError

            except:
                controller.popup(('Error'))
            
            self.menu[self.item_name] = self.cost
            self.last = self.item_name