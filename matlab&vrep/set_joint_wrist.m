function set_joint_wrist(han, w)
%
% SET_JOINT_WRIST
% ----------------
%
% This function imposes a position on the joints of the wrist in the v_rep  
% model.
% For a correct operation, before calling this function it's necessary
% run the function CONNECT_VREP to establish the connection with the
% simulator enviorement.
%
% SYNTAX:
% set_joint_wrist(han, w)
%
% INPUT:
% - han : is a column vector of three elements that contains the handlers
%   of the wrist of the hand;
% - w : is a column vector of three elements that contains the joint angles
%   of the wrist of the hand; they are expressed in degree
% 
% The structure of this two vector is so defined
%           joint   
%   JOINT_1    |
%   JOINT_2    |
%   JOINT_3    |
%
% Programmed by : Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 27, 2014

global vrep clientID;
% test on the dimension of parameters
if (length(han) ~= 3 || length(han) ~= length(w))
    disp('the dimension of the two parameters must be 3x1 \n');
    return;
end


% send the value to v-rep
opmode = vrep.simx_opmode_oneshot;
vrep.simxPauseCommunication(clientID,1);
for index=1:length(w)
    vrep.simxSetJointPosition(clientID, han(index), w(index)*pi/180, opmode);
end
vrep.simxPauseCommunication(clientID,0);

end
