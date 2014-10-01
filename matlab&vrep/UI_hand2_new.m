function varargout = UI_hand2(varargin)
% UI_HAND2 MATLAB code for UI_hand2.fig
%      UI_HAND2, by itself, creates a new UI_HAND2 or raises the existing
%      singleton*.
%
%      H = UI_HAND2 returns the handle to a new UI_HAND2 or the handle to
%      the existing singleton*.
%
%      UI_HAND2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in UI_HAND2.M with the given input arguments.
%
%      UI_HAND2('Property','Value',...) creates a new UI_HAND2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before UI_hand2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to UI_hand2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help UI_hand2

% Last Modified by GUIDE v2.5 06-Jun-2014 23:24:58

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @UI_hand2_OpeningFcn, ...
                   'gui_OutputFcn',  @UI_hand2_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before UI_hand2 is made visible.
function UI_hand2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to UI_hand2 (see VARARGIN)

% Choose default command line output for UI_hand2
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% Define the variables
global ck_value text_error N q_control w_control time;
time = 0;
ck_value = 0;
text_error = handles.error_text;
N = 10;
q_control = zeros(5,4);
w_control = zeros(3,1);

% create the database
letter_database;
% UIWAIT makes UI_hand2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);

% --- Outputs from this function are returned to the command line.
function varargout = UI_hand2_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double
global word;
word = get(hObject,'String');

% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes during object creation, after setting all properties.
function error_text_CreateFcn(hObject, eventdata, handles)
% hObject    handle to error_text (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes on button press in "SHOW WORDS".
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global ck_value;
hand(ck_value)


% --- Executes on button press in "START COMUNICATION".
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global vrep clientID text_error s;

set(text_error,'String','open the comunication between matlab and v-rep');

% estabilize the connection with v-rep
connect_vrep(19997);

% recover all joint handle
joint_handle();

% start the simulation on v-rep environment
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot);

%s = serial('COM7','BaudRate',115200,'DataBits',8);
%s = serial('/dev/ttyUSB0','BaudRate',115200,'DataBits',8);
s = serial('/dev/ttyACM0','BaudRate',9600,'DataBits',8);
fopen(s);

% --- Executes on button press in "PAUSE COMUNICATION".
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% start the simulation on v-rep environment

global vrep clientID;

% pause the simulation
vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot);

% --- Executes on button press in "STOP COMUNICATION".
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global vrep clientID s;

% stop the simulation on v-rep environment
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait);

% close the connection with v-rep
vrep.simxFinish(clientID);
vrep.delete();
fclose(s);

% --- Executes on button press in "RESUME COMUNICATION".
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global vrep clientID;

% resume the simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot);

% --- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global ck_value;
ck_value = get(hObject,'Value');
% Hint: get(hObject,'Value') returns toggle state of checkbox1

% --- Executes on slider "TIME BETWEEN LETTERS".
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global time;
time = 3*get(hObject,'Value');

% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

% --- Executes on slider "PRECISION OF MOVEMENT".
function slider3_Callback(hObject, eventdata, handles)
% hObject    handle to slider3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global N;
N = 10 + 40*get(hObject,'Value');

% --- Executes during object creation, after setting all properties.
function slider3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
UI_control;
