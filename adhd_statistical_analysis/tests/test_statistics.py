import numpy as np
import pytest
from scipy import stats
from statsmodels.stats.multitest import multipletests

from statistics_helpers import holm, mean_ci, welch_from_summary


@pytest.mark.parametrize("means,sds,expected", [
    ((5.55, 6.04), (1.04, 1.17), 0.00151),
    ((5.41, 6.03), (1.49, 1.25), 0.00268),
])
def test_welch_against_independent_scipy_and_validation_values(means, sds, expected):
    result = welch_from_summary(68, means[0], sds[0], 197, means[1], sds[1])
    reference = stats.ttest_ind_from_stats(means[0], sds[0], 68, means[1], sds[1], 197, equal_var=False)
    assert result["statistic"] == pytest.approx(reference.statistic, rel=1e-12)
    assert result["p_raw"] == pytest.approx(reference.pvalue, rel=1e-12)
    assert result["p_raw"] == pytest.approx(expected, abs=0.00001)
    assert result["ci_low"] < result["difference"] < result["ci_high"] < 0
    assert result["hedges_g"] < 0
    # The Welch CI is obtained by inverting the same t pivot.
    pivot = (result["difference"] - result["ci_low"]) / result["standard_error"]
    assert stats.t.sf(pivot, result["df"]) == pytest.approx(0.025, rel=1e-10)


def test_direction_reversal_preserves_p_and_reverses_effect_and_interval():
    forward = welch_from_summary(68, 5.55, 1.04, 197, 6.04, 1.17)
    reverse = welch_from_summary(197, 6.04, 1.17, 68, 5.55, 1.04)
    assert forward["p_raw"] == reverse["p_raw"]
    assert forward["df"] == reverse["df"]
    assert forward["hedges_g"] == -reverse["hedges_g"]
    assert forward["ci_low"] == -reverse["ci_high"]


def test_null_means_and_units():
    equal = welch_from_summary(20, 3, 1, 30, 3, 2)
    assert equal["p_raw"] == 1
    base = welch_from_summary(20, 3, 1, 30, 4, 2)
    scaled = welch_from_summary(20, 300, 100, 30, 400, 200)
    assert base["hedges_g"] == pytest.approx(scaled["hedges_g"])
    assert base["p_raw"] == pytest.approx(scaled["p_raw"])
    assert 100 * base["ci_low"] == pytest.approx(scaled["ci_low"])


@pytest.mark.parametrize("values", [[.01, .04, .03], [.8, .2, .9], [.0015, .0027], [.04, .04, .001]])
def test_holm_against_statsmodels(values):
    assert holm(values) == pytest.approx(multipletests(values, method="holm")[1])


def test_mean_ci():
    low, high = mean_ci(68, 5.55, 1.04)
    assert (low + high) / 2 == pytest.approx(5.55)
    assert (5.55 - low) / (1.04 / np.sqrt(68)) == pytest.approx(stats.t.ppf(.975, 67))


@pytest.mark.parametrize("args", [(1, 0, 1, 20, 1, 1), (20, 0, -1, 20, 1, 1), (20, float('nan'), 1, 20, 1, 1)])
def test_invalid_summaries_rejected(args):
    with pytest.raises(ValueError):
        welch_from_summary(*args)
