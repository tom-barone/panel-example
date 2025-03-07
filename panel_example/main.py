from   hvplot                   import pandas as _
import numpy as np
import pandas as pd
import panel as pn

# Stop the unused import being flagged
_.__doc__ = ""

PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = (
    "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)

pn.extension(design="material", sizing_mode="stretch_width")

@pn.cache
def get_data():
  return pd.read_csv(CSV_FILE, parse_dates=["date"], index_col="date")

data = get_data()

data.tail()

def transform_data(variable, window, sigma):
    """Calculates the rolling average and identifies outliers"""
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return avg, avg[outliers]


def get_plot(variable="Temperature", window=30, sigma=10):
    """Plots the rolling average and the outliers"""
    avg, highlight = transform_data(variable, window, sigma)
    return avg.hvplot( # pyright: ignore
        height=300, legend=False, color=PRIMARY_COLOR
                      ) * highlight.hvplot.scatter(color=SECONDARY_COLOR, padding=0.1, legend=False) # pyright: ignore

get_plot(variable='Temperature', window=20, sigma=10)

variable_widget = pn.widgets.Select(name="variable", value="Temperature", options=list(data.columns))
window_widget = pn.widgets.IntSlider(name="window", value=30, start=1, end=60)
sigma_widget = pn.widgets.IntSlider(name="sigma", value=10, start=0, end=20)

bound_plot = pn.bind(
    get_plot, variable=variable_widget, window=window_widget, sigma=sigma_widget
)

widgets = pn.Column(variable_widget, window_widget, sigma_widget, sizing_mode="fixed", width=300)
pn.Column(widgets, bound_plot)

logout_button = pn.widgets.Button(name="Log out", margin=(50, 0, 0, 0))
logout_button.js_on_click(code="""window.location.href = './logout'""")

pn.template.MaterialTemplate(
    site="Panel",
    title="Example Panel app",
    sidebar=[variable_widget, window_widget, sigma_widget, logout_button],
    main=[bound_plot],
).servable(); # The ; is needed in the notebook to not display the template. Its not needed in a script
