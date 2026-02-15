import requests
from bs4 import BeautifulSoup
from queue import Queue




class Crawler:
  visited = {}
  queue = Queue()
  enqueued = set() 
  max_depth = 0
  iteration = 0

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

  def getLinks(self, data: str):
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
        el not in self.enqueued):
        self.queue.put(el)
        self.enqueued.add(el)


  def search(self):
    self.iteration += 1
    self.visited[self.url] = 1
    data = self.getData(self.url)
    self.getLinks(data)

    while not self.queue.empty() and self.iteration < self.max_iter:
      name = self.queue.get()
      data = self.getData(name)
      self.getLinks(data)
      self.visited[name] = 1
      self.iteration += 1
    

  def maxIterations(self):
    return self.iteration
  
  def getVisited(self):
    return list(self.visited.keys())


crawler = Crawler("https://en.wikipedia.org/wiki/Internet")
crawler.search()
print(crawler.maxIterations())
for el in crawler.getVisited():
  print(el)