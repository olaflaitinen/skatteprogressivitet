# R cross-validation: Gini coefficient
# Replicates skatteprogressivitet.progressivity.indices.gini()
# Run with: Rscript R/gini_crosscheck.R

stopifnot(R.Version()$major >= "4")

gini_r <- function(x) {
  x <- sort(x[x >= 0])
  n <- length(x)
  if (n == 0 || sum(x) == 0) return(0)
  ranks <- seq_len(n)
  total <- sum(x)
  (2 * sum(ranks * x) / (n * total)) - (n + 1) / n
}

# Test against known value: gini([1,2,3,4]) == 0.25
x <- c(1, 2, 3, 4)
g <- gini_r(x)
stopifnot(abs(g - 0.25) < 1e-8)
cat(sprintf("gini([1,2,3,4]) = %.8f (expected 0.25)\n", g))

# Synthetic income array (seed-matched to Python: numpy default_rng(19960307))
set.seed(19960307L)
n <- 500
labour <- rlnorm(n, meanlog = 12.5, sdlog = 0.7)
g_r <- gini_r(labour)
cat(sprintf("Gini of synthetic income (n=%d): %.6f\n", n, g_r))

# Write result for Python comparison
results <- data.frame(
  metric = "gini",
  value  = g_r
)
write.csv(results, file = "reports/r_gini_crosscheck.csv", row.names = FALSE)
cat("R Gini cross-check written to reports/r_gini_crosscheck.csv\n")
