%%==========================================================================
 % Copyright (c) 2014 Carnegie Mellon University.  All Rights Reserved.
 %
 % Use of the Lemur Toolkit for Language Modeling and Information Retrieval
 % is subject to the terms of the software license set forth in the LICENSE
 % file included with this software (and below), and also available at
 % http://www.lemurproject.org/license.html
 %
%%==========================================================================

function deep_lasso(A_file, y_file, A_test_file, y_test_file)

% expression used to expand a feature instance

% no expansion f_exp = @(x) [x(1), x(2), x(3), x(4)]; %, x(5)];
%f_exp = @(x) x;

% 17 features as in SIGIR draft
%f_exp = @(x) [ x(2), x(3), x(4), x(13), x(14), x(15), x(16), x(17), x(18), x(19), x(20), x(21), x(22), x(23), x(24), x(1), x(25), x(26)];

% 17 features as in SIGIR draft + (google ngram, wiki titles, AOL log)
%f_exp = @(x) [ x(2), x(3), x(4), x(13), x(14), x(15), x(16), x(17), x(18), x(19), x(20), x(21), x(22), x(23), x(24), x(1), x(25), x(26), x(27), x(28), x(29)];

% experimental 1
%f_exp = @(x) [ x(2), x(3), x(4), x(24), x(1), x(25), x(29)];

% experimental 2: 11 features which result in relatively good results
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(26), x(27), x(28), x(29)];


% experimental 3 with inq features 
% starting point for week of 20140421
% f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(26), x(27), x(28), x(29), x(30), x(31), x(32)];

% feature set 4
%f_exp = @(x) [ x(17), x(24), x(1), x(25), x(26), x(27), x(28), x(29), x(30), x(31), x(32)];

% feature set 5
%f_exp = @(x) [ x(2), x(3), x(4), x(1), x(25), x(26), x(27), x(28), x(29), x(30), x(31), x(32)];

% feature set 6
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(26), x(27), x(28), x(29), x(30), x(31), x(32)];

% feature set 7
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(27), x(28), x(29), x(30), x(31), x(32)];

% feature set 8
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(26),  x(28), x(29), x(30), x(31), x(32)];

% feature set 9
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(26), x(27), x(29), x(30), x(31), x(32)];

%feature set 10
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(26), x(27), x(28), x(30), x(31), x(32)];

%feature set 11
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25), x(30), x(31), x(32)];

%feature set 12
%f_exp = @(x) [ x(2), x(3), x(4), x(17), x(24), x(1), x(25),  x(29), x(30), x(31), x(32)];

%feature set 13 with deep features
%f_exp = @(x) [ x(17), x(24), x(1), x(25), x(33), x(34), x(35)];

%feature set 14: all deep features 300d
f_exp = @(x) x;


% -FG1
%f_exp = @(x) [ x(1), x(5), x(6), x(7), x(8), x(9), x(13), x(14), x(15), x(16), x(17), x(18), x(19), x(20), x(21), x(22), x(23), x(24), x(25), x(26)];

% for trec 13-14
%f_exp = @(x) [x(1), x(6), x(7), x(8), x(9), x(13), x(14), x(15), x(16), x(17), x(18), x(19), x(20), x(21), x(22), x(23), x(24), x(25), x(26)];

%f_exp = @(x) [x(1), x(2), x(3), x(4), x(5), x(6)];

%Test all features except svd
%f_exp = @(x) [x(1), x(6), x(7), x(8), x(9), x(10), x(11), x(12)];

% New df features
%f_exp = @(x) [x(1), x(2), x(3), x(4), x(6), x(7), x(8), x(9)]; %, x(5)];

% quadratic expansion
%f_exp = @(x) [x(1)^2, x(2)^2, x(3)^2, x(4)^2, x(5)^2, 2*x(1)*x(2), 2*x(1)*x(3), 2*x(1)*x(4), 2*x(1)*x(5), 2*x(2)*x(3), 2*x(2)*x(4), 2*x(2)*x(5), 2*x(3)*x(4), 2*x(3)*x(5), 2*x(4)*x(5)];
%f_exp = @(x) [x(1)^2, x(2)^2, x(3)^2, x(4)^2, 2*x(1)*x(2), 2*x(1)*x(3), 2*x(1)*x(4), 2*x(2)*x(3), 2*x(2)*x(4), 2*x(3)*x(4)];

% cubic expansion
%f_exp = @(x) [x(1)^3, 3*x(2)*x(1)^2, 3*x(3)*x(1)^2, 3*x(4)*x(1)^2, 3*x(5)*x(1)^2, 3*x(2)^2*x(1), 3*x(3)^2*x(1), 3*x(4)^2*x(1), 3*x(5)^2*x(1), 6*x(2)*x(3)*x(1), 6*x(2)*x(4)*x(1), 6*x(3)*x(4)*x(1), 6*x(2)*x(5)*x(1), 6*x(3)*x(5)*x(1), 6*x(4)*x(5)*x(1), x(2)^3, x(3)^3, x(4)^3, x(5)^3, 3*x(2)*x(3)^2, 3*x(2)*x(4)^2, 3*x(3)*x(4)^2, 3*x(2)*x(5)^2, 3*x(3)*x(5)^2, 3*x(4)*x(5)^2, 3*x(2)^2*x(3), 3*x(2)^2*x(4), 3*x(3)^2*x(4), 6*x(2)*x(3)*x(4), 3*x(2)^2*x(5),  3*x(3)^2*x(5),  3*x(4)^2*x(5), 6*x(2)*x(3)*x(5), 6*x(2)*x(4)*x(5), 6*x(3)*x(4)*x(5)];
%f_exp = @(x) [x(1)^3, 3*x(2)*x(1)^2, 3*x(3)*x(1)^2, 3*x(4)*x(1)^2, 3*x(2)^2*x(1), 3*x(3)^2*x(1), 3*x(4)^2*x(1), 6*x(2)*x(3)*x(1), 6*x(2)*x(4)*x(1), 6*x(3)*x(4)*x(1),  x(2)^3, x(3)^3, x(4)^3, 3*x(2)*x(3)^2, 3*x(2)*x(4)^2, 3*x(3)*x(4)^2,  3*x(2)^2*x(3), 3*x(2)^2*x(4), 3*x(3)^2*x(4), 6*x(2)*x(3)*x(4) ];

% Load and expand original matrix
A=kernel_expand(load(A_file), f_exp);
A_test=kernel_expand(load(A_test_file), f_exp);
y=load(y_file);


% from oddp to P
z=y./(y+1);

z_p=y./(y+1);

% from P to log odds
z=log(z./(1-z));

% control to use L1 norm or L2 norm
L1NORM = 1;

% Pad 1 to A and A_test
% DEEP

if L1NORM == 1 
  A=[A, ones(size(A,1), 1)];
  A_test=[A_test, ones(size(A_test,1),1)];
else % L2NORM
  A_test=[ones(size(A_test,1),1), A_test];
end

% 5-fold cross validation for choosing lambda
lams = [0, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100];
nfold = 5;
cv_indices = crossvalind('Kfold', size(A,1), nfold);
cv_err = zeros(size(lams));


for k=1:nfold
  dev = (cv_indices == k);
  train = ~dev;
  A_train = A(train,:);
  z_train = z(train,:);
  A_dev = A(dev,:);
  z_dev = z(dev,:);

  if L1NORM == 1
    % L1-regularizer
    ws = lasso(A_train, z_train, 'Lambda', lams);
  else
    % L2-regularizer
    ws = ridge(z_train, A_train, lams, 0);
    A_dev = [ones(size(A_dev, 1),1), A_dev];
  end

  zs_dev_learned = A_dev * ws;
  error_zs = zs_dev_learned - repmat(z_dev, size(lams));
  cv_err = cv_err + sum(power(error_zs, 2));
end

[min_err, min_index ] = min(cv_err);

cv_lambda = lams(min_index);
        
% METHOD -1 LASSO
tic
if L1NORM == 1
  % L1-regularizer
  w = lasso(A, z, 'Lambda', cv_lambda);
else
  % L2-regularizer
  w = ridge(z, A, cv_lambda, 0);
end

toc


% METHOD 0 ridge regression
%tic
%P = A'*A + lambda * eye(size(A,2));
%w = inv(P) * A' * z;
%toc


y_learned = A_test*w;

% convert x to x / (1+|x|)
%y_learned = 0.5 + 0.5 * y_learned ./ (1+abs(y_learned));

%convert logodds to p
y_learned = exp(y_learned) ./ ( 1+ exp(y_learned));

y_test_true = load(y_test_file);
y_test_true = y_test_true ./ (y_test_true +1);

fprintf('%s %s cv_lambda:%f Lo|w|:%d Prediction error:%f.\n', A_file, A_test_file, cv_lambda, nnz(w), norm(y_test_true-y_learned, 1)/size(y_test_true, 1));


A_test_file_parts = regexp(A_test_file, '/', 'split');
outputfile = strcat(A_file, '.', A_test_file_parts{end}, '.out');
w_output = strcat(A_file, '.', A_test_file_parts{end}, '.w');
A_output = strcat(A_file, '.', A_test_file_parts{end}, '.Train.wsd');
A_test_output = strcat(A_file, '.', A_test_file_parts{end}, '.Test.wsd');

save(outputfile, 'y_learned', '-ascii');
save(w_output, 'w', '-ascii');
save(A_output, 'A', '-ascii');
save(A_test_output, 'A_test', '-ascii');
exit;
