import bpy

class BTT_PG_TransferObject(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="オブジェクト名")
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    use_child_bones: bpy.props.BoolProperty(
        name="子ボーンも含める",
        default=True,
        description="ウェイトのある親ボーンを移植する際に、ウエイトのない子ボーンも一緒に移植するかを切り替えます"
    )

def get_classes():
    return [BTT_PG_TransferObject]