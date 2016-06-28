# Willow-Cutting Distributed Hash Table

*Note: This README page is a working document. Assume everything is subject to changes.*

Willow-Cutting Distributed Hash Table presents a novel implementation of a distributed hash table. The hash table algorithm that will serve as the backbone of our proposed implementation takes a similar approach in organizing its elements as that of extensible hash table algorithm, but maintains a greater degree of orderliness through its usage of binary search tree data structure. We believe Willow-Cutting Distributed Hash Table will be scalable and efficient, and through our implementatino, we hope to bring some interesting perspectives to the topic of designing a distributed hash table.


## Content Description
#### Data Structure Class Files

A comprehensive layout of data structure file content, and class inheritance between the classes.


*Note: All node classes either directly or indirectly inherit from Node(object), and all data structure classes either directly or indirectly inherit from DataStructure(object). Importantly, DataStructure(object) declares all the essential public functions that will be implemented by its children classes.*

##### 1. dataStructure.py
  * DataStructure(object)

##### 2. node.py
  * Node(object)

##### 3. linkedList.py
  * LinkedListNode(Node)
  * LinkedList(DataStructure)

##### 4. BST.py
  * TreeNode(Node)
  * BST(DataStructure)

##### 5. PDBST.py
  * PDBSTNode(TreeNode)
  * PDBST(BST)

##### 6. chainedHashTable.py
  * ChainedHashTable(DataStructure)

##### 7. willowCuttingHashTable.py
*Note: There are some known bugs in willowCuttingHashTable. We will get to this very soon.*
  * WillowCuttingHashTable(ChainedHashTable)

##### ~~8. AVLTree.py~~ (AVL is not supported anymore)
  * ~~AVLTree(BST)~~


#### Willow-Cutting Distribution Related Files

Distribution relies on Python Twisted Library. 

##### 1. utils.py
  * Contains all global variables that are used in DHT and WCDHT clients and servers.

##### 2. DHTclient.py
  * Regular distributed hash table client implementation. It currently only connects to the server running on localhost.
  * Usage: DHTclient.py request_type key [value]
  * request_type = put, get, delete in lowercase or uppercase
  * key = key you want to access
  * value = used if you are putting a value

##### 3. DHTserver.py
  * Regular distributed hash table sever implementation, which only supports one node.
  * Usage: DHTserver.py initialCapacity loadFactor {LL|BST}
  * initialCapacity = starting number of buckets of the chained hash table
  * loadFactor = load factor the DHT will use to decide when to expand
  * {LL|BST} = Deciding whether the chained data structure is a linked list or binary search tree


##### 4. routingTable.py
  * Contains routing table that keeps track of IP address and Willow-Cutting Hash Table range. 

##### 5. WCDHTclient.py
  * The client to interact with our Willow-Cutting Distributed Hash Table
  * Usage: WCDHTclient.py ip_address request_type key [value]
  * ip_address = IP address of the node you would like to send a request to.
  * the other arguments are the same for DHTclient.py
 
##### 6. WCDHTserver.py
  * The WCDHT implementation, supporting multiple nodes
  * Usage: WCDHTserver.py loadFactor [ip_address]
  * loadFactor = Same as the DHT above. This decides when the table will expand its capacity. This value is only used if no IP address is supplied because this will be the first node
  * ip_address = the IP address of the node you would like to split its data with

#### Performance Test Application Files

Our testing files are not formalized yet, but still provides useful insight into some of our data structures. These files will get updated further as we proceed.

##### 1. pdbstTest.py
  * Includes some rudimentary tests for our PDBST implementation.

##### 2. performanceTest.py
  * Performance comparision test between PDBST and BST. This test can easily be modified for other data structures as well. 

##### 3. FOLDER: textfiles
  * Contains .txt files that are used in testing applications

## Usage
#### Important Tuning Points
Our data structures can be tuned so it would optimize to its environment. Here are some of noteworthy tuning points users should be aware of. 

* PDBST: Upper/lower bound can be tuned at the creation of PDBST object. 
* ChainedHashTable: 
  * Initial Capacity: Initial number of buckets. Can be set at the creation of ChainedHashTable object. Defaults to 12. 
  * Load Factor: Tipping point for deciding when to resize. Can be set at the creatino of ChainedHashTable object. Defaults to 0.8.
  * Chained Data Structure: Can be set either to "LL" for linked list of "BST" for binary search tree. Defaults to LL.
* WillowCuttingHashTable: Upper/lower bound can be tuned at the creation of hash table object. 
* DTHServer/Client: When using localhost, port number can be tuned in the file. It currently uses 1234. 

#### Running Test Files

##### General Data Structure 
* Almost all files contain some form of rudimentary `if __name__=="__main__"` for basic validity checking. To run these, simply type `python [filename].py` in the terminal. 

##### Test files
* Running pdbstTest.py: `python pdbstTest.py textfiles/[textfileName].txt`
* Running performanceTest.py: `python performanceTest.py textfiles/[textfileName].txt`

*Note: Try running with `textfiles/bigfile.txt` first. For a bigger file, there is `textfiles/biggerfile.txt` as well.*

##### DHT Client/Server
Step 1: Start the server by typing `python DHTserver.py`

Step 2: Connect to the server with a client by typing `python DHTclient.py request_type key [value]`
* option:
  * 1 *for GET*
  * 2 *for PUT*
  * 3 *for DELETE*
* key: the dictionary key you are performing operation on.
* [value]: only for PUT. This is the value related to the current key. 

##### WCDHT Client/Server
Step 1: Start a server by typing `python WCDHTserver.py loadFactor`. This creates a node containing the "global" hash table which has a range of 0 - 5000.

Step 2: Spawn more nodes by typing `python WCDHTserver.py loadFactor ip_address` which ignores the loadFactor and connects to the node at the supplied IP address. The Twisted library will take care of host name lookup, so if you are in the Swarthmore CS department, you can use the single name of each computer (i.e. molasses, milk, bacon,...). Each server node must be running on a seperate machine as they all bind to the same port (1234).

Step 3: At any point in this process, with any number of nodes running, the client can connect to any node via `python WCDHTclient.py ip request_type key [value]` with the same usage above, except you must supply the IP address of any of the nodes participating in the WCDHT.

## Authors
Authors: Joon Sung Park and Jacob Carstenson

Adviser: Tia Newhall

Institution: Swarthmore College, PA. Computer Science.
## Acknowledgement

The backbone of our distribution implementation relies on Python Twisted Library. 

The general structure of BST was referred by Brad Miller and David Ranum's online textbook, Problem Solving with Algorithms and Data Structures. 

