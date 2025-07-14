# brt_json.py
import os
import json
import shutil
import datetime

# デフォルト識別子の定義
def DEFAULT_BONE_PATTERN():
    return [
        {
            "label": "DIVA(Default)",
            "rules": [
                {"right": "_r_", "left": "_l_", "use_regex": False},
                {"right": "_r0", "left": "_l0", "use_regex": False},
                {"right": "_r1", "left": "_l1", "use_regex": False},
            ],
        }
    ]

def get_json_path():
    path = os.path.join(os.path.dirname(__file__), "bone_patterns.json")
    print("[DIVA] JSON path:", path)
    return path

# JSONファイルの読み込み
def load_bone_patterns_to_preferences(prefs):
    path = get_json_path()

    def apply_default():
        prefs.bone_patterns.clear()
        for p in DEFAULT_BONE_PATTERN():
            pattern = prefs.bone_patterns.add()
            pattern.label = p["label"]
            for r in p["rules"]:
                rule = pattern.rules.add()
                rule.right = r["right"]
                rule.left = r["left"]
                rule.use_regex = r.get("use_regex", False)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BONE_PATTERN(), f, ensure_ascii=False, indent=2)
        apply_default()
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSONルートが配列形式ではありません")

        prefs.bone_patterns.clear()
        unnamed_count = 1
        for entry in data:
            label = entry.get("label", "").strip() or f"未定義セット{unnamed_count}"
            if not entry.get("label"):
                unnamed_count += 1
            pattern = prefs.bone_patterns.add()
            pattern.label = label
            for rule_data in entry.get("rules", []):
                rule = pattern.rules.add()
                rule.right = rule_data.get("right", "")
                rule.left = rule_data.get("left", "")
                rule.use_regex = rule_data.get("use_regex", False)
    except Exception as e:
        print(f"[DIVA] ⚠ JSON読み込みエラー: {e}")

        # タイムスタンプ付きでバックアップ
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.replace(".json", f".invalid_{timestamp}.json")
        try:
            shutil.move(path, backup_path)
            print(f"[DIVA] ⚠ 破損JSONをバックアップ: {backup_path}")
        except Exception as move_err:
            print(f"[DIVA] ⚠ バックアップに失敗しました: {move_err}")

        # デフォルトで再生成
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BONE_PATTERN(), f, ensure_ascii=False, indent=2)
        apply_default()

def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_BoneRenameTools"].preferences
    items = []

    for i, pattern in enumerate(prefs.bone_patterns):
        label = pattern.label.strip()

        # 識別子としてそのまま使える名前に（ascii前提）
        identifier = label
        name = label  # 表示用にもそのまま使う（日本語でない前提）

        items.append((identifier, name, ""))

    return items

# 選択したボーン識別子セットの識別子ルールを取得
def get_rule_items(self, context):
    prefs = context.preferences.addons.get("DIVA_BoneRenameTools")
    if not prefs:
        return []

    label = self.bone_pattern  # 現在のセットラベル
    patterns = prefs.preferences.bone_patterns

    for pattern in patterns:
        if pattern.label == label:
            return [
                (str(i), f"{r.right} / {r.left}", "")
                for i, r in enumerate(pattern.rules)
                if r.right and r.left
            ]

    return []