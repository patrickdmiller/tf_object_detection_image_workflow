import sys, getopt, glob,os, shutil, math
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

opts, args = getopt.getopt(sys.argv[1:], "hs", ["split="])
split = 67
for opt, arg in opts:
    if opt == '-h':
        print("split.py -s <splitpercentage as whole number> ")
        sys.exit()
    elif opt in ("s","split"):
        split = float(arg)

if(not opts and sys.argv[1:]):
    print("no opt , attempting to parse argv")
    split = float(sys.argv[1])

if(split <= 0 or split > 100):
    print("invalid split value")
    exit()

#check test and training directories
imgs = glob.glob('./resized/*.jpg')
xmls = glob.glob('./resized/*.xml')
xmls_set = set(xmls[i] for i in range(0,len(xmls)))
train = glob.glob('./train/*.jpg')
test = glob.glob('./test/*.jpg')
if train or test:
    print("train and test not empty. exiting")
    exit()


split = math.floor(len(imgs) * (split/100))
print("there are ", len(imgs)," images")
print("splitting training", split, " and ", ((len(imgs))-split))


for img in imgs:
    if img.replace('.jpg','.xml') not in xmls_set:
        print("missing xml for ", img)
        exit()


train = imgs.copy()
test = []
#cp files over
for i in range(0,(len(imgs)-split)):

    index = np.random.randint(len(train))
    test.append(train[index]) #string does real copy
    del train[index]

for c,i in enumerate(train):
    # print(c,i)
    shutil.copyfile(i, i.replace('/resized','/train'))
    shutil.copyfile(i, i.replace('/resized','/train').replace('.jpg','.xml'))

for c,i in enumerate(test):
    # print(c,i)
    shutil.copyfile(i, i.replace('/resized','/test'))
    shutil.copyfile(i, i.replace('/resized','/test').replace('.jpg','.xml'))

#copy all the test and train 

# credit to https://github.com/TannerGilbert
def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

for folder in ['train', 'test']:
    image_path = os.path.join(os.getcwd(), ('images/' + folder))
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(('images/'+folder+'_labels.csv'), index=None)