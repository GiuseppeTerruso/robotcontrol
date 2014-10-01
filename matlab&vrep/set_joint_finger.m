
function set_joint_finger(han, q)
%
% SET_JOINT_FINGER
% ----------------
%
% This function imposes a position for the joints of the specified finger in 
% the v-rep model.
% For a correct operation, before the call of this function it's necessary to 
% run the function CONNECT_VREP to establish the connection with the
% simulator enviorement.
%
% SYNTAX:
% set_joint_finger(han, q)
%
% INPUT:
% - han : is a row vector of four elements that contains the handlers of
%   the finger that you want to adjust;
% - q : is a row vector of four elements that contains the joint angles of
%   the finger that you want set; they are expressed in degree
% 
% The structure of this two matrix is so defined
%             base  prox_ph  inter_ph  dist_ph  
%   finger      |       |        |        |
%
% Programmed by : Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 29, 2014
 

global vrep clientID;
% test on the dimension of parameters
if(length(han) ~= 4 || length(han) ~= length(q))
    disp('the length of the two parameters must be equal 4 \n');
    return;
end

% send the value to v-rep
opmode = vrep.simx_opmode_oneshot;
vrep.simxPauseCommunication(clientID,1);
for index=1:length(han);
    vrep.simxSetJointPosition(clientID,han(index),q(index)*pi/180,opmode);
end
vrep.simxPauseCommunication(clientID,0);
end