# Nodes 

In the Scene's `render` function, we call `render` on each of the items in the Scene's `node_list`. But what are the elements of that list? We call them _nodes_. Conceptuallu, a node is anything that can be placed in the scene. In object-oriented software, we write `Node` as an abstract base class. Any classes that represent objects to be placed in the `Scene` will inherit from `Node`. This base calss allows us to reason about the scene abastractly. The rest of the code base doesn't need to know about the details of the object it displays. it only needs to know that they are of the class `Node`.

Each type of `Node` defines its own behaviour for rendering itself and for any other interactions. The `Node` keeps track of important data about itself: _translation of matrix, scale matrix, color, etc..._ Multiplying the node's translatrion matrix by its scaling matrix gives the transformation matrix from the node's mnodel coodinate space to the world coordinate space. The node also stores an axis-aligned bounding box( AABB ). We'll see more about *AABBs* when (...)

The simplest concrete implementation of `Node` is a _primitive_ is a single solid shape that can be added the scene. In this project, the primitives are `Cube` and `Sphere`.

```python
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

Rendering nodes is based on the transformation matrices that each node stores. The transformation matrix for a node is the combination of its scaling matrix and its translation matrix. Regardless of the type of the node, the first step to rendering is to set the OpenGL matrices are up to date, we call `render_self` to tell the node to make the necessary OpenGL calls to draw itself. Finally, we undo any changes we made to the OpenGL state for this specific node. We use the `glPushMatrix` and `glPopMatrix` functions in OpenGL to save and restore the state of the ModelView ntrix before and after we render the node. Notice that the node stores its color, location, and scale, and applies these to the OpenGL state before rendering.

If the node is currently selected, we make it emit light. This way, the user has a visual indication of which node they have selected.

For example, the call list for a cube draws the 6 faces of the cube, with the center at the origin and the edges exactly 1 unit long.

```python
# Pseudocode Cube definition
# Left face
((-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)),
# Back face
((-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5)),
# Right face
((0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5)),
# Front face
((-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)),
# Bottom face
((-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5)),
# Top face
((-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5))
```

Using only primitives would be quite limiting for modelling applications. 3D models are generally made up of multiple primitives (or triangular meshes, which are outside the scope of this project). Fourtnunely, our design of the `Node` class facilitates `Scene` nodes that are made up of multiples primitives. In fact, we can support arbitrary groupings of nodes with no added complexity.

As motivation, let us consider a very basic figure: a typical snowman, or snow figure, made up of three spheres. Even though the figure is comprise of three separate primitives, we would like to be able to treat it as a single object.

We create a class called `HierarchicalNode`, a Node that contains other nodes. It manages a list of "children". The `render_self` function for hierarchical nodes simply calls `render_self` on each of the child nodes. With the `HierarchicalNode` class, it is very easy to add figures to the scene. Now, defining the snow figure is as simple as specifying the shapes that comprise it, and their relative positions and sizes.

<img src='https://aosabook.org/en/500L/modeller-images/nodes.jpg'/>


```python
class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()
```

```python
class SnowFigure(HierarchicalNode):
    def __init__(self):
        super(SnowFigure, self).__init__()
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        self.child_nodes[0].translate(0, -0.6, 0) # scale 1.0
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[1].scaling_matrix = numpy.dot(
            self.scaling_matrix, scaling([0.8, 0.8, 0.8]))
        self.child_nodes[2].translate(0, 0.75, 0)
        self.child_nodes[2].scaling_matrix = numpy.dot(
            self.scaling_matrix, scaling([0.7, 0.7, 0.7]))
        for child_node in self.child_nodes:
            child_node.color_index = color.MIN_COLOR
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])
```

You migth observe that the `Node` objects form a tree data structure. The `render` function, through hierarchical nodes, does a depth-fisrt traversal through the tree. As it traverses, it keeps a stack of `ModelView` matrices, used for conversion into the world space. At each step, it pushes the current `ModelView` matrix onto the stack, and when it completes rendering of all child nodes, it pops the matrix off the stack, leaving the parent node's `ModelView` matrix at the top of the stack. 

By making the `Node` class extensible in this way, we can add new types of shapes to the scene without changing any of the other code for scene manipulation and rendering. Using the node concept to abstract away the fact that on `Scene` object may have many children is known as the Composite design pattern. 