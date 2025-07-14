import bpy

translation_dict = {
    "ja_JP": {
        # brt_panel.py:44, brt_types.py:75, brt_ui_rename.py:15
        ("*", "共通部分"): "ベース名",
        # brt_panel.py:48, brt_ui_rename.py:19
        ("*", "連番開始番号"): "連番開始番号",
        # brt_panel.py:49, brt_ui_rename.py:20
        ("*", "法則"): "法則",
        # brt_panel.py:50, brt_ui_rename.py:21
        ("*", "末尾"): "末尾",
        # brt_panel.py:52, brt_ui_rename.py:23
        ("*", "連番リネーム実行"): "連番リネーム実行",
        # brt_panel.py:102, brt_ui_replace.py:35
        ("*", "重複識別子を削除"): "重複識別子を削除",
        # brt_panel.py:104, brt_ui_replace.py:37
        ("*", "指定名でボーン名変更"): "指定名でボーン名変更",
        # brt_panel.py:141, brt_ui_invert.py:33
        ("*", "ボーン識別子:"): "ボーン識別子:",
        # brt_panel.py:160, brt_types.py:165, brt_ui_invert.py:40
        ("*", "左右識別子を付与する"): "左右識別子を付与する",
        # brt_panel.py:165, brt_ui_invert.py:45
        ("*", "選択ボーンをグローバルXミラーする"): "選択ボーンをグローバルXミラーする",
        # brt_panel.py:169, brt_ui_invert.py:49
        ("*", "複製してリネームする"): "複製してリネームする",
        # brt_panel.py:171, brt_ui_invert.py:51
        ("*", "選択ボーン反転リネーム"): "選択ボーン反転リネーム",
        # brt_panel.py:182, brt_ui_other.py:15
        ("*", "全対称化付与"): "全対称化付与",
        # brt_panel.py:183, brt_ui_other.py:16
        ("*", "全対称化削除"): "全対称化削除",
        # brt_preferences.py:121
        ("*", "識別子セットの編集"): "識別子セット編集",
        # brt_preferences.py:140
        ("*", "セット名"): "セット名",
        # brt_preferences.py:146
        ("*", "右"): "右",
        # brt_preferences.py:147
        ("*", "左"): "左",
        # brt_preferences.py:154
        ("*", "ペアを追加"): "ペアを追加",
        # brt_preferences.py:163, brt_preferences.py:174
        ("*", "Add Identifier Set"): "識別子セットを追加します",
        # brt_preferences.py:166
        ("*", "デフォルトセットを復元"): "デフォルトセットを復元",
        # brt_preferences.py:167
        ("*", "リセット"): "リセット",
        # brt_preferences.py:168
        ("*", "保存"): "保存",
        # brt_preferences.py:175
        ("*", "Add a new identifier set to the preferences"): "新しい識別子を設定に追加します",
        # brt_preferences.py:190
        ("*", "Add Identifier Rule"): "識別子ルールを追加します",
        # brt_preferences.py:191
        ("*", "Add a left-right identifier rule to the selected set"): "選択したセットに左右識別子ルールを追加します",
        # brt_preferences.py:209
        ("*", "Move Indentifier Set Up"): "識別子セットを上にを移動します",
        # brt_preferences.py:210
        ("*", "Move the identifier set up one position"): "識別子セットをひとつ上に移動します",
        # brt_preferences.py:225
        ("*", "Move Indentifier Set Down"): "識別子セットを下に移動します",
        # brt_preferences.py:226
        ("*", "Move the identifier set down one position"): "識別子セットをひとつ下に移動します",
        # brt_preferences.py:241
        ("*", "Save Identifier Sets"): "識別子セットを保存します",
        # brt_preferences.py:242
        ("*", "Save all identifier sets to a JSON file"): "すべての識別子セットをJSONファイルに保存します",
        # brt_preferences.py:253
        ("*", "{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください"): "{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください",
        # brt_preferences.py:257
        ("*", "識別子セットの名前を入力してください"): "識別子セットの名前を入力してください",
        # brt_preferences.py:264
        ("*", "{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）"): "{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）",
        # brt_preferences.py:268
        ("*", "{label}に片側だけ空白の識別子ペアがあります（両方入力してください）"): "{label}に片側だけ空白の識別子ペアがあります（両方入力してください）",
        # brt_preferences.py:282
        ("*", "保存しました！"): "保存しました！",
        # brt_preferences.py:291
        ("*", "Reload Identifier Sets"): "識別子セットをリセット",
        # brt_preferences.py:292
        ("*", "Reload the identifier sets from the saved JSON file"): "保存されたJSONファイルから識別子セットをリロードします",
        # brt_preferences.py:297
        ("*", "識別子セットを元に戻しました"): "識別子セットを元に戻しました",
        # brt_preferences.py:303
        ("*", "Append Default Set"): "デフォルトセットを復元します",
        # brt_preferences.py:304
        ("*", "Insert the default set of identifiers at the top"): "最上部に識別子のデフォルトセットを復元します",
        # brt_preferences.py:322
        ("*", "デフォルトセットを追加しました"): "デフォルトセットを追加しました",
        # brt_preferences.py:329
        ("*", "Delete Identifier Set"): "識別子セットを削除します",
        # brt_preferences.py:330
        ("*", "Delete the selected identifier set"): "選択した識別子セットを削除します",
        # brt_preferences.py:337
        ("*", "最低でも1つの識別子セットを設定してください"): "最低でも1つの識別子セットを設定してください",
        # brt_preferences.py:346
        ("*", "Delete Identifier Pair"): "識別子ペアを削除します",
        # brt_preferences.py:347
        ("*", "Remove the selected identifier pair from the set"): "選択した識別子ペアをセットから削除します",
        # brt_preferences.py:356
        ("*", "最低でも1つの識別子ペアを設定してください"): "最低でも1つの識別子ペアを設定してください",
        # brt_types.py:44
        ("*", "識別子セット"): "識別子セット",
        # brt_types.py:49
        ("*", "識別子ペア"): "識別子ペア",
        # brt_types.py:50
        ("*", "現在のセット内のルールを選択"): "現在のセット内のルールを選択",
        # brt_types.py:76
        ("*", "ボーン名の共通部分を入力"): "ボーン名の共通部分を入力",
        # brt_types.py:80
        ("*", "開始番号"): "開始番号",
        # brt_types.py:81
        ("*", "連番の開始値の設定"): "連番の開始値の設定",
        # brt_types.py:88
        ("*", "ボーン名の末尾を選択"): "ボーン名の末尾を選択",
        # brt_types.py:90
        ("*", "ボーン名の末尾に `_wj` を追加"): "ボーン名の末尾に `_wj` を追加",
        # brt_types.py:91
        ("*", "ボーン名の末尾に `wj` を追加"): "ボーン名の末尾に `wj` を追加",
        # brt_types.py:92
        ("*", "ボーン名の末尾に `_wj_ex` を追加"): "ボーン名の末尾に `_wj_ex` を追加",
        # brt_types.py:93
        ("*", "ボーン名の末尾に `wj_ex` を追加"): "ボーン名の末尾に `wj_ex` を追加",
        # brt_types.py:98
        ("*", "連番法則"): "連番法則",
        # brt_types.py:99
        ("*", "ボーンの連番ルールを選択"): "ボーンの連番ルールを選択",
        # brt_types.py:101
        ("*", "000 (3桁)"): "000 (3桁)",
        # brt_types.py:101
        ("*", "3桁の番号を付加"): "3桁の番号を付加",
        # brt_types.py:102
        ("*", "00 (2桁)"): "00 (2桁)",
        # brt_types.py:102
        ("*", "2桁の番号を付加"): "2桁の番号を付加",
        # brt_types.py:110
        ("*", "変更前ボーン名"): "変更前ボーン名",
        # brt_types.py:111
        ("*", "元のボーン名を入力"): "元のボーン名を入力",
        # brt_types.py:116
        ("*", "変更後ボーン名"): "変更後ボーン名",
        # brt_types.py:117
        ("*", "新しいボーン名を入力"): "新しいボーン名を入力",
        # brt_types.py:122
        ("*", "番号サフィックスを削除"): "番号サフィックスを削除",
        # brt_types.py:123
        ("*", ".001 などの複製識別子を削除します"): ".001 などの複製識別子を削除します",
        # brt_types.py:129
        ("*", "ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示"): "ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示",
        # brt_types.py:135
        ("*", "ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示"): "ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示",
        # brt_types.py:141
        ("*", "L/RやLeft/Rightなどを対象に選択ボーンの名称を反転するツールを表示"): "L/RやLeft/Rightなどを対象に選択ボーンの名称を反転するツールを表示",
        # brt_types.py:153
        ("*", "選択したボーンをグローバルX軸でミラー反転させる"): "選択したボーンをグローバルX軸でミラー反転させる",
        # brt_types.py:159
        ("*", "選択したボーンを複製してリネームする"): "選択したボーンを複製してリネームする",
        # brt_ui_invert.py:84, brt_ui_rename.py:56
        ("*", "一致しないボーンを除外"): "一致しないボーンを除外",
        # brt_ui_invert.py:85
        ("*", "ネーミング規則が共通しないボーンを除外します"): "ネーミング規則が共通しないボーンを除外します",
        # brt_ui_invert.py:94, brt_ui_rename.py:66, brt_ui_replace.py:82
        ("*", "アーマチュアが選択されていません"): "アーマチュアが選択されていません",
        # brt_ui_invert.py:103
        ("*", "対応モードは Pose または Edit です"): "対応モードは Pose または Edit です",
        # brt_ui_invert.py:107
        ("*", "起点となるボーンが選択されていません"): "起点となるボーンが選択されていません",
        # brt_ui_invert.py:122
        ("*", "線形チェーンを選択しました"): "線形チェーンを選択しました",
        # brt_ui_rename.py:30
        ("*", "Renames the selected bone rows based on the specified settings"): "選択されたボーン列の名前を指定の設定に基づいて連番リネームします",
        # brt_ui_rename.py:45
        ("*", "共通部分を検出"): "共通部分を検出",
        # brt_ui_rename.py:47
        ("*", "選択ボーン名の共通部分を抽出 または 線形チェーン選択"): "選択ボーン名の共通部分を抽出 または 線形チェーン選択",
        # brt_ui_rename.py:50, brt_ui_replace.py:72
        ("*", "線形チェーンを選択"): "線形チェーンを選択",
        # brt_ui_rename.py:51, brt_ui_replace.py:73
        ("*", "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します"): "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        # brt_ui_rename.py:57
        ("*", "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します"): "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します",
        # brt_ui_rename.py:77
        ("*", "対応しているのは Pose モードまたは Edit モードです"): "対応しているのは Pose モードまたは Edit モードです",
        # brt_ui_rename.py:81, brt_ui_replace.py:95
        ("*", "ボーンが選択されていません"): "ボーンが選択されていません",
        # brt_ui_rename.py:95, brt_ui_replace.py:109
        ("*", "共通部分が検出できませんでした"): "ベース名が検出できませんでした",
        # brt_ui_replace.py:60
        ("*", "ボーン名の置換を完了しました"): "ボーン名の置換を完了しました",
        # brt_ui_replace.py:70
        ("*", "選択ボーンから置換元名を抽出"): "選択ボーンから置換元名を抽出",
        # brt_ui_replace.py:91
        ("*", "対応しているのは Pose または Edit モードです"): "対応しているのは Pose または Edit モードです",
        # brt_update.py:9
        ("*", "アップデート"): "アップデート",
        # brt_update.py:12
        ("*", "更新を確認"): "更新を確認",
        # brt_update.py:15
        ("*", "インストール"): "インストール",
        # brt_update.py:16
        ("*", "アドオンフォルダを開く"): "アドオンフォルダを開く",
        # brt_update.py:24
        ("*", "Check for Updates"): "更新を確認",
        # brt_update.py:25
        ("*", "Opens the GitHub release page to check for update files"): "GitHubリリースページを開き、更新ファイルを確認します",
        # brt_update.py:38
        ("*", "Install Update File"): "更新ファイルをインストールします",
        # brt_update.py:39
        ("*", "Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update"): "Diva_BoneRenameTools.zipを選択してください。インストールを実行します",
        # brt_update.py:42
        ("*", "Select ZIP File"): "zipファイルを選択します",
        # brt_update.py:43
        ("*", "Choose a ZIP file starting with DIVA_BoneRenameTools"): "DIVA_BoneRenameToolsのzipファイルを選択してください",
        # brt_update.py:51
        ("*", "Choose the folder where the addon is installed"): "アドオンがインストールされているフォルダーを選択します",
        # brt_update.py:83
        ("*", "DIVA_BoneRenameTools で始まるZIPファイル以外は処理できません"): "「DIVA_BoneRenameTools」以外のZIPファイルはインストールできません",
        # brt_update.py:99
        ("*", "ZIP内に DIVA_BoneRenameTools フォルダまたは __init__.py が見つかりません"): "ZIP内に DIVA_BoneRenameTools フォルダまたは __init__.py が見つかりません",
        # brt_update.py:105
        ("*", "ZIP内の bl_info.name を取得できません"): "ZIP内の bl_info.name を取得できません",
        # brt_update.py:126
        ("*", "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください"): "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください",
        # brt_update.py:132
        ("*", "インストールはキャンセルされました"): "インストールはキャンセルされました",
        # brt_update.py:139
        ("*", "選択されたフォルダに __init__.py が見つかりません"): "選択されたフォルダに __init__.py が見つかりません",
        # brt_update.py:145
        ("*", "bl_info.name が一致しないため、更新できません"): "bl_info.name が一致しないため、更新できません",
        # brt_update.py:166
        ("*", "更新に失敗しました: {error}"): "更新に失敗しました: {error}",
        # brt_update.py:173, brt_update.py:174
        ("*", "更新が完了しました。Blenderを再起動してください"): "更新が完了しました。Blenderを再起動してください",
        # brt_update.py:180
        ("*", "Open Addon Folder"): "Addonフォルダーを開きます",
        # brt_update.py:181
        ("*", "Opens the folder where this addon is installed"): "このアドオンがインストールされているフォルダーを開きます",
    },
    "en_US": {
        # brt_panel.py:44, brt_types.py:75, brt_ui_rename.py:15
        ("*", "共通部分"): "Base name",
        # brt_panel.py:48, brt_ui_rename.py:19
        ("*", "連番開始番号"): "Serial number start number",
        # brt_panel.py:49, brt_ui_rename.py:20
        ("*", "法則"): "law",
        # brt_panel.py:50, brt_ui_rename.py:21
        ("*", "末尾"): "end",
        # brt_panel.py:52, brt_ui_rename.py:23
        ("*", "連番リネーム実行"): "Running serial number renames",
        # brt_panel.py:102, brt_ui_replace.py:35
        ("*", "重複識別子を削除"): "Remove duplicate identifiers",
        # brt_panel.py:104, brt_ui_replace.py:37
        ("*", "指定名でボーン名変更"): "Change bone name with specified name",
        # brt_panel.py:141, brt_ui_invert.py:33
        ("*", "ボーン識別子:"): "Bone Identifier:",
        # brt_panel.py:160, brt_types.py:165, brt_ui_invert.py:40
        ("*", "左右識別子を付与する"): "Give left and right identifiers",
        # brt_panel.py:165, brt_ui_invert.py:45
        ("*", "選択ボーンをグローバルXミラーする"): "Global X-mirror of selection bones",
        # brt_panel.py:169, brt_ui_invert.py:49
        ("*", "複製してリネームする"): "Duplicate and rename",
        # brt_panel.py:171, brt_ui_invert.py:51
        ("*", "選択ボーン反転リネーム"): "Select bone inverted rename",
        # brt_panel.py:182, brt_ui_other.py:15
        ("*", "全対称化付与"): "All symmetricalization",
        # brt_panel.py:183, brt_ui_other.py:16
        ("*", "全対称化削除"): "All symmetric removal",
        # brt_preferences.py:121
        ("*", "識別子セットの編集"): "Editing Identifier Sets",
        # brt_preferences.py:140
        ("*", "セット名"): "Set name",
        # brt_preferences.py:146
        ("*", "右"): "right",
        # brt_preferences.py:147
        ("*", "左"): "left",
        # brt_preferences.py:154
        ("*", "ペアを追加"): "Add a pair",
        # brt_preferences.py:163, brt_preferences.py:174
        ("*", "Add Identifier Set"): "Add Identifier Set",
        # brt_preferences.py:166
        ("*", "デフォルトセットを復元"): "Restore default set",
        # brt_preferences.py:167
        ("*", "リセット"): "Reset",
        # brt_preferences.py:168
        ("*", "保存"): "keep",
        # brt_preferences.py:175
        ("*", "Add a new identifier set to the preferences"): "Add a new identifier set to the preferences",
        # brt_preferences.py:190
        ("*", "Add Identifier Rule"): "Add Identifier Rule",
        # brt_preferences.py:191
        ("*", "Add a left-right identifier rule to the selected set"): "Add a left-right identifier rule to the selected set",
        # brt_preferences.py:209
        ("*", "Move Indentifier Set Up"): "Move Indentifier Set Up",
        # brt_preferences.py:210
        ("*", "Move the identifier set up one position"): "Move the identifier set up one position",
        # brt_preferences.py:225
        ("*", "Move Indentifier Set Down"): "Move Indentifier Set Down",
        # brt_preferences.py:226
        ("*", "Move the identifier set down one position"): "Move the identifier set down one position",
        # brt_preferences.py:241
        ("*", "Save Identifier Sets"): "Save Identifier Sets",
        # brt_preferences.py:242
        ("*", "Save all identifier sets to a JSON file"): "Save all identifier sets to a JSON file",
        # brt_preferences.py:253
        ("*", "{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください"): "{label} contains unavailable characters.Use only half-width alphanumeric characters and symbols in set names.",
        # brt_preferences.py:257
        ("*", "識別子セットの名前を入力してください"): "Enter the name of the identifier set",
        # brt_preferences.py:264
        ("*", "{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）"): "{label} does not have any valid identifier pairs (requires pairs with both sides entered)",
        # brt_preferences.py:268
        ("*", "{label}に片側だけ空白の識別子ペアがあります（両方入力してください）"): "{label} has an identifier pair that is only one side (please enter both)",
        # brt_preferences.py:282
        ("*", "保存しました！"): "Saved!",
        # brt_preferences.py:291
        ("*", "Reload Identifier Sets"): "Reload Identifier Sets",
        # brt_preferences.py:292
        ("*", "Reload the identifier sets from the saved JSON file"): "Reload the identifier sets from the saved JSON file",
        # brt_preferences.py:297
        ("*", "識別子セットを元に戻しました"): "Identifier set has been reverted",
        # brt_preferences.py:303
        ("*", "Append Default Set"): "Append Default Set",
        # brt_preferences.py:304
        ("*", "Insert the default set of identifiers at the top"): "Insert the default set of identifiers at the top",
        # brt_preferences.py:322
        ("*", "デフォルトセットを追加しました"): "Added default set",
        # brt_preferences.py:329
        ("*", "Delete Identifier Set"): "Delete Identifier Set",
        # brt_preferences.py:330
        ("*", "Delete the selected identifier set"): "Delete the selected identifier set",
        # brt_preferences.py:337
        ("*", "最低でも1つの識別子セットを設定してください"): "Set at least one identifier set",
        # brt_preferences.py:346
        ("*", "Delete Identifier Pair"): "Delete Identifier Pair",
        # brt_preferences.py:347
        ("*", "Remove the selected identifier pair from the set"): "Remove the selected identifier pair from the set",
        # brt_preferences.py:356
        ("*", "最低でも1つの識別子ペアを設定してください"): "Set at least one identifier pair",
        # brt_types.py:44
        ("*", "識別子セット"): "Identifier set",
        # brt_types.py:49
        ("*", "識別子ペア"): "Identifier pair",
        # brt_types.py:50
        ("*", "現在のセット内のルールを選択"): "Select a rule in the current set",
        # brt_types.py:76
        ("*", "ボーン名の共通部分を入力"): "Enter the common part of the bone name",
        # brt_types.py:80
        ("*", "開始番号"): "Starting number",
        # brt_types.py:81
        ("*", "連番の開始値の設定"): "Setting the start value for serial numbers",
        # brt_types.py:88
        ("*", "ボーン名の末尾を選択"): "Select the end of bone name",
        # brt_types.py:90
        ("*", "ボーン名の末尾に `_wj` を追加"): "Add `_wj` to the end of bone name",
        # brt_types.py:91
        ("*", "ボーン名の末尾に `wj` を追加"): "Add `wj` to the end of bone name",
        # brt_types.py:92
        ("*", "ボーン名の末尾に `_wj_ex` を追加"): "Add `_wj_ex` to the end of bone name",
        # brt_types.py:93
        ("*", "ボーン名の末尾に `wj_ex` を追加"): "Add `wj_ex` to the end of bone name",
        # brt_types.py:98
        ("*", "連番法則"): "Trace rules",
        # brt_types.py:99
        ("*", "ボーンの連番ルールを選択"): "Select a bone sequential number rule",
        # brt_types.py:101
        ("*", "000 (3桁)"): "000 (3 digits)",
        # brt_types.py:101
        ("*", "3桁の番号を付加"): "Add a 3-digit number",
        # brt_types.py:102
        ("*", "00 (2桁)"): "00 (2 digits)",
        # brt_types.py:102
        ("*", "2桁の番号を付加"): "Add two digit numbers",
        # brt_types.py:110
        ("*", "変更前ボーン名"): "Before the change bone name",
        # brt_types.py:111
        ("*", "元のボーン名を入力"): "Enter the original bone name",
        # brt_types.py:116
        ("*", "変更後ボーン名"): "Changed bone name",
        # brt_types.py:117
        ("*", "新しいボーン名を入力"): "Enter the new bone name",
        # brt_types.py:122
        ("*", "番号サフィックスを削除"): "Remove number suffix",
        # brt_types.py:123
        ("*", ".001 などの複製識別子を削除します"): "Removes a replica identifier such as .001",
        # brt_types.py:129
        ("*", "ボーンの共通接頭辞とルールに基づいた連番リネーム操作を表示"): "Shows sequential rename operations based on bone common prefixes and rules",
        # brt_types.py:135
        ("*", "ボーン名の部分文字列置換や.001などの識別子削除を行うツールを表示"): "Show tools that can replace bone names and delete identifiers such as .001",
        # brt_types.py:141
        ("*", "L/RやLeft/Rightなどを対象に選択ボーンの名称を反転するツールを表示"): "Displays tools that invert the name of the selected bone for L/R, Left/R, etc.",
        # brt_types.py:153
        ("*", "選択したボーンをグローバルX軸でミラー反転させる"): "Mirror flip selected bones on the global X-axis",
        # brt_types.py:159
        ("*", "選択したボーンを複製してリネームする"): "Duplicate and rename selected bones",
        # brt_ui_invert.py:84, brt_ui_rename.py:56
        ("*", "一致しないボーンを除外"): "Exclude non-matched bones",
        # brt_ui_invert.py:85
        ("*", "ネーミング規則が共通しないボーンを除外します"): "Exclude bones that do not share naming rules",
        # brt_ui_invert.py:94, brt_ui_rename.py:66, brt_ui_replace.py:82
        ("*", "アーマチュアが選択されていません"): "No armature selected",
        # brt_ui_invert.py:103
        ("*", "対応モードは Pose または Edit です"): "Supported modes are Pose or Edit",
        # brt_ui_invert.py:107
        ("*", "起点となるボーンが選択されていません"): "No starting bone selected",
        # brt_ui_invert.py:122
        ("*", "線形チェーンを選択しました"): "Linear chain selected",
        # brt_ui_rename.py:30
        ("*", "Renames the selected bone rows based on the specified settings"): "Renames the selected bone rows based on the specified settings",
        # brt_ui_rename.py:45
        ("*", "共通部分を検出"): "Detect common parts",
        # brt_ui_rename.py:47
        ("*", "選択ボーン名の共通部分を抽出 または 線形チェーン選択"): "Extract common parts of selected bone names or linear chain selection",
        # brt_ui_rename.py:50, brt_ui_replace.py:72
        ("*", "線形チェーンを選択"): "Select a linear chain",
        # brt_ui_rename.py:51, brt_ui_replace.py:73
        ("*", "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します"): "When ON, a parent-child structure with no branches is automatically selected from the selected bone as the starting point.",
        # brt_ui_rename.py:57
        ("*", "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します"): "Bones with obviously different naming rules are excluded from common extraction targets",
        # brt_ui_rename.py:77
        ("*", "対応しているのは Pose モードまたは Edit モードです"): "Supported in Pose or Edit modes",
        # brt_ui_rename.py:81, brt_ui_replace.py:95
        ("*", "ボーンが選択されていません"): "No bones selected",
        # brt_ui_rename.py:95, brt_ui_replace.py:109
        ("*", "共通部分が検出できませんでした"): "Unable to detect the base name",
        # brt_ui_replace.py:60
        ("*", "ボーン名の置換を完了しました"): "Bone name replacement completed",
        # brt_ui_replace.py:70
        ("*", "選択ボーンから置換元名を抽出"): "Extract replacement source name from the selection bone",
        # brt_ui_replace.py:91
        ("*", "対応しているのは Pose または Edit モードです"): "Supported in Pose or Edit mode",
        # brt_update.py:9
        ("*", "アップデート"): "update",
        # brt_update.py:12
        ("*", "更新を確認"): "Check for updates",
        # brt_update.py:15
        ("*", "インストール"): "install",
        # brt_update.py:16
        ("*", "アドオンフォルダを開く"): "Open Add-ons Folder",
        # brt_update.py:24
        ("*", "Check for Updates"): "Check for Updates",
        # brt_update.py:25
        ("*", "Opens the GitHub release page to check for update files"): "Opens the GitHub release page to check for update files",
        # brt_update.py:38
        ("*", "Install Update File"): "Install Update File",
        # brt_update.py:39
        ("*", "Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update"): "Select a ZIP archive beginning with DIVA_BoneRenameTools to install the update",
        # brt_update.py:42
        ("*", "Select ZIP File"): "Select ZIP File",
        # brt_update.py:43
        ("*", "Choose a ZIP file starting with DIVA_BoneRenameTools"): "Choose a ZIP file starting with DIVA_BoneRenameTools",
        # brt_update.py:51
        ("*", "Choose the folder where the addon is installed"): "Choose the folder where the addon is installed",
        # brt_update.py:83
        ("*", "DIVA_BoneRenameTools で始まるZIPファイル以外は処理できません"): "Cannot process anything other than ZIP files that start with DIVA_BoneRenameTools",
        # brt_update.py:99
        ("*", "ZIP内に DIVA_BoneRenameTools フォルダまたは __init__.py が見つかりません"): "Cannot find DIVA_BoneRenameTools folder or __init__.py in ZIP",
        # brt_update.py:105
        ("*", "ZIP内の bl_info.name を取得できません"): "Unable to get bl_info.name in ZIP",
        # brt_update.py:126
        ("*", "インストール先のアドオンフォルダが見つかりませんでした。インストール先を選択してください"): "The add-on folder to install could not be found.Please select the installation location",
        # brt_update.py:132
        ("*", "インストールはキャンセルされました"): "Installation has been cancelled",
        # brt_update.py:139
        ("*", "選択されたフォルダに __init__.py が見つかりません"): "__init__.py not found in selected folder",
        # brt_update.py:145
        ("*", "bl_info.name が一致しないため、更新できません"): "Cannot update because bl_info.name does not match",
        # brt_update.py:166
        ("*", "更新に失敗しました: {error}"): "Update failed: {error}",
        # brt_update.py:173, brt_update.py:174
        ("*", "更新が完了しました。Blenderを再起動してください"): "The update is complete.Please restart Blender",
        # brt_update.py:180
        ("*", "Open Addon Folder"): "Open Addon Folder",
        # brt_update.py:181
        ("*", "Opens the folder where this addon is installed"): "Opens the folder where this addon is installed",
    },
}

def register(name):
    bpy.app.translations.unregister(name)
    bpy.app.translations.register(name, translation_dict)

def unregister(name):
    bpy.app.translations.unregister(name)