# sotfs_save_backup_and_swap
Simple python script for backing up dark souls 1,2,3, Sekiro, probably also Elden Ring save files - and for bypassing the limited character slots per save file by allowing easy swapping between files.

## To Start
Populate config.config:

save_string: No major purpose, don't use special characters.
	
save_path: The path to the game's save file - including the file. Usually in Appdata/Roaming
	
chardir: The directory in which you wish to store characters/backup profiles. Can leave as is when running script from its directory.
	
backup_interval: Interval between backups in seconds.