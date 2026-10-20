"""Statistical functions with explicit directions and no synthetic observations."""
from __future__ import annotations

import numpy as np
from scipy import special, stats


def holm(p_values):
    """Holm step-down adjusted p-values, returned in input order."""
    values = np.asarray(p_values, dtype=float)
    if values.ndim != 1 or np.any(~np.isfinite(values)) or np.any((values < 0) | (values > 1)):
        raise ValueError("p-values must be a finite one-dimensional array in [0,1]")
    order = np.argsort(values, kind="stable")
    adjusted = np.minimum(1.0, np.maximum.accumulate((len(values) - np.arange(len(values))) * values[order]))
    result = np.empty_like(adjusted)
    result[order] = adjusted
    return result


def welch_from_summary(n1, mean1, sd1, n0, mean0, sd0, alpha=0.05):
    """Two-sided Welch test; difference and g are group 1 minus group 0.

    Hedges' g uses the pooled sample SD and the exact gamma-ratio correction
    J(n1+n0-2). This standardized index is descriptive when variances differ;
    Welch inference for the raw mean difference does not assume equal variances.
    The optional g interval is an approximate normal interval using pooled-SD
    variance, not an exact unequal-variance interval.
    """
    if int(n1) != n1 or int(n0) != n0 or min(n1, n0) < 2:
        raise ValueError("Each group requires an integer n >= 2")
    if not all(np.isfinite([mean1, sd1, mean0, sd0])) or min(sd1, sd0) <= 0:
        raise ValueError("Means must be finite and sample SDs positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    v1, v0 = sd1**2 / n1, sd0**2 / n0
    se = np.sqrt(v1 + v0)
    difference = mean1 - mean0
    statistic = difference / se
    df = (v1 + v0)**2 / (v1**2 / (n1 - 1) + v0**2 / (n0 - 1))
    p_value = 2 * stats.t.sf(abs(statistic), df)
    half_width = stats.t.ppf(1 - alpha / 2, df) * se
    pooled_df = n1 + n0 - 2
    pooled_sd = np.sqrt(((n1 - 1) * sd1**2 + (n0 - 1) * sd0**2) / pooled_df)
    cohen_d = difference / pooled_sd
    correction = np.exp(special.gammaln(pooled_df / 2) - special.gammaln((pooled_df - 1) / 2)) / np.sqrt(pooled_df / 2)
    hedges_g = correction * cohen_d
    g_se = correction * np.sqrt((n1 + n0) / (n1 * n0) + cohen_d**2 / (2 * pooled_df))
    g_half = stats.norm.ppf(1 - alpha / 2) * g_se
    return dict(n1=int(n1), n0=int(n0), difference=float(difference), standard_error=float(se),
                statistic=float(statistic), df=float(df), p_raw=float(p_value),
                ci_low=float(difference - half_width), ci_high=float(difference + half_width),
                pooled_sd=float(pooled_sd), cohen_d=float(cohen_d), hedges_g=float(hedges_g),
                hedges_correction=float(correction), g_ci_low_approx=float(hedges_g - g_half),
                g_ci_high_approx=float(hedges_g + g_half))


def mean_ci(n, mean, sample_sd):
    width = stats.t.ppf(0.975, n - 1) * sample_sd / np.sqrt(n)
    return float(mean - width), float(mean + width)


def pearson_with_ci(x, y):
    result = stats.pearsonr(x, y)
    ci = result.confidence_interval(confidence_level=0.95)
    n = len(x)
    t_value = result.statistic * np.sqrt((n - 2) / (1 - result.statistic**2))
    return dict(estimate=float(result.statistic), p_raw=float(result.pvalue), statistic=float(t_value),
                df=n - 2, ci_low=float(ci.low), ci_high=float(ci.high), ci_method="Fisher z, marginal 95%")


def spearman_with_ci(x, y, seed=42, resamples=5000):
    """Asymptotic two-sided p and paired nonparametric percentile bootstrap CI."""
    x, y = np.asarray(x), np.asarray(y)
    result = stats.spearmanr(x, y)
    rng = np.random.default_rng(seed)
    boot = []
    for offset in range(0, resamples, 250):
        indices = rng.integers(0, len(x), size=(min(250, resamples - offset), len(x)))
        rx = stats.rankdata(x[indices], axis=1)
        ry = stats.rankdata(y[indices], axis=1)
        rx -= rx.mean(axis=1, keepdims=True)
        ry -= ry.mean(axis=1, keepdims=True)
        boot.extend(np.sum(rx * ry, axis=1) / np.sqrt(np.sum(rx**2, axis=1) * np.sum(ry**2, axis=1)))
    low, high = np.quantile(boot, [0.025, 0.975])
    return dict(estimate=float(result.statistic), p_raw=float(result.pvalue), statistic=float(result.statistic),
                df=np.nan, ci_low=float(low), ci_high=float(high),
                ci_method=f"Paired percentile bootstrap, {resamples} resamples, seed {seed}")
