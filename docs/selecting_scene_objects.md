# Selecing Scene Objects

Now that the user can move and rotate the entire scene to get the perspective they want, the next step is to allow the user to modify and manipulate the objects that make up the scene.

In order for the user to manipulate objects in the scene, they need to be able to select items.

To select an item, we use the current projection matrix to generate a ray that represents the mouse click, as if the mouse pointer shoots a ray into the scene. The selected node is the closest node to the camera with which the ray intersects. Thus the problem of picking reduced to the problem of finding intersections between a ray and nodes in the scene. So the question is: How do we tell if the ray hits a node?

Calculating exactly whether a ray intersects with a node is a challenging problem in terms of both complexity of code and of performance. We would need to write a ray-object intersection check for each type of primitive. For scene nodes with complex mesh geometries with many faces, calculating exact ray-object intersection would require testing the ray against each face and would be computationally expensive.

For the purposes of keeping the code compact and performance reasonable, we use a simple, fast approximation for the ray-object intersection test. In our implementation, each node stores an axis-aligned bounding box (AABB), which is an approximation of the space it occupies. To test whether a ray intersects with a node, we test whether the ray intersects with the node's AABB. This implementation means that all nodes share the same code for intersection tests, and it means that the performance cost is constant and small for all node types.

```python
    # class Viewer
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
        """ Execute pick of an object. Selects an object in the scene. """
        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.modelView)
```

To determine which node was clicked on, we traverse the scene to test whether the ray hits any nodes. We deselect the currently selected node and then choose the node with the intersection closest to the ray origin.

```python
    # class Scene
    def pick(self, start, direction, mat):
        """ 
        Execute selection.
            
        start, direction describe a Ray. 
        mat is the inverse of the current modelview matrix for the scene.
        """
        if self.selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None

        # Keep track of the closest hit.
        mindist = sys.maxint
        closest_node = None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < mindist:
                mindist, closest_node = distance, node

        # If we hit something, keep track of it.
        if closest_node is not None:
            closest_node.select()
            closest_node.depth = mindist
            closest_node.selected_loc = start + direction * mindist
            self.selected_node = closest_node
```

Withing the `Node` class, the `pick` function tests whether the ray intersects with the axis-aligned bounding box of the `Node`. If a node is selected, the `select` function toggles the selected state of the node. Notice that the AABB's `ray_hit` function accepts the transformation matrix between the box's coordinate space and the ray's coodinate space as the third paramenter. Each node applies its own transformation the the matrix before making `ray_hit` function call.

