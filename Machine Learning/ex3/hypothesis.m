function hyp = hypothesis(theta, X)

temp=theta'*X';
temp=temp';

hyp=((1+exp(-temp)).^(-1));