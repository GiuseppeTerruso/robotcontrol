function hand(step_motion, s)

%
% HAND
% ------------
% This function make differents steps. It takes one letter at time from a
% word written. For each letter finds the relative informations thanks to the  
% function find_letter. After this it calls motion function that provvides
% for the motion in v-rep.
%
% SYNTAX:
% hand(step_motion)
% 
% INPUT:
% - step_motion: is a variable that establishes if the movement of the hand
%                has to be continuos or not
%          


    % global variables
    global word no_letter time N;

    % compute some movements
    q_temp = zeros(5,4);
    w_temp = zeros(3,1);
    for index_l = 1:length(word)
        if (word(index_l) == ' ')
            pause(time);
            show_letter(no_letter);
            [q_temp,w_temp] = motion(zeros(5,4), zeros(3,1), q_temp, w_temp, N);
            perform_sign('REST', s);
        else
            [q, w, coord, found] = find_letter(word(index_l));
            if (found)
                show_letter(coord);
                % execute letter
                [q_temp,w_temp] = motion(q, w(:,1), q_temp, w_temp, N);
                if (size(w,2) > 1)
                    for index_2 = 2:size(w,2)
                        [q_temp,w_temp] = motion(q, w(:,index_2), q_temp, w_temp, N);
                    end
                end

                perform_sign(upper(word(index_l)), s);

                pause(time);
                % open hand
                if (not(step_motion))
                    show_letter(no_letter);
                    [q_temp,w_temp] = motion(zeros(5,4), zeros(3,1), q_temp, w_temp, N);
                end
            else
                show_letter(no_letter);
                motion(zeros(5,4), zeros(3,1), q_temp, w_temp, N);
                perform_sign('REST', s);
                return;
            end
        end 
    end
    
    show_letter(no_letter);
    motion(zeros(5,4), zeros(3,1), q_temp, w_temp, N);
end


function send_commands(cmds, s)

    cmds2send = '';
    [m,n] = size(cmds);
    %for i = 1:m
    for j = 1:n
        cmds2send = strcat(cmds2send, char(cmds(j)));
    end
    %end
    fwrite(s, cmds2send);
end


function set_finger_position(s,  finger, pos)
    
    global joint_set

	cmds = [0 0 0];
    cmds(1) = 242;
    tmp = strmatch(finger, joint_set);
    cmds(2) = tmp(1) - 1;
    cmds(3) = pos;
    send_commands(cmds, s);
end


function perform_sign(msg, s)
    
    global joint_set

    joint_set = {'thumb', 'index', 'middle', 'ring', 'little', 'thumb_a', 'index_a', 'middle_a', 'wrist'};
    
    switch msg
    case 'a'
        list = ['little', 'ring', 'middle', 'index', 'thumb'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end

    case 'b'
        set_finger_position(s, 'thumb_a', 180)
        set_finger_position(s, 'thumb', 0)
        set_finger_position(s, 'wrist', 150)

    case 'c'
        set_finger_position(s, 'thumb', 90)
        set_finger_position(s, 'index', 65)
        set_finger_position(s, 'middle', 75)
        set_finger_position(s, 'middle_a', 20)
        set_finger_position(s, 'ring', 80)
        set_finger_position(s, 'little', 165)

    case 'd'
        list = ['little', 'ring', 'middle'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
        set_finger_position(s, 'index_a', 180)
        set_finger_position(s, 'thumb', 90)

    case 'f'
        set_finger_position(s, 'index', 40)
        set_finger_position(s, 'thumb_a', 100)
        set_finger_position(s, 'thumb', 55)

    case 'i'
        list = ['ring', 'middle', 'index', 'thumb'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
            
    case 'l'
        list = ['little', 'ring', 'middle', 'thumb_a'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end  

    case 'o'
        set_finger_position(s, 'little', 130)
        set_finger_position(s, 'ring', 60)
        set_finger_position(s, 'middle', 40)
        set_finger_position(s, 'index', 20)
        set_finger_position(s, 'thumb', 80)
        set_finger_position(s, 'thumb_a', 180)

    case 'r'
        set_finger_position(s, 'index', 180)
        set_finger_position(s, 'index_a', 50)
        time.sleep(1)
        set_finger_position(s, 'middle_a', 180)
        set_finger_position(s, 'middle', 130)
        time.sleep(1)
        set_finger_position(s, 'index', 160)     
        list = ['little', 'ring', 'thumb'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
        % da verificare -> ci va una transizione per rest?!

    case 's'
        list = ['little', 'ring', 'middle', 'index', 'thumb_a'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end

	case 'u'
        list = ['little', 'ring', 'thumb', 'index_a', 'thumb_a'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
        set_finger_position(s, 'middle_a', 75)
			
    case 'v'
        list = ['little', 'ring', 'thumb', 'middle_a', 'thumb_a'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
        set_finger_position(s, 'index_a', 180)

    case 'w'         
        list = ['little', 'thumb', 'thumb_a'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
        set_finger_position(s, 'middle_a', 40)
        set_finger_position(s, 'index_a', 180)

    case 'x'
        list = ['little', 'ring', 'middle', 'thumb'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end
        set_finger_position(s, 'index_a', 180)
        set_finger_position(s, 'index', 100)

    case 'y'
        list = ['ring', 'middle', 'index', 'thumb_a'];
        for joint=1:length(list)
            set_finger_position(s, list(joint), 0);
        end

    otherwise
		%REST position
        set_finger_position(s, 'thumb', 180)
        set_finger_position(s, 'thumb_a', 70)
        set_finger_position(s, 'index', 180)
        set_finger_position(s, 'index_a', 90)
        set_finger_position(s, 'middle', 180)
        set_finger_position(s, 'middle_a', 50)
        set_finger_position(s, 'ring', 180)
        set_finger_position(s, 'little', 180)
        set_finger_position(s, 'wrist', 120)
    end
end