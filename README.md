## YOLOstratifiedKFold
Implementation of paper - [Improving the performance of object detection by preserving label distribution](no)

## Requirements
- pandas
- iterative-stratification
- pillow

## How to use
You can insert the path to the folder with the image and label files in the 7th and 8th lines.
```
img_dir_path = './COCO_val2017/images/' # image path
txt_dir_path = './COCO_val2017/labels/' # label path
```

Then, put the type of dataset into the task variable in the read_txt on the 41st line.
```
- 'det' : object detection YOLO format
- 'seg' : instance segmentation YOLO format
```

At the end of the code, you can append additional lines to produce the desired output, such as saving an image and its corresponding label file, or generating a text file with a list of images and labels.

## Experiments
### class distribution error(using MAE(unit=1e-7))
| **Dataset**          | **Entropy** | **Train KFold**        | **Train Ours**         | **Validation KFold**          | **Validation Ours**           |
|----------------------|-------------|------------------------|------------------------|-------------------------------|-------------------------------|
| COCO val2017         | 3.39        | **165±127**            | 168±128                | **1466.5±1126.5**             | 1506.5±1144.5                 |
| Pascal VOC 2012 val  | 2.31        | **591.5±408.5**        | 618±391                | 5299±3712                     | **5279±3330**                 |
| PlantDoc             | 3.17        | 463.5±321.5            | **301.5±255.5**        | 4097±2803                     | **2614.5±2205.5**             |
| Website screenshot   | 1.61        | 4864±3880              | **4092.5±3428.5**      | 42897±34009                   | **35538.5±29582.5**           |
| Aquarium             | 1.42        | 5172.5±4075.5          | **3943±2202**          | 44031.5±33452.5               | **38541±22795**               |
| BCCD                 | 0.53        | 1973.5±1417.5          | **1224±862**           | 17683.5±12738.5               | **11459±8186**                |
