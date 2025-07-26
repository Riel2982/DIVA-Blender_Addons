# DIVA-Blender_Addons
DIVAのモデル編集に活用するBlenderアドオン集。  
コードは **Microsoft Copilot** を使用して生成され、一部調整が加えられています。    
**Blender 3.6** にて検証済み。

- **Bone Position Rotation Scale**
  - Blenderのアーマチュアからボーンデータ（位置・回転・スケール・親ボーン情報）を取得し、ファイルに保存するためのツール。
  - Saltlapse氏が公開しているコード（[GitHubリポジトリ](https://github.com/Saltlapse/Blender-Mod-Scripts)）のBlenderアドオン化。  

- **Bone Rename Tools**
  - 選択したボーン列の連番をDIVAの規則に合わせて割り振り直すツール。
  - 選択したボーンの名前の一部を置き換える機能もあり。
  - DIVA独自の左右ボーン名規則をBlender標準機能で対応できるようにリネームすることも可能。
  - DIVAの左右識別子を検出して**.R** **.L**形式を付与することでBlenderのボーンX対称操作に対応可能。元に戻すことも可能。

- **Bone Transfer Tools**
  - ボーンを簡単に移植するためのツール。  
  - 移植するボーンに合わせてMESHモード・BONEモード・MULTIモードの三つのモードを切り替えて実行できます。

- **Mesh Weight Reflector**
  - メッシュの鏡像反転版を作成するツール。
  - 頂点グループ名（ウエイト）の左右識別子も一緒に反転リネームされます。

- **Splite Mirror Weight**
  - 更新終了しました。
  - オリジナルを左右反転したオブジェクト（メッシュ）を作成する。
  - ウエイトも左右反転に対応。
  

各アドオンの詳細については [Wiki](https://github.com/Riel2982/DIVA-Blender_Addons/wiki)を確認してください。 
