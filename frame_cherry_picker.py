bl_info = {
  "name" : "The Cherry Picker",
  "category": "3D View",
  "author": "Corwin Smith"
}

import bpy


class cherry_picker(bpy.types.Panel):
    bl_label = "Frame Cherry Picker"
    bl_id = "view3D.custom_menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        split = layout.split()

        # Layout for entering frames that need to be rendered
        row = layout.row()
        row.prop(context.scene, "render_frames_cherry_picker", text="Input Frames")
        row = layout.row()
        row.label("Enter file name (will use default if not specified):")
        rd = context.scene.render
        image_settings = rd.image_settings
        file_format = image_settings.file_format
        layout.prop(rd, "filepath", text="")
        row = layout.row()
        row.operator("frame.cherrypicker")


class OBJECT_OT_BUTTON(bpy.types.Operator):
    bl_idname = "frame.cherrypicker"
    bl_label = "Submit"

    def execute(self, context):
        frame_string = bpy.data.scenes[0].render_frames_cherry_picker
        frames_render = convert_string(frame_string)
        render_frames(frames_render)
        return{'FINISHED'}


def convert_string(frame_string):
    frames_render = []
    frame_split = frame_string.split(',')
    for frame in frame_split:
        hyphen = False
        for char in frame:
            if char == '-':
                hyphen = True
        if hyphen == True:
            temp = frame.split('-')
            for num in range(int(temp[0]), int(temp[1])+1):
                frames_render.append(int(num))
        else:
            frames_render.append(int(frame))

    return sorted(frames_render)


def render_frames(frames_render):
    filepath = bpy.data.scenes[0].render.filepath
    for frame in frames_render:
        bpy.data.scenes[0].frame_current = frame
        renderpath = filepath + str(bpy.data.scenes[0].frame_current)
        bpy.data.scenes[0].render.filepath = renderpath
        bpy.ops.render.render(write_still = True)
    bpy.data.scenes[0].render.filepath = filepath


def register():
    bpy.utils.register_class(cherry_picker)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.render_frames_cherry_picker = bpy.props.StringProperty (name = "", description = "Frames", default = "")


def unregister():
    bpy.utils.unregister_class(cherry_picker)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.render_frames_cherry_picker


if __name__ == "__main__":
    register()
