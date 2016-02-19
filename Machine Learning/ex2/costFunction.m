function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%



hyp=hypothesis(theta,X);
part1=y'*log(hyp);
part2=(1-y)'*(log(1-hyp));
sum=(part1*(-1))+(part2*(-1));
J=sum/m;

grad=((hyp-y)'*X)./m;





% sum=0;
% for i=1:size(X,1)
%     temp1=theta'*X(i,:)';
%     hyp=pinv(1+exp(temp1));
%     temp2=log(hyp)*y(i);
%     temp3=log(1-hyp)*(1-y(i));
%     temp2=temp2*(-1);
%     temp3=temp3*(-1);
%     sum=sum+temp2+temp3;
% end
% 
% J=sum/size(X,1);




% =============================================================

end
