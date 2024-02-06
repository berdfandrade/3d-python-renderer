# User Interaction

Now that our modeller is capable of storing and displaying the scene, we need a way to interact with it. There are two types of interactions that we need to facilitate. First, we need the capability of changing the viewing perspective of the scene. We want to be able to move the eye, or camera, around the scene. Second, we need to be able to add new nodes and to modify nodes in the scene.

To enable user interaction, we need to know when the user presses keys or moves the mouse. Luckily, the operating system already knows when these events happen. GLUT allows us to register a function to be called whenever a certain event occurs. We write functions to interpret key presses and mouse movement, and tell GLUT to call those functions when the corresponding keys are pressed. Once we know which keys the user is pressing, we need to interpret the input and apply the intended actions to the scene.

The logic for listening to operating system events and interpreting their meaning is found in the Interaction class. The `Viewer` class we wrote earlier owns the single instance of Interaction. We will use the GLUT callback mechanism to register functions to be called when a mouse button is pressed (`glutMouseFunc`), when the mouse is moved (`glutMotionFunc`), when a keyboard button is pressed (glutKeyboardFunc), and when the arrow keys are pressed (`glutSpecialFunc`). We'll see the functions that handle input events shortly.

```python
class Interaction(object):
    def __init__(self):
        """ Handles user interaction """
        # currently pressed mouse button
        self.pressed = None
        # the current location of the camera
        self.translation = [0, 0, 0, 0]
        # the trackball to calculate rotation
        self.trackball = trackball.Trackball(theta = -25, distance=15)
        # the current mouse location
        self.mouse_loc = None
        # Unsophisticated callback mechanism
        self.callbacks = defaultdict(list)

        self.register()

    def register(self):
        """ register callbacks with glut """
        glutMouseFunc(self.handle_mouse_button)
        glutMotionFunc(self.handle_mouse_move)
        glutKeyboardFunc(self.handle_keystroke)
        glutSpecialFunc(self.handle_keystroke)
```
