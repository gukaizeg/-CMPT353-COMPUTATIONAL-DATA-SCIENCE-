Adding a column for the national total covid cases/deaths seem to change the performance drastically.

On one hand, it is probably not a good change to do if we aim to train the multi polynomial regression model:
Some scores went up a lot (Alberta's score went up from 0.118056975515683 to 0.787486523056723), wheareas others even got to negative values (Ontario's multi polynomial regression got from 0.436719343778554 to  -0.595550122644689).
Augmenting these two columns in multi-polynomial regression makes the performance much more unstable, and we may get much worse results 

On the other hand, augmenting the Canada total does help with multi linear regression:
With exception of Saskatchewan, whose score went down from 0.0525641462326443 to 0.503762123065592, and Canada, whose score very reasonably kept unchanged, all other regions have seen an improvement of accuracy after adding the extra columns national total covid cases/deaths.
The highest improvement being British Columbia, whose score went from 0.0246535128345458 to 0.523143663463915
In general, augmenting these two columns in multi-linear regression gives us a considerable boost in model accuracy basically for free.

Quebec's unemployment is still easiest to predict using only multi-linear regression: this probably means that Quebec's unemployment is most affected by the covid cases and deaths.