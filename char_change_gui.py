import tkinter as tk

class display_params:
    button_width=30
    button_height=5
    reduced_button_width=int(button_width*0.8)
    
    padx,pady=2,5
    col_max=5
    
    fullwidth=(button_width+padx)*(col_max+1)
    
    fgcol="white"
    bgcol="black"
    
def increment_grid():
    global cur_row
    global cur_col
    
    cur_col+=1
    if cur_col>display_params.col_max:
        cur_col=0
        cur_row+=1

cur_row,cur_col=1,0

global out_char_name
out_char_name=None

class button_builder():
    def __init__(self,char_name, frame, root):
        self.char_name=char_name
        self.frame=frame
        self.root=root
        self.pack_self()
    def pack_self(self):
        
        self.button = tk.Button(self.frame,text=self.char_name,width=display_params.button_width, height=display_params.button_height,command=self.get_name)
        
        self.button.grid(row=cur_row,column=cur_col,padx=display_params.padx,pady=display_params.pady)
        increment_grid()
    def get_name(self):
        global out_char_name
        out_char_name=self.char_name
        self.root.destroy()
    
def main(character_list):

    root=tk.Tk()
    root.title("Character Select")
    
    root.tk_setPalette(foreground=display_params.fgcol,background=display_params.bgcol)
    
    def fullclose():
        root.destroy()
        from sys import exit
        exit()
    root.protocol('WM_DELETE_WINDOW', fullclose)
    
    def tkquit():root.destroy()
    
    mainframe=tk.Frame(root)
    
    greeting=tk.Label(mainframe,text="Choose Character to Enable",width=display_params.fullwidth,height=3,bg=display_params.fgcol,fg=display_params.bgcol)
    greeting.grid(row=0,column=0,columnspan=display_params.col_max+1)
    
    button_list=[button_builder(char_string,mainframe,root) for char_string in character_list]
    
    mainframe.pack()
    
    root.mainloop()
    return(out_char_name)