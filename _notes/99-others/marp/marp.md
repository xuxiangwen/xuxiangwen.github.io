---
marp: true
theme: default
style: |
  section {
    background-color: #ccc;
  } 
  section.lead h1 {
    text-align: center;
  }
  section::after {
    font-weight: bold;
    text-shadow: 1px 1px 0 #fff;
  }
paginate: true
_paginate: true
_backgroundImage: "linear-gradient(to right, #97b8e3, #0188d1)" 
---

# <!-- fit --> Marpit Markdown
本文内容来自： https://marpit.marp.app/markdown



---
<!-- _class: lead -->
# Slide 1



---

<!-- backgroundColor: aqua -->
<!-- _backgroundColor: darkgreen -->
<!-- _color: white -->
# Slide 2

bar

---



<!-- backgroundColor: orange -->
# Slide 3

bar

---

<!-- 
footer: '![hp logo](images/hp.png)' 
backgroundColor: white
-->

---

![bg](https://fakeimg.pl/800x600/0288d1/fff/?text=A)
![bg](https://fakeimg.pl/800x600/02669d/fff/?text=B)
![bg](https://fakeimg.pl/800x600/67b8e3/fff/?text=C)

--- 

![bg vertical](https://fakeimg.pl/800x600/0288d1/fff/?text=A)
![bg](https://fakeimg.pl/800x600/02669d/fff/?text=B)
![bg](https://fakeimg.pl/800x600/67b8e3/fff/?text=C)

---

![bg left](https://picsum.photos/720?image=29)

# Split backgrounds

The space of a slide content will shrink to the right side.

---

![bg right](https://picsum.photos/720?image=3)
![bg](https://picsum.photos/720?image=20)

# Split + Multiple BGs

The space of a slide content will shrink to the left side.

---


![bg left:33%](https://picsum.photos/720?image=27)

# Split backgrounds with specified size


--- 

# Hex color (White BG + Black text)

![bg](#fff)
![](#000)

---

# Named color (rebeccapurple BG + White text)

![bg](rebeccapurple)
![](white)

---

# RGB values (Orange BG + White text)

![bg](rgb(255,128,0))
![](rgb(255,255,255))

--- 

# Bullet list

- One
- Two
- Three

---

# Fragmented list

* One
* Two
* Three

---

# Ordered list

1. One
2. Two
3. Three

---

# Fragmented list

1) One
2) Two
3) Three

---

<!-- Global style -->
<style>
h1 {
  color: darkgreen;
}
</style>

# Red text

---

<!-- Scoped style -->
<style scoped>
h1 {
  color: blue;
}
</style>

# Blue text (only in the current slide page)

---

# Red text