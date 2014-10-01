%% this file contains the database of the joints' configurations
global letters j_conf j_wrist alphabet coordinates_image no_letter;
letters = ['a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'o'...
    'p' 'q' 'r' 's' 't' 'u' 'v' 'w' 'x' 'y' 'z'];

%% import the image of all letters
alphabet = importdata('alphabet.jpg');
coordinates_image = zeros(2,length(letters));
% a
coordinates_image(:,1) = [190; 66];
% b
coordinates_image(:,2) = [190; 191];
% c
coordinates_image(:,3) = [190; 317];
% d
coordinates_image(:,4) = [314; 66];
% e
coordinates_image(:,5) = [314; 191];
% f
coordinates_image(:,6) = [314; 317];
% g
coordinates_image(:,7) = [438; 66];
% h
coordinates_image(:,8) = [438; 191];
% i
coordinates_image(:,9) = [438; 317];
% j
coordinates_image(:,10) = [563; 66];
% k
coordinates_image(:,11) = [563; 191];
% l
coordinates_image(:,12) = [563; 317];
% m
coordinates_image(:,13) = [66; 484];
% n
coordinates_image(:,14) = [66; 609];
% o
coordinates_image(:,15) = [66; 735];
% p
coordinates_image(:,16) = [190; 484];
% q
coordinates_image(:,17) = [190; 609];
% r
coordinates_image(:,18) = [190; 735];
% s
coordinates_image(:,19) = [314; 484];
% t
coordinates_image(:,20) = [314; 609];
% u
coordinates_image(:,21) = [314; 735];
% v
coordinates_image(:,22) = [438; 484];
% w
coordinates_image(:,23) = [438; 609];
% x
coordinates_image(:,24) = [438; 735];
% y
coordinates_image(:,25) = [563; 484];
% z
coordinates_image(:,26) = [563; 609];
% ' '
no_letter = [563; 735];

%% fingers database
j_conf = zeros(5,4,length(letters));
% a 
j_conf(:,:,1) = [40 0 0 0; 0 80 100 50; 0 80 100 50; 0 80 100 50; 0 80 100 50];
% b
j_conf(:,:,2) = [70 0 45 45; 0 0 0 0; 0 0 0 0; 0 0 0 0; 0 0 0 0];
% c
j_conf(:,:,3) = [20 30 10 5; 0 30 45 20; 0 30 45 20; 0 30 45 20; 0 45 10 5];
% d
j_conf(:,:,4) = [50 30 50 25; 0 0 0 0; 0 70 55 30; 0 70 55 30; 0 70 55 30];
% e
j_conf(:,:,5) = [50 30 60 45; 0 15 100 50; 0 15 100 50; 0 15 100 50; 0 15 100 50];
% f
j_conf(:,:,6) = [20 30 50 25;  10 70 55 30; 10 10 20 10; 0 10 10 5; -30 0 0 0];
% g
j_conf(:,:,7) = [55 0 20 -15; 0 10 0 0; 0 30 100 50; 0 30 100 50; 0 30 100 50];
% h
j_conf(:,:,8) = [55 0 20 15; 0 10 0 0; 0 10 0 0; 0 30 100 50; 0 30 100 50];
% i 
j_conf(:,:,9) = [45 10 0 30; 0 60 80 40; 0 90 90 0; 0 90 90 0; 10 30 0 0];
% j 
j_conf(:,:,10) = [45 10 0 30; 0 60 80 40; 0 90 90 0; 0 90 90 0; 10 30 0 0];
% k
j_conf(:,:,11) = [55 0 45 -20; 0 0 0 0; -10 0 0 0; -10 90 90 0; -10 90 90 0];
% l
j_conf(:,:,12) = [0 30 5 0; 10 5 0 0; 0 90 80 40; 0 90 80 40; 0 90 80 40];
% m
j_conf(:,:,13) = [50 10 30 45; 0 80 30 15; 0 80 30 15; 0 80 30 15; 0 80 80 40];
% n
j_conf(:,:,14) = [50 10 30 45; 0 80 30 15; 0 80 30 15; 0 80 80 40; 0 80 80 40];
% o
j_conf(:,:,15) = [50 40 50 25; 0 70 55 30; 0 70 55 30; 0 70 55 30; 0 70 55 30];
% p
j_conf(:,:,16) = [40 10 10 -15; 0 10 0 0; 0 90 10 5; 0 90 90 0; 0 90 90 0];
% q
j_conf(:,:,17) = [50 40 10 -15; 0 80 10 5; 0 90 90 0; 0 90 90 0; 0 90 90 0];
% r 
j_conf(:,:,18) = [90 50 30 20; -20 30 0 0; -5 0 0 0; -10 90 90 0; -10 90 90 0];
% s
j_conf(:,:,19) = [55 35 45 50; 0 80 100 50; 0 80 100 50; 0 80 100 50; 0 80 100 50];
% t 
j_conf(:,:,20) = [75 0 20 0; 20 60 90 45; 0 90 80 40; 0 90 80 40; 0 90 80 40];
% u 
j_conf(:,:,21) = [90 50 30 20; -5 0 0 0; 0 0 0 0; -10 90 90 0; -10 90 90 0];
% v 
j_conf(:,:,22) = [90 50 30 20; 5 0 0 0; -10 0 0 0; -10 90 90 0; -10 90 90 0];
% w 
j_conf(:,:,23) = [100 60 40 10; 10 0 0 0; 0 0 0 0; -5 15 0 0; -20 90 90 0];
% x
j_conf(:,:,24) = [70 35 30 30; 0 30 45 20; 0 80 100 50; 0 80 100 50; 0 80 100 50];
% y
j_conf(:,:,25) = [0 30 5 0; 0 90 80 40; 0 90 80 40; 0 90 80 40; -10 5 0 0];
% z
j_conf(:,:,26) = [40 10 10 -15; 0 10 0 0; 0 90 90 0; 0 90 90 0; 0 90 90 0];

%% wrist database
% N is the number of flying points to realize the motion of the letters 
%j(1), x(1) and z(3)
N = 5;
j_wrist = zeros(3,length(letters)+N);
%a
j_wrist(:,1) = [180; 0; 0];
%b
j_wrist(:,2) = [180;0 ; 0];
%c
j_wrist(:,3) = [110; 30; 0];
%d
j_wrist(:,4) = [190; 0; 0];
%e
j_wrist(:,5) = [180; 0; 0];
%f
j_wrist(:,6) = [180; 0; 0];
%g
j_wrist(:,7) = [90; 70; 90];
%h
j_wrist(:,8) = [90; 70; 90];
%i
j_wrist(:,9) = [180; 0; 0];
%j
j_wrist(:,10) = [180; 0; 0];
%k
j_wrist(:,11) = [180; 0; 0];
%l
j_wrist(:,12) = [180; 0; 0];
%m
j_wrist(:,13) = [180; 80; 0];
%n
j_wrist(:,14) = [180; 80; 0];
%o
j_wrist(:,15) = [90; 0; 0];
%p
j_wrist(:,16) = [225; 80; 0];
%q
j_wrist(:,17) = [215; 80; 0];
%r
j_wrist(:,18) = [180; 0; 0];
%s
j_wrist(:,19) = [180; 0; 0];
%t
j_wrist(:,20) = [180; 0; 0];
%u
j_wrist(:,21) = [180; 0; 0];
%v
j_wrist(:,22) = [180; 0; 0];
%w
j_wrist(:,23) = [180; 0; 0];
%x
j_wrist(:,24) = [100; 0; 0];
%y
j_wrist(:,25) = [90; -15; -90];
%z
j_wrist(:,26) = [180; 80; 0];
%j_flying
j_wrist(:,27) = [170; 70; 90];
%x_flying
j_wrist(:,28) = [150; 70; 90];
%z_flying_1
j_wrist(:,29) = [225; 80; 0];
%z_flying_2
j_wrist(:,30) = [180; 110; 0];
%z_flying_3
j_wrist(:,31) = [225; 110; 0];




