%MV-CH650-90TM/TC - Gpixel GMAX3265 sensor - Resolution of 9344 ? 7000, and
%pixel size of 3.2 ?m ? 3.2 ?m. Binning Supports 1 ? 1, 1 ? 2, 1 ? 4, 2 ? 1, 2 ? 2, 2 ? 4, 4 ? 1, 4 ? 2, 4 ? 4
%��� ������� 2*2 ����� ���������� 4672 * 3500 ��������, ������ �������
%3,2*2 = 6,4
clc
clear all;

%��������� �������
lenght_string_in_pixel = 640; %����� ������ ������� � �������� (����� �������� �� ������)
pixel_size = 12 / 1000000;%  
%pixel_size = 2.74 / 1000000% ��� Sony Pregios S /// DZK38GX540-a DZK38GX541-a DZK38GX542-a /// MVL-KF5024M-25MP https://www.hikrobotics.com/en/machinevision/productdetail?id=5783&pageNumber=1&pageSize=500
%pixel_size = 3.2 / 1000000% Gpixel GMAX

%����� ������
bihhig = 1


pixel_size = pixel_size*bihhig
lenght_string_in_pixel = lenght_string_in_pixel/bihhig
physical_dimention_matrix = lenght_string_in_pixel*pixel_size %���������� ������ ������� (����� ��� ������) � ������, const ��� �������
distance_of_object = 50; %��������� (����������) �� �������, � �
focus = 0.013; %�������� ���������� ��������� � �

%1. ������ ������� ���� ������ ��� �������� ��������� 
H_field_of_vision = (physical_dimention_matrix*distance_of_object)/focus
resolution_on_distance__m_pix = H_field_of_vision/lenght_string_in_pixel % 2. ������� ����������� ���������� � ������ �� ������� �� ������ ������������� ������� ���� ������ � ������ � ������ �������
resolution_on_distance__pix_m = lenght_string_in_pixel/H_field_of_vision % 2. ������� ����������� ���������� � �������� �� ���� �� ������ ������������� ������� ���� ������ � ������ � ������ ������� 
FOV_angle_rad = 2*atan(physical_dimention_matrix/(2*focus))%���� ���� ������ � ��������[ ��� �������� ��������� ���������� � ����������� ������� ������� 
FOV_angle = rad2deg(FOV_angle_rad)%���� ���� ������ � �������� ��� �������� ��������� ���������� � ����������� ������� ������� 

% ������ ��������� ��� ��������� ���� ������ � ��������� ����������
focus = 0.013; %�������� ���������� ��������� � �
H_field_of_vision = lenght_string_in_pixel;
distance_of_object_calc = ((H_field_of_vision*focus)/physical_dimention_matrix);
resolution_on_distance__pix_m = lenght_string_in_pixel/H_field_of_vision % 2. ������� ����������� ���������� � �������� �� ���� �� ������ ������������� ������� ���� ������ � ������ � ������ ������� 
mess = ['��� ��������� ���������� ', num2str(focus*1000), ' ��', ' ������� ��������� ����� ', ' = ', num2str(distance_of_object_calc), '���������� ', num2str(resolution_on_distance__pix_m), '����/�'];
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