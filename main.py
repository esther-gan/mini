from GUI import *

app = Window()

# set window to 800x600 and place it in center of your screen
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

win_width = 800
win_height = 600

start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height/2))

app.geometry('{}x{}+{}+{}'.format(win_width, win_height, start_x, start_y))

app.mainloop()