from pathlib import Path

#Matrix Manipulation is the most common operation to do on 3D objects
from pyrr import Matrix44, Vector3

import moderngl
import moderngl_window
from moderngl_window import geometry

#Camera.py above this file
from camera import CameraWindow


class CubeSimple(CameraWindow):
    #title of window
    title = "Plain Cube"
    #Where to look for images,shader programs etc
    resource_dir = (Path(__file__).parent).resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Makes the Cursor stuck to the center
        self.wnd.mouse_exclusivity = True
        #Creates a 2 by 2 by 2 cube 
        self.cube = geometry.cube(size=(2, 2, 2))
        #Loads a GLSL program Simple Shader.glsl located in same folder
        self.prog = self.load_program('Simple Shader.glsl')
        #color of cube (can be modified)
        self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        #https://learnopengl.com/Advanced-OpenGL/Face-culling | https://learnopengl.com/Advanced-OpenGL/Depth-testing
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        #Creates a 4x4 Matrix that translates the cube's vertices
        rotation = Matrix44.from_eulers((time,time,time), dtype='f4')
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation

        #Writes the nessesary information to shaders https://learnopengl.com/Getting-started/Shaders MUST READ!
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)

        #Renders the Shaders
        self.cube.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(CubeSimple)