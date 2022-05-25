# sotfs_save_backup_and_swap
A python tool for backing up and switching between dark souls 1,2,3, Sekiro, and Elden Ring save files - and for bypassing the limited character slots per save file.

# Getting Started:
## Preparations
Make a manual backup of your save file, just to be safe. This can be found in Documents/NBGI for the steam version of DaS, and AppData for the other games.

It may be desirable to make a 'blank slate' save file prior to running the tool for the first time - this will be used as the base for any new character/save profiles made by the tool.

Some of the games store some of the game's settings in the save file, so ensure these are as desired before running the tool.

## First Time Setup
When ready to start, run save_tool.py. In the configuration interface that should appear:
* browse to and select the save file of the chosen game for the 'Save Location' field;
* enter a folder in which the save backups will be stored for the 'Backup Directory' field- this can be either the name of a folder which will be created in the tool's directory, or the full path to a desired folder elsewhere;
* enter the desired interval between backups, in seconds for the 'Backup Interval' field. Enter a number (e.g. 100 or 15.5) only - any other input will result in periodic backups being disabled.
* Hit confirm.
When prompted, enter the name of your first character, and confirm it by entering 'y' and hitting Enter.

The next steps will be encountered on subsequent uses of the tool.

## Typical Usage
Upon launching the tool or completing first-time setup, you will be prompted for input. Either leave the field blank and hit Enter to continue to the backup loop, or enter any input and hit Enter to open the character management interface.

## Character Management Interface
Here you can select either an existing character, or choose to create a new character.

## Backup Loop
Here saves will be backed up to the currently active character/save's directory, at the interval chosen during configuration. To cease backups, hit ctrl+c, and one final backup will be performed and the tool will terminate.
