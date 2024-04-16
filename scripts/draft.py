import os
import numpy as np

file_list_all=os.listdir("D:\\2024\\теплак_дрон\\img\\")
file_list = []
for i in file_list_all:
   if i.endswith('.txt'):
      file_list.append(i)

all_bbox = np.array([])
for i in range(len(file_list)):
    path = ("D:\\2024\\теплак_дрон\\img\\" + file_list[i]) 
    data = np.genfromtxt(path, delimiter=" ").astype('float')
    if data.shape[0] != 0:
       data = np.append(data, i)
       all_bbox = np.append(all_bbox, data)
 

  
all_bbox = all_bbox.reshape((all_bbox.shape[0]//6, 6))