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
    