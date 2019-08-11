clear all;
wp=readtable('wp.txt');
len=height(wp);
i=1;
j=1;
while i<=len
    if wp{i,9}~=0
        wp2(j,1)=wp{i,10};
        wp2(j,2)=wp{i,9};        
        i=i+1;
        j=j+1;
    else
        i=i+1;
    end
end
dlmwrite('wpout.txt',wp2,'precision',10);

    