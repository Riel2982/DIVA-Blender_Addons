import bpy

translation_dict = {
    "ja_JP": {
        # mwr_panel.py:40
        ("*", "Bone Identifier:"): "ボーン識別子:",
        # mwr_panel.py:48
        ("*", "Duplicate and Mirror"): "複製して反転",
        # mwr_panel.py:53
        ("*", "Symmetrize Mode"): "対称化モード",
        # mwr_panel.py:59
        ("*", "Merge Center"): "頂点をマージ",
        # mwr_panel.py:63
        ("*", "Merge Distance"): "閾値",
        # mwr_panel.py:69
        ("*", "Reflect Mesh Weights"): "鏡像反転実行",
        # mwr_panel.py:83
        ("*", "Creates a mirrored version of the selected mesh object"): "選択されたオブジェクトの鏡像反転版を作成",
        # mwr_panel.py:106, mwr_panel.py:177
        ("*", "The editing object {name} is not a mesh. Please switch to Object Mode"): "オブジェクトモードに切り替えてください",
        # mwr_panel.py:111, mwr_panel.py:182
        ("*", "The current mode is {mode}. Please run in Object Mode"): "現在のモードは{mode}です。オブジェクトモードで実行してください。",
        # mwr_panel.py:116, mwr_panel.py:187
        ("*", "The selected object {name} is not a mesh. Please select a mesh object"): "オブジェクトを選択してください",
        # mwr_panel.py:124
        ("*", "Identifier rule {label} not found"): "識別子ルール{label}が見つかりません",
        # mwr_panel.py:146
        ("*", "Mirrored version generated: {name}"): "鏡像反転完了: {name}",
        # mwr_panel.py:154
        ("*", "Symmetrizes the selected mesh object"): "選択されたオブジェクトを対称化します",
        # mwr_panel.py:163, mwr_panel.py:92
        ("*", "No object is selected in the 3D View"): "3D Viewでオブジェクトを選択してください",
        # mwr_panel.py:168, mwr_panel.py:97
        ("*", "The active object is not a mesh"): "オブジェクトを選択してください",
        # mwr_panel.py:206
        ("*", "Symmetrization completed: {name}"): "対称化完了: {name}",
        # mwr_panel.py:214
        ("*", "Open the addon settings in Preferences"): "プリファレンスのアドオン設定画面を開きます",
        # mwr_preferences.py:54
        ("*", "Editing Identifier Sets"): "識別子セット編集",
        # mwr_preferences.py:84
        ("*", "Set name"): "セット名",
        # mwr_preferences.py:91
        ("*", "Right"): "右",
        # mwr_preferences.py:92
        ("*", "Left"): "左",
        # mwr_preferences.py:99
        ("*", "Add a pair"): "ペアを追加",
        # mwr_preferences.py:109
        ("*", "Add Identifier Set"): "識別子セットを追加",
        # mwr_preferences.py:110
        ("*", "Restore default set"): "デフォルトセットを復元",
        # mwr_preferences.py:113
        ("*", "Synchronize"): "同期",
        # mwr_preferences.py:114
        ("*", "Reset"): "リセット",
        # mwr_preferences.py:115
        ("*", "Save"): "保存",
        # mwr_preferences.py:122
        ("*", "Add a new identifier set to the preferences"): "新しい識別子を設定に追加します",
        # mwr_preferences.py:135
        ("*", "A new set of identifiers has been added"): "新しい識別子セットを追加しました",
        # mwr_preferences.py:143
        ("*", "Add a left-right identifier rule to the selected set"): "選択したセットに左右識別子ルールを追加します",
        # mwr_preferences.py:156
        ("*", "Identifier pair has been added"): "識別子ペアを追加しました",
        # mwr_preferences.py:165
        ("*", "Move the identifier set up one position"): "識別子セットをひとつ上に移動します",
        # mwr_preferences.py:175
        ("*", "Already at the top"): "既に先頭にあります",
        # mwr_preferences.py:179
        ("*", "Moved up"): "上に移動しました",
        # mwr_preferences.py:187
        ("*", "Move the identifier set down one position"): "識別子セットをひとつ下に移動します",
        # mwr_preferences.py:198
        ("*", "Moved down"): "下に移動しました",
        # mwr_preferences.py:200
        ("*", "Already at the bottom"): "既に末尾にあります",
        # mwr_preferences.py:209
        ("*", "Save all identifier sets to a JSON file"): "すべての識別子セットをJSONファイルに保存します",
        # mwr_preferences.py:219
        ("*", "Please enter a name for the identifier set"): "識別子セットの名前を入力してください",
        # mwr_preferences.py:222
        ("*", "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name"): "{label}には使用できない文字が含まれています。セット名には半角英数字のみを使用してください",
        # mwr_preferences.py:229
        ("*", "{label} requires identifier pairs with both sides filled in"): "{label}には両側が入力された識別子ペアが必要です",
        # mwr_preferences.py:232
        ("*", "There is an identifier pair with only one side"): "{label}に片側だけの識別子ペアがあります",
        # mwr_preferences.py:243
        ("*", "Saved!"): "保存しました！",
        # mwr_preferences.py:251
        ("*", "Reload the identifier sets from the saved JSON file"): "保存されたJSONファイルから識別子セットをリロードします",
        # mwr_preferences.py:256
        ("*", "Reloaded identifier sets"): "識別子セットを再読込しました",
        # mwr_preferences.py:263
        ("*", "Synchronize identifier sets"): "識別子セットを同期します",
        # mwr_preferences.py:271
        ("*", "Synchronized: {names}"): "同期：{名前}",
        # mwr_preferences.py:273
        ("*", "No addons were synchronized"): "同期されたアドオンはありませんでした",
        # mwr_preferences.py:275
        ("*", "Sync failed: {msg}"): "同期失敗：{msg}",
        # mwr_preferences.py:283
        ("*", "Insert the default set of identifiers at the top"): "最上部に識別子のデフォルトセットを復元します",
        # mwr_preferences.py:302
        ("*", "Default set added"): "デフォルトセットを追加しました",
        # mwr_preferences.py:310
        ("*", "Delete the selected identifier set"): "選択した識別子セットを削除します",
        # mwr_preferences.py:318
        ("*", "At least one identifier set must be defined"): "最低でも1つの識別子セットを設定してください",
        # mwr_preferences.py:328
        ("*", "Remove the selected identifier pair from the set"): "選択した識別子ペアをセットから削除します",
        # mwr_preferences.py:340
        ("*", "At least one pair is required"): "最低1ペアは必要です",
        # mwr_preferences.py:344
        ("*", "Identifier pair removed"): "識別子ペアを削除しました",
        # mwr_preferences.py:348
        ("*", "Failed to delete: {msg}"): "削除に失敗しました: {msg}",
        # mwr_types.py:15
        ("*", "Duplicate and mirror selected mesh"): "選択したオブジェクトを複製してミラーする",
        # mwr_types.py:21
        ("*", "Enable alternative symmetrize mode"): "対称化モードに切り替える",
        # mwr_types.py:27
        ("*", "Merge vertices near X=0 when mirroring"): "ミラー時にX=0付近の頂点をマージ",
        # mwr_types.py:33
        ("*", "X-axis threshold used for merge detection"): "マージ判定に使うX軸閾値",
        # mwr_types.py:49
        ("*", "Whether to use regular expressions"): "正規表現を使用するかどうか",
        # mwr_types.py:71, mwr_update.py:375
        ("*", "Display UI to edit identifier sets"): "識別子セットを編集するUIを表示する",
        # mwr_update.py:16
        ("*", "Update"): "アップデート",
        # mwr_update.py:19
        ("*", "Check for Updates"): "更新を確認",
        # mwr_update.py:22
        ("*", "Install"): "インストール",
        # mwr_update.py:23
        ("*", "Open Addon Folder"): "アドオンフォルダを開く",
        # mwr_update.py:27
        ("*", "Path to ZIP download folder"): "ZIP保存先フォルダ",
        # mwr_update.py:37
        ("*", "Update file list: "): "更新ファイル一覧: ",
        # mwr_update.py:93
        ("*", "Opens the GitHub release page to check for update files"): "GitHubのリリースページを開き、アップデートファイルを確認できます",
        # mwr_update.py:111
        ("*", "Select a ZIP archive beginning with DIVA_MeshWeightReflector to install the update"): "アップデートをインストールするには、DIVA_MeshWeightReflectorで始まるZIPファイルを選択してください",
        # mwr_update.py:116
        ("*", "Choose a ZIP file starting with DIVA_MeshWeightReflector"): "DIVA_MeshWeightReflectorで始まるZIPファイルを選択してください",
        # mwr_update.py:123
        ("*", "Choose the folder where the addon is installed"): "アドオンがインストールされているフォルダを選択してください",
        # mwr_update.py:154
        ("*", "No ZIP file selected. Please specify a file"): "ZIPファイルが選択されていません。ファイルを指定してください",
        # mwr_update.py:163
        ("*", "Only ZIP files starting with DIVA_MeshWeightReflector can be processed"): "DIVA_MeshWeightReflector で始まるZIPファイル以外は処理できません",
        # mwr_update.py:180
        ("*", "Missing DIVA_MeshWeightReflector folder or __init__.py inside the ZIP file"): "ZIP内に DIVA_MeshWeightReflector フォルダまたは __init__.py が見つかりません",
        # mwr_update.py:188
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "ZIP内の bl_info.name を取得できません",
        # mwr_update.py:211
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください",
        # mwr_update.py:217
        ("*", "Installation was cancelled"): "インストールはキャンセルされました",
        # mwr_update.py:225
        ("*", "__init__.py not found in the selected folder"): "選択されたフォルダに __init__.py が見つかりません",
        # mwr_update.py:232
        ("*", "Update failed because bl_info.name does not match"): "bl_info.name が一致しないため、更新できません",
        # mwr_update.py:251, mwr_update.py:32
        ("*", "Update completed. Please restart Blender"): "更新が完了しました。Blenderを再起動してください",
        # mwr_update.py:256
        ("*", "Update failed: {error}"): "更新に失敗しました: {error}",
        # mwr_update.py:264
        ("*", "Please select a ZIP file"): "ZIPファイルを選択してください",
        # mwr_update.py:265
        ("*", "Please restart Blender after the update"): "更新後はBlenderを再起動してください",
        # mwr_update.py:272
        ("*", "Opens the folder where this addon is installed"): "現在のアドオンフォルダを開く",
        # mwr_update.py:290
        ("*", "Scan the folder and list update candidate files"): "ZIPファイルリストの更新",
        # mwr_update.py:303
        ("*", "Download folder setting has been saved"): "DLフォルダ設定が保存されました",
        # mwr_update.py:325
        ("*", "Sort update files by file name. Click again to toggle order"): "ZIPファイル名ソート(A–Z / Z–A)",
        # mwr_update.py:344
        ("*", "Sort update files by update/download date. Click again to toggle order"): "日時順ソート(newest ↔ oldest)",
        # mwr_update.py:382
        ("*", "Specify the folder where the update ZIP is stored"): "更新用ZIPが保存されているフォルダを指定してください",
    },
    "en_US": {
        # mwr_panel.py:40
        ("*", "Bone Identifier:"): "Bone Identifier:",
        # mwr_panel.py:48
        ("*", "Duplicate and Mirror"): "Duplicate and Mirror",
        # mwr_panel.py:53
        ("*", "Symmetrize Mode"): "Symmetrize Mode",
        # mwr_panel.py:59
        ("*", "Merge Center"): "Merge Center",
        # mwr_panel.py:63
        ("*", "Merge Threshold"): "Merge Threshold",
        # mwr_panel.py:69
        ("*", "Reflect Mesh Weights"): "Reflect Mesh Weights",
        # mwr_panel.py:83
        ("*", "Creates a mirrored version of the selected mesh object"): "Creates a mirrored version of the selected mesh object",
        # mwr_panel.py:106, mwr_panel.py:177
        ("*", "The editing object {name} is not a mesh. Please switch to Object Mode"): "The editing object {name} is not a mesh. Please switch to Object Mode",
        # mwr_panel.py:111, mwr_panel.py:182
        ("*", "The current mode is {mode}. Please run in Object Mode"): "The current mode is {mode}. Please run in Object Mode",
        # mwr_panel.py:116, mwr_panel.py:187
        ("*", "The selected object {name} is not a mesh. Please select a mesh object"): "The selected object {name} is not a mesh. Please select a mesh object",
        # mwr_panel.py:124
        ("*", "Identifier rule {label} not found"): "Identifier rule {label} not found",
        # mwr_panel.py:146
        ("*", "Mirrored version generated: {name}"): "Mirrored version generated: {name}",
        # mwr_panel.py:154
        ("*", "Symmetrizes the selected mesh object"): "Symmetrizes the selected mesh object",
        # mwr_panel.py:163, mwr_panel.py:92
        ("*", "No object is selected in the 3D View"): "No object is selected in the 3D View",
        # mwr_panel.py:168, mwr_panel.py:97
        ("*", "The active object is not a mesh"): "The active object is not a mesh",
        # mwr_panel.py:206
        ("*", "Symmetrization completed: {name}"): "Symmetrization completed: {name}",
        # mwr_panel.py:214
        ("*", "Open the addon settings in Preferences"): "Open the addon settings in Preferences",
        # mwr_preferences.py:54
        ("*", "Editing Identifier Sets"): "Editing Identifier Sets",
        # mwr_preferences.py:84
        ("*", "Set name"): "Set name",
        # mwr_preferences.py:91
        ("*", "Right"): "Right",
        # mwr_preferences.py:92
        ("*", "Left"): "Left",
        # mwr_preferences.py:99
        ("*", "Add a pair"): "Add a pair",
        # mwr_preferences.py:109
        ("*", "Add Identifier Set"): "Add Identifier Set",
        # mwr_preferences.py:110
        ("*", "Restore default set"): "Restore default set",
        # mwr_preferences.py:113
        ("*", "Synchronize"): "Synchronize",
        # mwr_preferences.py:114
        ("*", "Reset"): "Reset",
        # mwr_preferences.py:115
        ("*", "Save"): "Save",
        # mwr_preferences.py:122
        ("*", "Add a new identifier set to the preferences"): "Add a new identifier set to the preferences",
        # mwr_preferences.py:135
        ("*", "A new set of identifiers has been added"): "A new set of identifiers has been added",
        # mwr_preferences.py:143
        ("*", "Add a left-right identifier rule to the selected set"): "Add a left-right identifier rule to the selected set",
        # mwr_preferences.py:156
        ("*", "Identifier pair has been added"): "Identifier pair has been added",
        # mwr_preferences.py:165
        ("*", "Move the identifier set up one position"): "Move the identifier set up one position",
        # mwr_preferences.py:175
        ("*", "Already at the top"): "Already at the top",
        # mwr_preferences.py:179
        ("*", "Moved up"): "Moved up",
        # mwr_preferences.py:187
        ("*", "Move the identifier set down one position"): "Move the identifier set down one position",
        # mwr_preferences.py:198
        ("*", "Moved down"): "Moved down",
        # mwr_preferences.py:200
        ("*", "Already at the bottom"): "Already at the bottom",
        # mwr_preferences.py:209
        ("*", "Save all identifier sets to a JSON file"): "Save all identifier sets to a JSON file",
        # mwr_preferences.py:219
        ("*", "Please enter a name for the identifier set"): "Please enter a name for the identifier set",
        # mwr_preferences.py:222
        ("*", "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name"): "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name",
        # mwr_preferences.py:229
        ("*", "{label} requires identifier pairs with both sides filled in"): "{label} requires identifier pairs with both sides filled in",
        # mwr_preferences.py:232
        ("*", "There is an identifier pair with only one side"): "There is an identifier pair with only one side",
        # mwr_preferences.py:243
        ("*", "Saved!"): "Saved!",
        # mwr_preferences.py:251
        ("*", "Reload the identifier sets from the saved JSON file"): "Reload the identifier sets from the saved JSON file",
        # mwr_preferences.py:256
        ("*", "Reloaded identifier sets"): "Reloaded identifier sets",
        # mwr_preferences.py:263
        ("*", "Synchronize identifier sets"): "Synchronize identifier sets",
        # mwr_preferences.py:271
        ("*", "Synchronized: {names}"): "Synchronized: {names}",
        # mwr_preferences.py:273
        ("*", "No addons were synchronized"): "No addons were synchronized",
        # mwr_preferences.py:275
        ("*", "Sync failed: {msg}"): "Sync failed: {msg}",
        # mwr_preferences.py:283
        ("*", "Insert the default set of identifiers at the top"): "Insert the default set of identifiers at the top",
        # mwr_preferences.py:302
        ("*", "Default set added"): "Default set added",
        # mwr_preferences.py:310
        ("*", "Delete the selected identifier set"): "Delete the selected identifier set",
        # mwr_preferences.py:318
        ("*", "At least one identifier set must be defined"): "At least one identifier set must be defined",
        # mwr_preferences.py:328
        ("*", "Remove the selected identifier pair from the set"): "Remove the selected identifier pair from the set",
        # mwr_preferences.py:340
        ("*", "At least one pair is required"): "At least one pair is required",
        # mwr_preferences.py:344
        ("*", "Identifier pair removed"): "Identifier pair removed",
        # mwr_preferences.py:348
        ("*", "Failed to delete: {msg}"): "Failed to delete: {msg}",
        # mwr_types.py:15
        ("*", "Duplicate and mirror selected mesh"): "Duplicate and mirror selected mesh",
        # mwr_types.py:21
        ("*", "Enable alternative symmetrize mode"): "Enable alternative symmetrize mode",
        # mwr_types.py:27
        ("*", "Merge vertices near X=0 when mirroring"): "Merge vertices near X=0 when mirroring",
        # mwr_types.py:33
        ("*", "X-axis threshold used for merge detection"): "X-axis threshold used for merge detection",
        # mwr_types.py:49
        ("*", "Whether to use regular expressions"): "Whether to use regular expressions",
        # mwr_types.py:71, mwr_update.py:375
        ("*", "Display UI to edit identifier sets"): "Display UI to edit identifier sets",
        # mwr_update.py:16
        ("*", "Update"): "Update",
        # mwr_update.py:19
        ("*", "Check for Updates"): "Check for Updates",
        # mwr_update.py:22
        ("*", "Install"): "Install",
        # mwr_update.py:23
        ("*", "Open Addon Folder"): "Open Addon Folder",
        # mwr_update.py:27
        ("*", "Path to ZIP download folder"): "Path to ZIP download folder",
        # mwr_update.py:37
        ("*", "Update file list:"): "Update file list:",
        # mwr_update.py:93
        ("*", "Opens the GitHub release page to check for update files"): "Opens the GitHub release page to check for update files",
        # mwr_update.py:111
        ("*", "Select a ZIP archive beginning with DIVA_MeshWeightReflector to install the update"): "Select a ZIP archive beginning with DIVA_MeshWeightReflector to install the update",
        # mwr_update.py:116
        ("*", "Choose a ZIP file starting with DIVA_MeshWeightReflector"): "Choose a ZIP file starting with DIVA_MeshWeightReflector",
        # mwr_update.py:123
        ("*", "Choose the folder where the addon is installed"): "Choose the folder where the addon is installed",
        # mwr_update.py:154
        ("*", "No ZIP file selected. Please specify a file"): "No ZIP file selected. Please specify a file",
        # mwr_update.py:163
        ("*", "Only ZIP files starting with DIVA_MeshWeightReflector can be processed"): "Only ZIP files starting with DIVA_MeshWeightReflector can be processed",
        # mwr_update.py:180
        ("*", "Missing DIVA_MeshWeightReflector folder or __init__.py inside the ZIP file"): "Missing DIVA_MeshWeightReflector folder or __init__.py inside the ZIP file",
        # mwr_update.py:188
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "Could not retrieve bl_info.name from the ZIP file",
        # mwr_update.py:211
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "Addon installation folder not found. Please select the destination folder manually",
        # mwr_update.py:217
        ("*", "Installation was cancelled"): "Installation was cancelled",
        # mwr_update.py:225
        ("*", "__init__.py not found in the selected folder"): "__init__.py not found in the selected folder",
        # mwr_update.py:232
        ("*", "Update failed because bl_info.name does not match"): "Update failed because bl_info.name does not match",
        # mwr_update.py:251, mwr_update.py:32
        ("*", "Update completed. Please restart Blender"): "Update completed. Please restart Blender",
        # mwr_update.py:256
        ("*", "Update failed: {error}"): "Update failed: {error}",
        # mwr_update.py:264
        ("*", "Please select a ZIP file"): "Please select a ZIP file",
        # mwr_update.py:265
        ("*", "Please restart Blender after the update"): "Please restart Blender after the update",
        # mwr_update.py:272
        ("*", "Opens the folder where this addon is installed"): "Opens the folder where this addon is installed",
        # mwr_update.py:290
        ("*", "Scan the folder and list update candidate files"): "Scan the folder and list update candidate files",
        # mwr_update.py:303
        ("*", "Download folder setting has been saved"): "Download folder setting has been saved",
        # mwr_update.py:325
        ("*", "Sort update files by file name. Click again to toggle order"): "Sort update files by file name. Click again to toggle order",
        # mwr_update.py:344
        ("*", "Sort update files by update/download date. Click again to toggle order"): "Sort update files by update/download date. Click again to toggle order",
        # mwr_update.py:382
        ("*", "Specify the folder where the update ZIP is stored"): "Specify the folder where the update ZIP is stored",
    },
}

def register():
    bpy.app.translations.unregister(__name__)
    bpy.app.translations.register(__name__, translation_dict)

def unregister():
    bpy.app.translations.unregister(__name__)