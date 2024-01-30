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



