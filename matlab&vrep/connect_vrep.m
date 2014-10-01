function connect_vrep(port)
%
% CONNECT_VREP
% ------------
%
% This function estabilishes the connection between matlab and the remoteAPI
% server to comunicate with the simulator v-rep.
% 
% SYNTAX:
% connect_vrep(port)
%
% INPUT:
% port : specifies the server's port to estabilish the comunication
%
% Programmed by : Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena 
% LastEditDate : may 29, 2014

%% FUNCTION
global vrep clientID;
vrep=remApi('remoteApi','extApi.h');
% vrep=remApi('remoteApi'); % using the header (requires a compiler)
vrep.simxFinish(-1); % just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',port,true,true,5000,5);

%% test if the connection is ok
if (clientID>-1)
	disp('Connected to remote API server');
else
	disp('Failed connecting to remote API server');
    vrep.simxFinish(clientID); % close the line if still open
    vrep.delete(); % call the destructor!
end

end