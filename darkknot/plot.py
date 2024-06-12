import re
import numpy as np
import matplotlib.pyplot as plt
from anesthetic import NestedSamples
from fgivenx import plot_contours, plot_lines
from darkknot import darkknot


def plot(
    samples: NestedSamples,
    ax=None,
    resolution=100,
    colors="Blues_r",
    xlabel=r"$a$",
    ylabel=r"$w(a)$",
    contours=True,
    color="blue",
    **kwargs,
):
    """
    Plot functional posterior of w(a) samples.

    Parameters
    ----------
    samples : NestedSamples
        Samples to plot.

    ax : matplotlib.Axes, optional
        Axes to plot on. If None, a new figure is created.

    resolution : int, optional
        Resolution of the plot.

    colors : str, optional
        Color map to use for contours.

    xlabel : str, optional
        Label for x-axis.

    ylabel : str, optional
        Label for y-axis.

    contours : bool, optional
        use fgivenx.plot_contours, else fgivenx.plot_lines

    color : str, optional
        Color of lines.

    **kwargs : passed to fgivenx.plot_contours or fgivenx.plot_lines

    Returns
    -------
    ax : matplotlib.Axes

    """
    if ax is None:
        _, ax = plt.subplots()

    pattern = re.compile(r"^[wa]\d+$|^wn$|^Nw$")
    keys = [key for key in list(samples.columns.get_level_values(0))
            if pattern.match(key)]
    n = max(int(key[1:]) for key in keys if key != "wn" and key != "Nw") + 2
    # regex matching may pick up the wrong order of keys, so get the correct
    # order from the relevant theory
    if "Nw" in keys:
        theory = darkknot.Adaptive({"n": n})
        keys = theory.params.keys()
        keys = list(filter(lambda k: k in samples, keys))
    else:
        theory = darkknot.Vanilla({"n": n})
        keys = theory.params.keys()

    if contours:
        plot_contours(
            lambda a, theta: theory.flexknot(a, theta),
            np.linspace(theory.amin, theory.atoday, resolution),
            samples[keys],
            weights=samples.get_weights(),
            ax=ax,
            colors=colors,
            **kwargs,
        )
    else:
        plot_lines(
            lambda a, theta: theory.flexknot(a, theta),
            np.linspace(theory.amin, theory.atoday, resolution),
            samples[keys],
            weights=samples.get_weights(),
            ax=ax,
            color=color,
            **kwargs,
        )
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return ax
