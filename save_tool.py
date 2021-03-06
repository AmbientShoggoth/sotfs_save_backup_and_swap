#from shutil import copyfile
#from datetime import datetime
from time import sleep
from os import makedirs, chdir as os_chdir,listdir
from os.path import isdir as os_isdir, dirname as os_dirname, realpath as os_realpath

class escapeException(Exception):pass

#import src.static as v
import src.core
    

def main():
    # change working directory to file's directory
    os_chdir(os_dirname(os_realpath(__file__)))
    
    
    global config
    config,char_name=src.core.startup()
    
    char_name_=src.core.character_manage()
    if char_name_:char_name=char_name_
    
    backup_loop(char_name)
    

def backup_loop(char_name):
    
    while True:
        src.core.backup_char(char_name)
        try:
            sleep(config.sleeptime)
        except KeyboardInterrupt:
            src.core.backup_char(char_name)
            break



if __name__=="__main__":
    try:main()
    except escapeException:pass
    input("Hit Enter to quit")