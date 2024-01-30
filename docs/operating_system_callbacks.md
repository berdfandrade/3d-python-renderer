# Operating System Callbacks

In order to meaningfully interpret user input, we need to combine knowledge of the mouse postion, mose buttons, and keyboard. Because interpreting user input into meaningful actions requires many lines of code, we encapsulate it in a separate class, away from the main code path. The `Interaction` class hides unrelared complexity from the rest of the codebase and translate operating system events into application-level events.

```python
    # class Interaction 
    def translate(self, x, y, z):
        """ translate the camera """
        self.translation[0] += x
        self.translation[1] += y
        self.translation[2] += z

    def handle_mouse_button(self, button, mode, x, y):
        """ Called when the mouse button is pressed or released """
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - y  # invert the y coordinate because OpenGL is inverted
        self.mouse_loc = (x, y)

        if mode == GLUT_DOWN:
            self.pressed = button
            if button == GLUT_RIGHT_BUTTON:
                pass
            elif button == GLUT_LEFT_BUTTON:  # pick
                self.trigger('pick', x, y)
            elif button == 3:  # scroll up
                self.translate(0, 0, 1.0)
            elif button == 4:  # scroll up
                self.translate(0, 0, -1.0)
        else:  # mouse button release
            self.pressed = None
        glutPostRedisplay()

    def handle_mouse_move(self, x, screen_y):
        """ Called when the mouse is moved """
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y  # invert the y coordinate because OpenGL is inverted
        if self.pressed is not None:
            dx = x - self.mouse_loc[0]
            dy = y - self.mouse_loc[1]
            if self.pressed == GLUT_RIGHT_BUTTON and self.trackball is not None:
                # ignore the updated camera loc because we want to always
                # rotate around the origin
                self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)
            elif self.pressed == GLUT_LEFT_BUTTON:
                self.trigger('move', x, y)
            elif self.pressed == GLUT_MIDDLE_BUTTON:
                self.translate(dx/60.0, dy/60.0, 0)
            else:
                pass
            glutPostRedisplay()
        self.mouse_loc = (x, y)

    def handle_keystroke(self, key, x, screen_y):
        """ Called on keyboard input from the user """
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y
        if key == 's':
            self.trigger('place', 'sphere', x, y)
        elif key == 'c':
            self.trigger('place', 'cube', x, y)
        elif key == GLUT_KEY_UP:
            self.trigger('scale', up=True)
        elif key == GLUT_KEY_DOWN:
            self.trigger('scale', up=False)
        elif key == GLUT_KEY_LEFT:
            self.trigger('rotate_color', forward=True)
        elif key == GLUT_KEY_RIGHT:
            self.trigger('rotate_color', forward=False)
        glutPostRedisplay()

```

### Internal Callbacks

In the code snippet above, you will notice that when the `Interaction` instance interprets a user aciton, it calls `self.trigger` with a string describing the action type. The `trigger` function of the `Interaction` class is part of a simple callback system function on the `Viewer` class registers callbacks on the `Interaction` instance by calling `register_callback`.

```python
# class Interaction
def register_callback(self, name, func):
    self.callbacks[name].append(func)
```

When user interface code needs to trigger an event on the scene, the `Interaction` class calls all of the saved callbacks it has for that specific event:

```python
# class Interaction
def trigger(self, name, * args, **kwargs):
    for func in self.callbacks[name]:
        func(*args, **kwargs)
```

This application-level callback system abstracts away the need of the system to know about operating system input. Each application-level callback represetns a meaningful request within the application. The `Interaction` class acts as a translator between operating system events and application-level events. This means that if we decided to port the modeller to another toolkit in addition to GLUT, we would onlyu need to replace the `Interaction` class with a class that converts the input from the new toolkit into the same set of meaningful application-level callbacks. We use callbacks and arguments in Table 13.1 

#### Table 13.1 - Interaction callback and arguments

| Callback      | Arguments                        | Purpose                                                                         |
|---------------|----------------------------------|---------------------------------------------------------------------------------|
| `pick`          | x:number, y:number                | Selects the node at the mouse pointer location.                                  |
| `move`          | x:number, y:number                | Moves the currently selected node to the mouse pointer location.                |
| `place`         | shape:string, x:number, y:number  | Places a shape of the specified type at the mouse pointer location.             |
| `rotate_color`  | forward:boolean                  | Rotates the color of the currently selected node through the list of colors, forwards or backwards. |
| `scale`         | up:boolean                       | Scales the currently selected node up or down, according to parameter.         |

This simple callback system provides all of the functionality we need for this project. In a production 3D modeller, however, user interface objects are often created and destroyed dynamically. IN that case, we would need a more sophisticated envent listening system, where objects can both register and unregister callback for events.

##### Interfacing with the Scene

In this project, we accomplish camera motion by transforming the scene. In other words. The camera is at a fixed loction and userr input moves the scene instead of moving the camera. The camera is placed at `[0,0,-15]` and facnes the world space origin. (Alternatively, we could change the perspective matrix to move the camera instead of the scene. This design decising has very little impact on the rest of the project.) Revisiting the `render` function in interaction with the scene: rotation and translation. 

#### Rotation the Scene with a Trackball 

We accomplish rotation of the scene by using a _trackball_ algorithm. The trackball is an intuitive interface for manipulating the scene in tree dimensions. Conceptually, a trackball interfacec functions as if the scene was inside a transparent globe. Placing on the surface of the globe and pushing it rotatares the globe. Similarly, clicking the right mouse button and moving it on the screen rotates the scene. You can find out more about the theory on trackball at the [OpenGL Wiki](www.opengl.org/wiki/Object_Mouse_Trackball). In this projectm we use a trackball implementation provaide as part of [Glumpy](https://code.google.com/archive/p/glumpy/source).

We interact with the trackball using the `drag_to` function, with the current location of the mouse as the stating location and the change in mouse location as paramenters

`self.trackball.drag_to(self.mouse_loc[0], self.mouse_loc[1], dx, dy)`

the resulting rotation matrix is `trackball.matrix` in the viewer when the scene is rendered. 

#### Aside : Quaternations 

Rotations are traditionally represented in one of two ways. The first is a rotation value around each axis; you could store this as a 3-tuple of floating point numbers. The other common representation for rotations is a quaternion, an element composed of a vector with x, y, and z coordinates, and a w rotation. Using quaternions has numerous benefits over per-axis rotation; in particular, they are more numerically stable. Using quaternions avoids problems like gimbal lock. The downside of quaternions is that they are less intuitive to work with and harder to understand. If you are brave and would like to learn more about quaternions, you can refer to this [explanation](http://3dgep.com/?p=1815).