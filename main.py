import random

from kazoo.client import KazooClient

# Constants for Zookeeper paths
# These paths are used to create a test structure in Zookeeper
# and demonstrate basic operations like creating nodes and setting data.
# The TEST_NODE_ROOT is the root node for our test structure,
# and SUB_NODES are the child nodes we will create under it.
TEST_NODE_ROOT = "/servers"

# List of sub-nodes to create under the TEST_NODE_ROOT
# Each sub-node represents a server in our test structure.
# The IP addresses for these nodes will be randomly generated.
# This simulates a scenario where each server has a unique IP address.
SUB_NODES = [
    "server1",
    "server2",
    "server3"
]


def main():
    print("Zookeeper Kazoo Test!")

    # The Zookeeper server is assumed to be running on localhost at port 2181.
    # The KazooClient is used to interact with the Zookeeper service. It provides
    # methods to create nodes, set data, and retrieve children. Ensure that the
    # Zookeeper server is running before executing this script.
    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()

    if zk.exists("/"):
        print("Zookeeper is running.")
    
    # Check if the TEST_NODE_ROOT exists, and create it if it does not. This is 
    # the root node for our test structure. If it already exists, we simply print
    # a message indicating that it exists. If it does not exist, we create it using
    # ensure_path, which creates the node and any necessary parent nodes.
    if zk.exists(TEST_NODE_ROOT):
        print(f"{TEST_NODE_ROOT} already exists.")
    
    else:
        print(f"Creating {TEST_NODE_ROOT}...")

        # ensure_path will recursively create the node and any nodes in the path.
        # This setups up the structure but does not set any data for the nodes.
        zk.ensure_path(TEST_NODE_ROOT)

    # For each node in SUB_NODES, we create the node under TEST_NODE_ROOT.
    # If the node already exists, we print a message indicating that.
    # If it does not exist, we create it and set some data (a random IP).
    for node in SUB_NODES:
        node_path = f"{TEST_NODE_ROOT}/{node}"

        # Generate a random IP address for the node to simulate assigning a unique
        # IP address to each server. If the nodes already exist, it will overwrite
        # the data with the new IP address.
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))

        if zk.exists(node_path):
            print(f"{node_path} already exists.")
        else:
            print(f"Creating {node_path}...")
            zk.create(node_path, b"data")
        
        zk.set(node_path, ip.encode())
    
    # Retrieve and print the children of TEST_NODE_ROOT. This will show the nodes
    # we created under it. We also retrieve the data for each child node and print.
    children = zk.get_children(TEST_NODE_ROOT)

    print(f"Children of {TEST_NODE_ROOT}: {children}")
    
    # For each child node, we retrieve its data and print it.
    # The data is expected to be the IP address we set earlier.
    for node in children:
        node_path = f"{TEST_NODE_ROOT}/{node}"
        data, stat = zk.get(node_path)
        print(f"\t{node_path}: {data.decode()}")

    # Stop the Zookeeper client connection. This is important to release resources
    # and ensure that the connection to the Zookeeper server is properly closed.
    zk.stop()


if __name__ == "__main__":
    main()