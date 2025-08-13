## DIVA - Bone Position Rotation Scale  
### Overview  
This addon allows you to **extract bone data (position, rotation, scale, and parent bone info) from a Blender armature and save it to a file**.  
You can easily access it from the "DIVA" tab in the Sidebar.  

### How to Use: Bone Data Exporter  
1. **Select the armature** from which you want to extract bone data.  
2. Open the **"DIVA" tab in the Sidebar** and click **Export Bone Data**.  
3. A bone data file will be generated based on your settings.  

#### Settings Options  
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


### How to Use – Bone Data Checker  
1. In Object Mode, **select the armature from which you want to retrieve bone data**.  
2. In the **Bone Data Checker** section, click the **Export Bone Data** button.  
   It will switch to Edit Mode and display a list of bone names.  
3. Check the boxes next to the bones you want to inspect.  
4. Selected bone data will be displayed beneath the list.  
   Use the **Copy** button on the right to copy values and paste them into MMM.

#### Additional Notes  
- **List Mode** (List display filter)  
   - **Show All**: Displays all bones in the armature  
   - **Visible Only**: Hidden bones in the 3D View are excluded  
   - **Selected Only**: Displays only bones currently selected in the 3D View  
   - **Unselected Only**: Displays bones that are not currently selected  

- **+ / - buttons**  
   - Add or remove data-display checkmarks for bones selected in the 3D View  

- **Mouse Pointer icon**  
   - Select or deselect all bones shown in List Mode in the 3D View  

- **Checkbox icon**  
   - Mark or unmark all bones in List Mode as data-display targets


### About the Code  
**Original script by Saltlapse.**  
This addon is based on a script published by Saltlapse on GitHub ([GitHub Repository](https://github.com/Saltlapse/Blender-Mod-Scripts)).  
While adapting it into an addon, I **kept the original script's structure mostly intact** while adding some features.  
Special thanks to Saltlapse for allowing this!   