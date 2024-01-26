class Viewer(object):
    def __init__(self):
        
        """Initialze the viewer"""
        
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()

    def init_interface(self):
        
        """
        initialize the window and 
        register the render function
        """
        
        glutInit()
        glutInitWindowSize(640, 480)
        glutCreateWindow("3D Modeller")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.render)

    def init_opengl(self):
        
        """
        initialize the opengl 
        settings to render the scene
        """
        self.inverseModelView = numpy.identity(4)
        self.modelView = numpy.identity(4)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)

    def init_viewer(self):
        
        """
        initialize the projection matrix
        """

        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGET(GET_WINDOW_HEIGTH)
        aspect_ratio = float(xSize) / float(ySize)

        # Load the projection matrix. Always the same
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)
