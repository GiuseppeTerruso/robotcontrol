function [letter, wrist, coordinates, found] = find_letter(l)
%
% FIND_LETTER
% -----------
% 
% This function associates fingers and wrist joints configuration to a
% letter passed as parameter.
% For a correct operation, before the call of this function it's necessary
% define
% - a global vector called "letters" that contains the character to find;
% - a global matrix called "j_conf" of dimension 5x4xN, where N is the 
%   length of "letters". This contains the joint configurations of all the
%   fingers; for the definition of the element of this matrix see the
%   structure of the output letter defined below;
% - a global matrix called "j_wrist" of dimension 3xN, where N is the 
%   length of "letters",that contains the joint configurations of all the
%   wrist poses;
% - a global matrix called "coordinates_image" that is a matrix 2xN,
%   where N is the length of "letters". It contains che coordinates y and x
%   of a centre of a window relative to a letter that we want to show.
% 
% SYNTAX:
% [letter, wrist, coordinates] = find_letter(l)
%
% INPUT:
% l : is the letter of which we want to know the joints configuration
%
% OUTPUT:
% - letter : is a matrix that contains all the joint configurations of the 
%            finger; it has 5 rows, one for each finger, and 4 columns, 
%            one for each joint; the structure is the following
%
%                   base  prox_ph  inter_ph  dist_ph 
%           thumb     |       |        |           |
%           index     |       |        |           |
%           middle    |       |        |           |
%           ring      |       |        |           |
%           pinky     |       |        |           |
% - wrist : is a matrix that contains all the wrist configurations;
%         it has 3 rows, one for each joint, and so many columns as are the
%         motions required to show the letter;
% - coordinates : is a matrix that contains the coordinates relative to the
%                the centre of window we want to show relative to a letter
%
%                 letter
%                y  |
%                x  |
% - found : is a variable that can be equal to 1 when the letter put in
%           input has been found and 0 if not.
%
% Programmed by :  Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 14, 2014

global letters j_conf j_wrist coordinates_image text_error;
letter = zeros(5,4);
wrist = zeros(3,1);
coordinates = zeros(2,1);

i_start = 1;
i_end = length(letters);
while( i_start <= i_end )
    index = round((i_start + i_end)/2);
    if (letters(index) == l)
        letter = j_conf(:,:,index);
        wrist = j_wrist(:,index);
        if(l == 'j')
            wrist(:,2) = j_wrist(:,27);
        elseif(l == 'x')
            wrist(:,2) = j_wrist(:,28);
        elseif(l == 'z')
            wrist(:,2:4) = j_wrist(:,29:end);
        end
        coordinates = coordinates_image(:, index);
        found = 1;
        return;
    elseif (letters(index) < l)
        i_start = index + 1;
    else
        i_end = index - 1;
    end
end

set(text_error,'String',['the symbol ', l, ' is not present in the database']);
found = 0;

end