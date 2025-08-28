import bpy

translation_dict = {
    "ja_JP": {
        # fop_panel.py:40
        ("*", "Please enable Blenders built-in FBX format addon"): "Blender標準の『FBX format』アドオンを有効化してください",
        # fop_panel.py:53
        ("*", "Open the FBX Format addon settings in Preferences"): "FBX format アドオンのプリファレンス設定を開きます",
        # fop_types.py:25
        ("*", "Save with numbering if a file with the same name exists"): "同名ファイルがある場合はナンバリングして保存",
        # fop_types.py:26
        ("*", "Always save blend files with numbering to prevent overwriting existing files"): "ファイル名にナンバリングを付けて保存",
        # fop_types.py:38
        ("*", "Disable Blenders Automatically Pack Resources when saving in UNPACK mode"): "パック解除モードで保存するときに、Blenderのリソースの自動パック機能を無効化します",
        # fop_types.py:45
        ("*", "External data pack mode"): "外部データのパックモード選択",
        # fop_types.py:47, fop_types.py:60, fop_ui_save.py:63
        ("*", "Pack Resources"): "リソースをパック",
        # fop_types.py:48
        ("*", "Unpack Resources"): "パックしない",
        # fop_types.py:49, fop_types.py:64
        ("*", "Auto / Mixed"): "変更なし / 混在",
        # fop_types.py:49
        ("*", "Do not change packing state"): "外部データのリソース格納方式をそのままにします",
        # fop_types.py:55
        ("*", "External Data Storage Mode"): "外部データの格納方式",
        # fop_types.py:58
        ("*", "External data pass mode"): "外部データのパスモード選択",
        # fop_types.py:61
        ("*", "Make Paths Relative"): "相対パスで格納",
        # fop_types.py:62
        ("*", "Make Paths Absolute"): "絶対パスで格納",
        # fop_types.py:63, fop_types.py:64
        ("*", "Do not change external file paths"): "外部データのパス格納形式をそのままにします",
        # fop_types.py:63
        ("*", "Leave As-Is"): "変更なし",
        # fop_types.py:73
        ("*", "Import custom normals if they are available; if not, Blender will recompute them automatically"): "カスタム法線をインポート（できない場合はBlenderが自動的に再計算）",
        # fop_types.py:78
        ("*", "Create a new collection for imported FBX"): "コレクションを作成してFBXインポートデータを格納",
        # fop_types.py:84
        ("*", "Name of the FBX file to export"): "出力するFBXファイル名",
        # fop_types.py:90
        ("*", "Save with numbering if a data with the same name exists"): "同名ファイルがある場合はナンバリングして保存",
        # fop_types.py:91
        ("*", "Always save with numbering to prevent overwriting existing files"): "ファイル名にナンバリングを付けて保存",
        # fop_types.py:124
        ("*", "Show tool to save blend file"): "Blendファイルを保存するツールを表示",
        # fop_types.py:129
        ("*", "Show tool to import fbx data"): "FBXファイルを読み込むツールを表示",
        # fop_types.py:134
        ("*", "Show tool to export fbx data"): "FBXファイルを出力するツールを表示",
        # fop_types.py:140
        ("*", "Select the external data storage method"): "外部データの格納方法を選択",
        # fop_types.py:146
        ("*", "Folder to save blend file"): "Blendファイルの保存先フォルダ",
        # fop_types.py:152
        ("*", "Whether the blend file is saved"): "Blendファイルが保存されているかどうか",
        # fop_types.py:156
        ("*", "Name of the blend file to save"): "保存するBlendファイル名",
        # fop_types.py:161, fop_ui_export.py:40
        ("*", "Save in the same location as the blend file"): "Blendファイルと同じ場所に保存する",
        # fop_ui_export.py:36, fop_ui_save.py:68
        ("*", "Auto Numbering"): "自動ナンバリング保存（上書き防止）",
        # fop_ui_export.py:46
        ("*", "Export Options :"): "出力オプション",
        # fop_ui_export.py:53
        ("*", "Export FBX Data"): "Export FBX Data",
        # fop_ui_export.py:61
        ("*", "FBX Exported"): "FBXで出力",
        # fop_ui_export.py:65
        ("*", "Path to export FBX file"): "FBXファイルの保存場所",
        # fop_ui_export.py:111, fop_ui_export.py:125
        ("*", "Export filename is empty"): "ファイル名を設定してください",
        # fop_ui_export.py:173, fop_ui_export.py:214
        ("*", "No Armature found in export data"): "出力データにアーマーチュアが存在しません。確認してください",
        # fop_ui_export.py:184, fop_ui_export.py:221
        ("*", "There are {count} mesh objects not linked to any Armature"): "{count} 個のオブジェクトがアーマーチュアにペアレントされていません。確認してください",
        # fop_ui_export.py:237
        ("*", "FBX data exported to: {path}"): "FBX出力完了：{path}",
        # fop_ui_export.py:238, fop_ui_export.py:241
        ("*", "FBX data exported"): "FBX出力完了",
        # fop_ui_export.py:248
        ("*", "Please select where you would like to export the FBX file"): "FBXファイルの保存場所を選択してください",
        # fop_ui_import.py:26
        ("*", "Import Custom Normals"): "カスタム法線をインポート",
        # fop_ui_import.py:31
        ("*", "Import into New Collection"): "コレクションを作成",
        # fop_ui_import.py:33
        ("*", "Import FBX Data"): "Import FBX Data",
        # fop_ui_import.py:43
        ("*", "FBX Imported"): "FBXを読み込む",
        # fop_ui_import.py:70
        ("*", "FBX data imported to: {name}"): "FBXインポート完了：{name}",
        # fop_ui_import.py:79
        ("*", "Please select the FBX file you wish to import"): "FBXファイルを選択してください",
        # fop_ui_save.py:41
        ("*", "File Name :"): "ファイル名：",
        # fop_ui_save.py:47
        ("*", "Save Path :"): "保存場所：",
        # fop_ui_save.py:56, fop_ui_save.py:59
        ("*", "External Data :"): "外部データ：",
        # fop_ui_save.py:74, fop_ui_save.py:81, fop_ui_save.py:94
        ("*", "External data storage method selection"): "外部データ格納方式オプション",
        # fop_ui_save.py:101, fop_ui_save.py:109, fop_ui_save.py:87
        ("*", "Disable Auto-Pack"): "自動パック無効",
        # fop_ui_save.py:113
        ("*", "Pack Mode"): "パックモード",
        # fop_ui_save.py:114
        ("*", "Resources Packing Mode"): "リソースのパックモード",
        # fop_ui_save.py:120
        ("*", "Path Mode"): "パスモード",
        # fop_ui_save.py:121
        ("*", "External Data Path Mode"): "外部データパスモード",
        # fop_ui_save.py:139
        ("*", "Open dialog to select blend file save location"): "Blendファイル保存先選択ダイアグを開く",
        # fop_ui_save.py:154
        ("*", "Save location has been set"): "保存先を設定しました",
        # fop_ui_save.py:163
        ("*", "Save blend file"): "Blendファイルを保存する",
        # fop_ui_save.py:203
        ("*", "Please select a valid folder to save"): "有効な保存先フォルダを選択してください",
        # fop_ui_save.py:303
        ("*", "Invalid folder path"): "保存先が見つかりません",
        # fop_ui_save.py:308
        ("*", "Cannot write to the selected folder"): "保存先に書き込み権限がありません",
        # fop_ui_save.py:322, fop_ui_save.py:394
        ("*", "Cannot write to the selected location (permission denied)"): "アクセスが拒否されたため保存できません",
        # fop_ui_save.py:324, fop_ui_save.py:396
        ("*", "Blend file could not be saved because it is locked or in use"): "ファイルがロックされているため保存できません",
        # fop_ui_save.py:326, fop_ui_save.py:398
        ("*", "Invalid path. Please check the save location"): "保存先ファイルパスが存在しないため保存できません",
        # fop_ui_save.py:328, fop_ui_save.py:400
        ("*", "Failed to save Blend file: {error}"): "保存できませんでした：{error}",
        # fop_ui_save.py:353, fop_ui_save.py:378, fop_ui_save.py:467
        ("*", "Blend file has been saved"): "Blendファイルを保存しました",
        # fop_ui_save.py:359, fop_ui_save.py:446
        ("*", "Packed external data using relative paths and saved the Blend file as {name}.blend"): "外部データを相対パス形式でパックし、Blendファイルを{name}.blendで保存しました",
        # fop_ui_save.py:362, fop_ui_save.py:448
        ("*", "Packed external data using absolute paths and saved the Blend file as {name}.blend"): "外部データを絶対パス形式でパックし、Blendファイルを{name}.blendで保存しました",
        # fop_ui_save.py:365, fop_ui_save.py:453
        ("*", "Unpacked external data using relative paths and saved the Blend file as {name}.blend"): "外部データを相対パス形式でアンパックし、Blendファイルを{name}.blendで保存しました",
        # fop_ui_save.py:368, fop_ui_save.py:455
        ("*", "Unpacked external data using absolute paths and saved the Blend file as {name}.blend"): "外部データを絶対パス形式でアンパックし、Blendファイルを{name}.blendで保存しました",
        # fop_ui_save.py:371, fop_ui_save.py:450
        ("*", "Packed external data and saved the Blend file as {name}.blend"): "外部データをパックし、Blendファイルを{name}.blendで保存しました",
        # fop_ui_save.py:374, fop_ui_save.py:457
        ("*", "Unpacked external data and saved the Blend file as {name}.blend"): "外部データをアンパックし、Blendファイルを{name}.blendで保存しました",
        # fop_ui_save.py:413
        ("*", "Auto-pack disabled, using relative paths and saved the Blend file as {name}.blend"): "リソースの自動パック機能を解除して、相対パス形式でBlendファイルを{name}.blendとして保存しました",
        # fop_ui_save.py:415
        ("*", "Auto-pack disabled, using absolute paths and saved the Blend file as {name}.blend"): "リソースの自動パック機能を解除して、絶対パス形式でBlendファイルを{name}.blendとして保存しました",
        # fop_ui_save.py:417
        ("*", "Auto-pack disabled, paths unchanged, and saved the Blend file as {name}.blend"): "リソースの自動パック機能を解除して、Blendファイルを{name}.blendとして保存しました。",
        # fop_ui_save.py:419
        ("*", "Auto-pack detected and disabled. UNPACK re-applied before saving."): "自動リソースパック機能を無効化してそのまま保存しました",
        # fop_ui_save.py:424
        ("*", "Resources were automatically re-packed and using relative paths and saved the Blend file as {name}.blend"): "リソースの自動パック機能が有効状態です。外部データをパックして相対パス形式でBlendファイルを{name}.blendとして保存しました。",
        # fop_ui_save.py:426
        ("*", "Resources were automatically re-packed and using absolute paths and saved the Blend file as {name}.blend"): "リソースの自動パック機能が有効状態です。外部データをパックして絶対パス形式でBlendファイルを{name}.blendとして保存しました。",
        # fop_ui_save.py:428
        ("*", "Resources were automatically re-packed and saved the Blend file as {name}.blend"): "リソースの自動パック機能が有効状態です。外部データをパックしてBlendファイルを{name}.blendとして保存しました。",
        # fop_ui_save.py:430, fop_ui_save.py:439
        ("*", "Some resources were automatically re-packed and saved the Blend file as {name}.blend"): "リソースの自動パック機能が有効状態です。外部データをパックしてBlendファイルを{name}.blendとして保存しました",
        # fop_ui_save.py:460
        ("*", "Packing state kept as-is, paths made relative, and saved the Blend file as {name}.blend"): "相対パス形式でBlendファイルを{name}.blendとして保存しました",
        # fop_ui_save.py:462
        ("*", "Packing state kept as-is, paths made absolute, and saved the Blend file as {name}.blend"): "絶対パス形式でBlendファイルを{name}.blendとして保存しました",
        # fop_ui_save.py:464
        ("*", "Packing state kept as-is, paths unchanged, and saved the Blend file as {name}.blend"): "Blendファイルを{name}.blendとして保存しました",
        # fop_ui_save.py:482
        ("*", "Please select where you would like to export the blend file"): "Blendファイルを保存する場所を選択してください",
        # fop_uix_update.py:47
        ("*", "Update"): "アップデート",
        # fop_uix_update.py:50
        ("*", "Check for Updates"): "更新を確認",
        # fop_uix_update.py:53
        ("*", "Install"): "インストール",
        # fop_uix_update.py:54
        ("*", "Open Addon Folder"): "アドオンフォルダを開く",
        # fop_uix_update.py:65
        ("*", "GitHub has a recent release: "): "GitHubに最新リリースあり ",
        # fop_uix_update.py:79, fop_uix_update.py:80
        ("*", "GitHub has a recent release. "): "GitHubに最新リリースあり。",
        # fop_uix_update.py:84
        ("*", "Path to ZIP download folder "): "ZIP保存先フォルダ ",
        # fop_uix_update.py:94
        ("*", "Update file list: "): "更新ファイル一覧：",
        # fop_uix_update.py:128
        ("*", "Opens the GitHub release page to check for update files"): "GitHubのリリースページを開き、アップデートファイルを確認できます",
        # fop_uix_update.py:158
        ("*", "Download URL could not be retrieved"): "ダウンロードURLが取得できません",
        # fop_uix_update.py:166
        ("*", "Please specify a valid download folder and run again"): "ZIP保存先フォルダを指定後、再び実行してください",
        # fop_uix_update.py:178
        ("*", "Download completed"): "ダウンロードが完了しました",
        # fop_uix_update.py:181
        ("*", "Download failed"): "ダウンロードできませんでした",
        # fop_uix_update.py:189
        ("*", "Select a ZIP archive beginning with DIVA_FBXOperationPack to install the update"): "アップデートをインストールするには、DIVA_FBXOperationPackで始まるZIPファイルを選択してください",
        # fop_uix_update.py:195
        ("*", "Choose a ZIP file starting with DIVA_FBXOperationPack"): "DIVA_FBXOperationPackで始まるZIPファイルを選択してください",
        # fop_uix_update.py:211
        ("*", "Choose the folder where the addon is installed"): "アドオンがインストールされているフォルダを選択してください",
        # fop_uix_update.py:244
        ("*", "No ZIP file selected. Please specify a file"): "ZIPファイルが選択されていません。ファイルを指定してください",
        # fop_uix_update.py:254
        ("*", "No ZIP file selected"): "ZIPファイルを選択してください",
        # fop_uix_update.py:261
        ("*", "Only ZIP files starting with DIVA_FBXOperationPack can be processed"): "DIVA_FBXOperationPack で始まるZIPファイル以外は処理できません",
        # fop_uix_update.py:278
        ("*", "Missing DIVA_FBXOperationPack folder or __init__.py inside the ZIP file"): "ZIP内に DIVA_FBXOperationPack フォルダまたは __init__.py が見つかりません",
        # fop_uix_update.py:285
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "ZIP内の bl_info.name を取得できません",
        # fop_uix_update.py:308
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください",
        # fop_uix_update.py:314
        ("*", "Installation was cancelled"): "インストールはキャンセルされました",
        # fop_uix_update.py:322
        ("*", "__init__.py not found in the selected folder"): "選択されたフォルダに __init__.py が見つかりません",
        # fop_uix_update.py:329
        ("*", "Update failed because bl_info.name does not match"): "bl_info.name が一致しないため、更新できません",
        # fop_uix_update.py:368, fop_uix_update.py:89
        ("*", "Update completed. Please restart Blender"): "更新が完了しました。Blenderを再起動してください",
        # fop_uix_update.py:373
        ("*", "Update failed: {error}"): "更新に失敗しました: {error}",
        # fop_uix_update.py:381
        ("*", "Please select a ZIP file"): "ZIPファイルを選択してください",
        # fop_uix_update.py:382
        ("*", "Please restart Blender after the update"): "更新後はBlenderを再起動してください",
        # fop_uix_update.py:389
        ("*", "Opens the folder where this addon is installed"): "現在のアドオンフォルダを開く",
        # fop_uix_update.py:407
        ("*", "Scan the folder and list update candidate files"): "ZIPファイルリストの更新",
        # fop_uix_update.py:421
        ("*", "Download folder setting has been saved"): "DLフォルダ設定が保存されました",
        # fop_uix_update.py:445
        ("*", "Sort update files by file name. Click again to toggle order"): "ZIPファイル名ソート(A–Z / Z–A)",
        # fop_uix_update.py:464
        ("*", "Sort update files by update/download date. Click again to toggle order"): "日時順ソート(newest ↔ oldest)",
        # fop_uix_update.py:498
        ("*", "Specify the folder where the update ZIP is stored"): "更新用ZIPが保存されているフォルダを指定してください",
        # fop_uix_update.py:509
        ("*", "After selecting a ZIP file, click the Install button to update the currently installed addon"): "リストからZIPファイルを選び、インストールボタンをクリックすると、アドオンを更新できます",
    },
    "en_US": {
        # fop_panel.py:40
        ("*", "Please enable Blenders built-in FBX format addon"): "Please enable Blenders built-in FBX format addon",
        # fop_panel.py:53
        ("*", "Open the FBX Format addon settings in Preferences"): "Open the FBX Format addon settings in Preferences",
        # fop_types.py:25
        ("*", "Save with numbering if a file with the same name exists"): "Save with numbering if a file with the same name exists",
        # fop_types.py:26
        ("*", "Always save blend files with numbering to prevent overwriting existing files"): "Always save blend files with numbering to prevent overwriting existing files",
        # fop_types.py:38
        ("*", "Disable Blenders Automatically Pack Resources when saving in UNPACK mode"): "Disable Blender's Automatically Pack Resources when saving in Unpack Resources mode",
        # fop_types.py:45
        ("*", "External data pack mode"): "External data pack mode",
        # fop_types.py:47, fop_types.py:60, fop_ui_save.py:63
        ("*", "Pack Resources"): "Pack Resources",
        # fop_types.py:48
        ("*", "Unpack Resources"): "Unpack Resources",
        # fop_types.py:49, fop_types.py:64
        ("*", "Auto / Mixed"): "Auto / Mixed",
        # fop_types.py:49
        ("*", "Do not change packing state"): "Do not change packing state",
        # fop_types.py:55
        ("*", "External Data Storage Mode"): "External Data Storage Mode",
        # fop_types.py:58
        ("*", "External data pass mode"): "External data pass mode",
        # fop_types.py:61
        ("*", "Make Paths Relative"): "Make Paths Relative",
        # fop_types.py:62
        ("*", "Make Paths Absolute"): "Make Paths Absolute",
        # fop_types.py:63, fop_types.py:64
        ("*", "Do not change external file paths"): "Do not change external file paths",
        # fop_types.py:63
        ("*", "Leave As-Is"): "Leave As-Is",
        # fop_types.py:73
        ("*", "Import custom normals if they are available; if not, Blender will recompute them automatically"): "Import custom normals if they are available; if not, Blender will recompute them automatically",
        # fop_types.py:78
        ("*", "Create a new collection for imported FBX"): "Create a new collection for imported FBX",
        # fop_types.py:84
        ("*", "Name of the FBX file to export"): "Name of the FBX file to export",
        # fop_types.py:90
        ("*", "Save with numbering if a data with the same name exists"): "Save with numbering if a data with the same name exists",
        # fop_types.py:91
        ("*", "Always save with numbering to prevent overwriting existing files"): "Always save with numbering to prevent overwriting existing files",
        # fop_types.py:124
        ("*", "Show tool to save blend file"): "Show tool to save blend file",
        # fop_types.py:129
        ("*", "Show tool to import fbx data"): "Show tool to import fbx data",
        # fop_types.py:134
        ("*", "Show tool to export fbx data"): "Show tool to export fbx data",
        # fop_types.py:140
        ("*", "Select the external data storage method"): "Select the external data storage method",
        # fop_types.py:146
        ("*", "Folder to save blend file"): "Folder to save blend file",
        # fop_types.py:152
        ("*", "Whether the blend file is saved"): "Whether the blend file is saved",
        # fop_types.py:156
        ("*", "Name of the blend file to save"): "Name of the blend file to save",
        # fop_types.py:161, fop_ui_export.py:40
        ("*", "Save in the same location as the blend file"): "Save in the same location as the blend file",
        # fop_ui_export.py:36, fop_ui_save.py:68
        ("*", "Auto Numbering"): "Auto Numbering",
        # fop_ui_export.py:46
        ("*", "Export Options :"): "Export Options :",
        # fop_ui_export.py:53
        ("*", "Export FBX Data"): "Export FBX Data",
        # fop_ui_export.py:61
        ("*", "FBX Exported"): "FBX Exported",
        # fop_ui_export.py:65
        ("*", "Path to export FBX file"): "Path to export FBX file",
        # fop_ui_export.py:111, fop_ui_export.py:125
        ("*", "Export filename is empty"): "Export filename is empty",
        # fop_ui_export.py:173, fop_ui_export.py:214
        ("*", "No Armature found in export data"): "No Armature found in export data",
        # fop_ui_export.py:184, fop_ui_export.py:221
        ("*", "There are {count} mesh objects not linked to any Armature"): "There are {count} mesh objects not linked to any Armature",
        # fop_ui_export.py:237
        ("*", "FBX data exported to: {path}"): "FBX data exported to: {path}",
        # fop_ui_export.py:238, fop_ui_export.py:241
        ("*", "FBX data exported"): "FBX data exported",
        # fop_ui_export.py:248
        ("*", "Please select where you would like to export the FBX file"): "Please select where you would like to export the FBX file",
        # fop_ui_import.py:26
        ("*", "Import Custom Normals"): "Import Custom Normals",
        # fop_ui_import.py:31
        ("*", "Import into New Collection"): "Import into New Collection",
        # fop_ui_import.py:33
        ("*", "Import FBX Data"): "Import FBX Data",
        # fop_ui_import.py:43
        ("*", "FBX Imported"): "FBX Imported",
        # fop_ui_import.py:70
        ("*", "FBX data imported to: {name}"): "FBX data imported to: {name}",
        # fop_ui_import.py:79
        ("*", "Please select the FBX file you wish to import"): "Please select the FBX file you wish to import",
        # fop_ui_save.py:41
        ("*", "File Name :"): "File Name :",
        # fop_ui_save.py:47
        ("*", "Save Path :"): "Save Path :",
        # fop_ui_save.py:56, fop_ui_save.py:59
        ("*", "External Data :"): "External Data :",
        # fop_ui_save.py:74, fop_ui_save.py:81, fop_ui_save.py:94
        ("*", "External data storage method selection"): "External data storage method selection",
        # fop_ui_save.py:101, fop_ui_save.py:109, fop_ui_save.py:87
        ("*", "Disable Auto-Pack"): "Disable Auto-Pack",
        # fop_ui_save.py:113
        ("*", "Pack Mode"): "Pack Mode",
        # fop_ui_save.py:114
        ("*", "Resources Packing Mode"): "Resources Packing Mode",
        # fop_ui_save.py:120
        ("*", "Path Mode"): "Path Mode",
        # fop_ui_save.py:121
        ("*", "External Data Path Mode"): "External Data Path Mode",
        # fop_ui_save.py:139
        ("*", "Open dialog to select blend file save location"): "Open dialog to select blend file save location",
        # fop_ui_save.py:154
        ("*", "Save location has been set"): "Save location has been set",
        # fop_ui_save.py:163
        ("*", "Save blend file"): "Save blend file",
        # fop_ui_save.py:203
        ("*", "Please select a valid folder to save"): "Please select a valid folder to save",
        # fop_ui_save.py:303
        ("*", "Invalid folder path"): "Invalid folder path",
        # fop_ui_save.py:308
        ("*", "Cannot write to the selected folder"): "Cannot write to the selected folder",
        # fop_ui_save.py:322, fop_ui_save.py:394
        ("*", "Cannot write to the selected location (permission denied)"): "Cannot write to the selected location (permission denied)",
        # fop_ui_save.py:324, fop_ui_save.py:396
        ("*", "Blend file could not be saved because it is locked or in use"): "Blend file could not be saved because it is locked or in use",
        # fop_ui_save.py:326, fop_ui_save.py:398
        ("*", "Invalid path. Please check the save location"): "Invalid path. Please check the save location",
        # fop_ui_save.py:328, fop_ui_save.py:400
        ("*", "Failed to save Blend file: {error}"): "Failed to save Blend file: {error}",
        # fop_ui_save.py:353, fop_ui_save.py:378, fop_ui_save.py:467
        ("*", "Blend file has been saved"): "Blend file has been saved",
        # fop_ui_save.py:359, fop_ui_save.py:446
        ("*", "Packed external data using relative paths and saved the Blend file as {name}.blend"): "Packed external data using relative paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:362, fop_ui_save.py:448
        ("*", "Packed external data using absolute paths and saved the Blend file as {name}.blend"): "Packed external data using absolute paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:365, fop_ui_save.py:453
        ("*", "Unpacked external data using relative paths and saved the Blend file as {name}.blend"): "Unpacked external data using relative paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:368, fop_ui_save.py:455
        ("*", "Unpacked external data using absolute paths and saved the Blend file as {name}.blend"): "Unpacked external data using absolute paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:371, fop_ui_save.py:450
        ("*", "Packed external data and saved the Blend file as {name}.blend"): "Packed external data and saved the Blend file as {name}.blend",
        # fop_ui_save.py:374, fop_ui_save.py:457
        ("*", "Unpacked external data and saved the Blend file as {name}.blend"): "Unpacked external data and saved the Blend file as {name}.blend",
        # fop_ui_save.py:413
        ("*", "Auto-pack disabled, using relative paths and saved the Blend file as {name}.blend"): "Auto-pack disabled, using relative paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:415
        ("*", "Auto-pack disabled, using absolute paths and saved the Blend file as {name}.blend"): "Auto-pack disabled, using absolute paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:417
        ("*", "Auto-pack disabled, paths unchanged, and saved the Blend file as {name}.blend"): "Auto-pack disabled, paths unchanged, and saved the Blend file as {name}.blend",
        # fop_ui_save.py:419
        ("*", "Auto-pack detected and disabled. UNPACK re-applied before saving."): "Auto-pack detected and disabled. UNPACK re-applied before saving.",
        # fop_ui_save.py:424
        ("*", "Resources were automatically re-packed and using relative paths and saved the Blend file as {name}.blend"): "Resources were automatically re-packed and using relative paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:426
        ("*", "Resources were automatically re-packed and using absolute paths and saved the Blend file as {name}.blend"): "Resources were automatically re-packed and using absolute paths and saved the Blend file as {name}.blend",
        # fop_ui_save.py:428
        ("*", "Resources were automatically re-packed and saved the Blend file as {name}.blend"): "Resources were automatically re-packed and saved the Blend file as {name}.blend",
        # fop_ui_save.py:430, fop_ui_save.py:439
        ("*", "Some resources were automatically re-packed and saved the Blend file as {name}.blend"): "Some resources were automatically re-packed and saved the Blend file as {name}.blend",
        # fop_ui_save.py:460
        ("*", "Packing state kept as-is, paths made relative, and saved the Blend file as {name}.blend"): "Packing state kept as-is, paths made relative, and saved the Blend file as {name}.blend",
        # fop_ui_save.py:462
        ("*", "Packing state kept as-is, paths made absolute, and saved the Blend file as {name}.blend"): "Packing state kept as-is, paths made absolute, and saved the Blend file as {name}.blend",
        # fop_ui_save.py:464
        ("*", "Packing state kept as-is, paths unchanged, and saved the Blend file as {name}.blend"): "Packing state kept as-is, paths unchanged, and saved the Blend file as {name}.blend",
        # fop_ui_save.py:482
        ("*", "Please select where you would like to export the blend file"): "Please select where you would like to export the blend file",
        # fop_uix_update.py:47
        ("*", "Update"): "Update",
        # fop_uix_update.py:50
        ("*", "Check for Updates"): "Check for Updates",
        # fop_uix_update.py:53
        ("*", "Install"): "Install",
        # fop_uix_update.py:54
        ("*", "Open Addon Folder"): "Open Addon Folder",
        # fop_uix_update.py:65
        ("*", "GitHub has a recent release: "): "GitHub has a recent release: ",
        # fop_uix_update.py:79, fop_uix_update.py:80
        ("*", "GitHub has a recent release. "): "GitHub has a recent release. ",
        # fop_uix_update.py:84
        ("*", "Path to ZIP download folder "): "Path to ZIP download folder ",
        # fop_uix_update.py:94
        ("*", "Update file list: "): "Update file list: ",
        # fop_uix_update.py:128
        ("*", "Opens the GitHub release page to check for update files"): "Opens the GitHub release page to check for update files",
        # fop_uix_update.py:158
        ("*", "Download URL could not be retrieved"): "Download URL could not be retrieved",
        # fop_uix_update.py:166
        ("*", "Please specify a valid download folder and run again"): "Please specify a valid download folder and run again",
        # fop_uix_update.py:178
        ("*", "Download completed"): "Download completed",
        # fop_uix_update.py:181
        ("*", "Download failed"): "Download failed",
        # fop_uix_update.py:189
        ("*", "Select a ZIP archive beginning with DIVA_FBXOperationPack to install the update"): "Select a ZIP archive beginning with DIVA_FBXOperationPack to install the update",
        # fop_uix_update.py:195
        ("*", "Choose a ZIP file starting with DIVA_FBXOperationPack"): "Choose a ZIP file starting with DIVA_FBXOperationPack",
        # fop_uix_update.py:211
        ("*", "Choose the folder where the addon is installed"): "Choose the folder where the addon is installed",
        # fop_uix_update.py:244
        ("*", "No ZIP file selected. Please specify a file"): "No ZIP file selected. Please specify a file",
        # fop_uix_update.py:254
        ("*", "No ZIP file selected"): "No ZIP file selected",
        # fop_uix_update.py:261
        ("*", "Only ZIP files starting with DIVA_FBXOperationPack can be processed"): "Only ZIP files starting with DIVA_FBXOperationPack can be processed",
        # fop_uix_update.py:278
        ("*", "Missing DIVA_FBXOperationPack folder or __init__.py inside the ZIP file"): "Missing DIVA_FBXOperationPack folder or __init__.py inside the ZIP file",
        # fop_uix_update.py:285
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "Could not retrieve bl_info.name from the ZIP file",
        # fop_uix_update.py:308
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "Addon installation folder not found. Please select the destination folder manually",
        # fop_uix_update.py:314
        ("*", "Installation was cancelled"): "Installation was cancelled",
        # fop_uix_update.py:322
        ("*", "__init__.py not found in the selected folder"): "__init__.py not found in the selected folder",
        # fop_uix_update.py:329
        ("*", "Update failed because bl_info.name does not match"): "Update failed because bl_info.name does not match",
        # fop_uix_update.py:368, fop_uix_update.py:89
        ("*", "Update completed. Please restart Blender"): "Update completed. Please restart Blender",
        # fop_uix_update.py:373
        ("*", "Update failed: {error}"): "Update failed: {error}",
        # fop_uix_update.py:381
        ("*", "Please select a ZIP file"): "Please select a ZIP file",
        # fop_uix_update.py:382
        ("*", "Please restart Blender after the update"): "Please restart Blender after the update",
        # fop_uix_update.py:389
        ("*", "Opens the folder where this addon is installed"): "Opens the folder where this addon is installed",
        # fop_uix_update.py:407
        ("*", "Scan the folder and list update candidate files"): "Scan the folder and list update candidate files",
        # fop_uix_update.py:421
        ("*", "Download folder setting has been saved"): "Download folder setting has been saved",
        # fop_uix_update.py:445
        ("*", "Sort update files by file name. Click again to toggle order"): "Sort update files by file name. Click again to toggle order",
        # fop_uix_update.py:464
        ("*", "Sort update files by update/download date. Click again to toggle order"): "Sort update files by update/download date. Click again to toggle order",
        # fop_uix_update.py:498
        ("*", "Specify the folder where the update ZIP is stored"): "Specify the folder where the update ZIP is stored",
        # fop_uix_update.py:509
        ("*", "After selecting a ZIP file, click the Install button to update the currently installed addon"): "After selecting a ZIP file, click the Install button to update the currently installed addon",
    },
}

DOMAIN = "diva_fop"

def register():
    bpy.app.translations.unregister(DOMAIN)
    bpy.app.translations.register(DOMAIN, translation_dict)

def unregister():
    bpy.app.translations.unregister(DOMAIN)