from tkinter import filedialog as filedialogue, simpledialog as simpledialogue
import tkinter as tk
from tkinter import ttk


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
        ttk.Label(self.frame, text=label, width=20,).grid(column=0, row=self.pos[1])
        
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
    

def main(input_dict):
    global row_counter
    row_counter=1
    
    root = tk.Tk()
    root.title("Configuration")
    
    frame = ttk.Frame(root, padding=20)
    frame.grid()
    
    
    field_dict={
        "save_file_location":field_entry(root=root,frame=frame,start_vals=input_dict["save_file_location"],dialogue="file"),
        "chardir":field_entry(root=root,frame=frame,start_vals=input_dict["chardir"],dialogue="dir"),
        "backup_interval_seconds":field_entry(root=root,frame=frame,start_vals=input_dict["backup_interval_seconds"]),
    }
    
    def update_and_terminate():
        for field in field_dict.values():field.update_self_value()
        root.destroy()
        
    ttk.Label(frame, text="Configuration", width=20,).grid(column=0, row=0,columnspan=3)
    
    
    row_counter+=1
    ttk.Button(frame, text="Confirm", command=update_and_terminate).grid(column=1, row=row_counter)
    
    def fullclose():
        root.destroy()
        from sys import exit
        exit()
    root.protocol('WM_DELETE_WINDOW', fullclose)
    
    def tkquit():root.destroy()
    
    root.mainloop()
    
    config_dict={index: field.get_value() for index,field in field_dict.items()}
    
    return(config_dict)