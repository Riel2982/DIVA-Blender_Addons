import bpy

translation_dict = {
    "ja_JP": {
        # bprs_check.py:117
        ("*", "Editing armature switched to: {name}"): "アーマチュア{name}に編集モードを切り替えました",
        # bprs_types.py:10
        ("*", "Display all bones"): "すべてのボーンを表示",
        # bprs_types.py:10
        ("*", "Show All"): "全表示",
        # bprs_types.py:11
        ("*", "Display only bones not hidden in Edit Mode"): "編集モード上で非表示でないボーンのみ表示",
        # bprs_types.py:11
        ("*", "Visible Bones Only"): "表示されているボーンのみ",
        # bprs_types.py:12
        ("*", "Only bones selected in Edit Mode"): "編集モードで選択中のボーンのみ",
        # bprs_types.py:12
        ("*", "Selected Only"): "選択済のみ",
        # bprs_types.py:12
        ("*", "選択中のみ"): "選択中のみ",
        # bprs_types.py:13
        ("*", "Only bones not selected"): "選択されていないボーンのみ",
        # bprs_types.py:13
        ("*", "Unselected Only"): "未選択のみ",
        # bprs_types.py:20
        ("*", "Show"): "表示",
        # bprs_types.py:34
        ("*", "Show tool to export bone data of selected armature to file"): "選択アーマーチュアのボーンデータをファイルに出力するツールを表示",
        # bprs_types.py:40
        ("*", "Show tool to generate hidden bones from bone data"): "ボーンデータから隠しボーンを生成するツールを表示",
        # bprs_types.py:46
        ("*", "Show tool to inspect bone data of selected armature"): "選択アーマチュアのボーンデータを確認するツールを表示",
        # bprs_types.py:54
        ("*", "Filename to save - without extension"): "保存するファイル名（拡張子なし）",
        # bprs_types.py:59
        ("*", "Destination folder"): "保存先フォルダ",
        # bprs_types.py:63, bprs_ui_export.py:42
        ("*", "Auto Open File"): "ファイルを自動で開く",
        # bprs_types.py:64
        ("*", "Automatically open the file after export"): "エクスポート後に自動でファイルを開く",
        # bprs_types.py:68, bprs_ui_export.py:46
        ("*", "Overwrite Existing File"): "ファイルの上書きを防止",
        # bprs_types.py:69
        ("*", "Overwrite existing file / rename if unchecked"): "既存ファイルを上書きする（OFFならリネーム）",
        # bprs_types.py:73, bprs_ui_export.py:50
        ("*", "Export as JSON"): "JSON形式で保存",
        # bprs_types.py:74
        ("*", "Save in JSON format / TXT if unchecked"): "JSON形式で保存する（チェックなしならTXT）",
        # bprs_types.py:84
        ("*", "List of armature bones"): "アーマチュアのボーン一覧",
        # bprs_ui_check.py:24
        ("*", "Please execute the checker after selecting an armature"): "オブジェクトモードでアーマチュアを選択した状態で実行してください",
        # bprs_ui_check.py:33
        ("*", "List Mode"): "List Mode",
        # bprs_ui_check.py:69
        ("*", "Retrieve armature bone data and register to the display list"): "アーマチュアのボーンデータを取得して表示リストに登録する",
        # bprs_ui_check.py:76
        ("*", "The selected object is not an armature: {name}"): "対象のオブジェクトがアーマチュアではありません: {name}",
        # bprs_ui_check.py:90
        ("*", "Failed to retrieve bone data"): "ボーンデータが取得できませんでした",
        # bprs_ui_check.py:98
        ("*", "Retrieved {count} bones from armature: {name}"): "{name}から{count} 本のボーン情報を取得しました",
        # bprs_ui_check.py:103
        ("*", "Retrieval error: {error}"): "取得エラー: {error}",
        # bprs_ui_check.py:208
        ("*", "Copy the specified string to the clipboard"): "指定された文字列をクリップボードにコピーする",
        # bprs_ui_check.py:214
        ("*", "Copied to clipboard"): "クリップボードにコピーしました",
        # bprs_ui_check.py:222
        ("*", "Toggle bone display checkboxes ON/OFF in bulk"): "ボーン表示のチェックを一括 ON/OFF",
        # bprs_ui_check.py:239
        ("*", "Select Bone \n Shift: Add Selection \n Alt: Deselect"): "ボーンを選択\n Shift：追加選択\n Alt：選択解除",
        # bprs_ui_check.py:246
        ("*", "No valid armature found"): "アーマチュアが見つかりません",
        # bprs_ui_check.py:250, bprs_ui_check.py:287, bprs_ui_check.py:334
        ("*", "No armature is selected"): "アーマチュアが選択されていません",
        # bprs_ui_check.py:257
        ("*", "Target bone not found: {name}"): "対象ボーンが見つかりません: {name}",
        # bprs_ui_check.py:279
        ("*", "Select or deselect all bones currently visible in the list"): "リストに表示中のボーンを一括で選択／選択解除",
        # bprs_ui_check.py:319
        ("*", "deselected"): "選択解除",
        # bprs_ui_check.py:319
        ("*", "selected"): "選択",
        # bprs_ui_check.py:320
        ("*", "{count} visible bones {mode}"): "{count} 個の表示中ボーンを{mode}しました",
        # bprs_ui_check.py:327
        ("*", "Toggle display flag for selected bones in edit mode"): "編集モードで選択中のボーンに対して表示フラグを ON/OFF",
        # bprs_ui_check.py:347
        ("*", "added"): "追加",
        # bprs_ui_check.py:347
        ("*", "removed"): "解除",
        # bprs_ui_check.py:348
        ("*", "{count} bones were {mode} from display"): "{count} 件のボーン表示を {mode} しました",
        # bprs_ui_export.py:27
        ("*", "File Name :"): "ファイル名：",
        # bprs_ui_export.py:33
        ("*", "Export Path :"): "保存場所：",
        # bprs_ui_export.py:60
        ("*", "Open folder selection dialog"): "フォルダ選択ダイアログを開く",
        # bprs_ui_export.py:82
        ("*", "Selected folder: {path}"): "選択したフォルダ：{path}",
        # bprs_ui_export.py:91
        ("*", "Retrieve bone data from the selected armature and export to file"): "アーマチュアを選択した状態でボーンデータを取得しファイルに出力",
        # bprs_ui_export.py:113
        ("*", "Invalid destination folder. Please select a proper directory"): "保存先のフォルダが無効です。適切なフォルダを選択してください",
        # bprs_ui_export.py:119
        ("*", "Cannot save to Blender’s installation folder. Please choose another location"): "Blenderの実行フォルダには保存できません。別の場所を指定してください",
        # bprs_ui_export.py:136
        ("*", "Existing file renamed to: {name}"): "既存のファイルの名前を{name}に変更しました",
        # bprs_ui_export.py:141
        ("*", "No armature selected"): "アーマチュアを選択してください",
        # bprs_ui_export.py:154
        ("*", "Bone data exported to: {path}"): "ボーンデータのファイル出力完了：{path}",
        # bprs_ui_export.py:166
        ("*", "Failed to export: {error}"): "エクスポートに失敗しました: {error}",
        # bprs_uix_update.py:47
        ("*", "Update"): "アップデート",
        # bprs_uix_update.py:50
        ("*", "Check for Updates"): "更新を確認",
        # bprs_uix_update.py:53
        ("*", "Install"): "インストール",
        # bprs_uix_update.py:54
        ("*", "Open Addon Folder"): "アドオンフォルダを開く",
        # bprs_uix_update.py:65, bprs_uix_update.py:80
        ("*", "GitHub has a recent release: "): "GitHubに最新リリースあり ",
        # bprs_uix_update.py:89, bprs_uix_update.py:90
        ("*", "GitHub has a recent release. "): "GitHubに最新リリースあり。",
        # bprs_uix_update.py:94
        ("*", "Path to ZIP download folder "): "ZIP保存先フォルダ ",
        # bprs_uix_update.py:104
        ("*", "Update file list: "): "更新ファイル一覧：",
        # bprs_uix_update.py:137
        ("*", "Opens the GitHub release page to check for update files"): "GitHubのリリースページを開き、アップデートファイルを確認できます",
        # bprs_uix_update.py:168
        ("*", "Download URL could not be retrieved"): "ダウンロードURLが取得できません",
        # bprs_uix_update.py:176
        ("*", "Please specify a valid download folder and run again"): "ZIP保存先フォルダを指定後、再び実行してください",
        # bprs_uix_update.py:188
        ("*", "Download completed"): "ダウンロードが完了しました",
        # bprs_uix_update.py:191
        ("*", "Download failed"): "ダウンロードできませんでした",
        # bprs_uix_update.py:201
        ("*", "Select a ZIP archive beginning with DIVA_BonePositionRotationScale to install the update"): "アップデートをインストールするには、DIVA_BonePositionRotationScaleで始まるZIPファイルを選択してください",
        # bprs_uix_update.py:207
        ("*", "Choose a ZIP file starting with DIVA_BonePositionRotationScale"): "DIVA_BonePositionRotationScaleで始まるZIPファイルを選択してください",
        # bprs_uix_update.py:223
        ("*", "Choose the folder where the addon is installed"): "アドオンがインストールされているフォルダを選択してください",
        # bprs_uix_update.py:256
        ("*", "No ZIP file selected. Please specify a file"): "ZIPファイルが選択されていません。ファイルを指定してください",
        # bprs_uix_update.py:266
        ("*", "No ZIP file selected"): "zipファイルが選択されていません",
        # bprs_uix_update.py:273
        ("*", "Only ZIP files starting with DIVA_BonePositionRotationScale can be processed"): "DIVA_BonePositionRotationScale で始まるZIPファイル以外は処理できません",
        # bprs_uix_update.py:290
        ("*", "Missing DIVA_BonePositionRotationScale folder or __init__.py inside the ZIP file"): "ZIP内に DIVA_BonePositionRotationScale フォルダまたは __init__.py が見つかりません",
        # bprs_uix_update.py:297
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "ZIP内の bl_info.name を取得できません",
        # bprs_uix_update.py:320
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください",
        # bprs_uix_update.py:326
        ("*", "Installation was cancelled"): "インストールはキャンセルされました",
        # bprs_uix_update.py:334
        ("*", "__init__.py not found in the selected folder"): "選択されたフォルダに __init__.py が見つかりません",
        # bprs_uix_update.py:341
        ("*", "Update failed because bl_info.name does not match"): "bl_info.name が一致しないため、更新できません",
        # bprs_uix_update.py:379, bprs_uix_update.py:99
        ("*", "Update completed. Please restart Blender"): "更新が完了しました。Blenderを再起動してください",
        # bprs_uix_update.py:384
        ("*", "Update failed: {error}"): "更新に失敗しました: {error}",
        # bprs_uix_update.py:392
        ("*", "Please select a ZIP file"): "ZIPファイルを選択してください",
        # bprs_uix_update.py:393
        ("*", "Please restart Blender after the update"): "更新後はBlenderを再起動してください",
        # bprs_uix_update.py:400
        ("*", "Opens the folder where this addon is installed"): "現在のアドオンフォルダを開く",
        # bprs_uix_update.py:418
        ("*", "Scan the folder and list update candidate files"): "ZIPファイルリストの更新",
        # bprs_uix_update.py:431
        ("*", "Download folder setting has been saved"): "DLフォルダ設定が保存されました",
        # bprs_uix_update.py:456
        ("*", "Sort update files by file name. Click again to toggle order"): "ZIPファイル名ソート(A–Z / Z–A)",
        # bprs_uix_update.py:475
        ("*", "Sort update files by update/download date. Click again to toggle order"): "日時順ソート(newest ↔ oldest)",
        # bprs_uix_update.py:509
        ("*", "Specify the folder where the update ZIP is stored"): "更新用ZIPが保存されているフォルダを指定してください",
    },
    "en_US": {
        # bprs_check.py:117
        ("*", "Editing armature switched to: {name}"): "Editing armature switched to: {name}",
        # bprs_types.py:10
        ("*", "Display all bones"): "Display all bones",
        # bprs_types.py:10
        ("*", "Show All"): "Show All",
        # bprs_types.py:11
        ("*", "Display only bones not hidden in Edit Mode"): "Display only bones not hidden in Edit Mode",
        # bprs_types.py:11
        ("*", "Visible Bones Only"): "Visible Bones Only",
        # bprs_types.py:12
        ("*", "Only bones selected in Edit Mode"): "Only bones selected in Edit Mode",
        # bprs_types.py:12
        ("*", "Selected Only"): "Selected Only",
        # bprs_types.py:12
        ("*", "選択中のみ"): "Selected Only",
        # bprs_types.py:13
        ("*", "Only bones not selected"): "Only bones not selected",
        # bprs_types.py:13
        ("*", "Unselected Only"): "Unselected Only",
        # bprs_types.py:20
        ("*", "Show"): "Show",
        # bprs_types.py:34
        ("*", "Show tool to export bone data of selected armature to file"): "Show tool to export bone data of selected armature to file",
        # bprs_types.py:40
        ("*", "Show tool to generate hidden bones from bone data"): "Show tool to generate hidden bones from bone data",
        # bprs_types.py:46
        ("*", "Show tool to inspect bone data of selected armature"): "Show tool to inspect bone data of selected armature",
        # bprs_types.py:54
        ("*", "Filename to save - without extension"): "Filename to save - without extension",
        # bprs_types.py:59
        ("*", "Destination folder"): "Destination folder",
        # bprs_types.py:63, bprs_ui_export.py:42
        ("*", "Auto Open File"): "Auto Open File",
        # bprs_types.py:64
        ("*", "Automatically open the file after export"): "Automatically open the file after export",
        # bprs_types.py:68, bprs_ui_export.py:46
        ("*", "Overwrite Existing File"): "Overwrite Existing File",
        # bprs_types.py:69
        ("*", "Overwrite existing file / rename if unchecked"): "Overwrite existing file / rename if unchecked",
        # bprs_types.py:73, bprs_ui_export.py:50
        ("*", "Export as JSON"): "Export as JSON",
        # bprs_types.py:74
        ("*", "Save in JSON format / TXT if unchecked"): "Save in JSON format / TXT if unchecked",
        # bprs_types.py:84
        ("*", "List of armature bones"): "List of armature bones",
        # bprs_ui_check.py:24
        ("*", "Please execute the checker after selecting an armature"): "Please execute the checker after selecting an armature",
        # bprs_ui_check.py:33
        ("*", "List Mode"): "List Mode",
        # bprs_ui_check.py:69
        ("*", "Retrieve armature bone data and register to the display list"): "Retrieve armature bone data and register to the display list",
        # bprs_ui_check.py:76
        ("*", "The selected object is not an armature: {name}"): "The selected object is not an armature: {name}",
        # bprs_ui_check.py:90
        ("*", "Failed to retrieve bone data"): "Failed to retrieve bone data",
        # bprs_ui_check.py:98
        ("*", "Retrieved {count} bones from armature: {name}"): "Retrieved {count} bones from armature: {name}",
        # bprs_ui_check.py:103
        ("*", "Retrieval error: {error}"): "Retrieval error: {error}",
        # bprs_ui_check.py:208
        ("*", "Copy the specified string to the clipboard"): "Copy the specified string to the clipboard",
        # bprs_ui_check.py:214
        ("*", "Copied to clipboard"): "Copied to clipboard",
        # bprs_ui_check.py:222
        ("*", "Toggle bone display checkboxes ON/OFF in bulk"): "Toggle bone display checkboxes ON/OFF in bulk",
        # bprs_ui_check.py:239
        ("*", "Select Bone \n Shift: Add Selection \n Alt: Deselect"): "Select Bone \n Shift: Add Selection \n Alt: Deselect",
        # bprs_ui_check.py:246
        ("*", "No valid armature found"): "No valid armature found",
        # bprs_ui_check.py:250, bprs_ui_check.py:287, bprs_ui_check.py:334
        ("*", "No armature is selected"): "No armature is selected",
        # bprs_ui_check.py:257
        ("*", "Target bone not found: {name}"): "Target bone not found: {name}",
        # bprs_ui_check.py:279
        ("*", "Select or deselect all bones currently visible in the list"): "Select or deselect all bones currently visible in the list",
        # bprs_ui_check.py:319
        ("*", "deselected"): "deselected",
        # bprs_ui_check.py:319
        ("*", "selected"): "selected",
        # bprs_ui_check.py:320
        ("*", "{count} visible bones {mode}"): "{count} visible bones {mode}",
        # bprs_ui_check.py:327
        ("*", "Toggle display flag for selected bones in edit mode"): "Toggle display flag for selected bones in edit mode",
        # bprs_ui_check.py:347
        ("*", "added"): "added",
        # bprs_ui_check.py:347
        ("*", "removed"): "removed",
        # bprs_ui_check.py:348
        ("*", "{count} bones were {mode} from display"): "{count} bones were {mode} from display",
        # bprs_ui_export.py:27
        ("*", "File Name :"): "File Name :",
        # bprs_ui_export.py:33
        ("*", "Export Path :"): "Export Path :",
        # bprs_ui_export.py:60
        ("*", "Open folder selection dialog"): "Open folder selection dialog",
        # bprs_ui_export.py:82
        ("*", "Selected folder: {path}"): "Selected folder: {path}",
        # bprs_ui_export.py:91
        ("*", "Retrieve bone data from the selected armature and export to file"): "Retrieve bone data from the selected armature and export to file",
        # bprs_ui_export.py:113
        ("*", "Invalid destination folder. Please select a proper directory"): "Invalid destination folder. Please select a proper directory",
        # bprs_ui_export.py:119
        ("*", "Cannot save to Blender’s installation folder. Please choose another location"): "Cannot save to Blender’s installation folder. Please choose another location",
        # bprs_ui_export.py:136
        ("*", "Existing file renamed to: {name}"): "Existing file renamed to: {name}",
        # bprs_ui_export.py:141
        ("*", "No armature selected"): "No armature selected",
        # bprs_ui_export.py:154
        ("*", "Bone data exported to: {path}"): "Bone data exported to: {path}",
        # bprs_ui_export.py:166
        ("*", "Failed to export: {error}"): "Failed to export: {error}",
        # bprs_uix_update.py:47
        ("*", "Update"): "Update",
        # bprs_uix_update.py:50
        ("*", "Check for Updates"): "Check for Updates",
        # bprs_uix_update.py:53
        ("*", "Install"): "Install",
        # bprs_uix_update.py:54
        ("*", "Open Addon Folder"): "Open Addon Folder",
        # bprs_uix_update.py:65, bprs_uix_update.py:80
        ("*", "GitHub has a recent release: "): "GitHub has a recent release: ",
        # bprs_uix_update.py:89, bprs_uix_update.py:90
        ("*", "GitHub has a recent release. "): "GitHub has a recent release. ",
        # bprs_uix_update.py:94
        ("*", "Path to ZIP download folder "): "Path to ZIP download folder ",
        # bprs_uix_update.py:104
        ("*", "Update file list: "): "Update file list: ",
        # bprs_uix_update.py:137
        ("*", "Opens the GitHub release page to check for update files"): "Opens the GitHub release page to check for update files",
        # bprs_uix_update.py:168
        ("*", "Download URL could not be retrieved"): "Download URL could not be retrieved",
        # bprs_uix_update.py:176
        ("*", "Please specify a valid download folder and run again"): "Please specify a valid download folder and run again",
        # bprs_uix_update.py:188
        ("*", "Download completed"): "Download completed",
        # bprs_uix_update.py:191
        ("*", "Download failed"): "Download failed",
        # bprs_uix_update.py:201
        ("*", "Select a ZIP archive beginning with DIVA_BonePositionRotationScale to install the update"): "Select a ZIP archive beginning with DIVA_BonePositionRotationScale to install the update",
        # bprs_uix_update.py:207
        ("*", "Choose a ZIP file starting with DIVA_BonePositionRotationScale"): "Choose a ZIP file starting with DIVA_BonePositionRotationScale",
        # bprs_uix_update.py:223
        ("*", "Choose the folder where the addon is installed"): "Choose the folder where the addon is installed",
        # bprs_uix_update.py:256
        ("*", "No ZIP file selected. Please specify a file"): "No ZIP file selected. Please specify a file",
        # bprs_uix_update.py:266
        ("*", "No ZIP file selected"): "No ZIP file selected",
        # bprs_uix_update.py:273
        ("*", "Only ZIP files starting with DIVA_BonePositionRotationScale can be processed"): "Only ZIP files starting with DIVA_BonePositionRotationScale can be processed",
        # bprs_uix_update.py:290
        ("*", "Missing DIVA_BonePositionRotationScale folder or __init__.py inside the ZIP file"): "Missing DIVA_BonePositionRotationScale folder or __init__.py inside the ZIP file",
        # bprs_uix_update.py:297
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "Could not retrieve bl_info.name from the ZIP file",
        # bprs_uix_update.py:320
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "Addon installation folder not found. Please select the destination folder manually",
        # bprs_uix_update.py:326
        ("*", "Installation was cancelled"): "Installation was cancelled",
        # bprs_uix_update.py:334
        ("*", "__init__.py not found in the selected folder"): "__init__.py not found in the selected folder",
        # bprs_uix_update.py:341
        ("*", "Update failed because bl_info.name does not match"): "Update failed because bl_info.name does not match",
        # bprs_uix_update.py:379, bprs_uix_update.py:99
        ("*", "Update completed. Please restart Blender"): "Update completed. Please restart Blender",
        # bprs_uix_update.py:384
        ("*", "Update failed: {error}"): "Update failed: {error}",
        # bprs_uix_update.py:392
        ("*", "Please select a ZIP file"): "Please select a ZIP file",
        # bprs_uix_update.py:393
        ("*", "Please restart Blender after the update"): "Please restart Blender after the update",
        # bprs_uix_update.py:400
        ("*", "Opens the folder where this addon is installed"): "Opens the folder where this addon is installed",
        # bprs_uix_update.py:418
        ("*", "Scan the folder and list update candidate files"): "Scan the folder and list update candidate files",
        # bprs_uix_update.py:431
        ("*", "Download folder setting has been saved"): "Download folder setting has been saved",
        # bprs_uix_update.py:456
        ("*", "Sort update files by file name. Click again to toggle order"): "Sort update files by file name. Click again to toggle order",
        # bprs_uix_update.py:475
        ("*", "Sort update files by update/download date. Click again to toggle order"): "Sort update files by update/download date. Click again to toggle order",
        # bprs_uix_update.py:509
        ("*", "Specify the folder where the update ZIP is stored"): "Specify the folder where the update ZIP is stored",
    },
}

DOMAIN = "diva_bprs"

def register():
    bpy.app.translations.unregister(DOMAIN)
    bpy.app.translations.register(DOMAIN, translation_dict)

def unregister():
    bpy.app.translations.unregister(DOMAIN)