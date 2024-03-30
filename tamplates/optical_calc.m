%MV-CH650-90TM/TC - Gpixel GMAX3265 sensor - Resolution of 9344 ? 7000, and
%pixel size of 3.2 ?m ? 3.2 ?m. Binning Supports 1 ? 1, 1 ? 2, 1 ? 4, 2 ? 1, 2 ? 2, 2 ? 4, 4 ? 1, 4 ? 2, 4 ? 4
%ƒл€ бининга 2*2 имеем разрешение 4672 * 3500 пикселей, размер пиксел€
%3,2*2 = 6,4
clc
clear all;

%параметры матрицы
lenght_string_in_pixel = 640; %длина строки матрицы в пиксел€х (число пикселей на строку)
pixel_size = 12 / 1000000;%  
%pixel_size = 2.74 / 1000000% дл€ Sony Pregios S /// DZK38GX540-a DZK38GX541-a DZK38GX542-a /// MVL-KF5024M-25MP https://www.hikrobotics.com/en/machinevision/productdetail?id=5783&pageNumber=1&pageSize=500
%pixel_size = 3.2 / 1000000% Gpixel GMAX

%режим съемки
bihhig = 1


pixel_size = pixel_size*bihhig
lenght_string_in_pixel = lenght_string_in_pixel/bihhig
physical_dimention_matrix = lenght_string_in_pixel*pixel_size %физический размер матрицы (длина или ширина) в метрах, const дл€ матрицы
distance_of_object = 50; %дистанци€ (рассто€ние) до объекта, в м
focus = 0.013; %фокусное рассто€ние объектива в м

%1. –асчЄт размера пол€ зрени€ дл€ заданной дистанции 
H_field_of_vision = (physical_dimention_matrix*distance_of_object)/focus
resolution_on_distance__m_pix = H_field_of_vision/lenght_string_in_pixel % 2. –ассчЄт оптического разрешени€ в метрах на пиксель на основе рассчитанного размера пол€ зрени€ и данных о строке матрицы
resolution_on_distance__pix_m = lenght_string_in_pixel/H_field_of_vision % 2. –ассчЄт оптического разрешени€ в пиксел€х на метр на основе рассчитанного размера пол€ зрени€ и данных о строке матрицы 
FOV_angle_rad = 2*atan(physical_dimention_matrix/(2*focus))%угол пол€ зрени€ в радианах[ дл€ заданных фокусного рассто€ни€ и физического размера матрицы 
FOV_angle = rad2deg(FOV_angle_rad)%угол пол€ зрени€ в градусах дл€ заданных фокусного рассто€ни€ и физического размера матрицы 

% –асчет дистанции дл€ заданного пол€ зрени€ и фокусного рассто€ни€
focus = 0.013; %фокусное рассто€ние объектива в м
H_field_of_vision = lenght_string_in_pixel;
distance_of_object_calc = ((H_field_of_vision*focus)/physical_dimention_matrix);
resolution_on_distance__pix_m = lenght_string_in_pixel/H_field_of_vision % 2. –ассчЄт оптического разрешени€ в пиксел€х на метр на основе рассчитанного размера пол€ зрени€ и данных о строке матрицы 
mess = ['ƒл€ фокусного рассто€ни€ ', num2str(focus*1000), ' мм', ' рабоча€ дистанци€ равна ', ' = ', num2str(distance_of_object_calc), 'разрешение ', num2str(resolution_on_distance__pix_m), 'пикс/м'];
disp(mess)




distance_of_object = [0:1500];
H_field_of_vision = (physical_dimention_matrix*distance_of_object)/focus;
figure('Color','w')
plot(distance_of_object, H_field_of_vision, 'k', 'LineWidth',2)
title('Field of Vision vs. Distanse')
xlabel('Distanse, m') 
ylabel('FOV, m')
xlim([min(distance_of_object) max(distance_of_object)])
ylim([min(H_field_of_vision) max(H_field_of_vision)])
grid on


Resolution = H_field_of_vision/lenght_string_in_pixel;
figure('Color','w')
plot(H_field_of_vision, Resolution, 'k', 'LineWidth',2)
title('Optical Resolution vs. FOV')
xlabel('FOV, m') 
ylabel('Optical Resolution, m/pixel')
xlim([min(H_field_of_vision) max(H_field_of_vision)])
ylim([min(Resolution) max(Resolution)])
grid on


figure('Color','w')
plot(distance_of_object, Resolution, 'k', 'LineWidth',2)
title('Resolution vs. Distanse')
xlabel('Distanse, m') 
ylabel('Optical Resolution, m/pixel, m')
xlim([min(distance_of_object) max(distance_of_object)])
ylim([min(Resolution) max(Resolution)])
grid on