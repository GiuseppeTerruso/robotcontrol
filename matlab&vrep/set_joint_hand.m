function set_joint_hand(han, q)
%
% SET_JOINT_HAND
% ----------------
%
% This function imposes a position on the joints of all the finger in the 
% v-rep model.
% For a correct operation, before calling this function it's necessary
% run the function CONNECT_VREP to establish the connection with the
% simulator enviorement.
%
% SYNTAX:
% set_joint_hand(han, q)
%
% INPUT:
% - han : is a matrix of 5x4 elements that contains the handlers of all the
%   fingers of the hand;
% - q : is a vector of 5x4 elements that contains the joint angles of all 
%   the fingers of the hand; they are expressed in degree
% 
% The structure of this two matrix is so defined
%           base  prox_ph  inter_ph     dist_ph 
%   thumb     |       |        |           |
%   index     |       |        |           |
%   middle    |       |        |           |
%   ring      |       |        |           |
%   pinky     |       |        |           |
%
% Programmed by : Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 29, 2014
 


global vrep clientID;
% test on the dimension of parameters
if((size(han,1)~= size(q,1)) || (size(han,2)~= size(q,2)))
    disp('the dimension of the two parameters must be the same \n');
    return;
end

% send the value to v-rep
opmode = vrep.simx_opmode_oneshot;
vrep.simxPauseCommunication(clientID,1);
for index1=1:size(han,1)
    for index2=1:size(han,2)
        vrep.simxSetJointPosition(clientID,han(index1,index2),q(index1,index2)*pi/180,opmode);
    end
end
vrep.simxPauseCommunication(clientID,0);
end