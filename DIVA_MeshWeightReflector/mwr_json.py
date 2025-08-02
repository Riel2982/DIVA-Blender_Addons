# mwr_json.py
import bpy
import os
import json
import shutil
import datetime
import importlib
import traceback
from datetime import datetime
import re

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

            # 5件までに制限
            dir_path = os.path.dirname(backup_path)
            base_name = os.path.basename(path).replace(".json", "")
            pattern = re.compile(rf"{re.escape(base_name)}\.invalid_\d{{8}}_\d{{6}}\.json")
            backups = [f for f in os.listdir(dir_path) if pattern.match(f)]
            backups.sort()  # 古い順になる

            while len(backups) > 5: # 5件まで
                oldest = backups.pop(0)
                try:
                    os.remove(os.path.join(dir_path, oldest))
                    print(f"[DIVA] 🗑 古いバックアップ削除: {oldest}")
                except Exception as rm_err:
                    print(f"[DIVA] ⚠ 削除失敗: {rm_err}")

        except Exception as move_err:
            print(f"[DIVA] ⚠ バックアップに失敗しました: {move_err}")

        # デフォルトで再生成
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BONE_PATTERN(), f, ensure_ascii=False, indent=2)
        apply_default()

def get_bone_pattern_items(self, context):
    prefs = context.preferences.addons["DIVA_MeshWeightReflector"].preferences
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
    prefs = context.preferences.addons.get("DIVA_MeshWeightReflector")
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
                and r.use_regex in {False, "none", None}  # 正規表現ルールを除外
            ]

    return []

# ラベルに対応するルールセットを取得
def get_selected_rules(label):
    addon = bpy.context.preferences.addons.get("DIVA_MeshWeightReflector")
    if not addon:
        return []

    prefs = addon.preferences
    for p in prefs.bone_patterns:
        if p.label.strip() == label:
            return [
                {
                    "right": r.right,
                    "left": r.left,
                    "use_regex": getattr(r, "use_regex", False)
                }
                for r in p.rules
            ]
    return []


#　JSONファイル読み書き関数群
def load_json_data():
    try:
        with open(get_json_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_json_data(data):
    with open(get_json_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# JSON同期用
# 同期アドオン検出
def get_diva_sync_targets():
    exclude = "DIVA_MeshWeightReflector"
    enabled_addons = bpy.context.preferences.addons.keys() 
    
    # 既存のロジックに `if name != exclude:` を挿む感じ
    targets = []
    for name in enabled_addons:
        if not name.startswith("DIVA_"): # DIVA_で条件付
            continue

        if name == exclude: #   自身は除外する
            continue

        try:
            mod = importlib.import_module(name)
        except Exception:
            continue  # インポート失敗＝候補から除外

        bl_info = getattr(mod, "bl_info", {})

        if "Riel" not in bl_info.get("author", ""): # bl_info Author: Riel
            continue

        root_dir = os.path.dirname(mod.__file__)
        json_path = os.path.join(root_dir, "bone_patterns.json") # ファイル名: bone_patterns.json
        if not os.path.exists(json_path):
            continue

        if hasattr(mod, "load_bone_patterns_to_preferences"):
                targets.append((name, mod))

    return targets

# ファイルを同期先にコピー
def copy_json_to_targets(source_path, targets):
    for name, mod in targets:
        root_dir = os.path.dirname(mod.__file__)
        target_path = os.path.join(root_dir, "bone_patterns.json")

        if not os.path.exists(target_path):
            continue  # スキップ対象

        # バックアップ
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target_path.replace(".json", f"_{timestamp}.bak.json")
        shutil.copy2(target_path, backup_path)
        print(f"[BACKUP] {name}: {backup_path} にバックアップ")

        # 🔁 バックアップファイルを3件に制限
        base_name = os.path.basename(target_path).replace(".json", "")
        pattern = re.compile(rf"{re.escape(base_name)}_\d{{8}}_\d{{6}}\.bak\.json")
        backups = [
            f for f in os.listdir(root_dir)
            if pattern.match(f)
        ]
        backups.sort()  # 古い順

        while len(backups) > 3: # 3件まで
            oldest = backups.pop(0)
            try:
                os.remove(os.path.join(root_dir, oldest))
                print(f"[CLEANUP] {name}: 古いバックアップ削除 → {oldest}")
            except Exception as rm_err:
                print(f"[ERROR] {name}: バックアップ削除失敗 → {rm_err}")
        # 上書きコピー
        shutil.copy2(source_path, target_path)
        print(f"[COPY] {name}: {target_path} にコピー完了")

def sync_bone_patterns():
    synced = []  # ← 成功したアドオン名をここに記録

    try:
        # 編集元から保存
        mwr_prefs = bpy.context.preferences.addons["DIVA_MeshWeightReflector"].preferences
        mod_mwr = importlib.import_module("DIVA_MeshWeightReflector.mwr_json")
        if hasattr(mod_mwr, "save_json_data"):
            data = [
                {
                    "label": p.label,
                    "rules": [
                        {"right": r.right, "left": r.left, "use_regex": r.use_regex}
                        for r in p.rules
                    ],
                }
                for p in mwr_prefs.bone_patterns
            ]
            mod_mwr.save_json_data(data)
            print("[SYNC] bone_patterns 保存完了")

            source_path = mod_mwr.get_json_path()  # 編集元のJSONパス
            targets = get_diva_sync_targets()
            copy_json_to_targets(source_path, targets)

        # 対象DIVAアドオンへ反映
        for name, mod in get_diva_sync_targets():
            try:
                prefs_target = bpy.context.preferences.addons[name].preferences
                mod.load_bone_patterns_to_preferences(prefs_target)
                print(f"[SYNC] {name} → 同期成功")
                synced.append(name)
            except Exception as inner:
                print(f"[SYNC] {name} → 同期失敗: {inner}")

    except Exception as e:
        import traceback
        print("[SYNC] エラー発生:")
        print(traceback.format_exc())
        raise e  # 呼び出し元にエラーを渡す

    return synced  # ← 成功アドオン名を返す
