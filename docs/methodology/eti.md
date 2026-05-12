# Elasticity of Taxable Income

## Specification

The intensive-margin elasticity of taxable income (ETI) is estimated
using the constant-elasticity specification of Feldstein (1995):

$$\frac{d \log Y}{d \log(1 - t)} = \varepsilon$$

so that the behavioural income response to a marginal rate change is:

$$\Delta Y \approx -\varepsilon Y \frac{\Delta t}{1 - t}$$

## Calibration

The baseline intensive-margin ETI is $\varepsilon = 0.3$, consistent with:

- Blomquist and Selin (2010): ETI 0.21-0.37 for Swedish men, 1971-2003.
- Gelber (2014): ETI 0.35 for married couples around the 1990 ERTA reform.

The extensive-margin participation elasticity is $\eta = 0.1$, consistent
with the participation margin estimates from Eissa and Liebman (1996)
adapted for Sweden.

## Identification

The primary identification strategy uses a bunching estimator
(Chetty et al. 2011) at the statlig inkomstskatt lower britpunkt,
exploiting the sharp kink in the budget set created by the 20 percent
state income tax bracket.

An event-study design exploits the staggered reform episodes (1991, 1995,
2007, 2020) as quasi-experiments, estimating dynamic treatment effects
using the Callaway-Sant'Anna (2021) estimator.

## References

- Blomquist, S. and Selin, H. (2010). "Hourly wage rate and taxable labor income responsiveness to changes in marginal tax rates." *Journal of Public Economics* 94, 878-889.
- Chetty, R., Friedman, J.N., Olsen, T. and Pistaferri, L. (2011). "Adjustment costs, firm responses, and micro vs. macro labor supply elasticities." *Quarterly Journal of Economics* 126, 749-804.
- Feldstein, M. (1995). "The effect of marginal tax rates on taxable income." *Journal of Political Economy* 103, 551-572.
