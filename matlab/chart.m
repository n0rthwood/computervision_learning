x = [1:10];
y = [75,58,90,89,87,76,65,54,44,33];
bar(x,y),xlabel("student"),ylabel('Score')
title('mytitle')
print -deps graph.eps
