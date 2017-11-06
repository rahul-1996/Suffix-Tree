import string
from collections import defaultdict

class SuffixTree(object):

    class Node(object):
        def __init__(self, label):
            self.label = label  # label on path leading to this node
            self.out = {}  # outgoing edges; maps characters to nodes
            self.leaf = defaultdict(list)  # Suffixes that end at this node

    def add(self, s, pos):
        """  Make suffix tree, from s in quadratic time and linear space  """
        s += '$'
        if(pos == 0):
            self.root = self.Node(None)
            self.root.out[s[0]] = self.Node(s)  # trie for just longest suffix
            # add the rest of the suffixes, from longest to shortest
            for i in range(1, len(s)):
                cur = self.root
                j = i
                while j < len(s):
                    if s[j] in cur.out:
                        child = cur.out[s[j]]
                        label = child.label
                        # Walk along edge until we exhaust edge label or
                        # until we mismatch
                        k = j + 1
                        while k - j < len(label) and s[k] == label[k - j]:
                            k += 1
                        if k - j == len(label):
                            cur = child  # we exhausted the edge
                            j = k
                        else:
                            # we fell offset in middle of edge
                            cExist, cNew = label[k - j], s[k]
                            mid = self.Node(label[:k - j])
                            mid.out[cNew] = self.Node(s[k:])

                            # original child becomes mids child
                            mid.out[cExist] = child
                            # original childs labelel is curtailed
                            child.label = label[k - j:]
                            # mid becomes new child of original parent
                            cur.out[s[j]] = mid
                    else:
                        # Fell off tree at a node: make new edge hanging off it
                        cur.out[s[j]] = self.Node(s[j:])

        else:
            # Not the first string added to the tree.
            for i in range(0, len(s)):
                cur = self.root
                j = i
                while j < len(s):
                    if s[j] in cur.out:
                        child = cur.out[s[j]]
                        label = child.label
                        # Walk along edge until we exhaust edge label or
                        # until we mismatch
                        k = j + 1
                        while k - j < len(label) and s[k] == label[k - j]:
                            k += 1
                        if k - j == len(label):
                            cur = child  # we exhausted the edge
                            j = k
                        else:
                            # we fell offset in middle of edge
                            cExist, cNew = label[k - j], s[k]
                            mid = self.Node(label[:k - j])
                            mid.out[cNew] = self.Node(s[k:])
                            # original child becomes mids child
                            mid.out[cExist] = child
                            # original childs labelel is curtailed
                            child.label = label[k - j:]
                            # mid becomes new child of original parent
                            cur.out[s[j]] = mid
                    else:
                        # Fell offset tree at a node: make new edge hanging offset it
                        cur.out[s[j]] = self.Node(s[j:])

    def followPath(self, s):
        """ Follow path given by s.  If we fall offset tree, return None.  If we
            finish mid-edge, return (node, offset) where 'node' is child and
            'offset' is label offset.  If we finish on a node, return (node,
            None). """
        cur = self.root
        i = 0
        while i < len(s):
            c = s[i]
            if c not in cur.out:
                return (None, None)  # fell offset at a node
            child = cur.out[s[i]]
            label = child.label
            j = i + 1
            while j - i < len(label) and j < len(s) and s[j] == label[j - i]:
                j += 1
            if j - i == len(label):
                cur = child  # exhausted edge
                i = j
            elif j == len(s):
                # exhausted query string in middle of edge
                return (child, j - i)
            else:
                return (None, None)  # fell offset in the middle of the edge
        return (cur, None)  # exhausted query string at internal node

    def insertLeaves(self, s, pos):
        """For a given string, attach leaf nodes for all possible suffixes. """
        for i in range(len(s)):
            st = s[i:]
            node, offset = self.followPath(st)
            node.leaf[node.label[0]].append(pos)

    def dfs(self, node, visited):
        """ For tree rooted at the given node, we recursively visit all children nodes 
           until we exhaust the tree. """
        if(node not in visited):
            visited.append(node)
        for nodes in node.out:
            self.dfs(node.out[nodes], visited)
        return visited

    def getLeaves(self, s):
        """ We DFS and get all nodes rooted below the node. We iterate over their
            leaves and get the corresponding positions and return a list of positions"""
        res = []
        node, offset = self.followPath(s)
        visited = self.dfs(node, [])
        for v in visited:
            for a, b in v.leaf.items():
                res.extend(b)
        return res


# Preprocessing the text

finalWords = list()
document = list()
text = list()

# The tale titles are in the document list. 
# The corresponding stories are in the text list. 

document = list()
text = [[] for i in range(312)]

with open("AesopTales.txt") as fp:
    finalWords = list()
    lines = fp.readlines()
    document.append(lines[0])
    j = 0
    i = 0
    while(i < len(lines)):
        if(len(lines[i].strip()) == 0 and len(lines[i + 1].strip()) == 0):
            document.append(lines[i + 2])
            i += 2
            j += 1
        else:
            words = [word.strip(string.punctuation)
                     for word in lines[i].split()]
            for word in words:
                text[j].append(word)
        i += 1

# String the query. For A GST, only single word queries work. 
query = "was"

# Question 1
print("#################### QUESTION 1 ###############################")
for doc in range(312):
    #Object of class suffix tree.
    tree = SuffixTree()
    # Getting length and text of the first tale. 
    lenFinal = len(text[doc])
    finalWords = text[doc]
    # We insert words and leaves
    for i in range(lenFinal):
        tree.add(finalWords[i], i)
    for i in range(lenFinal):
        tree.insertLeaves(finalWords[i], i)
    try:
        # Get all leaf nodes for the query and print surrounding text
        # around the indexed word, if they exist. 
        k = tree.getLeaves(query)
        print("Document:", document[doc])
        for leaves in k:
            try:
                print(finalWords[leaves - 2], end=' ')
            except:
                pass
            try:
                print(finalWords[leaves - 1], end=' ')
            except:
                pass
            print(finalWords[leaves], end=' ')
            try:
                print(finalWords[leaves + 1], end=' ')
            except:
                pass
            try:
                print(finalWords[leaves + 2])
            except:
                pass
    except:
        pass

# Question 2
print("#################### QUESTION 2 ###############################")
for doc in range(312):
    tree = SuffixTree()
    lenFinal = len(text[doc])
    finalWords = text[doc]
    for i in range(lenFinal):
        #Found is a counter so that we stop after the first occurance. 
        found = False
        # z is used to slice the string and get smaller substrings. 
        z = 0
        #Inserting words and leaves into the tree. 
        tree.add(finalWords[i], i)
    for i in range(lenFinal):
        tree.insertLeaves(finalWords[i], i)
    while not found:
        try:
            #Get leaves for query string. If present, return the minimum of leaves. 
            # Stop the iteration by setting found to True. 
            k = tree.getLeaves(query[z:])
            print("Document:", document[doc])
            found = True
            leaves = min(k)
            print('      ', end='')
            try:
                print(finalWords[leaves - 2], end=' ')
            except:
                pass
            try:
                print(finalWords[leaves - 1], end=' ')
            except:
                pass
            print(finalWords[leaves], end=' ')
            try:
                print(finalWords[leaves + 1], end=' ')
            except:
                pass
            try:
                print(finalWords[leaves + 2])
            except:
                pass
        except:
            #If leaf is not found, z is incremented by 1 so that string can be sliced. ss
            z += 1
            pass

# Question 3
print("#################### QUESTION 3 ###############################")
# A bigger query string to test the third question.

query = "occasion when the shepherd laid hold of him"
# Words is a list consisting of all the words of the query string. 

words = query.split()

# List of ranks to rank the document. 
""" We first look for an exact match of the word. If it is not present, 
    we look for smaller substrings. We assign a score of 100/z for a match 
    that is found, where z is the slice index. Trivially, exact matches will have 
    a higher total score. Finally we sort the rank list by index(Not by magnitude of rank)
    and return the list of documents """

ranks = [0] * 312
for queryWord in words:
    for doc in range(312):
        tree = SuffixTree()
        lenFinal = len(text[doc])
        finalWords = text[doc]
        for i in range(lenFinal):
            found = False
            z = 0
            tree.add(finalWords[i], i)
        for i in range(lenFinal):
            tree.insertLeaves(finalWords[i], i)
        while not found:
            try:
                k = tree.getLeaves(queryWord[z:])
                # We increment total rank of the document and choose the first occurance.  
                found = True
                ranks[doc] += 100 / z
                leaves = min(k)
            except:
                z += 1
                pass


#Sorting ranks by their index
ranks = sorted(range(len(ranks)), key=lambda k: ranks[k])

#Printing documents 
for i in range(len(ranks)):
    print("Rank ", i + 1, " : ", document[ranks[i]])
