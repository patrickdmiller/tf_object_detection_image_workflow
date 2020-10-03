pipeline for images
Step 1. Put images in incoming
Step 2. Run resize.sh (will resize to 1024)
Step 3. Use labelimg on the ./resized folder
Step 4. Run split.py to split the data. pick train percentage. defaults to 67/33