import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin
from typing import Callable




class Stack:
  def __init__(self):
    self.data = []
    self.elements = set()

  def push(self, el):
    self.elements.add(el)
    self.data.append(el)
  
  def pop(self):
    el = self.data.pop()
    self.elements.remove(el)
    return el
  
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

  def visited(self):
    return list(self.tree.keys())










class Crawler:
  def clear(self, url: str, max_iter: int = 200, 
            begin: Callable = lambda soup: soup.find("h2", id="See_also"), 
            end: Callable = lambda sibling: getattr(sibling.next_element, "name", None) == "h2",
            get: Callable = lambda url, data: None):
    self.url = url
    self.max_iter = max_iter
    self.iteration = 0
    
    self.stack = Stack()
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
      print(f"Failed to fetch {url}: {e}")
      return None

  def getLinks(self, url:str, data: str):
    soup = BeautifulSoup(data, "html.parser")
    see_also = self.begin(soup)

    if(see_also):
      heading = see_also.parent
      for sibling in heading.next_siblings:
        if self.end(sibling):
          break

        if hasattr(sibling, "find_all"):
          for a_tag in sibling.find_all("a", href=True):
            el = urljoin("https://en.wikipedia.org/", a_tag["href"])
            if(not self.tree.exists(el) and not self.stack.exists(el)):
              self.stack.push(el)
              self.tree.addConnection(url, el)

  def search(self, url: str, max_iter: int = 200, 
            begin: Callable = lambda soup: soup.find("h2", id="See_also"), 
            end: Callable = lambda sibling: getattr(sibling.next_element, "name", None) == "h2",
            get: Callable = None):
    
    self.clear(url, max_iter, begin, end, get)
    pbar = tqdm(total=self.max_iter, desc="Searching")

    data = self.getData(self.url)
    if(get is not None):
      get(self.url, data)
    if(data is not None):
        self.getLinks(self.url, data)
      

    self.iteration += 1
    pbar.update(1)

    while self.stack.size() > 0 and self.iteration < self.max_iter:
      name = self.stack.pop()
      self.iteration += 1
      data = self.getData(name)
      
      if(get is not None):
        get(name, data)
      if(data is not None):
        self.getLinks(name, data)
      
      pbar.update(1)

  def maxDepth(self):        
    return self.tree.maxDepth()

  def maxIterations(self):
    return self.iteration
  
  def getVisited(self):
    return self.tree.visited()
