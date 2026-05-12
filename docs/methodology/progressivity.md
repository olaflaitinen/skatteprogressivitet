# Progressivity Indices

## Notation

Let $y_i$ denote pre-tax income for individual $i$ and $t_i$ the corresponding
tax liability. Let $G_Y$ denote the Gini coefficient of pre-tax income.

## Gini coefficient

$$G = \frac{2 \sum_{i=1}^{n} r_i y_i}{n \sum_i y_i} - \frac{n+1}{n}$$

where $r_i$ is the rank of individual $i$ in the income distribution.

## Concentration index

The concentration index of tax with respect to income is:

$$C_T = \frac{2 \sum_{i=1}^{n} r_i t_i}{n \sum_i t_i} - \frac{n+1}{n}$$

where individuals are ranked by pre-tax income.

## Kakwani index

$$K = C_T - G_Y$$

A positive $K$ indicates a progressive tax schedule. $K = 0$ for a
proportional tax. $K < 0$ for a regressive tax.

## Suits index

The Suits index is defined as:

$$S = 1 - 2 \int_0^1 L(x) dx$$

where $L(x)$ is the Lorenz-type curve of cumulative tax share as a function
of cumulative income share.

## Residual progression

Musgrave-Thin residual progression is defined as:

$$RP(y) = \frac{1 - t'(y)}{1 - \bar{t}(y)}$$

where $t'(y)$ is the marginal rate and $\bar{t}(y)$ is the average rate.
$RP < 1$ characterises a progressive schedule.

## Decomposition

The Rao (1969) decomposition attributes the overall Kakwani index to
individual tax components $k$:

$$K = \sum_k s_k (C_k - G_Y)$$

where $s_k = T_k / T$ is the revenue share of component $k$.

## References

- Kakwani, N.C. (1977). "Measurement of tax progressivity." *Economic Journal* 87, 71-80.
- Suits, D.B. (1977). "Measurement of tax progressivity." *American Economic Review* 67, 747-752.
- Rao, V.M. (1969). "Two decompositions of concentration ratio." *Journal of the Royal Statistical Society* 132, 418-425.
- Cowell, F.A. and Flachaire, E. (2007). "Income distribution and inequality measurement." *Journal of Econometrics* 141, 527-542.
