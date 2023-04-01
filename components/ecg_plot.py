# code pulled from https://github.com/dy1901/ecg_plot

from math import ceil

import matplotlib
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.ticker import AutoMinorLocator

matplotlib.use('QtAgg')


class ECGPlot(QWidget):
    lead_index = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    display_factor = 1
    line_width = 1

    def __init__(self, ecg, sample_rate=500, title='ECG 12', columns=4, row_height=6):
        super().__init__()

        fig = self.plot_ecg(ecg, sample_rate, title, columns, row_height)
        canvas = FigureCanvasQTAgg(fig)
        toolbar = NavigationToolbar2QT(canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        self.setLayout(layout)

    def plot_ecg(self, ecg, sample_rate=500, title='ECG 12', columns=4, row_height=6):
        lead_order = list(range(0, len(ecg)))
        sections = len(ecg[0]) / sample_rate
        leads = len(lead_order)
        rows = int(ceil(leads / columns))

        fig, ax = plt.subplots(
            figsize=(sections * columns * self.display_factor, rows * row_height / 5 * self.display_factor))
        fig.subplots_adjust(
            hspace=0,
            wspace=0,
            left=0,  # the left side of the subplots of the figure
            right=1,  # the right side of the subplots of the figure
            bottom=0,  # the bottom of the subplots of the figure
            top=1
        )

        display_factor = self.display_factor ** 0.5

        fig.suptitle(title)

        x_min = 0
        x_max = columns * sections
        y_min = row_height / 4 - (rows / 2) * row_height
        y_max = row_height / 4

        color_major = (1, 0, 0)
        color_minor = (1, 0.7, 0.7)
        color_line = (0, 0, 0)

        ax.set_xticks(np.arange(x_min, x_max, 0.2))
        ax.set_yticks(np.arange(y_min, y_max, 0.5))

        ax.minorticks_on()

        ax.set_yticklabels([])
        ax.set_xticklabels([])

        ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)

        ax.set_ylim(y_min, y_max)
        ax.set_xlim(x_min, x_max)

        for column in range(0, columns):
            for row in range(0, rows):
                if column * rows + row < leads:
                    y_offset = -(row_height / 2) * ceil(row % rows)
                    x_offset = 0
                    t_lead = lead_order[column * rows + row]

                    if column > 0:
                        x_offset = sections * column
                        ax.plot([x_offset, x_offset],
                                [ecg[t_lead][0] + y_offset - 0.3, ecg[t_lead][0] + y_offset + 0.3],
                                linewidth=self.line_width * display_factor, color=color_line)

                    step = 1.0 / sample_rate
                    ax.text(x_offset + 0.07, y_offset - 0.5, self.lead_index[t_lead], fontsize=9 * display_factor)
                    ax.plot(
                        np.arange(0, len(ecg[t_lead]) * step, step) + x_offset,
                        ecg[t_lead] + y_offset,
                        linewidth=self.line_width * display_factor,
                        color=color_line
                    )
        return fig
