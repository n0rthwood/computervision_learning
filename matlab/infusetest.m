a=ones(300)
b=zeros(300)



c=imfuse(a,b,"diff")
d=(a+b)*256/2
imshowpair(c,d,"montage")