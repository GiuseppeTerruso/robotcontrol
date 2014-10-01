

function joint_handle()
%
% JOINT_HANDLE
% ------------
% 
% This function recovers all the handles of the joints of the v-rep model.
% For a correct operation, before calling this function it's necessary to
% run the function CONNECT_VREP to estabilish the connection with the
% simulator enviorement.
%
% SYNTAX:
% joint_handle()
% 
% The results of the operation through this function are collected in four
% global variables:
% - finger : is a matrix of dimention 5x4 that contains the handlers of all 
%   finger's joints;
% - finger_rtn : is a matrix of dimention 5x4 that contains the error code
%   for the effort to recover the handlers; if the code is 0 no errors
%   occurs otherwise the position of the number indicates which joint
%   handler is not correct;
%   The structure of this two matrix is so defined
%           base  prox_ph  inter_ph    dist_ph 
%   thumb     |       |        |           |
%   index     |       |        |           |
%   middle    |       |        |           |
%   ring      |       |        |           |
%   pinky     |       |        |           |
% - wrist : is a column vector of three elements that contains the handlers 
%   of all wrist's joints;
% - wrist_rtn : is a column vector of three elements that contains the
%   error code for the attempt to recover the handlers; if the code is 0
%   no errors occurs otherwise the position of the number indicate which
%   joint handler is not correct;
%   The structure of this two vectors is so defined
%           joint   
%   joint_1   |
%   joint_2   |
%   joint_3   |
%
% Programmed by : Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 27, 2014
 

global vrep clientID finger finger_rtn wrist_rtn wrist text_error;
opmode_w = vrep.simx_opmode_oneshot_wait;
finger = zeros(5,4);
finger_rtn = zeros(5,4);

%% recovery the handler of the joints
% thumb
% [finger_rtn(1,1),finger(1,1)] = vrep.simxGetObjectHandle(clientID,'joint_attach_thumb', opmode_w);
% [finger_rtn(1,2),finger(1,2)] = vrep.simxGetObjectHandle(clientID,'joint_base_thumb',opmode_w);
% [finger_rtn(1,3),finger(1,3)] = vrep.simxGetObjectHandle(clientID,'joint_prox_ph_thumb',opmode_w);
% [finger_rtn(1,4),finger(1,4)] = vrep.simxGetObjectHandle(clientID,'joint_inter_ph_thumb',opmode_w);

% thumb
[finger(1,1),finger_rtn(1,1)] = vrep.simxGetObjectHandle(clientID,'joint_attach_thumb', opmode_w);
[finger(1,2),finger_rtn(1,2)] = vrep.simxGetObjectHandle(clientID,'joint_base_thumb',opmode_w);
[finger(1,3),finger_rtn(1,3)] = vrep.simxGetObjectHandle(clientID,'joint_prox_ph_thumb',opmode_w);
[finger(1,4),finger_rtn(1,4)] = vrep.simxGetObjectHandle(clientID,'joint_inter_ph_thumb',opmode_w);

% index
[finger_rtn(2,1),finger(2,1)] = vrep.simxGetObjectHandle(clientID,'joint_base_index',opmode_w);
[finger_rtn(2,2),finger(2,2)] = vrep.simxGetObjectHandle(clientID,'joint_prox_ph_index',opmode_w);
[finger_rtn(2,3),finger(2,3)] = vrep.simxGetObjectHandle(clientID,'joint_inter_ph_index',opmode_w);
[finger_rtn(2,4),finger(2,4)] = vrep.simxGetObjectHandle(clientID,'joint_dist_ph_index',opmode_w);
% middle
[finger_rtn(3,1),finger(3,1)] = vrep.simxGetObjectHandle(clientID,'joint_base_middle',opmode_w);
[finger_rtn(3,2),finger(3,2)] = vrep.simxGetObjectHandle(clientID,'joint_prox_ph_middle',opmode_w);
[finger_rtn(3,3),finger(3,3)] = vrep.simxGetObjectHandle(clientID,'joint_inter_ph_middle',opmode_w);
[finger_rtn(3,4),finger(3,4)] = vrep.simxGetObjectHandle(clientID,'joint_dist_ph_middle',opmode_w);
% ring
[finger_rtn(4,1),finger(4,1)] = vrep.simxGetObjectHandle(clientID,'joint_base_ring',opmode_w);
[finger_rtn(4,2),finger(4,2)] = vrep.simxGetObjectHandle(clientID,'joint_prox_ph_ring',opmode_w);
[finger_rtn(4,3),finger(4,3)] = vrep.simxGetObjectHandle(clientID,'joint_inter_ph_ring',opmode_w);
[finger_rtn(4,4),finger(4,4)] = vrep.simxGetObjectHandle(clientID,'joint_dist_ph_ring',opmode_w);
% pinky
[finger_rtn(5,1),finger(5,1)] = vrep.simxGetObjectHandle(clientID,'joint_base_pinky',opmode_w);
[finger_rtn(5,2),finger(5,2)] = vrep.simxGetObjectHandle(clientID,'joint_prox_ph_pinky',opmode_w);
[finger_rtn(5,3),finger(5,3)] = vrep.simxGetObjectHandle(clientID,'joint_inter_ph_pinky',opmode_w);
[finger_rtn(5,4),finger(5,4)] = vrep.simxGetObjectHandle(clientID,'joint_dist_ph_pinky',opmode_w);
% wrist
[wrist_rtn(1),wrist(1)] = vrep.simxGetObjectHandle(clientID,'joint_1',opmode_w);
[wrist_rtn(2),wrist(2)] = vrep.simxGetObjectHandle(clientID,'joint_2',opmode_w);
[wrist_rtn(3),wrist(3)] = vrep.simxGetObjectHandle(clientID,'joint_3',opmode_w);

%% verify
n = [1 1 1 1 1]*finger_rtn*[1 1 1 1]' + wrist_rtn*[1 1 1]';
if ( n == 0)
    set(text_error,'String','all handles are acquired correctly');
else
    %set(text_error,'String','there are some handles that are not acquired correctly');
    finger_rtn
    wrist_rtn
end
    
end