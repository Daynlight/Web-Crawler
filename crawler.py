import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from typing import Callable




class Stack:
  def __init__(self):
    self.data = []
    self.elements = set()

  def push(self, el):
    if el not in self.elements:
      self.elements.add(el)
      self.data.append(el)
  
  def pop(self):
    if self.data:
      el = self.data.pop()
      self.elements.remove(el)
      return el
    return None

  def size(self):
    return len(self.data)

  def exists(self, name):
    if name in self.elements:
      return True
    return False




class Queue:
  def __init__(self):
    self.data = []
    self.elements = set()

  def push(self, el):
    if el not in self.elements:
      self.elements.add(el)
      self.data.append(el)
  
  def pop(self):
    if self.data:
      el = self.data.pop(0)
      self.elements.remove(el)
      return el
    return None
  
  def size(self):
    return len(self.data)

  def exists(self, name):
    if name in self.elements:
      return True
    return False




class Tree:
  def __init__(self):
    self.tree = {}
    self.root = None

  def addConnection(self, parent, child):
    if child in self.tree:
      return
    
    if(self.root == None):
      self.root = parent

    if parent not in self.tree:
      self.tree[parent] = []

    self.tree[parent].append(child)

    if child not in self.tree:
      self.tree[child] = []
  
  def size(self):
    return len(self.tree)

  def exists(self, name):
    if name in self.tree:
      return True
    return False

  def maxDepth(self):
    max_depth = 0
    stack = [(self.root, 0)]
    visited = set()

    while stack:
      node, depth = stack.pop()
      max_depth = max(max_depth, depth)
      visited.add(node)

      for neighbor in self.tree[node]:
        if neighbor not in visited:
          stack.append((neighbor, depth + 1))

    return max_depth
  
  def remove(self, name):
    if name not in self.tree:
      return
    
    for children in self.tree.values():
      while name in children:
        children.remove(name)
    
    self.tree.pop(name)

  def visited(self):
    return list(self.tree.keys())










class Crawler:
  def clear(self, url: str, structure, begin: Callable, 
            end: Callable, max_iter: int = 200, 
            get: Callable = None):
    self.url = url
    self.max_iter = max_iter
    self.iteration = 0
    
    self.structure = structure
    self.tree = Tree()

    self.begin: Callable = begin
    self.end: Callable = end
    self.get = get

  def getData(self, url: str):
    headers = { "User-Agent": "Chrome/116.0 Safari/537.36" }
    try:
      res = requests.get(url, headers=headers, timeout=10)
      res.raise_for_status()
      return res.text 
    except requests.RequestException as e:
      tqdm.write(f"Failed to fetch {url}: {e}")
      return None

  def getLinks(self, url:str, data: str):
    soup = BeautifulSoup(data, "html.parser")
    see_also = self.begin(soup)

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    if(see_also):
      heading = see_also.parent
      for sibling in heading.next_siblings:
        if self.end(sibling):
          break

        if hasattr(sibling, "find_all"):
          for a_tag in sibling.find_all("a", href=True):
            el = urljoin(base_url, a_tag["href"])
            if(not self.tree.exists(el) and not self.structure.exists(el)):
              self.structure.push(el)
              self.tree.addConnection(url, el)

  def search(self, url: str, structure, begin: Callable, 
            end: Callable, max_iter: int = 200, 
            get: Callable = None):
    
    self.clear(url, structure, begin, end, max_iter, get)
    pbar = tqdm(total=self.max_iter, desc="Searching")

    data = self.getData(self.url)
    if(get is not None and data is not None):
      get(self.url, data)
    if(data is not None):
        self.getLinks(self.url, data)
      

    self.iteration += 1
    pbar.update(1)

    while self.structure.size() > 0 and self.iteration < self.max_iter:
      name = self.structure.pop()
      self.iteration += 1
      data = self.getData(name)
      
      if(get is not None and data is not None):
        get(name, data)
      if(data is not None):
        self.getLinks(name, data)
      
      pbar.update(1)

    while(self.structure.size() > 0):
      name = self.structure.pop()
      self.tree.remove(name)

  def maxDepth(self):        
    return self.tree.maxDepth()

  def maxIterations(self):
    return self.iteration
  
  def getVisited(self):
    return self.tree.visited()
