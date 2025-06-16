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
# from . import BoneTransferTools_N  # Nパネル用
from . import addon_panel 
# from . import BoneTransferTools # 右クリック用 
# from . import MergeSelectedMeshes # 右クリック用 

# ✅ **モジュールのリロードを試みる**
# importlib.reload(BoneTransferTools_N)
# importlib.reload(BoneTransferTools) # 右クリック用 
# importlib.reload(MergeSelectedMeshes) # 右クリック用 

def register():
    addon_panel.register()  
    # BoneTransferTools_N.register()  # ✅ **モジュール経由で `register()` を呼び出す**
    # BoneTransferTools.register()  # 右クリック用 
    # MergeSelectedMeshes.register()  # 右クリック用 

def unregister():
    addon_panel.unregister() 
    # BoneTransferTools_N.unregister()  # ✅ **モジュール経由で `unregister()` を呼び出す**
    # BoneTransferTools.unregister()
    # MergeSelectedMeshes.unregister()