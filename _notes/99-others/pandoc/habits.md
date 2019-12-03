---
title: My Slideshow
parallaxBackgroundImage: image/milky-way-starry-sky-night-sky-star-956999.jpeg)
author: Michael
date: May 13, 2019
---

## Slide One

Slide 1 has background_image.png as its background.

~~~shell
pandoc -t revealjs -s habits.md -o habits_revealjs.html -V revealjs-url=https://revealjs.com  -V theme=sky
~~~

## hello abcde  {data-background-image="image/pexels-photo-326311.jpeg"}

Slide 2 has a special image for its background, even though the heading has no content.

# In the morning

## Getting up

> - Turn off alarm
> - Get out of bed

::: notes

This is my note.

- It can contain Markdown
- like this list

:::

## Breakfast

::: notes

This is my note.

- It can contain Markdown
- like this list

:::

- Eat eggs
  - a
  - b

- Drink coffee
  - a
  - b

:::::::::::::: {.columns}
::: {.column width="40%"}
contents...
:::
::: {.column width="60%"}
contents...
:::
::::::::::::::

# In the evening

## Dinner

::: incremental

- Eat spaghetti
- Drink wine

:::

![img](image/Tarako_spaghetti.jpg)

. . .

## Going to sleep

::: incremental

- Get in bed
- Count sheep

:::

::: notes

This is my note.

- It can contain Markdown
- like this list

:::
