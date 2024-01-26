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
        glDepthFunc(GL_LESS)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, GLfloat_3(0, 0, -1))

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.4, 0.4, 0.4, 0.0)
    
    def init_scene(self):
        """ initialize the scene object and initial scene """
        self.scene = Scene()
        self.create_sample_scene()
    
    def create_sameple_scene(self):
        cube_node = Cube()
        cube.node.translate(2,0,2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)
        
        sphere_node = Sphere()
        sphere_node.translate(-2,0,2)
        shpere_node.color_index = 3
        self.scene.add_node(sphere_node)
        
        hierarchical_node = SnowFigure()
        hierarchical_node.translate(-2,0,2)
        self.scene.add_node(hierarchical_node)
    
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
