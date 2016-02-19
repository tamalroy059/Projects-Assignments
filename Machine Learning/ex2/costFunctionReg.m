function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

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

hyp=hypothesis(theta,X);
part1=y'*log(hyp);
part2=(1-y)'*(log(1-hyp));
sum=(part1*(-1))+(part2*(-1));

matrix=(ones(size(theta)));
matrix(1)=0;

lambda_part=(lambda/(2*m))*(matrix'*(theta.^2));

J=(sum/m)+lambda_part;

temp_theta=theta;
temp_theta(1)=0;
temp_theta=temp_theta*(lambda/m);

grad=(((hyp-y)'*X)./m)+tevmp_theta';




% =============================================================

end
