# Author: Logan Hunt

from queue import *
from math import ceil, log2

calcF = lambda num_objects: ceil(log2(num_objects))

class HuffmanNode(object):
  def __init__(self, symbol=None, frequency=None):
    self.symbol = symbol
    self.freq = frequency
    self.right = None
    self.left = None
  def __str__(self,):
    # string representation
    return "(" + str(self.symbol) + "," + str(round(self.freq,3)) + ")"

def findMinNode(list_of_nodes):
  # 1 is the largest possible frequency
  min_node = HuffmanNode(frequency=1)
  for i in list_of_nodes:
    if i.freq < min_node.freq:
      min_node = i
  return min_node

def findUniqueLetters(dataString):
  letters = []
  for i in dataString:
    if i not in letters:
      letters.append(i)
  return letters

def buildHuffman(dataString):
  # Initialize the list of huffman nodes
  q = list(map(lambda x: HuffmanNode(x, dataString.count(x) / len(dataString)), findUniqueLetters(dataString)))
  T = HuffmanNode()
  while (len(q) > 1):
    left_node = findMinNode(q)
    q.remove(left_node)
    right_node = findMinNode(q)
    q.remove(right_node)
    T = HuffmanNode(frequency=left_node.freq + right_node.freq)
    T.right = right_node
    T.left = left_node
    q.append(T)
  return T

def inOrder(tree, a=None):
  if (a is None):
    a = list()
  if (tree == None):
    return
  inOrder(tree.left, a)
  a.append([tree.symbol, tree.freq])
  inOrder(tree.right, a)
  return a

def isLeaf(tree):
  if (tree):
    return (tree.right == tree.left and tree.right is None)

def generateCodes(tree, curr_code=None, codes=None):
  if (curr_code is None):
    curr_code = list()
  if (codes is None):
    codes = dict()
  if (tree.left):
    curr_code.append("0")
    generateCodes(tree.left, curr_code, codes)
    curr_code.pop()
  if (tree.right):
    curr_code.append("1")
    generateCodes(tree.right, curr_code, codes)
    curr_code.pop()
  if tree.symbol:
    codes["".join(curr_code)] = str(tree.symbol)
    curr_code = ""
  return codes

def decodeHuffman(encodedString, tree):
  message = ""
  codes = generateCodes(tree)
  while encodedString:
    for i in codes.keys():
      if encodedString.startswith(i):
        encodedString = encodedString[len(i):]
        message += codes[i]
  return message

def encodeHuffman(dataString, codes=None):
  returnTree  = False
  if (codes is None):
    returnTree = True
    tempTree = buildHuffman(dataString)
    codes = generateCodes(tempTree)
  encoded = ""
  reversed_codes = dict(list(map(lambda x: [codes[x], x], codes.keys())))
  for i in dataString:
    encoded += reversed_codes[str(i)]

  if (returnTree):
    return [encoded, tempTree]
  return encoded

def calculateCompressionRatio(string):
  tempTree = buildHuffman(string)
  codes = generateCodes(tempTree)
  numBitsWithFixed = len(string) * calcF(len(codes))
  numBitsWithHuffman = len(encodeHuffman(string, codes))
  return round(100 * ((numBitsWithFixed - numBitsWithHuffman) / numBitsWithFixed), 2)
