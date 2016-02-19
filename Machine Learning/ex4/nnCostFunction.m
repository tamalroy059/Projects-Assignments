function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%

hyp=hypothesis(X,Theta1,Theta2);
label_y=labelVector(y,num_labels);

y_i=label_y(:);
hyp_i=hyp(:);

part1=y_i'*log(hyp_i);
part2=(1-y_i)'*(log(1-hyp_i));
J=(part1*(-1))+(part2*(-1));

% for i=1:size(X,1)
%     y_i=(label_y(i,:))';
%     hyp_i=(hyp(i,:))';
%     part1=y_i'*log(hyp_i);
%     part2=(1-y_i)'*(log(1-hyp_i));
%     J=J+(part1*(-1))+(part2*(-1));
% end

J=J/size(X,1);


theta1_s=matrixSquare(Theta1);

theta2_s=matrixSquare(Theta2);

sum_theta=(lambda/(2*size(X,1)))*(theta1_s+theta2_s);

J=J+sum_theta;

Big_delta_1=zeros(size(Theta1));
Big_delta_2=zeros(size(Theta2));

for i=1:size(X,1)
    a_1=X(i,:);
    a_1=[ones(size(a_1,1), 1) a_1];
    z_2=a_1*Theta1';
    a_2=sigmoid(z_2);
    a_2= [ones(size(a_2,1), 1) a_2];
    z_3=a_2*Theta2';
    a_3=sigmoid(z_3);
%     temp=hyp(i,:);
%     temp1=a_3-temp;
%     temp2=hypothesis(X(i,:),Theta1,Theta2);
%     temp3=temp2-temp;
%     temp4=temp1-temp3;
    delta_3=a_3-labelVector(y(i),num_labels);
    delta_3=delta_3';
%     delta_2=(Theta2'*delta_3);
%     temp=sigmoidGradient(a_2);
%     delta_2=delta_2.*temp';
%     delta_2=delta_2(2:end);
    t1=Theta2(:,2:end)';
    delta_2=t1*delta_3;
    temp=sigmoidGradient(z_2);
    delta_2=delta_2.*temp';
    
    Big_delta_1=Big_delta_1+delta_2*a_1;
    Big_delta_2=Big_delta_2+delta_3*a_2;
end

Theta1_grad=Big_delta_1./m;

Theta_reg_1=Theta1;
Theta_reg_1(:,1)=zeros(size(Theta1,1),1);
Theta_reg_1=(Theta_reg_1./m).*lambda;

Theta1_grad=Theta1_grad+Theta_reg_1;

Theta2_grad=Big_delta_2./m;

Theta_reg_2=Theta2;
Theta_reg_2(:,1)=zeros(size(Theta2,1),1);
Theta_reg_2=(Theta_reg_2./m).*lambda;

Theta2_grad=Theta2_grad+Theta_reg_2;

% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];




end
