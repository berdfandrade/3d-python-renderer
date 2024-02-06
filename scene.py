class Scene(object):
    # the defautlt depth from the camera to place an object at
    PLACE_DEPTH = 15.0
    
    def __init__(self):
        # The scene keeps a list of nodes that are displayed
        self.node_list = list()
        
        # Keep track of the currently selected node
        # Actions may depend on whether or not something is selected
        
        self.sected_node = None
        
    def add_node(self, node): 
        """ Add a new node to the scene """
        self.node_list.append(node)
    
    def render(self):
        """ Render the scene """
        for node in self.node_list:
            node.render(0)
    def pick(self, start, direction, mat):
        """
        Execute seleciton.
        
        Start, direction describe a Ray.
        mat is the inverse of the current modelview matrix for the scene.
        """
        
        if self.sected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None
        
        # Keep track of the closest hit
        midist = sys.maxint
        closest_node = NOne
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < mindist:
                mindist, closest_node = distance, node
                
        # If we hit something, keep track of it
        if closest_node is not None:
            closes_node.select()
            closest_node.depth = mindist
            closest_node.selected_loc = start + direction * mindist
            self.selected_node = closest_node
            

    