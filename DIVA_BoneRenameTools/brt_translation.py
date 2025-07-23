import bpy

translation_dict = {
    "ja_JP": {
        # brt_panel.py:44
        ("*", "共通部分"): "共通部分",
        # brt_panel.py:48
        ("*", "連番開始番号"): "連番開始番号",
        # brt_panel.py:49
        ("*", "法則"): "法則",
        # brt_panel.py:50
        ("*", "末尾"): "末尾",
        # brt_panel.py:52, brt_ui_rename.py:29
        ("*", "連番リネーム実行"): "連番リネーム実行",
        # brt_panel.py:102
        ("*", "重複識別子を削除"): "重複識別子を削除",
        # brt_panel.py:104
        ("*", "指定名でボーン名変更"): "指定名でボーン名変更",
        # brt_panel.py:141
        ("*", "ボーン識別子:"): "ボーン識別子:",
        # brt_panel.py:160
        ("*", "左右識別子を付与する"): "左右識別子を付与する",
        # brt_panel.py:165
        ("*", "選択ボーンをグローバルXミラーする"): "選択ボーンをグローバルXミラーする",
        # brt_panel.py:169
        ("*", "複製してリネームする"): "複製してリネームする",
        # brt_panel.py:171
        ("*", "選択ボーン反転リネーム"): "選択ボーン反転リネーム",
        # brt_panel.py:182
        ("*", "全対称化付与"): "全対称化付与",
        # brt_panel.py:183
        ("*", "全対称化削除"): "全対称化削除",
        # brt_preferences.py:133
        ("*", "Editing Identifier Sets"): "識別子セット編集",
        # brt_preferences.py:163
        ("*", "Set name"): "セット名",
        # brt_preferences.py:170
        ("*", "Right"): "右",
        # brt_preferences.py:171
        ("*", "Left"): "左",
        # brt_preferences.py:178
        ("*", "Add a pair"): "ペアを追加",
        # brt_preferences.py:187
        ("*", "Add Identifier Set"): "識別子セットを追加します",
        # brt_preferences.py:190
        ("*", "Restore default set"): "デフォルトセットを復元",
        # brt_preferences.py:191
        ("*", "Reset"): "リセット",
        # brt_preferences.py:192
        ("*", "Save"): "保存",
        # brt_preferences.py:199
        ("*", "Add a new identifier set to the preferences"): "新しい識別子を設定に追加します",
        # brt_preferences.py:212
        ("*", "A new set of identifiers has been added"): "新しい識別子セットを追加しました",
        # brt_preferences.py:220
        ("*", "Add a left-right identifier rule to the selected set"): "選択したセットに左右識別子ルールを追加します",
        # brt_preferences.py:233
        ("*", "Identifier pair has been added"): "識別子ペアを追加しました",
        # brt_preferences.py:242
        ("*", "Move the identifier set up one position"): "識別子セットをひとつ上に移動します",
        # brt_preferences.py:252
        ("*", "Already at the top"): "既に先頭にあります",
        # brt_preferences.py:256
        ("*", "Moved up"): "上に移動しました",
        # brt_preferences.py:264
        ("*", "Move the identifier set down one position"): "識別子セットをひとつ下に移動します",
        # brt_preferences.py:275
        ("*", "Moved down"): "下に移動しました",
        # brt_preferences.py:277
        ("*", "Already at the bottom"): "既に末尾にあります",
        # brt_preferences.py:286
        ("*", "Save all identifier sets to a JSON file"): "すべての識別子セットをJSONファイルに保存します",
        # brt_preferences.py:296
        ("*", "Please enter a name for the identifier set"): "識別子セットの名前を入力してください",
        # brt_preferences.py:299
        ("*", "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name"): "{label}には使用できない文字が含まれています。セット名には半角英数字のみを使用してください",
        # brt_preferences.py:306
        ("*", "{label} requires identifier pairs with both sides filled in"): "{label}には両側が入力された識別子ペアが必要です",
        # brt_preferences.py:309
        ("*", "There is an identifier pair with only one side"): "{label}に片側だけの識別子ペアがあります",
        # brt_preferences.py:320
        ("*", "Saved!"): "保存しました！",
        # brt_preferences.py:328
        ("*", "Reload the identifier sets from the saved JSON file"): "保存されたJSONファイルから識別子セットをリロードします",
        # brt_preferences.py:333
        ("*", "Reloaded identifier sets"): "識別子セットを再読込しました",
        # brt_preferences.py:341
        ("*", "Insert the default set of identifiers at the top"): "最上部に識別子のデフォルトセットを復元します",
        # brt_preferences.py:360
        ("*", "Default set added"): "デフォルトセットを追加しました",
        # brt_preferences.py:368
        ("*", "Delete the selected identifier set"): "選択した識別子セットを削除します",
        # brt_preferences.py:376
        ("*", "At least one identifier set must be defined"): "最低でも1つの識別子セットを設定してください",
        # brt_preferences.py:386
        ("*", "Remove the selected identifier pair from the set"): "選択した識別子ペアをセットから削除します",
        # brt_preferences.py:398
        ("*", "At least one pair is required"): "最低1ペアは必要です",
        # brt_preferences.py:402
        ("*", "Identifier pair removed"): "識別子ペアを削除しました",
        # brt_preferences.py:406
        ("*", "Failed to delete: {msg}"): "削除に失敗しました: {msg}",
        # brt_types.py:52
        ("*", "Select a rule in the current set"): "現在のセット内のルールを選択",
        # brt_types.py:63
        ("*", "Whether to use regular expressions"): "正規表現を使用するかどうか",
        # brt_types.py:85
        ("*", "Display UI to edit identifier sets"): "識別子セットを編集するUIを表示する",
        # brt_types.py:91
        ("*", "Enter the common part of the bone name"): "ボーン名の共通部分を入力",
        # brt_types.py:96
        ("*", "Setting the start value for serial numbers"): "連番の開始値の設定",
        # brt_types.py:103
        ("*", "Choose the suffix for bone names"): "ボーン名の末尾を選択",
        # brt_types.py:105
        ("*", "Append `_wj` to the bone name"): "ボーン名の末尾に `_wj` を追加",
        # brt_types.py:106
        ("*", "Append `wj` to the bone name"): "ボーン名の末尾に `wj` を追加",
        # brt_types.py:107
        ("*", "Append `_wj_ex` to the bone name"): "ボーン名の末尾に `_wj_ex` を追加",
        # brt_types.py:108
        ("*", "Append `wj_ex` to the bone name"): "ボーン名の末尾に `wj_ex` を追加",
        # brt_types.py:114
        ("*", "Select numbering pattern for bones"): "ボーンの連番ルールを選択",
        # brt_types.py:116
        ("*", "000 (3 digits)"): "000 (3桁)",
        # brt_types.py:116
        ("*", "Add a 3-digit number"): "3桁の番号を付加",
        # brt_types.py:117
        ("*", "00 (2 digits)"): "00 (2桁)",
        # brt_types.py:117
        ("*", "Add a 2-digit number"): "2桁の番号を付加",
        # brt_types.py:124
        ("*", "Add bones to the end of selected bone branches"): "選択したボーン枝の末端にボーンを追加する",
        # brt_types.py:130
        ("*", "Choose how many bones to add at the end"): "末端に追加するボーンの数を選択",
        # brt_types.py:138
        ("*", "Choose roll correction method for X-mirroring"): "Xミラー時のロール補正方式を選択",
        # brt_types.py:140
        ("*", "DIVA Mode"): "DIVA用",
        # brt_types.py:140
        ("*", "Invert roll, then add 180° and normalize to Blender format"): "roll を反転後 +180 → Blender仕様に正規化",
        # brt_types.py:141
        ("*", "Blender Mode"): "Blender仕様",
        # brt_types.py:141
        ("*", "Symmetry mode: roll *= -1 only"): "対称化モード：roll *= -1 のみ",
        # brt_types.py:142
        ("*", "ロール補正をしない"): "ロール補正をしない",
        # brt_types.py:142
        ("*", "補正なし"): "補正なし",
        # brt_types.py:143
        ("*", "+180"): "+180",
        # brt_types.py:143
        ("*", "+180 → Blender仕様に正規化"): "+180 → Blender仕様に正規化",
        # brt_types.py:150
        ("*", "Enter the original bone name"): "元のボーン名を入力",
        # brt_types.py:156
        ("*", "Enter the new bone name"): "新しいボーン名を入力",
        # brt_types.py:162
        ("*", "Remove duplicate identifiers"): ".001 などの複製識別子を削除します",
        # brt_types.py:168
        ("*", "Show renaming tools based on bone prefixes and numbering rules"): "ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示",
        # brt_types.py:174
        ("*", "Show tools for substring replacement and removing duplicate identifiers"): "ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示",
        # brt_types.py:180
        ("*", "Show tools to invert Left/Right identifiers for selected bones"): "選択ボーンの左右識別子を反転するツールを表示",
        # brt_types.py:186
        ("*", "Show batch renaming for symmetric bone names and revert option"): "左右対応名の一括リネーム（グループ名含む）や、元に戻す操作を表示",
        # brt_types.py:192
        ("*", "Mirror selected bones along global X axis"): "選択したボーンをグローバルX軸でミラー反転させる",
        # brt_types.py:198
        ("*", "Duplicate and rename selected bones"): "選択したボーンを複製してリネームする",
        # brt_types.py:204
        ("*", "Assign left/right identifiers"): "左右識別子を付与",
        # brt_ui_invert.py:34
        ("*", "Bone Identifier:"): "ボーン識別子:",
        # brt_ui_invert.py:41
        ("*", "Assign Left/Right Identifiers"): "左右識別子を付与",
        # brt_ui_invert.py:51
        ("*", "Duplicate and Rename"): "複製してリネーム",
        # brt_ui_invert.py:55
        ("*", "Mirror Selected Bones on X-axis"): "選択ボーンをXミラー",
        # brt_ui_invert.py:65
        ("*", "複製してリネーム"): "複製してリネーム",
        # brt_ui_invert.py:69
        ("*", "選択ボーンをXミラー"): "選択ボーンをXミラー",
        # brt_ui_invert.py:75
        ("*", "Invert Left/Right Bone Names"): "選択ボーン反転リネーム",
        # brt_ui_invert.py:82
        ("*", "Invert left/right in selected bone names"): "選択ボーンの左右反転リネーム",
        # brt_ui_invert.py:100
        ("*", "Renamed {count} bones"): "{count}本のボーン名を変更しました",
        # brt_ui_invert.py:109
        ("*", "Select a linear chain from the currently selected bone"): "選択中ボーンから線形チェーンを選択",
        # brt_ui_invert.py:122, brt_ui_rename.py:131
        ("*", "Filter Out Inconsistent Bones"): "一致しないボーンを除外",
        # brt_ui_invert.py:123
        ("*", "Exclude bones that do not share naming rules"): "ネーミング規則が共通しないボーンを除外します",
        # brt_ui_invert.py:129
        ("*", "Include Branches"): "分岐も含める",
        # brt_ui_invert.py:130
        ("*", "Include branch destinations as the selection target"): "分岐先も選択対象に含めます",
        # brt_ui_invert.py:136
        ("*", "Extended Selection"): "拡張選択",
        # brt_ui_invert.py:137
        ("*", "Select additional bones that match a common group name, ignoring embedded numbers"): "数字部分を除いた共通グループ名に一致するボーンを追加選択します",
        # brt_ui_invert.py:146, brt_ui_rename.py:143, brt_ui_replace.py:83
        ("*", "No armature is selected"): "アーマチュアが選択されていません",
        # brt_ui_invert.py:155
        ("*", "Supported modes are Pose and Edit"): "対応モードは Pose または Edit です",
        # brt_ui_invert.py:159
        ("*", "No origin bone selected"): "起点となるボーンが選択されていません",
        # brt_ui_invert.py:213
        ("*", "Linear chain selected"): "線形チェーンを選択しました",
        # brt_ui_invert.py:223
        ("*", "Open the addon settings in Preferences"): "プリファレンスのアドオン設定画面を開きます",
        # brt_ui_other.py:15
        ("*", "Apply Symmetric Renaming"): "全対称化付与",
        # brt_ui_other.py:16
        ("*", "Remove Symmetric Renaming"): "全対称化削除",
        # brt_ui_other.py:24
        ("*", "Rename specific words"): "特定単語をリネーム",
        # brt_ui_other.py:30
        ("*", "Symmetric renaming applied successfully"): "左右識別子の付与が完了しました",
        # brt_ui_other.py:38
        ("*", "Revert renamed names"): "名前を元に戻す",
        # brt_ui_other.py:44
        ("*", "Symmetric renaming reverted"): "左右識別子を削除しました",
        # brt_ui_rename.py:15
        ("*", "Base Name"): "ベース名",
        # brt_ui_rename.py:19
        ("*", "Start Number"): "連番開始番号",
        # brt_ui_rename.py:20
        ("*", "Rule"): "法則",
        # brt_ui_rename.py:21
        ("*", "Suffix"): "末尾",
        # brt_ui_rename.py:25
        ("*", "Add bones at chain end"): "末端にボーンを追加する",
        # brt_ui_rename.py:27, brt_ui_rename.py:42
        ("*", "Number of bones to add"): "追加ボーン数",
        # brt_ui_rename.py:30
        ("*", "Execute Sequential Rename"): "連番リネーム実行",
        # brt_ui_rename.py:39
        ("*", "Renames the selected bone rows based on the specified settings"): "選択されたボーン列の名前を指定の設定に基づいて連番リネームします",
        # brt_ui_rename.py:96
        ("*", "Detect common prefix among selected bone names and apply settings automatically"): "選択ボーン名の共通部分を抽出し、設定を自動反映します",
        # brt_ui_rename.py:116, brt_ui_replace.py:73
        ("*", "Select Linear Chain"): "線形チェーンを選択",
        # brt_ui_rename.py:117
        ("*", "If enabled, automatically selects linear parent-child chain from selected bone"): "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        # brt_ui_rename.py:123
        ("*", "Select Only Toward Terminal"): "末端方向のみ選択",
        # brt_ui_rename.py:124
        ("*", "If enabled, targets only the terminal direction from the initially selected bone"): "ONの場合、最初に選択されたボーンから末端までを対象とします",
        # brt_ui_rename.py:132
        ("*", "Filters out bones with clearly different naming patterns from extraction"): "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します",
        # brt_ui_rename.py:154, brt_ui_replace.py:92
        ("*", "Only Pose or Edit mode is supported"): "対応しているのは Pose モードまたは Edit モードです",
        # brt_ui_rename.py:158, brt_ui_replace.py:96
        ("*", "No bones are selected"): "ボーンが選択されていません",
        # brt_ui_rename.py:170
        ("*", "Common prefix set: {prefix}"): "ベース名を設定: {prefix}",
        # brt_ui_rename.py:172, brt_ui_replace.py:110
        ("*", "Could not detect common prefix"): "ベース名が検出できませんでした",
        # brt_ui_replace.py:35
        ("*", "Remove duplicate suffix"): "重複識別子を削除",
        # brt_ui_replace.py:37
        ("*", "Rename Bones by Specified Name"): "指定名でボーン名変更",
        # brt_ui_replace.py:45
        ("*", "Replace the selected bone name substring in bulk"): "ボーン名の一部を一括置換",
        # brt_ui_replace.py:61
        ("*", "Bone name replacement completed"): "ボーン名の置換を完了しました",
        # brt_ui_replace.py:71
        ("*", "Extract source name from selected bones"): "選択ボーンから置換元名を抽出",
        # brt_ui_replace.py:74
        ("*", "If enabled, automatically selects a linear parent-child chain from selected bone"): "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        # brt_ui_replace.py:108
        ("*", "Detected prefix: {prefix}"): "抽出結果: {prefix}",
        # brt_update.py:16
        ("*", "Update"): "アップデート",
        # brt_update.py:19
        ("*", "Check for Updates"): "更新を確認",
        # brt_update.py:22
        ("*", "Install"): "インストール",
        # brt_update.py:23
        ("*", "Open Addon Folder"): "アドオンフォルダを開く",
        # brt_update.py:27
        ("*", "Path to ZIP download folder"): "ダウンロードフォルダーへのzipへのパス",
        # brt_update.py:37
        ("*", "Update file list:"): "更新ファイル一覧: ",
        # brt_update.py:93
        ("*", "Opens the GitHub release page to check for update files"): "GitHubのリリースページを開き、アップデートファイルを確認できます",
        # brt_update.py:111
        ("*", "Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update"): "アップデートをインストールするには、DIVA_BoneRenameToolsで始まるZIPファイルを選択してください",
        # brt_update.py:116
        ("*", "Choose a ZIP file starting with DIVA_BoneRenameTools"): "DIVA_BoneRenameToolsで始まるZIPファイルを選択してください",
        # brt_update.py:123
        ("*", "Choose the folder where the addon is installed"): "アドオンがインストールされているフォルダを選択してください",
        # brt_update.py:154
        ("*", "No ZIP file selected. Please specify a file"): "ZIPファイルが選択されていません。ファイルを指定してください",
        # brt_update.py:162
        ("*", "Only ZIP files starting with DIVA_BoneRenameTools can be processed"): "DIVA_BoneRenameTools で始まるZIPファイル以外は処理できません",
        # brt_update.py:179
        ("*", "Missing DIVA_BoneRenameTools folder or __init__.py inside the ZIP file"): "ZIP内に DIVA_BoneRenameTools フォルダまたは __init__.py が見つかりません",
        # brt_update.py:186
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "ZIP内の bl_info.name を取得できません",
        # brt_update.py:208
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください",
        # brt_update.py:214
        ("*", "Installation was cancelled"): "インストールはキャンセルされました",
        # brt_update.py:222
        ("*", "__init__.py not found in the selected folder"): "選択されたフォルダに __init__.py が見つかりません",
        # brt_update.py:229
        ("*", "Update failed because bl_info.name does not match"): "bl_info.name が一致しないため、更新できません",
        # brt_update.py:248, brt_update.py:32
        ("*", "Update completed. Please restart Blender"): "更新が完了しました。Blenderを再起動してください",
        # brt_update.py:253
        ("*", "Update failed: {error}"): "更新に失敗しました: {error}",
        # brt_update.py:261
        ("*", "Please select a ZIP file"): "ZIPファイルを選択してください",
        # brt_update.py:262
        ("*", "Please restart Blender after the update"): "更新後はBlenderを再起動してください",
        # brt_update.py:269
        ("*", "Opens the folder where this addon is installed"): "現在のアドオンフォルダを開く",
        # brt_update.py:287
        ("*", "Scan the folder and list update candidate files"): "ZIPファイルリストの更新",
        # brt_update.py:300
        ("*", "Download folder setting has been saved"): "DLフォルダ設定が保存されました",
        # brt_update.py:322
        ("*", "Sort update files by file name. Click again to toggle order"): "ZIPファイル名ソート(A–Z / Z–A)",
        # brt_update.py:341
        ("*", "Sort update files by update/download date. Click again to toggle order"): "日時順ソート(newest ↔ oldest)",
        # brt_update.py:372
        ("*", "Specify the folder where the update ZIP is stored"): "更新用ZIPが保存されているフォルダを指定してください",
    },
    "en_US": {
        # brt_panel.py:44
        ("*", "共通部分"): "Base name",
        # brt_panel.py:48
        ("*", "連番開始番号"): "Serial number start number",
        # brt_panel.py:49
        ("*", "法則"): "law",
        # brt_panel.py:50
        ("*", "末尾"): "end",
        # brt_panel.py:52, brt_ui_rename.py:29
        ("*", "連番リネーム実行"): "Running serial number renames",
        # brt_panel.py:102
        ("*", "重複識別子を削除"): "Remove duplicate identifiers",
        # brt_panel.py:104
        ("*", "指定名でボーン名変更"): "Change bone name with specified name",
        # brt_panel.py:141
        ("*", "ボーン識別子:"): "Bone Identifier:",
        # brt_panel.py:160
        ("*", "左右識別子を付与する"): "Give left and right identifiers",
        # brt_panel.py:165
        ("*", "選択ボーンをグローバルXミラーする"): "Global X-mirror of selection bones",
        # brt_panel.py:169
        ("*", "複製してリネームする"): "Duplicate and rename",
        # brt_panel.py:171
        ("*", "選択ボーン反転リネーム"): "Select bone inverted rename",
        # brt_panel.py:182
        ("*", "全対称化付与"): "All symmetricalization",
        # brt_panel.py:183
        ("*", "全対称化削除"): "All symmetric removal",
        # brt_preferences.py:133
        ("*", "Editing Identifier Sets"): "Editing Identifier Sets",
        # brt_preferences.py:163
        ("*", "Set name"): "Set name",
        # brt_preferences.py:170
        ("*", "Right"): "Right",
        # brt_preferences.py:171
        ("*", "Left"): "Left",
        # brt_preferences.py:178
        ("*", "Add a pair"): "Add a pair",
        # brt_preferences.py:187
        ("*", "Add Identifier Set"): "Add Identifier Set",
        # brt_preferences.py:190
        ("*", "Restore default set"): "Restore default set",
        # brt_preferences.py:191
        ("*", "Reset"): "Reset",
        # brt_preferences.py:192
        ("*", "Save"): "Save",
        # brt_preferences.py:199
        ("*", "Add a new identifier set to the preferences"): "Add a new identifier set to the preferences",
        # brt_preferences.py:212
        ("*", "A new set of identifiers has been added"): "A new set of identifiers has been added",
        # brt_preferences.py:220
        ("*", "Add a left-right identifier rule to the selected set"): "Add a left-right identifier rule to the selected set",
        # brt_preferences.py:233
        ("*", "Identifier pair has been added"): "Identifier pair has been added",
        # brt_preferences.py:242
        ("*", "Move the identifier set up one position"): "Move the identifier set up one position",
        # brt_preferences.py:252
        ("*", "Already at the top"): "Already at the top",
        # brt_preferences.py:256
        ("*", "Moved up"): "Moved up",
        # brt_preferences.py:264
        ("*", "Move the identifier set down one position"): "Move the identifier set down one position",
        # brt_preferences.py:275
        ("*", "Moved down"): "Moved down",
        # brt_preferences.py:277
        ("*", "Already at the bottom"): "Already at the bottom",
        # brt_preferences.py:286
        ("*", "Save all identifier sets to a JSON file"): "Save all identifier sets to a JSON file",
        # brt_preferences.py:296
        ("*", "Please enter a name for the identifier set"): "Please enter a name for the identifier set",
        # brt_preferences.py:299
        ("*", "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name"): "{label} contains unsupported characters. Please use only ASCII letters and numbers in the set name",
        # brt_preferences.py:306
        ("*", "{label} requires identifier pairs with both sides filled in"): "{label} requires identifier pairs with both sides filled in",
        # brt_preferences.py:309
        ("*", "There is an identifier pair with only one side"): "There is an identifier pair with only one side",
        # brt_preferences.py:320
        ("*", "Saved!"): "Saved!",
        # brt_preferences.py:328
        ("*", "Reload the identifier sets from the saved JSON file"): "Reload the identifier sets from the saved JSON file",
        # brt_preferences.py:333
        ("*", "Reloaded identifier sets"): "Reloaded identifier sets",
        # brt_preferences.py:341
        ("*", "Insert the default set of identifiers at the top"): "Insert the default set of identifiers at the top",
        # brt_preferences.py:360
        ("*", "Default set added"): "Default set added",
        # brt_preferences.py:368
        ("*", "Delete the selected identifier set"): "Delete the selected identifier set",
        # brt_preferences.py:376
        ("*", "At least one identifier set must be defined"): "At least one identifier set must be defined",
        # brt_preferences.py:386
        ("*", "Remove the selected identifier pair from the set"): "Remove the selected identifier pair from the set",
        # brt_preferences.py:398
        ("*", "At least one pair is required"): "At least one pair is required",
        # brt_preferences.py:402
        ("*", "Identifier pair removed"): "Identifier pair removed",
        # brt_preferences.py:406
        ("*", "Failed to delete: {msg}"): "Failed to delete: {msg}",
        # brt_types.py:52
        ("*", "Select a rule in the current set"): "Select a rule in the current set",
        # brt_types.py:63
        ("*", "Whether to use regular expressions"): "Whether to use regular expressions",
        # brt_types.py:85
        ("*", "Display UI to edit identifier sets"): "Display UI to edit identifier sets",
        # brt_types.py:91
        ("*", "Enter the common part of the bone name"): "Enter the common part of the bone name",
        # brt_types.py:96
        ("*", "Setting the start value for serial numbers"): "Setting the start value for serial numbers",
        # brt_types.py:103
        ("*", "Choose the suffix for bone names"): "Choose the suffix for bone names",
        # brt_types.py:105
        ("*", "Append `_wj` to the bone name"): "Append `_wj` to the bone name",
        # brt_types.py:106
        ("*", "Append `wj` to the bone name"): "Append `wj` to the bone name",
        # brt_types.py:107
        ("*", "Append `_wj_ex` to the bone name"): "Append `_wj_ex` to the bone name",
        # brt_types.py:108
        ("*", "Append `wj_ex` to the bone name"): "Append `wj_ex` to the bone name",
        # brt_types.py:114
        ("*", "Select numbering pattern for bones"): "Select numbering pattern for bones",
        # brt_types.py:116
        ("*", "000 (3 digits)"): "000 (3 digits)",
        # brt_types.py:116
        ("*", "Add a 3-digit number"): "Add a 3-digit number",
        # brt_types.py:117
        ("*", "00 (2 digits)"): "00 (2 digits)",
        # brt_types.py:117
        ("*", "Add a 2-digit number"): "Add a 2-digit number",
        # brt_types.py:124
        ("*", "Add bones to the end of selected bone branches"): "Add bones to the end of selected bone branches",
        # brt_types.py:130
        ("*", "Choose how many bones to add at the end"): "Choose how many bones to add at the end",
        # brt_types.py:138
        ("*", "Choose roll correction method for X-mirroring"): "Choose roll correction method for X-mirroring",
        # brt_types.py:140
        ("*", "DIVA Mode"): "DIVA Mode",
        # brt_types.py:140
        ("*", "Invert roll, then add 180° and normalize to Blender format"): "Invert roll, then add 180° and normalize to Blender format",
        # brt_types.py:141
        ("*", "Blender Mode"): "Blender Mode",
        # brt_types.py:141
        ("*", "Symmetry mode: roll *= -1 only"): "Symmetry mode: roll *= -1 only",
        # brt_types.py:142
        ("*", "ロール補正をしない"): "Do not perform roll correction",
        # brt_types.py:142
        ("*", "補正なし"): "No correction",
        # brt_types.py:143
        ("*", "+180"): "+180",
        # brt_types.py:143
        ("*", "+180 → Blender仕様に正規化"): "+180 → Normalized to Blender specification",
        # brt_types.py:150
        ("*", "Enter the original bone name"): "Enter the original bone name",
        # brt_types.py:156
        ("*", "Enter the new bone name"): "Enter the new bone name",
        # brt_types.py:162
        ("*", "Remove duplicate identifiers"): "Remove duplicate identifiers",
        # brt_types.py:168
        ("*", "Show renaming tools based on bone prefixes and numbering rules"): "Show renaming tools based on bone prefixes and numbering rules",
        # brt_types.py:174
        ("*", "Show tools for substring replacement and removing duplicate identifiers"): "Show tools for substring replacement and removing duplicate identifiers",
        # brt_types.py:180
        ("*", "Show tools to invert Left/Right identifiers for selected bones"): "Show tools to invert Left/Right identifiers for selected bones",
        # brt_types.py:186
        ("*", "Show batch renaming for symmetric bone names and revert option"): "Show batch renaming for symmetric bone names and revert option",
        # brt_types.py:192
        ("*", "Mirror selected bones along global X axis"): "Mirror selected bones along global X axis",
        # brt_types.py:198
        ("*", "Duplicate and rename selected bones"): "Duplicate and rename selected bones",
        # brt_types.py:204
        ("*", "Assign left/right identifiers"): "Assign left/right identifiers",
        # brt_ui_invert.py:34
        ("*", "Bone Identifier:"): "Bone Identifier:",
        # brt_ui_invert.py:41
        ("*", "Assign Left/Right Identifiers"): "Assign Left/Right Identifiers",
        # brt_ui_invert.py:51
        ("*", "Duplicate and Rename"): "Duplicate and Rename",
        # brt_ui_invert.py:55
        ("*", "Mirror Selected Bones on X-axis"): "Mirror Selected Bones on X-axis",
        # brt_ui_invert.py:65
        ("*", "複製してリネーム"): "Duplicate and rename",
        # brt_ui_invert.py:69
        ("*", "選択ボーンをXミラー"): "X-mirror of selection bones",
        # brt_ui_invert.py:75
        ("*", "Invert Left/Right Bone Names"): "Invert Left/Right Bone Names",
        # brt_ui_invert.py:82
        ("*", "Invert left/right in selected bone names"): "Invert left/right in selected bone names",
        # brt_ui_invert.py:100
        ("*", "Renamed {count} bones"): "Renamed {count} bones",
        # brt_ui_invert.py:109
        ("*", "Select a linear chain from the currently selected bone"): "Select a linear chain from the currently selected bone",
        # brt_ui_invert.py:122, brt_ui_rename.py:131
        ("*", "Filter Out Inconsistent Bones"): "Filter Out Inconsistent Bones",
        # brt_ui_invert.py:123
        ("*", "Exclude bones that do not share naming rules"): "Exclude bones that do not share naming rules",
        # brt_ui_invert.py:129
        ("*", "Include Branches"): "Include Branches",
        # brt_ui_invert.py:130
        ("*", "Include branch destinations as the selection target"): "Include branch destinations as the selection target",
        # brt_ui_invert.py:136
        ("*", "Extended Selection"): "Extended Selection",
        # brt_ui_invert.py:137
        ("*", "Select additional bones that match a common group name, ignoring embedded numbers"): "Select additional bones that match a common group name, ignoring embedded numbers",
        # brt_ui_invert.py:146, brt_ui_rename.py:143, brt_ui_replace.py:83
        ("*", "No armature is selected"): "No armature is selected",
        # brt_ui_invert.py:155
        ("*", "Supported modes are Pose and Edit"): "Supported modes are Pose and Edit",
        # brt_ui_invert.py:159
        ("*", "No origin bone selected"): "No origin bone selected",
        # brt_ui_invert.py:213
        ("*", "Linear chain selected"): "Linear chain selected",
        # brt_ui_invert.py:223
        ("*", "Open the addon settings in Preferences"): "Open the addon settings in Preferences",
        # brt_ui_other.py:15
        ("*", "Apply Symmetric Renaming"): "Apply Symmetric Renaming",
        # brt_ui_other.py:16
        ("*", "Remove Symmetric Renaming"): "Remove Symmetric Renaming",
        # brt_ui_other.py:24
        ("*", "Rename specific words"): "Rename specific words",
        # brt_ui_other.py:30
        ("*", "Symmetric renaming applied successfully"): "Symmetric renaming applied successfully",
        # brt_ui_other.py:38
        ("*", "Revert renamed names"): "Revert renamed names",
        # brt_ui_other.py:44
        ("*", "Symmetric renaming reverted"): "Symmetric renaming reverted",
        # brt_ui_rename.py:15
        ("*", "Base Name"): "Base Name",
        # brt_ui_rename.py:19
        ("*", "Start Number"): "Start Number",
        # brt_ui_rename.py:20
        ("*", "Rule"): "Rule",
        # brt_ui_rename.py:21
        ("*", "Suffix"): "Suffix",
        # brt_ui_rename.py:25
        ("*", "Add bones at chain end"): "Add bones at chain end",
        # brt_ui_rename.py:27, brt_ui_rename.py:42
        ("*", "Number of bones to add"): "Number of bones to add",
        # brt_ui_rename.py:30
        ("*", "Execute Sequential Rename"): "Execute Sequential Rename",
        # brt_ui_rename.py:39
        ("*", "Renames the selected bone rows based on the specified settings"): "Renames the selected bone rows based on the specified settings",
        # brt_ui_rename.py:96
        ("*", "Detect common prefix among selected bone names and apply settings automatically"): "Detect common prefix among selected bone names and apply settings automatically",
        # brt_ui_rename.py:116, brt_ui_replace.py:73
        ("*", "Select Linear Chain"): "Select Linear Chain",
        # brt_ui_rename.py:117
        ("*", "If enabled, automatically selects linear parent-child chain from selected bone"): "If enabled, automatically selects linear parent-child chain from selected bone",
        # brt_ui_rename.py:123
        ("*", "Select Only Toward Terminal"): "Select Only Toward Terminal",
        # brt_ui_rename.py:124
        ("*", "If enabled, targets only the terminal direction from the initially selected bone"): "If enabled, targets only the terminal direction from the initially selected bone",
        # brt_ui_rename.py:132
        ("*", "Filters out bones with clearly different naming patterns from extraction"): "Filters out bones with clearly different naming patterns from extraction",
        # brt_ui_rename.py:154, brt_ui_replace.py:92
        ("*", "Only Pose or Edit mode is supported"): "Only Pose or Edit mode is supported",
        # brt_ui_rename.py:158, brt_ui_replace.py:96
        ("*", "No bones are selected"): "No bones are selected",
        # brt_ui_rename.py:170
        ("*", "Common prefix set: {prefix}"): "Common prefix set: {prefix}",
        # brt_ui_rename.py:172, brt_ui_replace.py:110
        ("*", "Could not detect common prefix"): "Could not detect common prefix",
        # brt_ui_replace.py:35
        ("*", "Remove duplicate suffix"): "Remove duplicate suffix",
        # brt_ui_replace.py:37
        ("*", "Rename Bones by Specified Name"): "Rename Bones by Specified Name",
        # brt_ui_replace.py:45
        ("*", "Replace the selected bone name substring in bulk"): "Replace the selected bone name substring in bulk",
        # brt_ui_replace.py:61
        ("*", "Bone name replacement completed"): "Bone name replacement completed",
        # brt_ui_replace.py:71
        ("*", "Extract source name from selected bones"): "Extract source name from selected bones",
        # brt_ui_replace.py:74
        ("*", "If enabled, automatically selects a linear parent-child chain from selected bone"): "If enabled, automatically selects a linear parent-child chain from selected bone",
        # brt_ui_replace.py:108
        ("*", "Detected prefix: {prefix}"): "Detected prefix: {prefix}",
        # brt_update.py:16
        ("*", "Update"): "Update",
        # brt_update.py:19
        ("*", "Check for Updates"): "Check for Updates",
        # brt_update.py:22
        ("*", "Install"): "Install",
        # brt_update.py:23
        ("*", "Open Addon Folder"): "Open Addon Folder",
        # brt_update.py:27
        ("*", "Path to ZIP download folder"): "Path to ZIP download folder",
        # brt_update.py:37
        ("*", "Update file list:"): "Update file list:",
        # brt_update.py:93
        ("*", "Opens the GitHub release page to check for update files"): "Opens the GitHub release page to check for update files",
        # brt_update.py:111
        ("*", "Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update"): "Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update",
        # brt_update.py:116
        ("*", "Choose a ZIP file starting with DIVA_BoneRenameTools"): "Choose a ZIP file starting with DIVA_BoneRenameTools",
        # brt_update.py:123
        ("*", "Choose the folder where the addon is installed"): "Choose the folder where the addon is installed",
        # brt_update.py:154
        ("*", "No ZIP file selected. Please specify a file"): "No ZIP file selected. Please specify a file",
        # brt_update.py:162
        ("*", "Only ZIP files starting with DIVA_BoneRenameTools can be processed"): "Only ZIP files starting with DIVA_BoneRenameTools can be processed",
        # brt_update.py:179
        ("*", "Missing DIVA_BoneRenameTools folder or __init__.py inside the ZIP file"): "Missing DIVA_BoneRenameTools folder or __init__.py inside the ZIP file",
        # brt_update.py:186
        ("*", "Could not retrieve bl_info.name from the ZIP file"): "Could not retrieve bl_info.name from the ZIP file",
        # brt_update.py:208
        ("*", "Addon installation folder not found. Please select the destination folder manually"): "Addon installation folder not found. Please select the destination folder manually",
        # brt_update.py:214
        ("*", "Installation was cancelled"): "Installation was cancelled",
        # brt_update.py:222
        ("*", "__init__.py not found in the selected folder"): "__init__.py not found in the selected folder",
        # brt_update.py:229
        ("*", "Update failed because bl_info.name does not match"): "Update failed because bl_info.name does not match",
        # brt_update.py:248, brt_update.py:32
        ("*", "Update completed. Please restart Blender"): "Update completed. Please restart Blender",
        # brt_update.py:253
        ("*", "Update failed: {error}"): "Update failed: {error}",
        # brt_update.py:261
        ("*", "Please select a ZIP file"): "Please select a ZIP file",
        # brt_update.py:262
        ("*", "Please restart Blender after the update"): "Please restart Blender after the update",
        # brt_update.py:269
        ("*", "Opens the folder where this addon is installed"): "Opens the folder where this addon is installed",
        # brt_update.py:287
        ("*", "Scan the folder and list update candidate files"): "Scan the folder and list update candidate files",
        # brt_update.py:300
        ("*", "Download folder setting has been saved"): "Download folder setting has been saved",
        # brt_update.py:322
        ("*", "Sort update files by file name. Click again to toggle order"): "Sort update files by file name. Click again to toggle order",
        # brt_update.py:341
        ("*", "Sort update files by update/download date. Click again to toggle order"): "Sort update files by update/download date. Click again to toggle order",
        # brt_update.py:372
        ("*", "Specify the folder where the update ZIP is stored"): "Specify the folder where the update ZIP is stored",
    },
}

def register():
    bpy.app.translations.unregister(__name__)
    bpy.app.translations.register(__name__, translation_dict)

def unregister():
    bpy.app.translations.unregister(__name__)