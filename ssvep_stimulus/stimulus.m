sca;
close all;
clearvars;

PsychDefaultSetup(2);
screen = max(Screen('Screens'));

[win,rect] = PsychImaging ('OpenWindow',screen,[0,0,0]);
ifi = Screen('GetFlipInterval', win);

while(1)
    Screen('FillRect',win,[0,0,255],[1000,400,1600,1000]);
    vbl = Screen('Flip', win);
    vb2 = Screen('Flip', win, vbl + 5 * ifi);
    vb3 = Screen('Flip', win, vb2 + 5 * ifi);
 
    [KD,SECS,KC]=KbCheck;
    if KC(KbName('return'))
        sca;
        clear;
        break;
    end
end
