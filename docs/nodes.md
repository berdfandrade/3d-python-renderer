# Nodes 

In the Scene's `render` function, we call `render` on each of the items in the Scene's `node_list`. But what are the elements of that list? We call them _nodes_. Conceptuallu, a node is anything that can be placed in the scene. In object-oriented software, we write `Node` as an abstract base class. Any classes that represent objects to be placed in the `Scene` will inherit from `Node`. This base calss allows us to reason about the scene abastractly. The rest of the code base doesn't need to know about the details of the object it displays. it only needs to know that they are of the class `Node`.

Each type of `Node` defines its own behaviour for rendering itself and for any other interactions. The `Node` keeps track of important data about itself: _translation of matrix, scale matrix, color, etc..._ Multiplying the node's translatrion matrix by its scaling matrix gives the transformation matrix from the node's mnodel coodinate space to the world coordinate space. The node also stores an axis-aligned bounding box( AABB ). We'll see more about *AABBs* when (...)

The simplest concrete implementation of `Node` is a _primitive_ is a single solid shape that can be added the scene. In this project, the primitives are `Cube` and `Sphere`.

````python
class Node(object):
    """ Base class for scene elements """
    def __init__(self):
        self.color_index = random.randint(color.MIN_COLOR, color.MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = numpy.identity(4)
        self.scaling_matrix = numpy.identity(4)
        self.selected = False

    def render(self):
        """ renders the item to the screen """
        glPushMatrix()
        glMultMatrixf(numpy.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        cur_color = color.COLORS[self.color_index]
        glColor3f(cur_color[0], cur_color[1], cur_color[2])
        if self.selected:  # emit light if the node is selected
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])

        self.render_self()

        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])
        glPopMatrix()

    def render_self(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'render_self'")

class Primitive(Node):
    def __init__(self):
        super(Primitive, self).__init__()
        self.call_list = None

    def render_self(self):
        glCallList(self.call_list)


class Sphere(Primitive):
    """ Sphere primitive """
    def __init__(self):
        super(Sphere, self).__init__()
        self.call_list = G_OBJ_SPHERE


class Cube(Primitive):
    """ Cube primitive """
    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = G_OBJ_CUBE
```