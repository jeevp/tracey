## Overview

[Tracey](https://tracey.jeev.me) is an online tool to transform raster images into SVG line art. To get started, simply upload a PNG or JPG image. Then, play around with the settings until you're ready to download the final product.

Made by [Jeev Prayaga](https://jeev.me) using Flask, the OpenCV Python library, Vue and Vercel. Inspired by [this project](https://github.com/johnafish/sketchbook) by John Fish and [this utility function](https://gist.github.com/steveruizok/ced3e793c552f348e1bcd655fafde910) by Steve Ruiz.

> [!NOTE]
> Tracey currently works best with small/medium PNG and JPEG files (e.g. portraits)

## How it works

1. Convert raster image to grayscale
2. Apply Gaussian blur to reduce noise
3. Apply threshold function to divide image into foreground and background
4. Use Canny edge detection to find areas where brightness changes sharply
5. Use contour mapping to convert edges into curve
6. Smooth contours to reduce the number of points in each curve
7. Apply Bézier curve splining to combine multiple curves into single paths
8. Export as SVG

## Installation

```bash
python3 -m venv venv # create a virtual environment
source venv/bin/activate # activate the virtual environment
flask --app api/index run # run the app at http://127.0.0.1:5000
```
