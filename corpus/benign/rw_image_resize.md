---
name: resize-images
version: "1.0"
description: Resize all images in a directory to a specified maximum dimension.
tags: [images, resize, batch]
allowed-tools: [Read, Write, Bash]
---
## Overview
Resizes images in a directory to fit within a maximum width/height
while preserving aspect ratio.

## Usage
1. List all .jpg, .png, .webp files in the target directory.
2. For each image, resize to fit within the specified max dimension.
3. Save resized images to an `output/` subdirectory.
4. Report the number of images processed and any failures.

## Notes
Does not overwrite original files. Creates an `output/` subdirectory.
