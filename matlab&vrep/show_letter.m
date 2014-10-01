function show_letter(coord)
% 
% SHOW_LETTER
% ---------------
% This function allows to display the image of sign relative to the letter
% we want to see.
%
% SYNTAX:
% show_letter(coord)
%
% INPUT:
% - coord: is a column vector of two elments that corrisponds to the 
%   coordinates of the center of window we want to display.
%   The first element corrisponds to the y-coordinate of centre
%   and the second the x-coordinate of centre.
%        coord
%   y      |
%   x      |
%
% Programmed by :  Mastrorillo Gianluca, Moramarco Annarita, Margaria Elena
% LastEditDate : may 14, 2014

global alphabet;
image (alphabet(coord(1)-60:coord(1)+60,coord(2)-60:coord(2)+60,:))

end