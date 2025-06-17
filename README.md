# DIVA-Blender_Addons
DIVAのモデル編集に活用するBlenderアドオン集。  
コードは **Microsoft Copilot** を使用して生成され、一部調整が加えられています。  
**Blender 3.6** にて検証済み。

- **Bone Position Rotation Scale**
  - Blenderのアーマチュアからボーンデータ（位置・回転・スケール・親ボーン情報）を取得し、ファイルに保存するためのツール。
  - Saltlapse氏が公開しているコード（[GitHubリポジトリ](https://github.com/Saltlapse/Blender-Mod-Scripts)）のBlenderアドオン化。  

- **Bone Rename Tools**
  - DIVA独自の左右ボーン名規則をBlender標準機能では対応させるツール。
  - DIVAの左右識別子を検出して**.R** **.L**形式を付与する。または取り除く。
  - 細分化で変わってしまったボーン名・頂点グループ名をDIVAの連番規則に合わせてリネームもできる。

- **Bone Transfer Tools**
  - ボーンを簡単に移植するためのツール。  

- **Splite Mirror Weight**
  - オリジナルを左右反転したオブジェクト（メッシュ）を作成する。
  - ウエイトも左右反転に対応。
  

各アドオンの詳細については [Wiki](https://github.com/Riel2982/DIVA-PVDataManager/wiki)を確認してください。 
