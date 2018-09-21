---
title: "Part 1.1 Car Nd Detect Road Lanes Using Computer Vision and Python 3"
date: 2017-02-24T11:46:09+12:00
draft: false
categories: ["Tutorial"]
tags: ["Python-3", "Machine-Learning", "Computer-Vision"]
description: "Road lane detection using computer vision in Python 3."
relImage: ""
---

This blog is few part series in the field of Computer Vision and Deep Learning. In this blog, we will try to understand the following questions:

1. What is Computer Vision?
2. Why use Computer Vision?
3. What are the languages out there that do Computer Vision?
4. A simple example of image manipulation.

## 1. What is Computer Vision?

According to Wikipedia

> Computer vision is an interdisciplinary field that deals with how computers can be made to gain high-level understanding from digital images or videos. From the perspective of engineering, it seeks to automate tasks that the human visual system can do.
In general, Computer Vision (CV) is the eyes for machines to interpret the surroundings. There are various implementations for CV, some but not limited to are:

Robotics
Face Recognition
Image Restoration
Medical Image Analysis
Autonomous Vehicles

## 2. Why use Computer Vision?

As described earlier CV is used as eyes for the machines to interpret its surroundings. Humans are limited with two eyes, but these limitations do not apply to machines, which means they can have n number of cameras attached to it and all these cameras could be used at the same time.

Humans process vision differently when compared to computers, we tend to extract more semantically meaningful features such as shapes, edges and so on, whereas computers have to process data that is fairly detectable but with less meaningful information such as colour, textures etc. (Zhang, 2010).

Deep learning could be able to help us detecting more meaningful features, more on this soon.

## 3. What are the languages out there that do Computer Vision?

Most popular Computer Vision library is the OpenCV, written in C++ it also has a Python warper. Other well-known libraries are:

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;margin:0px auto;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
@media screen and (max-width: 767px) {.tg {width: auto !important;}.tg col {width: auto !important;}.tg-wrap {overflow-x: auto;-webkit-overflow-scrolling: touch;margin: auto 0px;}}</style>
<div class="tg-wrap"><table class="tg">
  <tr>
    <th class="tg-031e">Python</th>
    <th class="tg-031e">C++</th>
    <th class="tg-031e">Java</th>
  </tr>
  <tr>
    <td class="tg-031e">SimpleCV</td>
    <td class="tg-031e">CVIPtools</td>
    <td class="tg-031e">BoofCV</td>
  </tr>
  <tr>
    <td class="tg-031e">Scilab Image Processing</td>
    <td class="tg-031e">OpenVX</td>
    <td class="tg-031e">ImageJ</td>
  </tr>
  <tr>
    <td class="tg-031e"></td>
    <td class="tg-031e">VIGRA (with Python wrapper)</td>
    <td class="tg-031e"></td>
  </tr>
</table></div>

## 4. A simple example of image manipulation

In this example, we will use [matplotlib](http://matplotlib.org/) and [NumPy](http://www.numpy.org/) to get the bright colours in an image.

```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys

try:
    image = mpimg.imread('test.jpg')  # Reading a image file.
except FileNotFoundError as e:
    print(e)
    sys.exit(1)
print('This image is: {}, with dimensions: {}'.format(type(image), image.shape))

# Making a copy of the image.
color_select = np.copy(image)

red_threshold = 200
green_threshold = 200
blue_threshold = 200
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

# Select any pixels less than given threshold.
thresholds = (image[:, :, 0] < rgb_threshold[0]) | (image[:, :, 1] < rgb_threshold[1]) | (image[:, :, 2] < rgb_threshold[2])
color_select[thresholds] = [0, 0, 0]

# Show image.
f = plt.figure()

f.add_subplot(1, 2, 1)
plt.imshow(image)
plt.title("Original image")

f.add_subplot(1, 2, 2)
plt.imshow(color_select)
plt.title("Gradient image")

plt.show()

```

Output for the example Python code.

## What's next?

In the next part, we will look at how to detect the road lanes using OpenCV and Python; like the one below.

Lane detection using OpenCV:

{{< youtube lgoS-6x4tZ8 >}}

Filtering the image to obtain a masked Hough transformed image:

{{< figure src="/img/blog/edge_detection.png" title="Stages of line detection." >}}
