function matrixSquare=matrixSquare(theta)

sum=0;
for i=1:size(theta,1)
    for j=2:size(theta,2)
      sum=sum+theta(i,j)^2;  
    end
end

matrixSquare=sum;