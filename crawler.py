import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class Stack:
  data = []

  def push(self, el):
    self.data.append(el)
  
  def pop(self):
    return self.data.pop()
  
  def size(self):
    return len(self.data)


class Crawler:
  visited = {}
  stack = Stack()
  enstackd = set() 
  max_depth = 0
  iteration = 0
  graph = defaultdict(list)

  def __init__(self, url: str, max_iter: int = 200):
    self.url = url
    self.max_iter = max_iter

  def getData(self, url: str):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0 Safari/537.36"
      }
    return requests.get(url, headers=headers).text

  def getLinks(self, url:str, data: str):
    soup = BeautifulSoup(data, "html.parser")
    links = []
    see_also_span = soup.find("h2", id="See_also")
    if(see_also_span):
      heading = see_also_span.parent
      for sibling in heading.next_siblings:
        if getattr(sibling.next_element, "name", None) == "h2":
          break

        if hasattr(sibling, "find_all"):
          for a_tag in sibling.find_all("a", href=True):
            links.append("https://en.wikipedia.org/" + a_tag["href"])

    for el in links:
      if(el not in self.visited or
        el not in self.enstackd):
        self.stack.push(el)
        self.enstackd.add(el)
        self.graph[url].append(el)


  def search(self):
    self.iteration += 1
    self.visited[self.url] = 1
    data = self.getData(self.url)
    self.getLinks(self.url, data)

    while self.stack.size() > 0 and self.iteration < self.max_iter:
      name = self.stack.pop()
      self.iteration += 1
      self.visited[name] = 1
      data = self.getData(name)
      self.getLinks(name, data)

  def maxDepth(self):        
    max_depth = 0
    stack = [(self.url, 0)]
    visited = set()

    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)
        visited.add(node)

        for neighbor in self.graph[node]:
            if neighbor not in visited:
                stack.append((neighbor, depth + 1))

    return max_depth

  def maxIterations(self):
    return self.iteration
  
  def getVisited(self):
    return list(self.visited.keys())


crawler = Crawler("https://en.wikipedia.org/wiki/Internet")
crawler.search()
print("Iterations:",crawler.maxIterations())
print("Max depth:", crawler.maxDepth())
for el in crawler.getVisited():
  print(el)