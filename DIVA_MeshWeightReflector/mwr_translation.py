import bpy

translation_dict = {
    "ja_JP": {
        # mwr_panel.py:47
        ("*", "Bone Identifier:"): "ボーン識別子:",
        # mwr_panel.py:60, mwr_panel.py:72, mwr_panel.py:82
        ("*", "Duplicate and Mirror"): "複製して反転",
        # mwr_panel.py:66, mwr_panel.py:76
        ("*", "Apply Modifiers"): "モディファイアーを適用",
        # mwr_panel.py:87
        ("*", "Symmetrize Mode"): "対称化モード",
        # mwr_panel.py:93
        ("*", "Merge Center"): "頂点をマージ",
        # mwr_panel.py:97
        ("*", "Merge Distance"): "閾値",
        # mwr_panel.py:103
        ("*", "Reflect Mesh Weights"): "鏡像反転実行",
        # mwr_panel.py:117
        ("*", "Creates a mirrored version of the selected mesh object"): "選択されたオブジェクトの鏡像反転版を作成",
        # mwr_panel.py:126, mwr_panel.py:245
        ("*", "No object is selected in the 3D View"): "3D Viewでオブジェクトを選択してください",
        # mwr_panel.py:131, mwr_panel.py:250
        ("*", "The active object is not a mesh"): "オブジェクトを選択してください",
        # mwr_panel.py:140, mwr_panel.py:259
        ("*", "The editing object {name} is not a mesh. Please switch to Object Mode"): "オブジェクトモードに切り替えてください",
        # mwr_panel.py:145, mwr_panel.py:264
        ("*", "The current mode is {mode}. Please run in Object Mode"): "現在のモードは{mode}です。オブジェクトモードで実行してください",
        # mwr_panel.py:150, mwr_panel.py:269
        ("*", "The selected object {name} is not a mesh. Please select a mesh object"): "オブジェクトを選択してください",
        # mwr_panel.py:158
        ("*", "Identifier rule {label} not found"): "識別子ルール{label}が見つかりません",
        # mwr_panel.py:176, mwr_panel.py:313
        ("*", "Symmetrization completed: {name}. Applied modifiers: {types}"): "{name}の対称化完了 / {types}のモディファイアーが適用されました",
        # mwr_panel.py:178, mwr_panel.py:180, mwr_panel.py:301, mwr_panel.py:315
        ("*", "Symmetrization completed: {name}"): "対称化完了: {name}",
        # mwr_panel.py:182
        ("*", "Symmetrization failed"): "対称化失敗",
        # mwr_panel.py:217, mwr_panel.py:227
        ("*", "Mirrored version generated: {name}"): "鏡像反転完了: {name}",
        # mwr_panel.py:225
        ("*", "Mirrored version generated: {name}. Applied modifiers: {types}"): " {name}の鏡像反転完了 / {types}のモディファイアーが適用されました",
        # mwr_panel.py:236
        ("*", "Symmetrizes the selected mesh object"): "選択されたオブジェクトを対称化します",
        # mwr_panel.py:323
        ("*", "Open the addon settings in Preferences"): "プリファレンスのアドオン設定画面を開きます",
        # mwr_preferences.py:46
        ("*", "Editing Identifier Sets"): "識別子セット編集",
        # mwr_preferences.py:76
        ("*", "Set name"): "セット名",
        # mwr_preferences.py:83
        ("*", "Right"): "右",
        # mwr_preferences.py:84
        ("*", "Left"): "左",
        # mwr_preferences.py:91
        ("*", "Add a pair"): "ペアを追加",
        # mwr_preferences.py:101
        ("*", "Add Identifier Set"): "識別子セットを追加",
        # mwr_preferences.py:102
        ("*", "Restore Default Set"): "デフォルトセットを復元",
        # mwr_preferences.py:105
        ("*", "Synchronize"): "同期",
        # mwr_preferences.py:106
        ("*", "Reset"): "リセット",
        # mwr_preferences.py:107
        ("*", "Save"): "保存",
        # mwr_preferences.py:114
        ("*", "Add a new identifier set to the preferences"): "新しい識別子を設定に追加します",
        # mwr_preferences.py:127
        ("*", "A new set of identifiers has been added"): "新しい識別子セットを追加しました",
        # mwr_preferences.py:135
        ("*", "Add a left-right identifier rule to the selected set"): "選択したセットに左右識別子ルールを追加します",
        # mwr_preferences.py:148
        ("*", "Identifier pair has been added"): "識別子ペアを追加しました",
        # mwr_preferences.py:157
        ("*", "Move the identifier set up one position"): "識別子セットをひとつ上に移動します",
        # mwr_preferences.py:167
        ("*", "Already at the top"): "既に先頭にあります",
        # mwr_preferences.py:171
        ("*", "Moved up"): "上に移動しました",
        # mwr_preferences.py:179
        ("*", "Move the identifier set down one position"): "識別子セットをひとつ下に移動します",
        # mwr_preferences.py:190
        ("*", "Moved down"): "下に移動しました",
        # mwr_preferences.py:192
        ("*", "Already at the bottom"): "既に末尾にあります",
        # mwr_preferences.py:201
        ("*", "Save all identifier sets to a JSON file"): "すべての識別子セットをJSONファイルに保存します",
        # mwr_preferences.py:211
        ("*", "Please enter a name for the identifier set"): "識別子セットの名前を入力してください",
        # mwr_preferences.py:214
        ("*", "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name"): "{label}には使用できない文字が含まれています。セット名には半角英数字のみを使用してください",
        # mwr_preferences.py:221
        ("*", "{label} requires identifier pairs with both sides filled in"): "{label}には両側が入力された識別子ペアが必要です",
        # mwr_preferences.py:224
        ("*", "There is an identifier pair with only one side"): "{label}に片側だけの識別子ペアがあります",
        # mwr_preferences.py:235
        ("*", "Saved!"): "保存しました！",
        # mwr_preferences.py:243
        ("*", "Reload the identifier sets from the saved JSON file"): "保存されたJSONファイルから識別子セットをリロードします",
        # mwr_preferences.py:248
        ("*", "Reloaded identifier sets"): "識別子セットを再読込しました",
        # mwr_preferences.py:255
        ("*", "Synchronize identifier sets"): "識別子セットを同期します",
        # mwr_preferences.py:263
        ("*", "Synchronized: {names}"): "同期：{names}",
        # mwr_preferences.py:265
        ("*", "No addons were synchronized"): "同期されたアドオンはありませんでした",
        # mwr_preferences.py:267
        ("*", "Sync failed: {msg}"): "同期失敗：{msg}",
        # mwr_preferences.py:275
        ("*", "Insert the default set of identifiers at the top"): "最上部に識別子のデフォルトセットを復元します",
        # mwr_preferences.py:294
        ("*", "Default set added"): "デフォルトセットを追加しました",
        # mwr_preferences.py:302
        ("*", "Delete the selected identifier set"): "選択した識別子セットを削除します",
        # mwr_preferences.py:310
        ("*", "At least one identifier set must be defined"): "最低でも1つの識別子セットを設定してください",
        # mwr_preferences.py:320
        ("*", "Remove the selected identifier pair from the set"): "選択した識別子ペアをセットから削除します",
        # mwr_preferences.py:332
        ("*", "At least one pair is required"): "最低1ペアは必要です",
        # mwr_preferences.py:336
        ("*", "Identifier pair removed"): "識別子ペアを削除しました",
        # mwr_preferences.py:340
        ("*", "Failed to delete: {msg}"): "削除に失敗しました: {msg}",
        # mwr_sub.py:10
        ("*", "Subdivision Surface"): "区画面",
        # mwr_sub.py:11
        ("*", "Mirror"): "ミラー",
        # mwr_sub.py:12
        ("*", "Lattice"): "ラティス",
        # mwr_sub.py:13
        ("*", "Shrinkwrap"): "シュリンクラップ",
        # mwr_sub.py:14
        ("*", "Data Transfer"): "データ転送",
        # mwr_sub.py:15
        ("*", "Mesh Deform"): "メッシュ変形",
        # mwr_sub.py:16
        ("*", "Vertex Weight Edit"): "頂点ウエイト編集",
        # mwr_sub.py:17
        ("*", "Vertex Weight Mix"): "頂点ウエイト合成",
        # mwr_sub.py:18
        ("*", "Vertex Weight Proximity"): "頂点ウエイト（近接）",
        # mwr_sub.py:19
        ("*", "Armature"): "アーマチュア",
        # mwr_sub.py:20
        ("*", "Solidify"): "ソリッド化",
        # mwr_sub.py:21
        ("*", "Decimate"): "デシメート",
        # mwr_sub.py:22
        ("*", "Boolean"): "ブーリアン",
        # mwr_types.py:15
        ("*", "Duplicate and mirror selected mesh"): "選択したオブジェクトを複製してミラーする",
        # mwr_types.py:21
        ("*", "Enable alternative symmetrize mode"): "対称化モードに切り替える",
        # mwr_types.py:27
        ("*", "Merge vertices near X=0 when mirroring"): "ミラー時にX=0付近の頂点をマージ",
        # mwr_types.py:33
        ("*", "X-axis threshold used for merge detection"): "マージ判定に使うX軸閾値",
        # mwr_types.py:43
        ("*", "Apply specific modifiers before processing"): "一部のモディファイアを適用してから実行",
        # mwr_types.py:55
        ("*", "Whether to use regular expressions"): "正規表現を使用するかどうか",
        # mwr_types.py:77, mwr_update - コピー.py:441
        ("*", "Display UI to edit identifier sets"): "識別子セットを編集するUIを表示する",
        # mwr_types.py:85
        ("*", "Name of the last symmetrized mesh object"): "最後に対称化処理をしたメッシュオブジェクトの名前",
        # mwr_uix_update.py:27, mwr_update - コピー.py:18
        ("*", "Update"): "アップデート",
        # mwr_uix_update.py:30, mwr_update - コピー.py:21
        ("*", "Check for Updates"): "更新を確認",
        # mwr_uix_update.py:33, mwr_update - コピー.py:24
        ("*", "Install"): "インストール",
        # mwr_uix_update.py:34, mwr_update - コピー.py:25
        ("*", "Open Addon Folder"): "アドオンフォルダを開く",
        # mwr_uix_update.py:48
        ("*", "GitHub has a preview release: "): "",
        # mwr_uix_update.py:50
        ("*", "GitHub has a recent release: "): "Githubに最近リリースあり ",
        # mwr_uix_update.py:64, mwr_uix_update.py:65
        ("*", "GitHub has a recent release. "): "Githubに最近リリースあり /  ",
        # mwr_uix_update.py:69
        ("*", "Path to ZIP download folder "): "ZIP保存先フォルダ ",
        # mwr_uix_update.py:79, mwr_update - コピー.py:44
        ("*", "Update file list: "): "更新ファイル一覧： ",
        # mwr_uix_update.py:112, mwr_update - コピー.py:145
        ("*", "Opens the GitHub release page to check for update files"): "GitHubのリリースページを開き、アップデートファイルを確認できます",
        # mwr_uix_update.py:142
        ("*", "Download URL could not be retrieved"): "ダウンロードURLが取得できません",
        # mwr_uix_update.py:150
        ("*", "Please specify a valid download folder and run again"): "ZIP保存先フォルダを指定後、再び実行してください",
        # mwr_uix_update.py:162
        ("*", "Download completed"): "ダウンロードが完了しました",
        # mwr_uix_update.py:165
        ("*", "Download failed"): "ダウンロードできませんでした",
        # mwr_uix_update.py:173, mwr_update - コピー.py:171
        ("*", "Select a ZIP archive beginning with DIVA_MeshWeightReflector to install the update"): "アップデートをインストールするには、DIVA_MeshWeightReflectorで始まるZIPファイルを選択してください",
        # mwr_uix_update.py:179, mwr_update - コピー.py:176
        ("*", "Choose a ZIP file starting with DIVA_MeshWeightReflector"): "DIVA_MeshWeightReflectorで始まるZIPファイルを選択してください",
        # mwr_uix_update.py:195, mwr_update - コピー.py:183
        ("*", "Choose the folder where the addon is installed"): "アドオンがインストールされているフォルダを選択してください",
        # mwr_uix_update.py:228, mwr_update - コピー.py:214
        ("*", "No ZIP file selected. Please specify a file"): "ZIPファイルが選択されていません。ファイルを指定してください",
        # mwr_uix_update.py:238
        ("*", "No ZIP file selected"): "ZIPファイルを選択してください",
        # mwr_uix_update.py:245, mwr_update - コピー.py:223
        ("*", "Only ZIP files starting with DIVA_MeshWeightReflector can be processed"): "DIVA_MeshWeightReflector で始まるZIPファイル以外は処理できません",
        # mwr_uix_update.py:262, mwr_update - コピー.py:240
        ("*", "Missing DIVA_MeshWeightReflector folder or __init__.py inside the ZIP file"): "ZIP内に DIVA_MeshWeightReflector フォルダまたは __init__.py が見つかりません",
        # mwr_uix_update.py:269, mwr_update - コピー.py:248
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "ZIP内の bl_info.name を取得できません",
        # mwr_uix_update.py:292, mwr_update - コピー.py:271
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください",
        # mwr_uix_update.py:298, mwr_update - コピー.py:277
        ("*", "Installation was cancelled"): "インストールはキャンセルされました",
        # mwr_uix_update.py:306, mwr_update - コピー.py:285
        ("*", "__init__.py not found in the selected folder"): "選択されたフォルダに __init__.py が見つかりません",
        # mwr_uix_update.py:313, mwr_update - コピー.py:292
        ("*", "Update failed because bl_info.name does not match"): "bl_info.name が一致しないため、更新できません",
        # mwr_uix_update.py:352, mwr_uix_update.py:74, mwr_update - コピー.py:315, mwr_update - コピー.py:39
        ("*", "Update completed. Please restart Blender"): "更新が完了しました。Blenderを再起動してください",
        # mwr_uix_update.py:357, mwr_update - コピー.py:320
        ("*", "Update failed: {error}"): "更新に失敗しました: {error}",
        # mwr_uix_update.py:365, mwr_update - コピー.py:328
        ("*", "Please select a ZIP file"): "ZIPファイルを選択してください",
        # mwr_uix_update.py:366, mwr_update - コピー.py:329
        ("*", "Please restart Blender after the update"): "更新後はBlenderを再起動してください",
        # mwr_uix_update.py:373, mwr_update - コピー.py:336
        ("*", "Opens the folder where this addon is installed"): "現在のアドオンフォルダを開く",
        # mwr_uix_update.py:391, mwr_update - コピー.py:354
        ("*", "Scan the folder and list update candidate files"): "ZIPファイルリストの更新",
        # mwr_uix_update.py:405, mwr_update - コピー.py:368
        ("*", "Download folder setting has been saved"): "DLフォルダ設定が保存されました",
        # mwr_uix_update.py:429, mwr_update - コピー.py:391
        ("*", "Sort update files by file name. Click again to toggle order"): "ZIPファイル名ソート(A–Z / Z–A)",
        # mwr_uix_update.py:448, mwr_update - コピー.py:410
        ("*", "Sort update files by update/download date. Click again to toggle order"): "日時順ソート(newest ↔ oldest)",
        # mwr_uix_update.py:481, mwr_update - コピー.py:448
        ("*", "Specify the folder where the update ZIP is stored"): "更新用ZIPが保存されているフォルダを指定してください",
        # mwr_update - コピー.py:30
        ("*", "GitHub has a recent release. Check if it includes updates for this addon."): "GitHubに新しいリリースがあります。更新が含まれているかご確認ください。",
        # mwr_update - コピー.py:34
        ("*", "Path to ZIP download folder"): "ZIP保存先フォルダ",
    },
    "en_US": {
        # mwr_panel.py:47
        ("*", "Bone Identifier:"): "Bone Identifier:",
        # mwr_panel.py:60, mwr_panel.py:72, mwr_panel.py:82
        ("*", "Duplicate and Mirror"): "Duplicate and Mirror",
        # mwr_panel.py:66, mwr_panel.py:76
        ("*", "Apply Modifiers"): "Apply Modifiers",
        # mwr_panel.py:87
        ("*", "Symmetrize Mode"): "Symmetrize Mode",
        # mwr_panel.py:93
        ("*", "Merge Center"): "Merge Center",
        # mwr_panel.py:97
        ("*", "Merge Distance"): "Merge Distance",
        # mwr_panel.py:103
        ("*", "Reflect Mesh Weights"): "Reflect Mesh Weights",
        # mwr_panel.py:117
        ("*", "Creates a mirrored version of the selected mesh object"): "Creates a mirrored version of the selected mesh object",
        # mwr_panel.py:126, mwr_panel.py:245
        ("*", "No object is selected in the 3D View"): "No object is selected in the 3D View",
        # mwr_panel.py:131, mwr_panel.py:250
        ("*", "The active object is not a mesh"): "The active object is not a mesh",
        # mwr_panel.py:140, mwr_panel.py:259
        ("*", "The editing object {name} is not a mesh. Please switch to Object Mode"): "The editing object {name} is not a mesh. Please switch to Object Mode",
        # mwr_panel.py:145, mwr_panel.py:264
        ("*", "The current mode is {mode}. Please run in Object Mode"): "The current mode is {mode}. Please run in Object Mode",
        # mwr_panel.py:150, mwr_panel.py:269
        ("*", "The selected object {name} is not a mesh. Please select a mesh object"): "The selected object {name} is not a mesh. Please select a mesh object",
        # mwr_panel.py:158
        ("*", "Identifier rule {label} not found"): "Identifier rule {label} not found",
        # mwr_panel.py:176, mwr_panel.py:313
        ("*", "Symmetrization completed: {name}. Applied modifiers: {types}"): "Symmetrization completed: {name}. Applied modifiers: {types}",
        # mwr_panel.py:178, mwr_panel.py:180, mwr_panel.py:301, mwr_panel.py:315
        ("*", "Symmetrization completed: {name}"): "Symmetrization completed: {name}",
        # mwr_panel.py:182
        ("*", "Symmetrization failed"): "Symmetrization failed",
        # mwr_panel.py:217, mwr_panel.py:227
        ("*", "Mirrored version generated: {name}"): "Mirrored version generated: {name}",
        # mwr_panel.py:225
        ("*", "Mirrored version generated: {name}. Applied modifiers: {types}"): "Mirrored version generated: {name}. Applied modifiers: {types}",
        # mwr_panel.py:236
        ("*", "Symmetrizes the selected mesh object"): "Symmetrizes the selected mesh object",
        # mwr_panel.py:323
        ("*", "Open the addon settings in Preferences"): "Open the addon settings in Preferences",
        # mwr_preferences.py:46
        ("*", "Editing Identifier Sets"): "Editing Identifier Sets",
        # mwr_preferences.py:76
        ("*", "Set name"): "Set name",
        # mwr_preferences.py:83
        ("*", "Right"): "Right",
        # mwr_preferences.py:84
        ("*", "Left"): "Left",
        # mwr_preferences.py:91
        ("*", "Add a pair"): "Add a pair",
        # mwr_preferences.py:101
        ("*", "Add Identifier Set"): "Add Identifier Set",
        # mwr_preferences.py:102
        ("*", "Restore Default Set"): "Restore Default Set",
        # mwr_preferences.py:105
        ("*", "Synchronize"): "Synchronize",
        # mwr_preferences.py:106
        ("*", "Reset"): "Reset",
        # mwr_preferences.py:107
        ("*", "Save"): "Save",
        # mwr_preferences.py:114
        ("*", "Add a new identifier set to the preferences"): "Add a new identifier set to the preferences",
        # mwr_preferences.py:127
        ("*", "A new set of identifiers has been added"): "A new set of identifiers has been added",
        # mwr_preferences.py:135
        ("*", "Add a left-right identifier rule to the selected set"): "Add a left-right identifier rule to the selected set",
        # mwr_preferences.py:148
        ("*", "Identifier pair has been added"): "Identifier pair has been added",
        # mwr_preferences.py:157
        ("*", "Move the identifier set up one position"): "Move the identifier set up one position",
        # mwr_preferences.py:167
        ("*", "Already at the top"): "Already at the top",
        # mwr_preferences.py:171
        ("*", "Moved up"): "Moved up",
        # mwr_preferences.py:179
        ("*", "Move the identifier set down one position"): "Move the identifier set down one position",
        # mwr_preferences.py:190
        ("*", "Moved down"): "Moved down",
        # mwr_preferences.py:192
        ("*", "Already at the bottom"): "Already at the bottom",
        # mwr_preferences.py:201
        ("*", "Save all identifier sets to a JSON file"): "Save all identifier sets to a JSON file",
        # mwr_preferences.py:211
        ("*", "Please enter a name for the identifier set"): "Please enter a name for the identifier set",
        # mwr_preferences.py:214
        ("*", "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name"): "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name",
        # mwr_preferences.py:221
        ("*", "{label} requires identifier pairs with both sides filled in"): "{label} requires identifier pairs with both sides filled in",
        # mwr_preferences.py:224
        ("*", "There is an identifier pair with only one side"): "There is an identifier pair with only one side",
        # mwr_preferences.py:235
        ("*", "Saved!"): "Saved!",
        # mwr_preferences.py:243
        ("*", "Reload the identifier sets from the saved JSON file"): "Reload the identifier sets from the saved JSON file",
        # mwr_preferences.py:248
        ("*", "Reloaded identifier sets"): "Reloaded identifier sets",
        # mwr_preferences.py:255
        ("*", "Synchronize identifier sets"): "Synchronize identifier sets",
        # mwr_preferences.py:263
        ("*", "Synchronized: {names}"): "Synchronized: {names}",
        # mwr_preferences.py:265
        ("*", "No addons were synchronized"): "No addons were synchronized",
        # mwr_preferences.py:267
        ("*", "Sync failed: {msg}"): "Sync failed: {msg}",
        # mwr_preferences.py:275
        ("*", "Insert the default set of identifiers at the top"): "Insert the default set of identifiers at the top",
        # mwr_preferences.py:294
        ("*", "Default set added"): "Default set added",
        # mwr_preferences.py:302
        ("*", "Delete the selected identifier set"): "Delete the selected identifier set",
        # mwr_preferences.py:310
        ("*", "At least one identifier set must be defined"): "At least one identifier set must be defined",
        # mwr_preferences.py:320
        ("*", "Remove the selected identifier pair from the set"): "Remove the selected identifier pair from the set",
        # mwr_preferences.py:332
        ("*", "At least one pair is required"): "At least one pair is required",
        # mwr_preferences.py:336
        ("*", "Identifier pair removed"): "Identifier pair removed",
        # mwr_preferences.py:340
        ("*", "Failed to delete: {msg}"): "Failed to delete: {msg}",
        # mwr_sub.py:10
        ("*", "Subdivision Surface"): "Subdivision Surface",
        # mwr_sub.py:11
        ("*", "Mirror"): "Mirror",
        # mwr_sub.py:12
        ("*", "Lattice"): "Lattice",
        # mwr_sub.py:13
        ("*", "Shrinkwrap"): "Shrinkwrap",
        # mwr_sub.py:14
        ("*", "Data Transfer"): "Data Transfer",
        # mwr_sub.py:15
        ("*", "Mesh Deform"): "Mesh Deform",
        # mwr_sub.py:16
        ("*", "Vertex Weight Edit"): "Vertex Weight Edit",
        # mwr_sub.py:17
        ("*", "Vertex Weight Mix"): "Vertex Weight Mix",
        # mwr_sub.py:18
        ("*", "Vertex Weight Proximity"): "Vertex Weight Proximity",
        # mwr_sub.py:19
        ("*", "Armature"): "Armature",
        # mwr_sub.py:20
        ("*", "Solidify"): "Solidify",
        # mwr_sub.py:21
        ("*", "Decimate"): "Decimate",
        # mwr_sub.py:22
        ("*", "Boolean"): "Boolean",
        # mwr_types.py:15
        ("*", "Duplicate and mirror selected mesh"): "Duplicate and mirror selected mesh",
        # mwr_types.py:21
        ("*", "Enable alternative symmetrize mode"): "Enable alternative symmetrize mode",
        # mwr_types.py:27
        ("*", "Merge vertices near X=0 when mirroring"): "Merge vertices near X=0 when mirroring",
        # mwr_types.py:33
        ("*", "X-axis threshold used for merge detection"): "X-axis threshold used for merge detection",
        # mwr_types.py:43
        ("*", "Apply specific modifiers before processing"): "Apply specific modifiers before processing",
        # mwr_types.py:55
        ("*", "Whether to use regular expressions"): "Whether to use regular expressions",
        # mwr_types.py:77, mwr_update - コピー.py:441
        ("*", "Display UI to edit identifier sets"): "Display UI to edit identifier sets",
        # mwr_types.py:85
        ("*", "Name of the last symmetrized mesh object"): "Name of the last symmetrized mesh object",
        # mwr_uix_update.py:27, mwr_update - コピー.py:18
        ("*", "Update"): "Update",
        # mwr_uix_update.py:30, mwr_update - コピー.py:21
        ("*", "Check for Updates"): "Check for Updates",
        # mwr_uix_update.py:33, mwr_update - コピー.py:24
        ("*", "Install"): "Install",
        # mwr_uix_update.py:34, mwr_update - コピー.py:25
        ("*", "Open Addon Folder"): "Open Addon Folder",
        # mwr_uix_update.py:48
        ("*", "GitHub has a preview release: "): "GitHub has a preview release: ",
        # mwr_uix_update.py:50
        ("*", "GitHub has a recent release: "): "GitHub has a recent release: ",
        # mwr_uix_update.py:64, mwr_uix_update.py:65
        ("*", "GitHub has a recent release. "): "GitHub has a recent release. ",
        # mwr_uix_update.py:69
        ("*", "Path to ZIP download folder "): "Path to ZIP download folder ",
        # mwr_uix_update.py:79, mwr_update - コピー.py:44
        ("*", "Update file list: "): "Update file list: ",
        # mwr_uix_update.py:112, mwr_update - コピー.py:145
        ("*", "Opens the GitHub release page to check for update files"): "Opens the GitHub release page to check for update files",
        # mwr_uix_update.py:142
        ("*", "Download URL could not be retrieved"): "Download URL could not be retrieved",
        # mwr_uix_update.py:150
        ("*", "Please specify a valid download folder and run again"): "Please specify a valid download folder and run again",
        # mwr_uix_update.py:162
        ("*", "Download completed"): "Download completed",
        # mwr_uix_update.py:165
        ("*", "Download failed"): "Download failed",
        # mwr_uix_update.py:173, mwr_update - コピー.py:171
        ("*", "Select a ZIP archive beginning with DIVA_MeshWeightReflector to install the update"): "Select a ZIP archive beginning with DIVA_MeshWeightReflector to install the update",
        # mwr_uix_update.py:179, mwr_update - コピー.py:176
        ("*", "Choose a ZIP file starting with DIVA_MeshWeightReflector"): "Choose a ZIP file starting with DIVA_MeshWeightReflector",
        # mwr_uix_update.py:195, mwr_update - コピー.py:183
        ("*", "Choose the folder where the addon is installed"): "Choose the folder where the addon is installed",
        # mwr_uix_update.py:228, mwr_update - コピー.py:214
        ("*", "No ZIP file selected. Please specify a file"): "No ZIP file selected. Please specify a file",
        # mwr_uix_update.py:238
        ("*", "No ZIP file selected"): "No ZIP file selected",
        # mwr_uix_update.py:245, mwr_update - コピー.py:223
        ("*", "Only ZIP files starting with DIVA_MeshWeightReflector can be processed"): "Only ZIP files starting with DIVA_MeshWeightReflector can be processed",
        # mwr_uix_update.py:262, mwr_update - コピー.py:240
        ("*", "Missing DIVA_MeshWeightReflector folder or __init__.py inside the ZIP file"): "Missing DIVA_MeshWeightReflector folder or __init__.py inside the ZIP file",
        # mwr_uix_update.py:269, mwr_update - コピー.py:248
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "Could not retrieve bl_info.name from the ZIP file",
        # mwr_uix_update.py:292, mwr_update - コピー.py:271
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "Addon installation folder not found. Please select the destination folder manually",
        # mwr_uix_update.py:298, mwr_update - コピー.py:277
        ("*", "Installation was cancelled"): "Installation was cancelled",
        # mwr_uix_update.py:306, mwr_update - コピー.py:285
        ("*", "__init__.py not found in the selected folder"): "__init__.py not found in the selected folder",
        # mwr_uix_update.py:313, mwr_update - コピー.py:292
        ("*", "Update failed because bl_info.name does not match"): "Update failed because bl_info.name does not match",
        # mwr_uix_update.py:352, mwr_uix_update.py:74, mwr_update - コピー.py:315, mwr_update - コピー.py:39
        ("*", "Update completed. Please restart Blender"): "Update completed. Please restart Blender",
        # mwr_uix_update.py:357, mwr_update - コピー.py:320
        ("*", "Update failed: {error}"): "Update failed: {error}",
        # mwr_uix_update.py:365, mwr_update - コピー.py:328
        ("*", "Please select a ZIP file"): "Please select a ZIP file",
        # mwr_uix_update.py:366, mwr_update - コピー.py:329
        ("*", "Please restart Blender after the update"): "Please restart Blender after the update",
        # mwr_uix_update.py:373, mwr_update - コピー.py:336
        ("*", "Opens the folder where this addon is installed"): "Opens the folder where this addon is installed",
        # mwr_uix_update.py:391, mwr_update - コピー.py:354
        ("*", "Scan the folder and list update candidate files"): "Scan the folder and list update candidate files",
        # mwr_uix_update.py:405, mwr_update - コピー.py:368
        ("*", "Download folder setting has been saved"): "Download folder setting has been saved",
        # mwr_uix_update.py:429, mwr_update - コピー.py:391
        ("*", "Sort update files by file name. Click again to toggle order"): "Sort update files by file name. Click again to toggle order",
        # mwr_uix_update.py:448, mwr_update - コピー.py:410
        ("*", "Sort update files by update/download date. Click again to toggle order"): "Sort update files by update/download date. Click again to toggle order",
        # mwr_uix_update.py:481, mwr_update - コピー.py:448
        ("*", "Specify the folder where the update ZIP is stored"): "Specify the folder where the update ZIP is stored",
        # mwr_update - コピー.py:30
        ("*", "GitHub has a recent release. Check if it includes updates for this addon."): "GitHub has a recent release. Check if it includes updates for this addon.",
        # mwr_update - コピー.py:34
        ("*", "Path to ZIP download folder"): "Path to ZIP download folder",
    },
}

DOMAIN = "diva_mwr"

def register():
    bpy.app.translations.unregister(DOMAIN)
    bpy.app.translations.register(DOMAIN, translation_dict)

def unregister():
    bpy.app.translations.unregister(DOMAIN)