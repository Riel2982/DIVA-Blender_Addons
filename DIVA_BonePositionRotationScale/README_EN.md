## DIVA - Bone Position Rotation Scale  
### Overview  
This addon allows you to **extract bone data (position, rotation, scale, and parent bone info) from a Blender armature and save it to a file**.  
You can easily access it from the "DIVA" tab in the N Panel.  

### How to Use  
1. **Select the armature** from which you want to extract bone data.  
2. Open the **"DIVA" tab in the N Panel** and click **Export Bone Data**.  
3. A bone data file will be generated based on your settings.  

### Settings Options  
- **File Name**  
  - Enter the desired file name (without an extension).  
  - You can leave it as the default setting if needed.  
- **Export Path**  
  - Click the folder icon to set the save location.  
  - By default, the file will be saved in the same folder as the current `.blend` file.  
- **Auto Open File**  
  - Check this option if you want the exported file to open automatically after saving.  
- **Overwrite Existing File**  
  - Uncheck this option to prevent overwriting existing files.  
  - If unchecked, the addon will append a timestamp to new file names instead of replacing existing ones.  
- **Export as JSON**  
  - **By default, the file is saved in text format**.  
  - Check this option to save the data as a **JSON file** instead.  

### About the Code  
**Original script by Saltlapse.**  
This addon is based on a script published by Saltlapse on GitHub ([GitHub Repository](https://github.com/Saltlapse/Blender-Mod-Scripts)).  
While adapting it into an addon, I **kept the original script's structure mostly intact** while adding some features.  
Special thanks to Saltlapse for allowing this!   