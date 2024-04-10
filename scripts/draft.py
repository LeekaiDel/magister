import os
import numpy as np

file_list_all=os.listdir("/home/user/Documents/polarization/new_project_11_2021/main/my_edit_code/data/")
file_list = []
for i in file_list_all:
   if i.endswith('.txt'):
      file_list.append(i)

all_bbox = np.array([])
for i in range(len(file_list)):
    path = ("/home/user/Documents/polarization/new_project_11_2021/main/my_edit_code/data/" + file_list[i]) 
    data = np.genfromtxt(path, delimiter=" ").as_type('int')# там инт или флоат?
    all_bbox = np.append(all_bbox, data)