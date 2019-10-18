from GUI import *

date_selection = False
timerange_selection = False

application = Window()

# set window to 800x600 and place it in center of your screen
screen_width = application.winfo_screenwidth()
screen_height = application.winfo_screenheight()

win_width = 800
win_height = 600

start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height/2))

application.geometry('{}x{}+{}+{}'.format(win_width, win_height, start_x, start_y))

application.mainloop()