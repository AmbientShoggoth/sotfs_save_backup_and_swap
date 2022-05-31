from tkinter import filedialog as filedialogue, simpledialog as simpledialogue
import tkinter as tk
from tkinter import ttk

initialised=False

class field_entry():
    def __init__(self,root,frame,label="entry",start_vals=[],dialogue=False):
        
        self.root=root
        self.frame=frame
        
        self.get_position()
        
        self.set_label(label)
        
        self.start_val=start_vals[0]
        self.start_path=start_vals[1]
        
        self.entry=tk.Entry(self.frame)
        
        if not dialogue:
            self.grid_normal()
        else:
            self.grid_dialogue(dialogue)
        
        self.set_string(self.start_val)
        
    def set_label(self,label):
        ttk.Label(self.frame, text=label, width=30,).grid(column=0, row=self.pos[1])
        
    def get_position(self):
        global row_counter
        row_counter+=1
        
        self.pos=(1,row_counter)
        
    def grid_normal(self):
        self.entry.grid(column=self.pos[0],row=self.pos[1],columnspan=2)
    
    def grid_dialogue(self,dialogue_type):
        self.entry.grid(column=self.pos[0],row=self.pos[1])
        
        if dialogue_type=="file":
            self.command=self.open_file_dialogue
        elif dialogue_type=="dir":
            self.command=self.open_dir_dialogue
        else:
            print(f"\n\n\nImproper dialogue type {dialogue_type} for field with start value: {self.start_val}\n\n\n")
            self.command=self.open_dir_dialogue
        
        ttk.Button(self.frame, text="Browse", command=self.command).grid(column=self.pos[0]+1, row=self.pos[1])
    
    def open_dialogue(self,askopentype):
        
        if self.start_path:
            path=askopentype(parent=self.root,initialdir=self.start_path)
        else:
            path=askopentype(parent=self.root)
        
        self.set_string(path)
        
    def open_file_dialogue(self):
        self.open_dialogue(filedialogue.askopenfilename)
        
    def open_dir_dialogue(self):
        self.open_dialogue(filedialogue.askdirectory)
        
    def set_string(self,string):
        current_length=len(self.entry.get())
        if current_length:
            self.entry.delete(0,current_length+1)
        self.entry.insert(0,string)
    
    def update_self_value(self):
        self.value=self.entry.get()
    
    def get_value(self):
        return(self.value)



def config_gui(input_dict):
    global row_counter
    row_counter=1
    
    #root = tk.Tk()
    root=initialise()
    root.title("Configuration")
    
    #frame = ttk.Frame(root, padding=20)
    frame = ttk.Frame(root)
    frame.grid()
    
    
    field_dict={
        "save_file_location":field_entry(root=root,frame=frame,start_vals=input_dict["save_file_location"],dialogue="file",label="Save File"),
        "chardir":field_entry(root=root,frame=frame,start_vals=input_dict["chardir"],dialogue="dir", label="Backups Directory"),
        "backup_interval_seconds":field_entry(root=root,frame=frame,start_vals=input_dict["backup_interval_seconds"],label="Backup Interval (seconds)"),
        
    }
    
    if "starting_character" in input_dict:
        field_dict["starting_character"]=field_entry(root=root,frame=frame,start_vals=input_dict["starting_character"],label="Name of first ")
    
    def update_and_terminate():
        for field in field_dict.values():field.update_self_value()
        #root.destroy()
        frame.grid_remove()
        root.quit()
        
    ttk.Label(frame, text="Enter Configuration Parameters", ).grid(column=0, row=0,columnspan=3)
    
    
    row_counter+=1
    ttk.Button(frame, text="Confirm", command=update_and_terminate).grid(column=1, row=row_counter)
    
    
    
    def tkquit():root.destroy()
    
    root.mainloop()
    
    config_dict={index: field.get_value() for index,field in field_dict.items()}
    
    return(config_dict)


def char_change_gui(character_list):
    global row_counter
    row_counter=1
    
    new_char_name=None
    
    #root = tk.Tk()
    root=initialise()
    root.title("Character Selection")
    
    #frame = ttk.Frame(root, padding=20)
    frame = ttk.Frame(root)
    frame.grid()
    
    
    def new_char_terminate():
        new_char_field.update_self_value()
        new_char_name=new_char_field.get_value()
        
        #root.destroy()
        frame.grid_remove()
        root.quit()
        char_change_gui.returners=(new_char_name,True)
    
    def char_terminate(char_name):
        
        #root.destroy()
        frame.grid_remove()
        root.quit()
        char_change_gui.returners=(char_name,False)
    
    ttk.Label(frame, text="Select a character, or enter the name of a new one.", ).grid(column=0, row=0,columnspan=3)
    
    class char_button():
        def __init__(self,char_name):
            self.name=char_name
            
            global row_counter
            row_counter+=1
            
            ttk.Button(frame, text=self.name, command=self.command).grid(column=1, row=row_counter)
        def command(self):
            char_terminate(self.name)
    char_button_list=[char_button(i) for i in character_list]
    
    
    
    new_char_field=field_entry(root=root,frame=frame,start_vals=("",""),label="--New Character/Profile--")
    row_counter+=1
    ttk.Button(frame, text="Create", command=new_char_terminate).grid(column=1, row=row_counter)
    
    
    
    def tkquit():root.destroy()
    
    root.mainloop()
    return(char_change_gui.returners)

def loop_or_manage_decision_gui():
    global row_counter
    row_counter=1
    
    root=initialise()
    root.title("Decision")
    
    frame = ttk.Frame(root)
    frame.grid()
    
    
    def change_char_terminate():
        frame.grid_remove()
        root.destroy()
        loop_or_manage_decision_gui.returners=True
    
    def retain_char_terminate():
        frame.grid_remove()
        root.destroy()
        loop_or_manage_decision_gui.returners=False
    
    ttk.Label(frame, text="Choose to either proceed to the backup loop, or change save profile.", ).grid(column=0, row=0,columnspan=3)
    
    row_counter+=1
    ttk.Button(frame, text="Continue", command=retain_char_terminate).grid(column=1, row=row_counter)
    ttk.Button(frame, text="Change Character", command=change_char_terminate).grid(column=2, row=row_counter)
    
    
    
    def tkquit():root.destroy()
    
    root.mainloop()
    return(loop_or_manage_decision_gui.returners)

def initialise():
    global initialised
    global main_root
    
    def fullclose():
        main_root.destroy()
        from sys import exit
        exit()
    
    
    if initialised:return(main_root)
    else:
        main_root=tk.Tk()
        main_root.protocol('WM_DELETE_WINDOW', fullclose)
        initialised=True
        return(main_root)
        