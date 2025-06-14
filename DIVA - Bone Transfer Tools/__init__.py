bl_info = {
    "name": "DIVA - Bone Transfer Tools",
    "author": "Riel",
    "version": (1, 0),
    "blender": (3, 6, 22),
    "location": "3D View > Sidebar > DIVA",
    "description": "Transfer bones and optionally duplicate b1 object to new armature",
    "category": "Rigging"
}

import bpy
import importlib
from . import BoneTransferTools_N  # Nパネル用
from . import BoneTransferTools # 右クリック用 

# ✅ **モジュールのリロードを試みる**
importlib.reload(BoneTransferTools_N)
importlib.reload(BoneTransferTools)

def register():
    BoneTransferTools_N.register()  # ✅ **モジュール経由で `register()` を呼び出す**
    BoneTransferTools.register()    

def unregister():
    BoneTransferTools_N.unregister()  # ✅ **モジュール経由で `unregister()` を呼び出す**
    BoneTransferTools.unregister()