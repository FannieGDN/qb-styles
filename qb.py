# QUANTUMBLACK CONFIDENTIAL
#
# Copyright (c) 2016 - present QuantumBlack Visual Analytics Ltd. All
# Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of
# QuantumBlack Visual Analytics Ltd. and its suppliers, if any. The
# intellectual and technical concepts contained herein are proprietary to
# QuantumBlack Visual Analytics Ltd. and its suppliers and may be covered
# by UK and Foreign Patents, patents in process, and are protected by trade
# secret or copyright law. Dissemination of this information or
# reproduction of this material is strictly forbidden unless prior written
# permission is obtained from QuantumBlack Visual Analytics Ltd.
"""
Some of the tick properties cannot be set using ``plt.style.use``,
so we have to set them in code.

We want the user to be able to apply the full style, including styling the
minor ticks, using only a _single_ function call. To make this possible we need
to monkey patch as we first need to apply the style using ``plt.style.use``,
then create a figure (using either ``plt.figure`` or ``plt.Figure`` or
``plt.subplots``), and _then_ get from this figure the axes to style the ticks.
"""
import matplotlib.pyplot as plt
import matplotlib.axes


COMMON_STYLE = './qb-common.mplstyle'
DARK_STYLE = './qb-dark.mplstyle'
LIGHT_STYLE = './qb-light.mplstyle'


def qb_style(dark=True):
    """Some of the tick properties cannot be set using ``plt.style.use``.
    Use this function as follows, to set them together with all other style
    properties:

    ::
        >>> from qb import qb_style
        >>> import numpy as np
        >>>
        >>> #create some data
        >>> rng = np.random.RandomState(4)
        >>> x = np.linspace(0, 10, 500)
        >>> y = np.cumsum(rng.randn(500, 4), 0)
        >>>
        >>> # plot
        >>> qb_style(dark=True)
        >>> plt.plot(x, y)

    Args:
        dark (bool)     : Use the dark or light style (default: True)
    """
    plt.style.use([COMMON_STYLE, DARK_STYLE if dark else LIGHT_STYLE])
    color = 'FFFFFF' if dark else '000000'

    plt.subplots = _monkey_patch_subplot(color, plt.subplots)
    plt.Figure = _monkey_patch_figure(color, plt.Figure)


def _style_ticks(axis, color):
    """ Enable minor ticks, and color major + minor ticks"""
    axis.minorticks_on()
    ticks = (axis.get_xticklines() +
             axis.xaxis.get_minorticklines() +
             axis.get_yticklines() +
             axis.yaxis.get_minorticklines())

    for tick in ticks:
        tick.set_color('#' + color + '3D')


def _monkey_patch_figure(color, Figure):
    """ Style a figure's current axis tick marks, just after the figure is
    created. """
    def _patch(*args, **kwargs):
        fig = Figure(*args, **kwargs)
        _style_ticks(fig.gca, color)
        return fig
    return _patch


def _monkey_patch_subplot(color, subplot):
    """ Style all axes of a figure containing subplots, just after the
    figure is created. """
    def _patch(*args, **kwargs):
        fig, axes = subplot(*args, **kwargs)
        axes_list = [axes] if isinstance(axes, matplotlib.axes.Axes) else axes
        for ax in axes_list:
            if isinstance(ax, matplotlib.axes.Axes):
                _style_ticks(ax, color)
            else:
                for each in ax:
                    _style_ticks(each, color)
        return fig, axes
    return _patch