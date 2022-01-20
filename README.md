# sotfs_save_backup_and_swap
Simple python script for backing up dark souls 1,2,3, Sekiro, probably also Elden Ring save files - and for bypassing the limited character slots per save file by allowing easy swapping between files.

## To Start
* Make a manual backup of your save file. If you don't have a save file, launch the game and enter the main menu to generate one.
* Populate config.config:
	- save_string: Prefix of backed up saves, followed by date and time; don't use special characters. Match the game's default save string to more easily restore back-ups - or use something shorter for easier readability.
	- save_path: The path to the game's save file - including the file. Usually in Appdata/Roaming
	- chardir: The directory in which you wish to store characters/backup profiles. Can leave as is when running script from its directory.
	- backup_interval: Interval between backups in seconds. Default of 300(s).
* Run script, and only press Enter to backup current character, named after the current contents of current.char (can change or leave as DEFAULT_CHAR). This will generate the characters directory, and two subdirectories - one named after the current.char, and one named 'base'.
* Press Ctrl+C to end the backup loop. This generates an additional backup, then closes the script.
* Copy a save file into the 'base' subdirectory of your character directory, and rename it to match your chosen save_string from config.config. This file will be copied and used as the base save file whenever a new profile is created - it is recommended to clear any contained characters for convenience. In DSII, you can save before creating a character, allowing you to quickly begin anew.
* To create new or switch save profiles, start the script, type anything, then hit Enter to bring up the GUI. This will list the save profiles (sub-directories of the character directory, excluding 'base'), and an additional option titled '--NEW--'.
	- Selecting a save will backup the current, then switch profiles to that. The backup loop will then ensue.
	- Selecting '--NEW--' will backup the current profile, then prompt you to enter the desired name for the new profile. Do so, and the backup file in 'base' will be used as the base of this new profile. This new profile will be set as the current profile, and the backup loop will ensue.
* Backed-up files will be named by date and time. To restore a save file, copy the chosen backup over to the save directory and overwrite the existing save file, renaming it to match.
