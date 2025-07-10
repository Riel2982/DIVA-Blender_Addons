import bpy

translation_dict = {
    "ja_JP": {
        # brt_panel.py:29
        ("*", "共通部分"): "ベース名",
        # brt_panel.py:33
        ("*", "連番開始番号"): "連番開始番号",
        # brt_panel.py:34
        ("*", "法則"): "法則",
        # brt_panel.py:35
        ("*", "末尾"): "末尾",
        # brt_panel.py:37
        ("*", "連番リネーム実行"): "連番リネーム実行",
        # brt_panel.py:87
        ("*", "重複識別子を削除"): "重複識別子を削除",
        # brt_panel.py:89
        ("*", "指定名でボーン名変更"): "指定名でボーン名変更",
        # brt_panel.py:126
        ("*", "ボーン識別子:"): "ボーン識別子:",
        # brt_panel.py:145
        ("*", "左右識別子を付与する"): "左右識別子を付与する",
        # brt_panel.py:150
        ("*", "選択ボーンをグローバルXミラーする"): "選択ボーンをグローバルXミラーする",
        # brt_panel.py:154
        ("*", "複製してリネームする"): "複製してリネームする",
        # brt_panel.py:156
        ("*", "選択ボーン反転リネーム"): "選択ボーン反転リネーム",
        # brt_panel.py:167
        ("*", "全対称化付与"): "全対称化付与",
        # brt_panel.py:168
        ("*", "全対称化削除"): "全対称化削除",
        # brt_panel.py:261, brt_panel.py:324
        ("*", "線形チェーンを選択"): "線形チェーンを選択",
        # brt_panel.py:262, brt_panel.py:325
        ("*", "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します"): "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します",
        # brt_panel.py:267, brt_panel.py:379
        ("*", "一致しないボーンを除外"): "一致しないボーンを除外",
        # brt_panel.py:268
        ("*", "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します"): "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します",
        # brt_panel.py:277, brt_panel.py:334, brt_panel.py:389
        ("*", "アーマチュアが選択されていません"): "アーマチュアが選択されていません",
        # brt_panel.py:288
        ("*", "対応しているのは Pose モードまたは Edit モードです"): "対応しているのは Pose モードまたは Edit モードです",
        # brt_panel.py:292, brt_panel.py:347
        ("*", "ボーンが選択されていません"): "ボーンが選択されていません",
        # brt_panel.py:306, brt_panel.py:361
        ("*", "共通部分が検出できませんでした"): "ベース名が検出できませんでした",
        # brt_panel.py:343
        ("*", "対応しているのは Pose または Edit モードです"): "対応しているのは Pose または Edit モードです",
        # brt_panel.py:380
        ("*", "ネーミング規則が共通しないボーンを除外します"): "ネーミング規則が共通しないボーンを除外します",
        # brt_panel.py:398
        ("*", "対応モードは Pose または Edit です"): "対応モードは Pose または Edit です",
        # brt_panel.py:402
        ("*", "起点となるボーンが選択されていません"): "起点となるボーンが選択されていません",
        # brt_panel.py:417
        ("*", "線形チェーンを選択しました"): "線形チェーンを選択しました",
        # brt_panel.py:482
        ("*", "ボーン名の置換を完了しました"): "ボーン名の置換を完了しました",
        # brt_panel.py:524
        ("*", "識別子セット"): "識別子セット",
        # brt_panel.py:529
        ("*", "識別子ペア"): "識別子ペア",
        # brt_panel.py:530
        ("*", "現在のセット内のルールを選択"): "現在のセット内のルールを選択",
        # brt_preferences.py:136
        ("*", "セット名"): "セット名",
        # brt_preferences.py:142
        ("*", "右"): "右",
        # brt_preferences.py:143
        ("*", "左"): "左",
        # brt_preferences.py:150
        ("*", "ペアを追加"): "ペアを追加",
        # brt_preferences.py:162
        ("*", "デフォルトセットを復元"): "デフォルトセットを復元",
        # brt_preferences.py:163
        ("*", "リセット"): "リセット",
        # brt_preferences.py:164
        ("*", "保存"): "保存",
        # brt_preferences.py:170
        ("*", "Add Identifier Set"): "識別子セットを追加します",
        # brt_preferences.py:171
        ("*", "Add a new identifier set to the preferences"): "新しい識別子を設定に追加します",
        # brt_preferences.py:186
        ("*", "Add Identifier Rule"): "識別子ルールを追加します",
        # brt_preferences.py:187
        ("*", "Add a left-right identifier rule to the selected set"): "選択したセットに左右識別子ルールを追加します",
        # brt_preferences.py:205
        ("*", "Move Indentifier Set Up"): "識別子セットを上にを移動します",
        # brt_preferences.py:206
        ("*", "Move the identifier set up one position"): "識別子セットをひとつ上に移動します",
        # brt_preferences.py:221
        ("*", "Move Indentifier Set Down"): "識別子セットを下に移動します",
        # brt_preferences.py:222
        ("*", "Move the identifier set down one position"): "識別子セットをひとつ下に移動します",
        # brt_preferences.py:237
        ("*", "Save Identifier Sets"): "識別子セットを保存します",
        # brt_preferences.py:238
        ("*", "Save all identifier sets to a JSON file"): "すべての識別子セットをJSONファイルに保存します",
        # brt_preferences.py:249
        ("*", "{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください"): "{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください",
        # brt_preferences.py:253
        ("*", "識別子セットの名前を入力してください"): "識別子セットの名前を入力してください",
        # brt_preferences.py:260
        ("*", "{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）"): "{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）",
        # brt_preferences.py:264
        ("*", "{label}に片側だけ空白の識別子ペアがあります（両方入力してください）"): "{label}に片側だけ空白の識別子ペアがあります（両方入力してください）",
        # brt_preferences.py:278
        ("*", "保存しました！"): "保存しました！",
        # brt_preferences.py:287
        ("*", "Reload Identifier Sets"): "識別子セットをリセット",
        # brt_preferences.py:288
        ("*", "Reload the identifier sets from the saved JSON file"): "保存されたJSONファイルから識別子セットをリロードします",
        # brt_preferences.py:293
        ("*", "識別子セットを元に戻しました"): "識別子セットを元に戻しました",
        # brt_preferences.py:299
        ("*", "Append Default Set"): "デフォルトセットを復元します",
        # brt_preferences.py:300
        ("*", "Insert the default set of identifiers at the top"): "最上部に識別子のデフォルトセットを復元します",
        # brt_preferences.py:317
        ("*", "デフォルトセットを追加しました"): "デフォルトセットを追加しました",
        # brt_preferences.py:324
        ("*", "Delete Identifier Set"): "識別子セットを削除します",
        # brt_preferences.py:325
        ("*", "Delete the selected identifier set"): "選択した識別子セットを削除します",
        # brt_preferences.py:332
        ("*", "最低でも1つの識別子セットを設定してください"): "最低でも1つの識別子セットを設定してください",
        # brt_preferences.py:341
        ("*", "Delete Identifier Pair"): "識別子ペアを削除します",
        # brt_preferences.py:342
        ("*", "Remove the selected identifier pair from the set"): "選択した識別子ペアをセットから削除します",
        # brt_preferences.py:351
        ("*", "最低でも1つの識別子ペアを設定してください"): "最低でも1つの識別子ペアを設定してください",
    },
    "en_US": {
        # brt_panel.py:29
        ("*", "共通部分"): "Base name",
        # brt_panel.py:33
        ("*", "連番開始番号"): "Serial number start number",
        # brt_panel.py:34
        ("*", "法則"): "law",
        # brt_panel.py:35
        ("*", "末尾"): "end",
        # brt_panel.py:37
        ("*", "連番リネーム実行"): "Running serial number renames",
        # brt_panel.py:87
        ("*", "重複識別子を削除"): "Remove duplicate identifiers",
        # brt_panel.py:89
        ("*", "指定名でボーン名変更"): "Change bone name with specified name",
        # brt_panel.py:126
        ("*", "ボーン識別子:"): "Bone Identifier:",
        # brt_panel.py:145
        ("*", "左右識別子を付与する"): "Give left and right identifiers",
        # brt_panel.py:150
        ("*", "選択ボーンをグローバルXミラーする"): "Global X-mirror of selection bones",
        # brt_panel.py:154
        ("*", "複製してリネームする"): "Duplicate and rename",
        # brt_panel.py:156
        ("*", "選択ボーン反転リネーム"): "Select bone inverted rename",
        # brt_panel.py:167
        ("*", "全対称化付与"): "All symmetricalization",
        # brt_panel.py:168
        ("*", "全対称化削除"): "All symmetric removal",
        # brt_panel.py:261, brt_panel.py:324
        ("*", "線形チェーンを選択"): "Select a linear chain",
        # brt_panel.py:262, brt_panel.py:325
        ("*", "ONの場合、選択ボーンを起点に分岐のない親子構造を自動選択します"): "When ON, a parent-child structure with no branches is automatically selected from the selected bone as the starting point.",
        # brt_panel.py:267, brt_panel.py:379
        ("*", "一致しないボーンを除外"): "Exclude non-matched bones",
        # brt_panel.py:268
        ("*", "明らかにネーミングルールが異なるボーンを共通抽出対象から除外します"): "Bones with obviously different naming rules are excluded from common extraction targets",
        # brt_panel.py:277, brt_panel.py:334, brt_panel.py:389
        ("*", "アーマチュアが選択されていません"): "No armature selected",
        # brt_panel.py:288
        ("*", "対応しているのは Pose モードまたは Edit モードです"): "Supported in Pose or Edit modes",
        # brt_panel.py:292, brt_panel.py:347
        ("*", "ボーンが選択されていません"): "No bones selected",
        # brt_panel.py:306, brt_panel.py:361
        ("*", "共通部分が検出できませんでした"): "Unable to detect the base name",
        # brt_panel.py:343
        ("*", "対応しているのは Pose または Edit モードです"): "Supported in Pose or Edit mode",
        # brt_panel.py:380
        ("*", "ネーミング規則が共通しないボーンを除外します"): "Exclude bones that do not share naming rules",
        # brt_panel.py:398
        ("*", "対応モードは Pose または Edit です"): "Supported modes are Pose or Edit",
        # brt_panel.py:402
        ("*", "起点となるボーンが選択されていません"): "No starting bone selected",
        # brt_panel.py:417
        ("*", "線形チェーンを選択しました"): "Linear chain selected",
        # brt_panel.py:482
        ("*", "ボーン名の置換を完了しました"): "Bone name replacement completed",
        # brt_panel.py:524
        ("*", "識別子セット"): "Identifier set",
        # brt_panel.py:529
        ("*", "識別子ペア"): "Identifier pair",
        # brt_panel.py:530
        ("*", "現在のセット内のルールを選択"): "Select a rule in the current set",
        # brt_preferences.py:136
        ("*", "セット名"): "Set name",
        # brt_preferences.py:142
        ("*", "右"): "right",
        # brt_preferences.py:143
        ("*", "左"): "left",
        # brt_preferences.py:150
        ("*", "ペアを追加"): "Add a pair",
        # brt_preferences.py:162
        ("*", "デフォルトセットを復元"): "Restore default set",
        # brt_preferences.py:163
        ("*", "リセット"): "Reset",
        # brt_preferences.py:164
        ("*", "保存"): "keep",
        # brt_preferences.py:170
        ("*", "Add Identifier Set"): "Add Identifier Set",
        # brt_preferences.py:171
        ("*", "Add a new identifier set to the preferences"): "Add a new identifier set to the preferences",
        # brt_preferences.py:186
        ("*", "Add Identifier Rule"): "Add Identifier Rule",
        # brt_preferences.py:187
        ("*", "Add a left-right identifier rule to the selected set"): "Add a left-right identifier rule to the selected set",
        # brt_preferences.py:205
        ("*", "Move Indentifier Set Up"): "Move Indentifier Set Up",
        # brt_preferences.py:206
        ("*", "Move the identifier set up one position"): "Move the identifier set up one position",
        # brt_preferences.py:221
        ("*", "Move Indentifier Set Down"): "Move Indentifier Set Down",
        # brt_preferences.py:222
        ("*", "Move the identifier set down one position"): "Move the identifier set down one position",
        # brt_preferences.py:237
        ("*", "Save Identifier Sets"): "Save Identifier Sets",
        # brt_preferences.py:238
        ("*", "Save all identifier sets to a JSON file"): "Save all identifier sets to a JSON file",
        # brt_preferences.py:249
        ("*", "{label}には使用できない文字が含まれています。セット名には半角の英数字と記号だけを使ってください"): "{label} contains unavailable characters.Use only half-width alphanumeric characters and symbols in set names.",
        # brt_preferences.py:253
        ("*", "識別子セットの名前を入力してください"): "Enter the name of the identifier set",
        # brt_preferences.py:260
        ("*", "{label}には有効な識別子ペアがひとつもありません（両側が入力されたペアが必要です）"): "{label} does not have any valid identifier pairs (requires pairs with both sides entered)",
        # brt_preferences.py:264
        ("*", "{label}に片側だけ空白の識別子ペアがあります（両方入力してください）"): "{label} has an identifier pair that is only one side (please enter both)",
        # brt_preferences.py:278
        ("*", "保存しました！"): "Saved!",
        # brt_preferences.py:287
        ("*", "Reload Identifier Sets"): "Reload Identifier Sets",
        # brt_preferences.py:288
        ("*", "Reload the identifier sets from the saved JSON file"): "Reload the identifier sets from the saved JSON file",
        # brt_preferences.py:293
        ("*", "識別子セットを元に戻しました"): "Identifier set has been reverted",
        # brt_preferences.py:299
        ("*", "Append Default Set"): "Append Default Set",
        # brt_preferences.py:300
        ("*", "Insert the default set of identifiers at the top"): "Insert the default set of identifiers at the top",
        # brt_preferences.py:317
        ("*", "デフォルトセットを追加しました"): "Added default set",
        # brt_preferences.py:324
        ("*", "Delete Identifier Set"): "Delete Identifier Set",
        # brt_preferences.py:325
        ("*", "Delete the selected identifier set"): "Delete the selected identifier set",
        # brt_preferences.py:332
        ("*", "最低でも1つの識別子セットを設定してください"): "Set at least one identifier set",
        # brt_preferences.py:341
        ("*", "Delete Identifier Pair"): "Delete Identifier Pair",
        # brt_preferences.py:342
        ("*", "Remove the selected identifier pair from the set"): "Remove the selected identifier pair from the set",
        # brt_preferences.py:351
        ("*", "最低でも1つの識別子ペアを設定してください"): "Set at least one identifier pair",
    },
}

def register(name):
    bpy.app.translations.unregister(name)
    bpy.app.translations.register(name, translation_dict)

def unregister(name):
    bpy.app.translations.unregister(name)