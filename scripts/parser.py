import os
import numpy as np
import matplotlib.pyplot as plt

input_path = "../marks/plane_1"

def getListBboxes(input_path: str):
   # Собираем список всех txt файлов в директории
   file_list_all=os.listdir(input_path)
   file_list = []
   for i in file_list_all:
      if i.endswith('.txt'):
         file_list.append(i)

   # 
   all_bbox = np.array([])
   for i in range(len(file_list)):
      path = (input_path + "/" + file_list[i]) 
      data = np.genfromtxt(path, delimiter=" ").astype('float')

      # print("Data %d: " % i, data)
      if data.shape[0] != 0:
         data = np.append(data, i)
         all_bbox = np.append(all_bbox, data)

      elif data.shape[0] == 0:
         d = np.array([0.0, -1.0, -1.0, -1.0, -1.0, float(i)])
         all_bbox = np.append(all_bbox, d)
         print("Lost ID: %d" % i)

   all_bbox = all_bbox.reshape((all_bbox.shape[0]//6, 6)) #<object-class> <x_center> <y_center> <width> <height> <frame_ID>

   print("Count files: %d" % len(file_list))
   print(all_bbox.shape) 

getListBboxes(input_path)

  

# all_x_center = all_bbox[:,1]
# all_y_center = all_bbox[:,2]
# all_width = all_bbox[:,3]
# all_height = all_bbox[:,4]
# all_frame_ID = all_bbox[:,5]

# full_width_frame = 640
# full_height_frame = 512

# all_width_in_pixel = full_width_frame * all_width

# all_height_in_pixel = full_height_frame * all_height

# fig = plt.figure('all_center_drone_position_in_pixels')
# plt.plot(all_x_center*full_width_frame, all_y_center*full_height_frame, 'o')




# plt.show()
