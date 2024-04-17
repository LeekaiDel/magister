import os
import numpy as np
import matplotlib.pyplot as plt


def getListBboxes(input_path: str, frame_count: int, plus_str: str = ""):
   # Собираем список всех txt файлов в директории
   # file_list_all=os.listdir(input_path)
   file_list = []
   # for i in file_list_all:
   for i in range(1, frame_count):
      # if i.endswith('.txt'):
      file_list.append( plus_str + ("%d" % i) + ".txt" )
      # print( "i = " + plus_str + ("%d" % i) + ".txt" ) 
   
   all_bbox = np.array([])
   # for i in range(len(file_list)):
   for i in file_list:
      path = (input_path + "/" + i) 
      # print("path = %s" % path)
      data = np.genfromtxt(path, delimiter=" ").astype('float')

      if data.shape[0] != 0:
         # data = np.append(data, i)
         all_bbox = np.append(all_bbox, data)

      elif data.shape[0] == 0:
         d = np.array([0.0, -1.0, -1.0, 0.0, 0.0])
         all_bbox = np.append(all_bbox, d)
         # print("Lost ID: %s" % i)      
   all_bbox = all_bbox.reshape((all_bbox.shape[0] // 5, 5)) #<object-class> <x_center> <y_center> <width> <height> <frame_ID>

   return all_bbox





if __name__ == "__main__":
   input_path = "../marks/plane_1"
   getListBboxes(input_path, 932)






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
