%%==========================================================================
 % Copyright (c) 2014 Carnegie Mellon University.  All Rights Reserved.
 %
 % Use of the Lemur Toolkit for Language Modeling and Information Retrieval
 % is subject to the terms of the software license set forth in the LICENSE
 % file included with this software (and below), and also available at
 % http://www.lemurproject.org/license.html
 %
%%==========================================================================

function B = kernel_expand(A, f_exp)
% f_exp is applied to each row of A and the result is pasted into each row of B
B=[];
for i=1:size(A,1)
    B=[B;f_exp(A(i,:))];
end
