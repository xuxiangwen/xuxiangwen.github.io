---
marp: true
title: Document with Some Tools
description: 
theme: default
paginate: true
_paginate: false
_backgroundImage: "linear-gradient(to right, white, #0088d1)" 
footer: "![hp logo](images/hp.png)"
_footer: ""
style: |
  section::after {
    color: #0096d6;
    font-size: 20px;
  } 
  section {
    font-size: 28px;
  }
  h1 {
    font-size: 64px;
  }
  h2 {
    font-size: 48px;
  }
  h3 {
    font-size: 40px;
  }  
---

<!-- Scoped style -->

<style scoped>
  section {
    font-size: 24px;
    text-align: center;
  }
</style>

# <!--fit-->  Document with Some Tools

Michael
June, 2020

---



#  Agenda

- Basic
  - Workflow
  - Use Markdown
  - Write Documents in Typora 
  - Share Documents With GitHub
- Advance
  - Write Slides in Visual Studio Code with Marp
  - Write Interactive Codes in Jupyter Notebook
  - Convert Markdown to Jupyter Notebook
  - Publish Documents with GitHub Pages

---

# Workflow



![width:1000px](images/image-20200618134211723.png)

> All tools are free.

---
## Principles
- Most documents are written by Markdown. 
- All history versions of documents are stored by Git and GitHub. 



---


# Use Markdown

[Markdown](https://en.wikipedia.org/wiki/Markdown) is a lightweight markup language with plain-text-formatting syntax, created in 2004.

- Fast: Without Rich Format
- Easy: Learn it in 5 minutes.
  tutorial: https://guides.github.com/features/mastering-markdown/

---


![bg fit](images/markdown.png)

---

## Show Mathematics using Tex/LaTeX syntax

All markdown tools supports rendering normal mathematics using Tex/LaTeX syntax.

![image-20200618114631577](images/image-20200618114631577.png)

---
Here are the codes behind the mathematics.
~~~markdown
\begin{align*}
y = y(x,t) &= A e^{i\theta} \\
&= A (\cos \theta + i \sin \theta) \\
&= A (\cos(kx - \omega t) + i \sin(kx - \omega t)) \\
&= A\cos(kx - \omega t) + i A\sin(kx - \omega t)  \\
&= A\cos \Big(\frac{2\pi}{\lambda}x - \frac{2\pi v}{\lambda} t \Big) + i A\sin \Big(\frac{2\pi}{\lambda}x - \frac{2\pi v}{\lambda} t \Big)  \\
&= A\cos \frac{2\pi}{\lambda} (x - v t) + i A\sin \frac{2\pi}{\lambda} (x - v t)
\end{align*}
~~~

---

## Show Diagrams using Mermaid 

 [Mermaid](https://mermaid-js.github.io/mermaid/#/) is a tool to geneate diagrams and flowcharts from text in a similar manner as markdown. 

Mermaid was nominated and won the JS Open Source Awards (2019) in the category "The most exciting use of technology"!!!

> The worflow diagram was done by Mermaid.  
> Though Mermaid is still much simpler than other commercial tools(like visio),  it is faster to create and modify diagrams via codes. 

---

![image-20200618115509038](images/image-20200618115509038.png)

see [more examples](https://mermaid-js.github.io/mermaid/#/examples), [Mermaid live editor](https://mermaid-js.github.io/mermaid-live-editor)

---

# Write Documents in Typora

[Typora](https://typora.io/) is a markdown editor.  It gives you a seamless experience as both a reader and a writer.

- Distractions Free
- Seamless Live Preview
- What You See Is What You Mean

> Typora is commercial software (not open source), but is free during beta.

---

Easy to locate the chapter in Outline. 

![width:900px](images/image-20200618105403720.png)

---

# Easy to Insert Image

- insert images via capturing screen 
- copy images from web pages

Don't need to download or upload, it only takes less than 3 seconds to add an image in the document.


![width:800px](images/image-20200618102348967.png)

---

# Share Documents With [GitHub](https://github.com/)

There are 3 actions.

1. Commit the changes with description.

2. Push to GitHub

   Share the changes to others.

3. Pull from GitHub

   Get updates from others.

> Suggest to use [GitHub Desktop](https://desktop.github.com/). 

---

GitHub Desktop monitors the documents automatically. It is pretty easy to commit, push and pull  changes on GitHub Desktop.

![width:800px](images/image-20200618102213933.png)

---


# Write Slides in Visual Studio Code with Marp

[Marp for VS Code](https://github.com/marp-team/marp-vscode) is a tool to create slide deck written in Marp Markdown on VS Code.

- Install [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) in VS Code.

- Tutorial: https://marpit.marp.app/markdown

> This PPT itself was done by Marp for VS Code.

---

![image-20200618131100978](images/image-20200618131100978.png)

---

# Write Interactive Codes in Jupyter Notebook

The [Jupyter Notebook](https://jupyter.org/) is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text.

- Jupyter supports over 40 programming languages, including Python, R, Julia, and Scala.

- Install [Jupyter Notebook](https://jupyter.org/install) 

---



![height:600px](images/image-20200618104558515.png)

[sample link](https://nbviewer.jupyter.org/github/odewahn/ipynb-examples/blob/master/SymPy%20Examples.ipynb)

---

# Convert Markdown to Jupyter Notebook

[notedown](http://github.com/aaren/notedown) is a simple tool to create [IPython notebooks](http://www.ipython.org/notebook) from markdown (and r-markdown).

~~~
 # Install
 sudo  pip3 install notedown
 # Convert
 notedown tutorial.md > tutorial.ipynb
~~~

 

---

# Publish Documents with GitHub Pages

use [GitHub Pages](https://pages.github.com/) to host a website about yourself, your organization, or your project directly from a GitHub repository.
    
        

---

## Example: [Twitter GitHub](https://twitter.github.io/)

![height:500px](images/image-20200618120441577.png)


see [more examples](https://github.com/collections/github-pages-examples)

---

<!-- 
_paginate: false
_footer: ''
_backgroundImage: "linear-gradient(to left, white, #0088d1)" 
-->

<!-- Scoped style -->

<style scoped>
  section {
    font-size: 24px;
    text-align: center;
  }
</style>


# Thank You :smile: