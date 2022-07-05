import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.saveconfig(buffer, format = 'png')
    buffer.seeker(0)
    image_png = buffer.getvalue()
    print(image_png)
    graph = base64.b64encode(image_png)
    print(graph)
    graph = graph.decode('utf-8')
    print(graph)
    buffer.close()

    return graph

def get_plot(x,y):
    #.
    graph = get_graph()
    return graph