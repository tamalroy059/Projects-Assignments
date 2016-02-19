function label_vector= labelVector(digit,num_labels)

label_vector=zeros(size(digit,1),num_labels);

for i=1:size(label_vector,1)
    temp=label_vector(i,:);
    temp(digit(i))=1;
    label_vector(i,:)=temp;
end