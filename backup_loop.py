from shutil import copyfile
from datetime import datetime
from time import sleep
from os import makedirs, chdir as os_chdir,listdir
from os.path import isdir as os_isdir, dirname as os_dirname, realpath as os_realpath

class escapeException(Exception):pass

def main():
    # change working directory to file's directory
    os_chdir(os_dirname(os_realpath(__file__)))

    def config_parse(config_string):
        config_list=config_string.split("\n")
        config_list=[i.split("=") for i in config_list]
        config_dict={i[0]:i[1] for i in config_list}
        
        sleeptime=int(config_dict["backup_interval"])
        save_string=config_dict["save_string"]
        save_path=config_dict["save_path"]
        chardir=config_dict["chardir"]
        
        return(sleeptime,save_string,save_path,chardir)
    
    try:
        with open("config.config","r") as f:
            sleeptime,save_string,save_path,chardir=config_parse(f.read())
    except FileNotFoundError as err:
        print(f"\n\n'config.config' file missing.\n{err}")
        return()
    try:
        with open("current.char","r") as f:
            current_char=f.read()
            print(f"Current: {current_char}")
    except FileNotFoundError as err:
        print(f"\n\n'current.char' file missing.\n{err}")
        return()
    
    if not os_isdir(chardir):
        for dirs in [f"{chardir}/base",f"{chardir}/{current_char}"]:
            try:makedirs(dirs)
            except OSError as err:
                print(f"\n\nIssue with '{dirs}', ensure there are no special characters:\n{err}")
                return()

    def backup_file():
        timenow=datetime.now()
        outfilename=f"{save_string}~{timenow.strftime('%m%b-%d - %H-%M-%S')}"
        outfilepath=f"{chardir}/{current_char}/?{outfilename}"
        
        try:copyfile(save_path,outfilepath)
        except FileNotFoundError as err:
            print(f"\n\nFile missing: Check save_path '{save_path}' and that '{current_char}' folder exists in characters directory.\n{err}")
            raise escapeException
        except OSError as err:
            print(f"\n\nError: Ensure there are no special characters in save profile name: '{current_char}' and save_string '{save_string}'.\n{err}")
            raise escapeException
            
        print(f"Copied: {outfilename}")

    def change_character():
        backup_file()
        
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
        if not os_isdir(char_path):
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

if __name__=="__main__":
    try:main()
    except escapeException:pass
    input("")