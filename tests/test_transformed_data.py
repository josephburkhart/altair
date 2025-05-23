import pkgutil
import sys
from importlib.metadata import version
from importlib.util import find_spec

import narwhals.stable.v1 as nw
import pytest
from packaging.version import Version

import altair as alt
from altair.utils.execeval import eval_block
from tests import (
    examples_methods_syntax,
    ignore_DataFrameGroupBy,
    skip_requires_vegafusion,
    slow,
)
from vega_datasets import data

XDIST_ENABLED: bool = "xdist" in sys.modules
"""Use as an `xfail` condition, if running in parallel may cause the test to fail."""

xfail_vegafusion_2: pytest.MarkDecorator = pytest.mark.xfail(
    bool(find_spec("vegafusion"))
    and Version(version("vegafusion")) >= Version("2.0.0a0"),
    raises=ValueError,
    reason="https://github.com/vega/altair/issues/3701",
)


# fmt: off
@ignore_DataFrameGroupBy
@skip_requires_vegafusion
@pytest.mark.parametrize(("filename", "rows", "cols"), [
    ("annual_weather_heatmap.py", 366, ["monthdate_date_end", "max_temp_max"]),
    ("anscombe_plot.py", 44, ["Series", "X", "Y"]),
    ("bar_chart_sorted.py", 6, ["site", "sum_yield"]),
    ("bar_chart_faceted_compact.py", 27, ["p", "p_end"]),
    ("beckers_barley_facet.py", 120, ["year", "site"]),
    ("beckers_barley_wrapped_facet.py", 120, ["site", "median_yield"]),
    ("bump_chart.py", 96, ["rank", "yearmonth_date"]),
    ("comet_chart.py", 120, ["variety", "delta"]),
    ("diverging_stacked_bar_chart.py", 40, ["value", "percentage_start"]),
    ("donut_chart.py", 6, ["value_start", "value_end"]),
    ("gapminder_bubble_plot.py", 187, ["income", "population"]),
    ("grouped_bar_chart2.py", 9, ["Group", "Value_start"]),
    ("hexbins.py", 84, ["xFeaturePos", "mean_temp_max"]),
    pytest.param("histogram_heatmap.py", 378, ["bin_maxbins_40_Rotten_Tomatoes_Rating", "__count"], marks=slow),
    ("histogram_scatterplot.py", 64, ["bin_maxbins_10_Rotten_Tomatoes_Rating", "__count"]),
    pytest.param("interactive_legend.py", 1708, ["sum_count_start", "series"], marks=slow),
    ("iowa_electricity.py", 51, ["net_generation_start", "year"]),
    ("isotype.py", 37, ["animal", "x"]),
    ("isotype_grid.py", 100, ["row", "col"]),
    ("lasagna_plot.py", 492, ["yearmonthdate_date", "sum_price"]),
    ("layered_area_chart.py", 51, ["source", "net_generation"]),
    ("layered_bar_chart.py", 51, ["source", "net_generation"]),
    ("layered_histogram.py", 113, ["bin_maxbins_100_Measurement"]),
    ("line_chart_with_cumsum.py", 52, ["cumulative_wheat"]),
    ("line_custom_order.py", 55, ["miles", "gas"]),
    pytest.param("line_percent.py", 30, ["sex", "perc"], marks=slow),
    ("line_with_log_scale.py", 15, ["year", "sum_people"]),
    ("multifeature_scatter_plot.py", 150, ["petalWidth", "species"]),
    pytest.param("natural_disasters.py", 686, ["Deaths", "Year"], marks=xfail_vegafusion_2),
    ("normalized_stacked_area_chart.py", 51, ["source", "net_generation_start"]),
    ("normalized_stacked_bar_chart.py", 60, ["site", "sum_yield_start"]),
    ("parallel_coordinates.py", 600, ["key", "value"]),
    ("percentage_of_total.py", 5, ["PercentOfTotal", "TotalTime"]),
    ("pie_chart.py", 6, ["category", "value_start"]),
    ("pyramid.py", 3, ["category", "value_start"]),
    ("stacked_bar_chart_sorted_segments.py", 60, ["variety", "site"]),
    ("stem_and_leaf.py", 100, ["stem", "leaf"]),
    pytest.param("streamgraph.py", 1708, ["series", "sum_count"], marks=slow),
    ("top_k_items.py", 10, ["rank", "IMDB_Rating_start"]),
    ("top_k_letters.py", 9, ["rank", "letters"]),
    pytest.param("top_k_with_others.py", 10, ["ranked_director", "mean_aggregate_gross"], marks=slow),
    ("area_faceted.py", 492, ["date", "price"]),
    ("distributions_faceted_histogram.py", 20, ["Origin", "__count"]),
    ("us_population_over_time.py", 38, ["sex", "people_start"]),
    ("us_population_over_time_facet.py", 285, ["year", "sum_people"]),
    ("wilkinson-dot-plot.py", 21, ["data", "id"]),
    ("window_rank.py", 12, ["team", "diff"]),
])
@pytest.mark.parametrize("to_reconstruct", [True, False])
def test_primitive_chart_examples(filename, rows, cols, to_reconstruct):
    # fmt: on
    source = pkgutil.get_data(examples_methods_syntax.__name__, filename)
    chart = eval_block(source, strict=True)
    if to_reconstruct:
        # When reconstructing a Chart, Altair uses different classes
        # then what might have been originally used. See
        # https://github.com/hex-inc/vegafusion/issues/354 for more info.
        chart = alt.Chart.from_dict(chart.to_dict())
    df = chart.transformed_data()
    assert df is not None
    nw_df = nw.from_native(df, eager_only=True)

    assert len(nw_df) == rows
    assert set(cols).issubset(set(nw_df.columns))


# fmt: off
@skip_requires_vegafusion
@pytest.mark.parametrize(("filename", "all_rows", "all_cols"), [
    ("errorbars_with_std.py", [10, 10], [["upper_yield"], ["extent_yield"]]),
    ("candlestick_chart.py", [44, 44], [["low"], ["close"]]),
    ("co2_concentration.py", [713, 7, 7], [["first_date"], ["scaled_date"], ["end"]]),
    pytest.param("falkensee.py", [2, 38, 38], [["event"], ["population"], ["population"]], marks=xfail_vegafusion_2),
    ("heat_lane.py", [10, 10], [["bin_count_start"], ["y2"]]),
    ("histogram_responsive.py", [20, 20], [["__count"], ["__count"]]),
    ("histogram_with_a_global_mean_overlay.py", [9, 1], [["__count"], ["mean_IMDB_Rating"]]),
    ("horizon_graph.py", [20, 20], [["x"], ["ny"]]),
    pytest.param("interactive_cross_highlight.py", [64, 64, 13], [["__count"], ["__count"], ["Major_Genre"]], marks=slow),
    ("interval_selection.py", [123, 123], [["price_start"], ["date"]]),
    ("layered_chart_with_dual_axis.py", [12, 12], [["month_date"], ["average_precipitation"]]),
    ("layered_heatmap_text.py", [9, 9], [["Cylinders"], ["mean_horsepower"]]),
    ("multiline_highlight.py", [560, 560], [["price"], ["date"]]),
    ("multiline_tooltip.py", [300, 300, 300, 0, 300], [["x"], ["y"], ["y"], ["x"], ["x"]]),
    ("pie_chart_with_labels.py", [6, 6], [["category"], ["value"]]),
    ("radial_chart.py", [6, 6], [["values"], ["values_start"]]),
    ("scatter_linked_table.py", [392, 14, 14, 14], [["Year"], ["Year"], ["Year"], ["Year"]]),
    ("scatter_marginal_hist.py", [34, 150, 27], [["__count"], ["species"], ["__count"]]),
    pytest.param(
        "scatter_with_layered_histogram.py",
        [2, 19],
        [["gender"], ["__count"]],
        marks=(slow, pytest.mark.xfail(
            XDIST_ENABLED,
            reason="Possibly `numpy` conflict with `xdist`.\n"
            "Very intermittent, but only affects `to_reconstruct=False`."
        )),
    ),
    ("scatter_with_minimap.py", [1461, 1461], [["date"], ["date"]]),
    ("scatter_with_rolling_mean.py", [1461, 1461], [["date"], ["rolling_mean"]]),
    ("seattle_weather_interactive.py", [1461, 5], [["date"], ["__count"]]),
    ("select_detail.py", [20, 1000], [["id"], ["x"]]),
    ("simple_scatter_with_errorbars.py", [5, 5], [["x"], ["upper_ymin"]]),
    ("stacked_bar_chart_with_text.py", [60, 60], [["site"], ["site"]]),
    ("us_employment.py", [120, 1, 2], [["month"], ["president"], ["president"]]),
    ("us_population_pyramid_over_time.py", [19, 38, 19], [["gender"], ["year"], ["gender"]]),
])
@pytest.mark.parametrize("to_reconstruct", [True, False])
def test_compound_chart_examples(filename, all_rows, all_cols, to_reconstruct):
    # fmt: on
    source = pkgutil.get_data(examples_methods_syntax.__name__, filename)
    chart = eval_block(source, strict=True)
    if to_reconstruct:
        # When reconstructing a Chart, Altair uses different classes
        # then what might have been originally used. See
        # https://github.com/hex-inc/vegafusion/issues/354 for more info.
        chart = alt.Chart.from_dict(chart.to_dict())

    assert isinstance(chart, (alt.LayerChart, alt.ConcatChart, alt.HConcatChart, alt.VConcatChart))
    dfs = chart.transformed_data()

    if not to_reconstruct:
        # Only run assert statements if the chart is not reconstructed. Reason
        # is that for some charts, the original chart contained duplicated datasets
        # which disappear when reconstructing the chart.

        nw_dfs = (nw.from_native(d, eager_only=True) for d in dfs)
        assert len(dfs) == len(all_rows)
        for df, rows, cols in zip(nw_dfs, all_rows, all_cols):
            assert len(df) == rows
            assert set(cols).issubset(set(df.columns))


@skip_requires_vegafusion
@pytest.mark.parametrize("to_reconstruct", [True, False])
def test_transformed_data_exclude(to_reconstruct):
    source = data.wheat()
    bar = alt.Chart(source).mark_bar().encode(x="year:O", y="wheat:Q")
    rule = alt.Chart(source).mark_rule(color="red").encode(y="mean(wheat):Q")
    some_annotation = (
        alt.Chart(name="some_annotation")
        .mark_text(fontWeight="bold")
        .encode(text=alt.value("Just some text"), y=alt.datum(85), x=alt.value(200))
    )

    chart = (bar + rule + some_annotation).properties(width=600)
    if to_reconstruct:
        # When reconstructing a Chart, Altair uses different classes
        # then what might have been originally used. See
        # https://github.com/hex-inc/vegafusion/issues/354 for more info.
        chart = alt.Chart.from_dict(chart.to_dict())
    assert isinstance(chart, alt.LayerChart)
    datasets = chart.transformed_data(exclude=["some_annotation"])

    _datasets = [nw.from_native(d, eager_only=True) for d in datasets]
    assert len(datasets) == len(_datasets)
    assert len(_datasets) == 2
    assert len(_datasets[0]) == 52
    assert "wheat_start" in _datasets[0]
    assert len(_datasets[1]) == 1
    assert "mean_wheat" in _datasets[1]
