function hypothesis=hypothesis(X,Theta1,Theta2)

X = [ones(size(X,1), 1) X];


z_2=X*Theta1';

a_2=sigmoid(z_2);

a_2= [ones(size(a_2,1), 1) a_2];

z_3=a_2*Theta2';

a_3=sigmoid(z_3);

hypothesis=a_3;
