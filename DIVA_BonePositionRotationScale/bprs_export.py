import bpy
import os
import sys
import time
import json
import subprocess

from . import DivaBonePositionRotationScale

# タイムスタンプを付与する関数
def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")

# ファイル名をチェックしてリネームする関数（上書きするかどうかをチェック）
def rename_existing_file(filepath, overwrite):
    if os.path.exists(filepath):
        if overwrite:
            return None  # 上書きモードの場合、リネームせずそのまま使用
        else:
            file_dir, file_name = os.path.split(filepath)
            file_base, file_ext = os.path.splitext(file_name)
            new_name = f"{file_base}_{get_timestamp()}{file_ext}"
            new_filepath = os.path.join(file_dir, new_name)
            os.rename(filepath, new_filepath)
            return new_filepath
    return None

# **JSON変換処理**
def convert_bone_data_to_json(raw_data):
    bone_data_json = [
        {
            "Signature": "OSG",
            "Name": parts[0].strip(),
            "ParentName": parts[1].split(":")[-1].strip(),
            "Position": parts[2].split(":")[-1].strip(),
            "Rotation": parts[3].split(":")[-1].strip(),
            "Scale": parts[4].split(":")[-1].strip()
        }
        for line in raw_data.split("\n\n")
        for parts in [line.split("\n")]
        if len(parts) >= 5
    ]
    return bone_data_json