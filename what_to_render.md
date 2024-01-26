## What to Render: The Scene

--- 

Now that we've initialized the rendering pipeline to handle drawing in the world coordinate spacem, what are we going to render? Recall that our goal is to have a desing consisting of 3D models. We need a data structure to contain the design, and we need use this data structure to render the design. Notice above that `self.scene.render()` from the viewer's render loop. Whais is the scene?

The `Scene` class is the interface to the data structure we use to represent the design. It abstracts away details of the data structe and provides the necessary intercade functions required to interact with the disign, including functions to render, add item, and manipulate items. There is one `Scene` object, owned by the viewer. The `Scene` instance keeps a list of all of the items in the scene, called `node_list`. It also keeps track of the slected item. The `render` function on the scene simply calls `render` on each of the members of `node_list`.


```python
class Scene(object):

    # the default depth from the camera to place an object at
    PLACE_DEPTH = 15.0

    def __init__(self):
        # The scene keeps a list of nodes that are displayed
        self.node_list = list()
        # Keep track of the currently selected node.
        # Actions may depend on whether or not something is selected
        self.selected_node = None

    def add_node(self, node):
        """ Add a new node to the scene """
        self.node_list.append(node)

    def render(self):
        """ Render the scene. """
        for node in self.node_list:
            node.render()
```