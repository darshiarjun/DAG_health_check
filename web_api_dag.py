from flask import Flask,request,jsonify,send_file,render_template #Importing flask libraries
import networkx as nx                                             #Importing flask libraries
import asyncio                                                    #Importing asyncio for asynchronous calls
import json
import random
# import matplotlib.pyplot as plt                                 #Importing matplotlib for creating images
# from io import BytesIO
import pandas as pd                                               #Importing pandas for creating dataframe of health results
from collections import deque                                     #Importing deque for
import argparse

#Initiating the Flask instance for hosting the web app
app = Flask(__name__)

# This POST api is used to upload the json as a file
@app.route("/json_upload", methods=["POST"])
def json_dag_upload():
    global graph, health_status
    data = request.get_json()               # Parse the uploaded json file to a dictionary
    graph.clear()                           # Initialize graph without any nodes or edges
    # Loop on all the items which are nodes of the dictionary and add
    for node, edges in data.items():        # Loop to iterate over each node and check if there are edges and add them to the graph.
        for dep in edges:                   # If there are 1 or more nodes connected to a node then this runs twice so there are 1 or more edges
            graph.add_edge(node, dep)
        if not edges:                       # If there are no outgoing edges add the node to graph
            graph.add_node(node)

    node_health_data = []
    for node in graph.nodes:
        # Append a tuple (node, "unknown") to the list
        node_health_data.append((node, "unknown"))

    # Create a dataframe of data of node health
    health_status = pd.DataFrame(node_health_data, columns=["Component", "Health"])
    return jsonify({"message": "Data json uploaded", "nodes": list(graph.nodes)})


# Function to create health randomly for test purpose
async def node_health_check(node):
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Generate network delay using asyncio
    return random.choice([True, False])


def breadth_first_search_traverse():
    node_visited = set()
    queue = deque()
    for node in graph.nodes:
        if graph.in_degree(node) == 0: # Check for root node
            queue.append(node)
    node_order = []                    # Initializes an empty list to store the traversal order.
    while queue:                       # Keep processing till queue is empty
        node = queue.popleft()         # Remove the first node from the queue FIFO order
        # If the node is not already visited, mark it as visited and add it to node_order.
        # get all direct connecting subsequent nodes of the current node.
        # Add each subsequent node to be processed in subsequent iterations.
        if node not in node_visited:
            node_visited.add(node)
            node_order.append(node)
            for adj_node in graph.successors(node):
                queue.append(adj_node)
    return node_order                   # Returns the list of nodes traversed in breadth first order.

# This POST api is used to check the health the json as a file or direct json.

@app.route("/check_health", methods=["POST"])
def check_health():                     # Check health needs to async because by default Flask is synchronous
    global health_status                # check_health() uses asyncio.gather() to run multiple health checks in paralle and it will fail if not set as async
    loop = asyncio.new_event_loop()     # Create a new event loop
    asyncio.set_event_loop(loop)        # Set the new loop as current loop

    queue = breadth_first_search_traverse()  # Use custom BFS traversal
    # Create an asynchronous task for each node
    # Create empty dictionary named tasks to store asynchronous tasks
    # Simulate health check by calling node_health_check
    # Wait for all the tasks to be completed
    # Store the results in dictionary in format like {"n1":"healthy"} for all nodes
    tasks = {}
    for node in queue:
        tasks[node] = loop.create_task(node_health_check(node))
    loop.run_until_complete(asyncio.gather(*tasks.values()))
    health_results = {node: tasks[node].result() for node in queue}

    # Update health status dataframe
    health_status["Health"] = health_status["Component"].apply(lambda x: health_results.get(x, "unknown"))

    return jsonify(health_results)

# This GET api is used to get the health status as json.
@app.route("/health_status", methods=["GET"])
def get_health_status():
    return jsonify(health_status.to_dict(orient="records"))

# This GET api is used to get the health status as table in browser as a html file
@app.route("/health_status_table", methods=["GET"])
def get_health_status_as_table():
    # Render the health_status DataFrame as an HTML table
	return render_template("health_status.html",tables=[health_status.to_html(classes="table table-bordered")])


# @app.route("/displaygraph", methods=["GET"])
# def displaygraph():
#     pos = nx.spring_layout(graph)
#     colors = []
#     for node in graph.nodes:
#       health = health_status.loc[health_status['Component'] == node, "Health"].values[0]
#       if health == "failed":
#         colors.append("red")
#       else:
#         colors.append("green")
#     plt.figure(figsize=(8, 6))
#     nx.draw(graph, pos, with_labels=True, node_color=colors, edge_color="black", node_size=3000, font_size=10)
#     buf = BytesIO()
#     plt.savefig(buf, format="png")
#     buf.seek(0)
#     return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    # Creating the data frame with columns "Component" and "Health to hold node and health values"
    health_status = pd.DataFrame(columns=["Component", "Health"])
    # Creating the Directed graph of the nodes"
    graph = nx.DiGraph()
    # Calling Flask instance on local host and port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)
