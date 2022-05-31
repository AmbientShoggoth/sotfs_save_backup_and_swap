import src.static as v
from os import listdir
from shutil import copyfile
from datetime import datetime

current_char_name=None

import src.config_gui

def generate_config(current_exists):
    from os import getenv,getcwd
    
    with open(f"./src/{v.config_filename}","r") as file:config_string=file.read()
    
    
    
    gui_start_dict={
        "save_file_location":("",getenv('APPDATA')),
        "chardir":("characters",getcwd()),
        "backup_interval_seconds":("300",""),
    }
    
    if not current_exists:
        gui_start_dict["starting_character"]=("","")
    
    
    config_dict=src.config_gui.config_gui(gui_start_dict)
    
    if "starting_character" in gui_start_dict:
        set_current_char_file(config_dict["starting_character"])
    
    config_string=config_string.replace("__save_string_response__",config_dict["save_file_location"])
    config_string=config_string.replace("__interval_response__",f"{config_dict['backup_interval_seconds']}")
    config_string=config_string.replace("__characters__",f"{config_dict['chardir']}")
    
    
    with open(v.config_filename,"w") as f:f.write(config_string)
    
    print(f"{v.config_filename} written.")
    
    return()
    
def read_config():
    with open(f"./{v.config_filename}","r") as file:config_string=file.read()
    
    config_list=config_string.split("\n")
    config_list=[i.split("=") for i in config_list]
    config_dict={i[0]:i[1] for i in config_list}
    
    class c:pass
    c.sleeptime=float(config_dict["backup_interval_seconds"])
    c.save_path=config_dict["save_file_location"]
    c.chardir=config_dict["chardir"]
    
    return(c)



def gen_base_char():
    
    
    print(f"Copying base save file to characters directory '{config.chardir}', from game's save directory, as '{v.base_save_name}'.\n\nIt may be desireable to use a blank slate save file for this.\nTo update the base save file, delete it and rerun the tool.")
    
    copyfile(config.save_path,f"{config.chardir}/{v.base_save_name}")

def check_current_char(char_list):
    global current_char_name
    
    with open(v.char_filename,"r") as f:
        current_char_name=f.read()
    
    if not current_char_name in char_list:
        # make backup of save currently in game's saves
        copyfile(config.save_path,"char_reconstruction_backup.sl")
        print("\nPreviously present save file backed up as char_reconstruction_backup.sl\n")
        
        make_new_char(current_char_name)
        restore_char(current_char_name)

def set_current_char_file(char_name):
    with open(v.char_filename, "w") as f:f.write(char_name)

def make_new_char(char_name):
    set_current_char_file(char_name)
    
    # make dir for new char
    from os import mkdir
    mkdir(f"{config.chardir}/{char_name}")
    
    print(f"{config.chardir}/{v.base_save_name}",f"{config.chardir}/{char_name}/0.sl")
    copyfile(f"{config.chardir}/{v.base_save_name}",f"{config.chardir}/{char_name}/0.sl")
    
def restore_char(char_name):
    dirname=f"{config.chardir}/{char_name}"
    #f"{dirname}/{listdir(dirname)[-1]}"
    #listdir(f"{config.chardir}/{char_name}")[-1]
    copyfile(f"{dirname}/{listdir(dirname)[-1]}",config.save_path)
    
    
def backup_char(char_name=current_char_name):
    save_file_name=f"{datetime.now().strftime('%m%b-%d - %H-%M-%S')}.sl2"
    copyfile(config.save_path, f"{config.chardir}/{char_name}/{save_file_name}")
    print(f"{char_name}: {save_file_name}")
    
def check_char_dir():
    
    from os.path import isdir
    
    while not isdir(config.chardir):
        from os import getcwd
        
        print(f"Cannot find character directory, attempting to generate...")
        
        from os import mkdir
        try:
            mkdir(config.chardir) #mkdir to avoid creation of subdirectories
            print("Complete")
        except FileNotFoundError:
            print(f"Unable to locate or create character directory\n'{config.chardir}'")
            input("Manually create this directory and hit enter, or amend the path in 'config.ini' and restart the tool\n.")
    
    chardir_ls=listdir(config.chardir)
    
    if not v.base_save_name in chardir_ls:gen_base_char()
    else:chardir_ls=[i for i in chardir_ls if not i==v.base_save_name]
    
    check_current_char(chardir_ls)

def character_manage():
    if not src.config_gui.loop_or_manage_decision_gui():return()
    
    global current_char_name
    backup_char(current_char_name)
        
    chardir_ls=listdir(config.chardir)
    chardir_ls.remove(v.base_save_name)
    chardir_ls=[i for i in chardir_ls if not "." in i]
    
    chosen_char,is_new=src.config_gui.char_change_gui(chardir_ls)
    
    if is_new:
        make_new_char(chosen_char)
        restore_char(chosen_char)
    else:
        set_current_char_file(chosen_char)
        restore_char(chosen_char)
    
    current_char_name=chosen_char
    print(f"Current character set to: '{chosen_char}'")
    return(current_char_name)
    
    
    

def switch_character():
    pass

def startup():
    
    file_list=listdir("./")
    
    if not v.config_filename in file_list:
        generate_config(v.char_filename in file_list)
    
    global config
    config=read_config()
    
    check_char_dir()
    
    return(config,current_char_name)
    #if not v.char_filename in file_list: