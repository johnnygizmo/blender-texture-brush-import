bl_info = {
    "name": "Import Image as Brush",
    "description": "Import an Image into a texture brush",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "File > Import",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Test"
}

import bpy, os


def read_some_data(context, filepath, ttype, mode):
    file = os.path.split(filepath)[-1]
    
    if os.path.isfile(filepath):
        brush = bpy.data.brushes.new(file,"TEXTURE_PAINT")
        tex   = bpy.data.textures.new(file,"IMAGE")
        image = bpy.data.images.load(filepath, False)
        tex.image = image
            
        if ttype == "TEX":
            brush.texture = tex
            brush.texture_slot.tex_paint_map_mode = mode
                
        elif ttype == "TEXMASK":
            brush.mask_texture = tex
            brush.mask_texture_slot.tex_paint_map_mode = mode
    
        brush.use_custom_icon = True
        brush.icon_filepath = filepath
        
        bpy.ops.brush.add()
        
        
    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Image to Brush"

    # ImportHelper mixin class uses this
    filename_ext = ".png"

    filter_glob = StringProperty(
            default="*.png",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )


    mode = EnumProperty(
            name="Mapping",
            description="Choose the mapping mode for the new brush",
            items=(
            
            ('STENCIL', "Stencil",""),
            ('RANDOM',"Random",""),
            ('3D',  "3D",""),
            ('TILED' , "Tiled",""),
            ('VIEW_PLANE', "View Plane","")
            ),
            
            default='STENCIL',

            )
            
    type = EnumProperty(
            name="Tex / Mask",
            description="Choose the slot to put the image in",
            items=(('TEX', "Texture", "Import Image as Texture"),
                   ('TEXMASK', "Texture Mask", "Import Image as Texture Mask")),
            default='TEX',

            )
#



    def execute(self, context):
        return read_some_data(context, self.filepath, self.type, self.mode)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="Import Image Texture Brush")


def register():
    bpy.utils.register_class(ImportSomeData)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_test.some_data('INVOKE_DEFAULT')
