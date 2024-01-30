class Interaction(object):
    def __init__(self):
        """Handles user interaction"""
        # currently pressed mouse button
        self.pressed = None
        # the current  location of the camera
        self.translation = [0, 0, 0, 0]
        # the trackball to calculate rotation 
        self.trackball = trackball.Trackball(theta = - 25, distance = 15)
        # the current ouse location 
        self.mouse_loc = None 
        # Unsophisticated callback mechanism 
        self.callbacks = defaultdict(list)
        
        self.register() 
        
    def register(self):
        """register callbacks with glut """
        glutMouseFunc(self.handle_mouse_button)
        glutMotionFunc(self.handle_mouse_move)
        glutKeyboardFunc(self.handle_keystroke)
        glutSpecialFunc(self.handle_keystroke)
        
    