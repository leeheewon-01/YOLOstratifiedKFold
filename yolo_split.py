import os
import pandas as pd
from tqdm import tqdm
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold

img_dir_path = './COCO_val2017/images/' # image path
txt_dir_path = './COCO_val2017/labels/' # label path

def read_txt(img_path, txt_path, task='det'):
    files_data = []
    img_file_list = set(os.path.splitext(f)[0] for f in os.listdir(img_path) if f.endswith('.jpg'))
    txt_file_list = set(os.path.splitext(f)[0] for f in os.listdir(txt_path) if f.endswith('.txt'))

    for filename in tqdm(img_file_list):
        if filename not in txt_file_list:
            files_data.append([filename+'.jpg','-1',None,None,None,None])
        else:
            txt_file_path = os.path.join(txt_path, filename+'.txt')
            with open(txt_file_path, 'r') as f:
                lines = f.readlines()
                if not lines:
                    files_data.append([filename+'.jpg','-1',None,None,None,None])
                else:
                    for line in lines:
                        line = line.split()
                        if len(line) == 5:
                            if task == 'seg':
                                x_list = [float(line[i]) for i in range(1,len(line),2)]
                                y_list = [float(line[i]) for i in range(2,len(line),2)]
                                x_max,x_min,y_max,y_min = max(x_list),min(x_list),max(y_list),min(y_list)
                                
                                x_center,y_center,w,h = (x_max+x_min)/2,(y_max+y_min)/2,x_max-x_min,y_max-y_min
                                files_data.append([filename+'.jpg',line[0],x_center,y_center,w,h])
                            elif task == 'det':
                                files_data.append([filename+'.jpg',line[0],line[1],line[2],line[3],line[4]])

    df = pd.DataFrame(files_data, columns=['filename','class','x','y','w','h'])
    return df

data = read_txt(img_dir_path, txt_dir_path, task='det')

# One-hot encode 'class', scale 'w' and 'h' by 1000, drop unnecessary columns, and group by 'filename'
new_df = (pd.get_dummies(data, columns=['class'], prefix='class')
            .assign(w = lambda df: df['w'].astype(float) * 1000, h = lambda df: df['h'].astype(float) * 1000)
            .drop(['x', 'y'], axis=1)
            .groupby('filename', as_index=False)
            .sum())
# Compute 'cnt', 'avg_w', 'avg_h' and 'avg_ratio'
new_df = (new_df.assign(cnt = lambda df: df.filter(regex='^class_').sum(axis=1).clip(lower=1),
                        avg_w = lambda df: df['w'] / df['cnt'],
                        avg_h = lambda df: df['h'] / df['cnt'],
                        avg_ratio = lambda df: df['w'] / df['h'].replace(0, 1))
            .drop(['w', 'h'], axis=1))

mskf = MultilabelStratifiedKFold(n_splits=5, shuffle=True, random_state=42)

new_df['fold'] = -1
for i, (train_idx, val_idx) in enumerate(mskf.split(new_df['filename'], new_df.iloc[:, 1:])):
    new_df.loc[val_idx, 'fold'] = i
