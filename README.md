# pipeline for images before object detection with tf

## Step 1. 
Put images in incoming

## Step 2. 
Run resize.sh (will resize to 1024) and move them to resized/

## Step 3. 
Use labelimg on the ./resized folder. The result will be labled images (.jpg and .xml)

## Step 4. 
Run split.py to split the data and build csv. pick train percentage. defaults to 67/33

```python split.py 75``` 

The above will put 75% of the files into training

## Step 5. 
convert to TFRecord

edit generate_tfrecord.py to your labels (replace aaa,bbb,ccc etc) [credit https://github.com/TannerGilbert]

## Step 6. 
edit lablemap.pbtxt for your labels
