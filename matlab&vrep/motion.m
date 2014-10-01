function [q_temp, w_temp] = motion(q_fin, w_fin, q_act, w_act, N)
% 
% MOTION
% -----------
% It is a function that allows hands to move into v-rep simulation.
%
% SYNTAX : 
% [q_temp, w_temp]= motion(q_fin, w_fin, q_act, w_act, N)   
% 
% INPUT:
% - q_fin: it is a matrix 5x4 that contains the configuration of all
%          hand joints that we want to set
% - w_fin: it is a matrix 3x1 that contains the configuration of all wrist
%          joints that we want to set
% - q_act: it is a matrix 5x4 that contains the configuration of all
%          hand joints in the actual position
% - w_fin: it is a matrix 3x1 that contains the configuration of all wrist
%          joints in the actual position
% - N: is an integer number that indicatas the steps to perform between the
%      actual and next position
%
% OUTPUT:
% - q_temp: it is a matrix 5x4 that contains the configuration of all hand
%          joints in a particular time instant
% - w_temp: it is a matrix 3x1 that contains the configuration of all wrist
%          joints in a particular time instant
% 
% Programmed by :  Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 14, 2014
%
global finger wrist

delta = 1/N;
q_temp = q_act;
w_temp = w_act;
for index = 1:N
   q_temp = q_temp + delta*(q_fin - q_act);
   w_temp = w_temp + delta*(w_fin - w_act);
   set_joint_hand(finger, q_temp);
   set_joint_wrist(wrist, w_temp);
   pause(0.1);
end

end