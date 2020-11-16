# equity-during-covid

This is the website for data visualization work in the class MIT 11.454 2020 fall.

* Author: Zihan Mei, Ryuhei Ichikura, Beko Liu
* 11.454 Big Data, Visualization, And Society
* Instructor: Sarah Williams, Yuan Lai
* TA: Yanchao Li, Lily Xie

## Frame and Modules Used

Python (`pandas` `numpy` `bokeh` `folium` `matplotlib`)

HTML/CSS/JavaScript (`Bootstrap`)

## Contents

1. Webpage source codes
2. Python Scripts analyzing datasets

## Specification

Used the grid system and flex system from [Bootstrap](https://getbootstrap.com/);

Used [markdown converter](https://github.com/saturn-drm/PythonMDtoHTML) by [saturn-drm](https://github.com/saturn-drm), based on Python [markdown](https://pypi.org/project/Markdown/) and [frontmatter](https://pypi.org/project/python-frontmatter/).

## Warning

### `href` Usage

When adding `href` in HTML/CSS/JavaScript, double check you are using:

```html
<link rel="stylesheet" type="text/css" href="css/vizdev-main-test.css" />
```

instead of:

```html
<link rel="stylesheet" type="text/css" href="/css/vizdev-main-test.css" />
```

**Reason:**

I'm using a independent project repo here other than sub-folder under my main site.
`href` as `/css/vizdev-main-test.css` will lead to `www.zmei.moe/css/vizdev-main-test.css` instead of `www.zmei.moe/equity-during-covid/css/vizdev-main-test.css` that we need.