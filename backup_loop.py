from shutil import copyfile
from datetime import datetime
from time import sleep
from os import makedirs
from os.path import isdir

def config_parse(config_string):
    config_list=config_string.split("\n")
    config_list=[i.split("=") for i in config_list]
    config_dict={i[0]:i[1] for i in config_list}
    
    sleeptime=int(config_dict["backup_interval"])
    save_string=config_dict["save_string"]
    save_path=config_dict["save_path"]
    chardir=config_dict["chardir"]
    
    return(sleeptime,save_string,save_path,chardir)

with open("config.config","r") as f:
    sleeptime,save_string,save_path,chardir=config_parse(f.read())

with open("current.char","r") as f:
    current_char=f.read()
    print(f"Current: {current_char}")

if not isdir(chardir):
    makedirs(f"{chardir}/base")
    makedirs(f"{chardir}/{current_char}")

def backup_file():
    timenow=datetime.now()
    outfilename=f"{save_string}~{timenow.strftime('%m%b-%d - %H-%M-%S')}"
    outfilepath=f"{chardir}/{current_char}/{outfilename}"
    copyfile(save_path,outfilepath)
    print(f"Copied: {outfilename}")

def change_character():
    backup_file()
    from os import listdir
    import char_change_gui
    char_list=listdir(chardir)
    char_list.remove("base")
    new_char=char_change_gui.main( char_list+["--NEW--"] )
    del char_change_gui
    
    if new_char not in char_list:
        new_char=input("Enter new character name: ")
    
    global current_char
    current_char=new_char
    char_path=f"{chardir}/{current_char}"
    if not isdir(char_path):
        makedirs(char_path)
        copyfile(f"{chardir}/base/{save_string}",f"{char_path}/{save_string}~{datetime.now().strftime('%m%b-%d - %H-%M-%S')}")
    
    last_file=[i for i in listdir(char_path) if save_string in i][-1]
    copyfile(f"{char_path}/{last_file}",save_path)
    
    with open("current.char","w") as f:f.write(new_char)
    

if input(f"Current Character: {current_char}, change?"):
    change_character()
    print(f"Current Character: {current_char}")

while True:
    try:
        backup_file()
        sleep(sleeptime)
    except KeyboardInterrupt:
        backup_file()
        break
