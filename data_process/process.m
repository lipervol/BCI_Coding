data=xlsread("./data_output.xlsx");
Fs=125;
N=length(x);
t = 0:1/Fs:(N-1)/Fs; 
shape=size(data);
for i = 1:shape(2)
    x=data(1:end,i);
    figure(i);
    subplot(121)
    plot(t,x);
    title('Original Signal');
    xlabel('Time'); 
    ylabel('Amplitude'); 
    
    subplot(122)
    y0 = abs(fft(x)); 
    f = (0:N-1)*Fs/N;
    plot(f,y0);
    xlabel('Frequency'); 
    ylabel('Amplitude');
end
