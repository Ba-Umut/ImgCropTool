# ImgCropTool

## Overview
ImgCropTool is a Python tool that allows you to manually select a region in large images, crop it, and save it in a fixed size (default: 640x640). The selection is done via a simple OpenCV-based interface.

## Features
- Select and crop specific regions from large images.
- Automatically adjusts selection to a square.
- Supports keyboard navigation for fine-tuning selections.
- Saves cropped images in a specified output directory.

## Usage

  Place your images in the input folder.
  Run the script:

  python cropper.py

  Select a region by clicking and dragging with the mouse.
  Adjust the selection using arrow keys if needed.
  Press 's' to save, 'q' to quit, 'space' to move to the next image, 'b' to go back.

## Keyboard Controls

  Mouse Drag → Select a region.                                                           
  Arrow Keys → Adjust the selection.                                                 
  's' → Save the selected region.                                      
  'space' → Move to the next image.                                      
  'b' → Go back to the previous image.                                        
  'q' → Quit the application.
