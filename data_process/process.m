x=table2array(data);
x=x(2:end,1);
Fs=125;
N=length(x);
t = 0:1/Fs:(N-1)/Fs; 

figure(1);
plot(t,x);
title('Original Signal');
xlabel('Time'); 
ylabel('Amplitude'); 

figure(2);
y0 = abs(fft(x)); 
f = (0:N-1)*Fs/N;
plot(f,y0);
xlabel('Frequency'); 
ylabel('Amplitude');