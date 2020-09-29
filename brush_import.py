bl_info = {
    "name": "Import Image as Brush",
    "description": "Import an Image into a texture brush",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 90, 1),
    "location": "File > Import",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

import bpy, os

def import_brush(context, filepath, options):

    file = os.path.split(filepath)[-1]

    if os.path.isfile(filepath):
        brush = bpy.data.brushes.new(file,mode=options.brush_type)
        tex   = bpy.data.textures.new(file,type="IMAGE")
        image = bpy.data.images.load(filepath, check_existing=False)
        tex.image = image

        if options.brush_type == "SCULPT":
            brush.texture = tex
            brush.texture_slot.tex_paint_map_mode = options.mode

        elif options.brush_type == "TEXTURE_PAINT":
            if options.ttype == "TEX":
                brush.texture = tex
                brush.texture_slot.tex_paint_map_mode = options.mode
            elif options.ttype == "TEXMASK":
                brush.mask_texture = tex
                brush.mask_texture_slot.tex_paint_map_mode = options.mode

        brush.use_custom_icon = True
        brush.icon_filepath = filepath
        brush.strength = options.default_strength
        brush.blend = options.blend

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty, FloatProperty
from bpy.types import Operator, OperatorFileListElement


class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Image to Brush"

    # ImportHelper mixin class uses this
    filename_ext = ".png"

    filter_glob = StringProperty(
        default="*.png;*.jpg;*.jpeg;*.tif;*.tiff",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    files = CollectionProperty(
        name="File Path",
        type=OperatorFileListElement
    )
    directory = StringProperty (
        subtype='DIR_PATH'
    )

    default_strength = FloatProperty (
        default = 0.5,
        soft_min = 0.0,
        soft_max = 1.0

    )
    brush_type = EnumProperty(
        name="Brush Type",
        description="Choose the Type of Brush",
        items=(
            ('TEXTURE_PAINT', "Texture Paint","Create a texture paint brush"),
            ('SCULPT',"Sculpt","Create a Sculpting brush")
        ),
        default='TEXTURE_PAINT',

    )

    mode = EnumProperty(
        name="Mapping",
        description="Choose the mapping mode for the new brush",
        items=(
            ('STENCIL', "Stencil","Set the texture to Stencil mode."),
            ('RANDOM',"Random","Set the texture to Random mode."),
            ('3D',  "3D","Set the texture to 3D mode."),
            ('TILED' , "Tiled","Set the texture to Tiled mode."),
            ('VIEW_PLANE', "View Plane","Set the texture to View Plane mode.")
        ),
        default='TILED'
    )

    ttype = EnumProperty(
           name="Tex / Mask",
           description="Choose the slot to put the image in",
           items=(('TEX', "Texture", "Import Image as Texture"),
                  ('TEXMASK', "Texture Mask", "Import Image as Texture Mask")),
           default='TEX',
           )

    blend = EnumProperty(
        name = "Blend Mode",
        description="default blending mode",
        default = 'MIX',
        items=(
            ('MIX'," Mix", "Use mix blending mode while painting."),
            ('ADD',"Add", "Use add blending mode while painting."),
            ('SUB',"Subtract", "Use subtract blending mode while painting."),
            ('MUL',"Multiply", "Use multiply blending mode while painting."),
            ('LIGHTEN',"Lighten", "Use lighten blending mode while painting."),
            ('DARKEN',"Darken", "Use darken blending mode while painting."),
            ('ERASE_ALPHA',"Erase Alpha", "Erase alpha while painting."),
            ('ADD_ALPHA',"Add Alpha", "Add alpha while painting."),
            ('OVERLAY',"Overlay", "Use overlay blending mode while painting."),
            ('HARDLIGHT',"Hard light", "Use hard light blending mode while painting."),
            ('COLORBURN',"Color burn", "Use color burn blending mode while painting."),
            ('LINEARBURN',"Linear burn", "Use linear burn blending mode while painting."),
            ('COLORDODGE',"Color dodge", "Use color dodge blending mode while painting."),
            ('SCREEN',"Screen", "Use screen blending mode while painting."),
            ('SOFTLIGHT',"Soft light", "Use softlight blending mode while painting."),
            ('PINLIGHT',"Pin light", "Use pinlight blending mode while painting."),
            ('VIVIDLIGHT',"Vivid light", "Use vividlight blending mode while painting."),
            ('LINEARLIGHT',"Linear light", "Use linearlight blending mode while painting."),
            ('DIFFERENCE',"Difference", "Use difference blending mode while painting."),
            ('EXCLUSION',"Exclusion", "Use exclusion blending mode while painting."),
            ('HUE',"Hue", "Use hue blending mode while painting."),
            ('SATURATION',"Saturation", "Use saturation blending mode while painting."),
            ('LUMINOSITY',"Luminosity", "Use luminosity blending mode while painting."),
            ('COLOR',"Color", "Use color blending mode while painting.")
        )
    )


    def execute(self, context):
        directory = self.directory
        for file in self.files:
            filepath = os.path.join(directory, file.name)
            import_brush(context, filepath, self)
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="Import Image Texture Brush")


def register():
    bpy.utils.register_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
    bpy.ops.import_test.some_data('INVOKE_DEFAULT')

