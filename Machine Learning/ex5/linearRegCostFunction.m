function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%

hyp=zeros(size(y));

for i=1:size(theta,1)
    hyp=hyp+(X(:,i)*theta(i,:));
end

t_theta=theta;
t_theta(1,:)=zeros(size(theta(1,:)));

J_1=sum((hyp-y).^2)*(.5/m);
J_2=sum(t_theta.^2)*(lambda/(2*m));

J=J_1+J_2;

grad_1=((hyp-y)'*X)'./m;
grad_2=t_theta.*(lambda/m);
grad=grad_1+grad_2;

% =========================================================================

grad = grad(:);

end
