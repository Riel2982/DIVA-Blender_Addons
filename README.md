# DIVA-Blender_Addons
DIVAのモデル編集に活用するBlenderアドオン集。  
コードは **Microsoft Copilot** および**ChatGPT**を使用して生成され、一部調整が加えられています。    
**Blender 3.6** にて検証済み。  

- **FBX Operatios Pack**  
  - FBXのインポートとエクスポートをサポートするツール。
  - 要標準アドオンFBX format。

- **Bone Position Rotation Scale**
  - Blenderのアーマチュアからボーンデータ（位置・回転・スケール・親ボーン情報）を取得するツール。
  - Saltlapse氏が公開しているコード（[GitHubリポジトリ](https://github.com/Saltlapse/Blender-Mod-Scripts)）のBlenderアドオン化。  

- **Bone Rename Tools**
  - DIVA独自のボーン規則名に合わせてリネームを行う関連ツール。
  - リネームと同時にボーンを複製・反転・追加する機能もあり。


- **Bone Transfer Tools**
  - ボーンを簡単に移植するためのツール。  
  - 移植するボーンに合わせてMESHモード・BONEモード・MULTIモードの三つのモードを切り替えて実行できます。
  - 現在開発中です。

- **Mesh Weight Reflector**
  - メッシュの鏡像反転版を作成するツール。
  - 頂点グループ名（ウエイト）の左右識別子も一緒に反転リネームされます。

  

各アドオンの詳細については [Wiki](https://github.com/Riel2982/DIVA-Blender_Addons/wiki)を確認してください。 


---

# DIVA-Blender_Addons(English)  
A collection of Blender addons designed to support editing DIVA models.  
The code was generated using **AI tools including Microsoft Copilot and ChatGPT**, with manual adjustments applied as needed.  
Verified on **Blender 3.6**.



- **FBX Operation Pack
  - fbx 
  - FBX format.

- **Bone Position Rotation Scale**  
  - Retrieves bone data (position, rotation, scale, and parent relationships) from Blender's armature system.  
  - Packaged as a Blender add-on based on code published by Saltlapse ([GitHub repository](https://github.com/Saltlapse/Blender-Mod-Scripts)).

- **Bone Rename Tools**  
  - Renames bones to follow DIVA-specific naming conventions.  
  - Also includes functions to duplicate, mirror, and add bones during renaming.

- **Bone Transfer Tools**  
  - Simplifies the process of transferring bones between armatures.
  - Currently under development.

- **Mesh Weight Reflector**  
  - Generates a mirror-image mesh with reflected vertex weights.  


Please refer to the [Wiki](https://github.com/Riel2982/DIVA-Blender_Addons/wiki#diva-blender_addonsenglish) for details about each addon.
 
