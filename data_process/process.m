data=xlsread("./data_output.xlsx");
Fs=250; 
data=data(Fs*5:end-Fs*5,:);
data=data(Fs*15:Fs*17,:);

shape=size(data);
for i = 1:shape(2)
    x=data(1:end,i);
    x=x-mean(x);
    N=length(x);
    t = 0:1/Fs:(N-1)/Fs;
    
    figure(i);
    subplot(121)
    plot(t,x);
    xlabel('Time'); 
    ylabel('Amplitude'); 
    
    subplot(122)
    y = abs(fft(x));  
    f = (0:N-1)*Fs/N;
    f_idx=find(f<=30);
    f=f(f_idx);
    y=y(f_idx);
    plot(f,y);
    %stem(f,y);
    xlabel('Frequency'); 
    ylabel('Amplitude');
end
