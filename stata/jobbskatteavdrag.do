* Stata cross-validation: jobbskatteavdrag computation
* Replicates compute_jobbskatteavdrag() for year 2025
* Run with: stata -b do stata/jobbskatteavdrag.do

version 17
clear all
set more off

* Parameters (2025)
local kommunal_rate = 0.3240
local pbb = 52500

* Generate income grid
range labour_income 0 2000000 1000

* Compute prisbasbelopp thresholds
local t0 = `pbb' * 0.91      // 47775
local t1 = `pbb' * 2.72      // 142800
local t2 = `pbb' * 7.0       // 367500

* Phase-in credit at t0
local credit_at_t0 = `kommunal_rate' * `t0'

* Max credit
local max_credit = `credit_at_t0' + `kommunal_rate' * (`t1' - `t0') * 0.3174

gen jsa = .

replace jsa = `kommunal_rate' * labour_income ///
    if labour_income <= `t0' & labour_income >= 0

replace jsa = `credit_at_t0' + `kommunal_rate' * (labour_income - `t0') * 0.3174 ///
    if labour_income > `t0' & labour_income <= `t1'

replace jsa = `max_credit' ///
    if labour_income > `t1' & labour_income <= `t2'

replace jsa = max(0, `max_credit' - `kommunal_rate' * (labour_income - `t2') * 0.03) ///
    if labour_income > `t2'

* Replace negatives with zero
replace jsa = max(0, jsa)

* Display summary
sum jsa, detail

* Save for comparison with Python output
export delimited using "reports/stata_jsa_2025.csv", replace

display "Stata jobbskatteavdrag cross-validation complete."
