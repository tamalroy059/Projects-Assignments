function [output_y] = compareVector(output_y, y, element);



for i=1:size(y,1)
    output_y(i)=isequal(y(i),element);
end

