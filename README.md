<div align=center>

# 🦀 Web-Crawler 🦀

[![wakatime](https://wakatime.com/badge/user/233b40bd-5512-4e3e-9573-916f7b4127c3/project/f474e8e9-45df-42a8-8579-073cb1377f7a.svg)](https://wakatime.com/badge/user/233b40bd-5512-4e3e-9573-916f7b4127c3/project/f474e8e9-45df-42a8-8579-073cb1377f7a)
</div>



## About
A simple **python web crawler** for searching through web and fetching data. Useful for **finding content** in web and fetching **links**.



## TOC
- [About](#about)
- [TOC](#toc)
- [Installation](#installation)
- [Usage](#usage)
- [Full Example](#full-example)
- [Methods](#methods)
- [Choosing **Stack** or **Queue**](#choosing-stack-or-queue)
- [Uses](#uses)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Kitty](#kitty)



## Installation
1. Clone repo
    ```bash
    git clone https://github.com/Daynlight/Web-Crawler
    cd Web-Crawler
    ```
2. Download python and pip
    ```bash
    sudo apt install python3 python3-pip
    ```
3. Create env and activate
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Install ```requirements.txt```
    ```bash
    pip install -r requirements.txt
    ```



## Usage
1. Include to your project
    ```python
    from crawler import Crawler, Stack, Queue
    ```

2. Create instance
   ```python
    crawler = Crawler()
   ```

3. Create begin and end cases
    ```python
    def begin(soup):
      return soup.find("h2", id="See_also")

    def end(sibling):
      return getattr(sibling.next_element, "name", None) == "h2"
    ``` 
Use ```bs4``` for html parsing

4. Add get function
    ```python
    keywords = []
    def findKeyword(url, data):
      if data is None:
        return
      
      if "internet" in data.lower():
        keywords.append(url)
    ```

5. Search url with your structure **Queue** or **Stack**
    ```python
    crawler.search(
      url="https://en.wikipedia.org/wiki/Internet",
      structure=Queue(),
      begin=begin, 
      end=end, 
      max_iter=100,
      get=findKeyword
    )
    ```



## Full Example
```python
from crawler import Crawler, Stack, Queue

keywords = []
def findKeyword(url, data):
  if data is None:
    return
  
  if "internet" in data.lower():
    keywords.append(url)

def begin(soup):
  return soup.find("h2", id="See_also")

def end(sibling):
  return getattr(sibling.next_element, "name", None) == "h2"

crawler = Crawler()
crawler.search(
  url="https://en.wikipedia.org/wiki/Internet", 
  structure=Queue(),
  begin=begin, 
  end=end, 
  max_iter=500, 
  get=findKeyword
)
```
See [main.ipynb](main.ipynb)



## Methods
- ```clear(url, structure, begin, end, max_iter, get)``` -> clean class.
- ```search(url, structure, begin, end, max_iter, get)``` -> start searching.
- ```getData(url)``` -> getting data from url.
- ```getLinks(url, data)``` -> getting links from data, add to stack and tree.
- ```maxDepth()``` -> getting max depth of tree (independent of Stack/Queue used)
- ```maxIterations()``` -> getting max iteration if stack was empty.
- ```getVisited()``` -> list of visited links.



## Choosing **Stack** or **Queue**
- ```Queue``` -> **BFS** search might is better for more relative links.
- ```Stack``` -> **DFS** search good for deep search, might go into bad direction.



## Uses
- Uses **requests** with header for **getting web content**.
- Uses **tqdm** for progress bar.
- Uses **BeautifulSoup4** for **html parsing**.
- Uses **urllib.parse** for link parsing and creation.
- Uses **Callable** for passing custom functions for ```begin```, ```end```, ```get```. 
- Uses **Tree** structure for saving **visited links** and new ones.
- Uses **Structure** to track links to visit. It **DFS** for **Stack** and **BFS** for **Queue**.



## Architecture
- Clean **Crawler** class every time we use ```search```.
- We begin from **provided link**.
- Fetch data via ```get``` function.
- Fetch links base on ```begin``` and ```end``` functions.
- We add this links to **Stack/Queue** and **Tree**.
- Before **adding to Stack/Queue** we check if it **doesn't appear** in **Tree** and **Stack/Queue** this **prevents revisiting** and **keep tree consistency**.
- When we reach **max iteration limit** or **Stack/Queue is empty** we end search. 
- Before ending ```search`` we **remove unvisited links** base on **Stack/Queue**.



## Prerequisites
- **python3**
- **pip**
- **venv** 
- **requests**
- **beautifulsoup4**
- **tqdm**
- **urllib.parse**



## Kitty
<img width=100% src="https://i.pinimg.com/1200x/0b/0b/ea/0b0bea9cd8a503ea46b14a7f344a1233.jpg">
