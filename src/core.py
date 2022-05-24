import src.static as v
from os import listdir
from shutil import copyfile
from datetime import datetime

current_char_name=None

def generate_config():
    from os import getenv
    
    with open(f"./src/{v.config_filename}","r") as file:config_string=file.read()
    
    for i,gamename in enumerate(v.game_list):
        print(f"{i}: {gamename}")
    gamename=input("Enter index of the game you wish to manage, or enter 'z' to enter custom values.")
    while True:
        try:
            gamename=int(gamename)
            gamename=v.game_list[gamename]
            break
        except ValueError:
            if gamename=="z":break
            else:gamename=input("Not a valid index, or 'z': try again.")
        except IndexError:
            gamename=input("Not a valid index, or 'z': try again.")
            
    if gamename=="z":
        print("Enter the full path to the desired save file,\ne.g.\n 'C:/Users/user/AppData/Roaming/DarkSoulsII/01100001061460b3/DS2SOFS0000.sl2'\n")
        save_file_path=input("")
    else:save_file_path=f"{getenv('APPDATA')}/{v.save_info_dict[gamename]}"
    
    while True:
        backup_interval=input("Enter the desired backup interval in seconds.")
        try:
            backup_interval=abs(float(backup_interval))
            if input(f"Is '{backup_interval}' seconds correct? y or n")=="y":
                break
        except ValueError:
            print("Not a valid number")
    
    
    
    config_string=config_string.replace("__save_string_response__",save_file_path)
    config_string=config_string.replace("__interval_response__",f"{backup_interval}")
    
    with open(v.config_filename,"w") as f:f.write(config_string)
    
    print(f"{v.config_filename} written.")
    
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

def check_current_char(current_exists,char_list):
    global current_char_name
    
    if not current_exists:
        print(f"'{v.char_filename}' not found.\n")
        if char_list:
            for i,val in enumerate(char_list):
                print(f"{i}: {val}")
            print("\nChoose the character to use as the currently selected character.\nEnter the index of a currently existing character to use that, or enter the name of a new character to be generated from the base save file.")
        else:
            print("Enter the name of a new character to be generated from the base save file and used as the currently selected character.")
        
        while True:
            new_char_name=input("\n\nEnter a new character name (or index of an existing character).\n")
            print("")
            if not new_char_name or not new_char_name.replace(" ",""):
                print("Enter something...")
                continue
            try:
                new_char_name=int(new_char_name)
                new_char_name=char_list[new_char_name]
            except ValueError:pass
            except IndexError:
                print(f"Not a valid index. Assuming you would like to name your character {new_char_name}.")
                new_char_name=str(new_char_name)
            
            # try to avoid invalid folder names
            test=[i for i in '<">/\\|?*:.' if i in new_char_name]
            if test:
                for i in test:
                    print(f'The following symbol cannot be included in the name: {i}')
                continue
            
            print(f"New character will be named '{new_char_name}'.\nIs this correct, 'y' or 'n'?")
            if input("")=="y":break
        
        with open(v.char_filename, "w") as f:f.write(new_char_name)
        current_char_name=new_char_name
        
        
    
    else:
        with open(v.char_filename,"r") as f:current_char_name=f.read()
    
    if not current_char_name in char_list:
        # make backup of save currently in game's saves
        copyfile(config.save_path,"char_reconstruction_backup.sl")
        print("\nPreviously present save file backed up as char_reconstruction_backup.sl\n")
        
        make_new_char(current_char_name)
        restore_char(current_char_name)
        

def input_new_char_name():

    while True:
        new_char_name=input("\n\nEnter a new character name\n\n")
        if not new_char_name or not new_char_name.replace(" ",""):
            print("Enter something...")
            continue
        
        # try to avoid invalid folder names
        test=[i for i in '<">/\\|?*:.' if i in new_char_name]
        if test:
            for i in test:
                print(f'The following symbol cannot be included in the name: {i}')
        else:
            return(new_char_name)
def set_current_char_file(char_name):
    with open(v.char_filename, "w") as f:f.write(char_name)

def make_new_char(char_name):
    set_current_char_file(char_name)
    
    # make dir for new char
    from os import mkdir
    mkdir(f"{config.chardir}/{char_name}")
    
    copyfile(f"{config.chardir}/{v.base_save_name}",f"{config.chardir}/{char_name}/0.sl")
    
def restore_char(char_name):
    
    copyfile(listdir(f"{config.chardir}/{char_name}")[-1],config.save_path)
    
    
def backup_char(char_name=current_char_name):
    save_file_name=f"{datetime.now().strftime('%m%b-%d - %H-%M-%S')}.sl2"
    copyfile(config.save_path, f"{config.chardir}/{char_name}/{save_file_name}")
    print(f"{char_name}: {save_file_name}")
    
def check_char_dir(current_exists):
    
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
    
    check_current_char(current_exists,chardir_ls)

def character_manage():
    global current_char_name
    backup_char(current_char_name)
    
    import src.char_change_gui
    
    chardir_ls=listdir(config.chardir)
    chardir_ls.remove(v.base_save_name)
    
    chosen_char=src.char_change_gui.main( chardir_ls+["--NEW--"] )
    del src.char_change_gui
    
    if chosen_char not in char_list:
        chosen_char=input_new_char_name()
        make_new_char(chosen_char)
        restore_char(chosen_char)
    else:
        set_current_char_file(chosen_char)
        restore_char(chosen_char)
    
    current_char_name=chosen_char
    print(f"Current character set to: '{chosen_char}'")
    
    

def switch_character():
    pass

def startup():
    
    file_list=listdir("./")
    
    if not v.config_filename in file_list:
        generate_config()
    
    global config
    config=read_config()
    
    check_char_dir(v.char_filename in file_list)
    
    return(config)
    #if not v.char_filename in file_list: