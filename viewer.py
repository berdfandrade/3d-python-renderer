import numpy as numpy


class Viewer(object):
    def __init__(self):
        """Initialize the viewer."""
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()

    def init_interface(self):
        """initialize the window and register the render function"""
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("3D Modeller")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.render)

    def init_opengl(self):
        """initialize the opengl settings to render the scene"""
        self.inverseModelView = numpy.identity(4)
        self.modelView = numpy.identity(4)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)

    def init_scene(self):
        """initialize the scene object and initial scene"""
        self.scene = Scene()
        self.create_sample_scene()

    def create_sample_scene(self):
        cube_node = Cube()
        cube_node.translate(2, 0, 2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)

        sphere_node = Sphere()
        sphere_node.translate(-2, 0, 2)
        sphere_node.color_index = 3
        self.scene.add_node(sphere_node)

        hierarchical_node = SnowFigure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_node(hierarchical_node)

    def init_interaction(self):
        """init user interaction and callbacks"""
        self.interaction = Interaction()
        self.interaction.register_callback("pick", self.pick)
        self.interaction.register_callback("move", self.move)
        self.interaction.register_callback("place", self.place)
        self.interaction.register_callback("rotate_color", self.rotate_color)
        self.interaction.register_callback("scale", self.scale)

    def render(self):
        """The render pass for the scene"""
        self.init_view()
        glEnable(GL_LIGHTING)
        glClear(GL_CLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Load the modelview matrix from the current state of the trackball
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrix(self.interaction.trackball.matrix)

        # Store the inverse of the current modelview.
        currentModedlView = numpy.array(glGetFloatv(GLMODELVIEW_MATRIX))
        self.modelView = numpy.transpose(currentModelView)
        self.inverseModelView = inv(numpy.transpose(currentModelView))

        """
        Render the scene. This will call the render function for each object in the scene
        """
        self.scene.render()

        # Draw the grid
        glDisable(GL_LIGHTING)
        glCallList(G_OBJ_PLANE)
        glPopMatrix()

        # Flush the buffers so that the scene can be drawn
        glFlush()

    def init_view(self):
        """initialize the projectin matrix"""
        xSize, ySzie = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)

        # Load the projection matrix. Always the same
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)

    def get_ray(self, x, y):
        """
        Generate a ray beginning at the near plane, in the direction that
        the x, y coordinates are facing

        Consumes: x, y coordinates of mouse on screen
        Return: start, direction of the ray
        """
        self.init_view()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # get two points on the line.
        start = numpy.array(gluUnProject(x, y, 0.001))
        end = numpy.array(gluUnProject(x, y, 0.999))

        # convert those points into a ray
        direction = end - start
        direction = direction / norm(direction)

        return (start, direction)

    def pick(self, x, y):
        """Execute pick of an object. Selects an object in the scene."""
        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.modelView)

    def main_loop(self):
        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.main_loop()
