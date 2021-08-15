# https://discourse.panda3d.org/t/visualize-scene-graph-python/27873
import panda3d.core as p3d
import matplotlib.pyplot as plt
import pydot
import cv2
import numpy as np
from direct.showbase.ShowBase import ShowBase

class VisualizeScene(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.load()
        self.showSceneGraph()

    # Sample usage
    def load(self):
        child1 = [base.render.attach_new_node(f'child{i}') for i in range(10)]
        for child in child1:
            child.setPos(*np.random.rand(3))

        child2 = [child1[2].attach_new_node(f'child{i}') for i in range(5)]
        for child in child2:
            child.setHpr(*np.random.rand(3))

    def showSceneGraph(self):
        plt.figure(figsize=(20,20))
        plt.imshow(self.draw_scene_graph(base.render))
        plt.savefig("SceneGraph.png")
        plt.title("Scene Graph")
        plt.show()

    def get_label(self, node: p3d.NodePath):
        """
        Get relevant values from a node path

        :param node:
        :return:
        """
        x, y, z = node.getPos()
        h, p, r = node.getHpr()
        label_dict = {'x': x, 'y': y, 'z': z, 'h': h, 'p': p, 'r': r}
        label = ''
        for key, value in label_dict.items():
            if value == 0:
                continue
            label += '{}={:.2f}\n'.format(key, value)
        return label


    def draw_scene_graph(self, rootnode: p3d.NodePath, graph: pydot.Dot = None, node_idx=0):
        """
        A simple visualization function for the scene graph

        :param rootnode: The reference node whose children you wish to visualize
        :param graph: pydot graph, leave to None to automatically create a new graph
        :param node_idx: current node index, do not change, used for recursion
        :return: image of the graph
        """
        if graph is None:
            graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white')
        label = rootnode.name
        info_label = self.get_label(rootnode)
        if info_label != '':
            label += '\n' + info_label

        graph.add_node(pydot.Node(str(rootnode), shape='circle', label=label))
        if len(rootnode.ancestors) > 1:
            graph.add_edge(pydot.Edge(str(rootnode.ancestors[1]), str(rootnode), color='blue'))

        for childnode in rootnode.children:
            self.draw_scene_graph(childnode, graph, node_idx + 1)
        if node_idx == 0:
            # Crashes if you install pydot via pip and not via anaconda OR if you do not have graphviz installed
            im_buf = graph.create_png()
            im_arr = np.frombuffer(im_buf, 'uint8')
            im_cv = cv2.imdecode(im_arr, cv2.IMREAD_ANYCOLOR)[..., ::-1]
            return im_cv

app = VisualizeScene()
app.run()