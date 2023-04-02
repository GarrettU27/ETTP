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

    def __init__(self, ecg_data, sample_rate=500, title='ECG 12', columns=4, row_height=6):
        super().__init__()

        self.lead_order = list(range(0, len(ecg_data)))
        self.sections = len(ecg_data[0]) / sample_rate
        self.leads = len(self.lead_order)
        self.rows = int(ceil(self.leads / columns))

        self.fig, self.ax = plt.subplots(
            figsize=(self.sections * columns * self.display_factor, self.rows * row_height / 5 * self.display_factor))
        self.fig.subplots_adjust(
            hspace=0,
            wspace=0,
            left=0,  # the left side of the subplots of the figure
            right=1,  # the right side of the subplots of the figure
            bottom=0,  # the bottom of the subplots of the figure
            top=1
        )
        self.fig.suptitle(title)

        self.canvas = FigureCanvasQTAgg(self.fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)

        self.update_plot(ecg_data)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plot(self, ecg_data):
        self.ax.cla()
        self.plot_ecg(ecg_data)
        self.canvas.draw()

    def plot_ecg(self, ecg_data, sample_rate=500, columns=4, row_height=6):
        self.setup_grid(columns, row_height)

        display_factor = self.display_factor ** 0.5
        color_line = (0, 0, 0)

        for column in range(0, columns):
            for row in range(0, self.rows):
                if column * self.rows + row < self.leads:
                    y_offset = -(row_height / 2) * ceil(row % self.rows)
                    x_offset = 0
                    t_lead = self.lead_order[column * self.rows + row]

                    if column > 0:
                        x_offset = self.sections * column
                        self.ax.plot([x_offset, x_offset],
                                     [ecg_data[t_lead][0] + y_offset - 0.3, ecg_data[t_lead][0] + y_offset + 0.3],
                                     linewidth=self.line_width * display_factor, color=color_line)

                    step = 1.0 / sample_rate
                    self.ax.text(x_offset + 0.07, y_offset - 0.5, self.lead_index[t_lead], fontsize=9 * display_factor)
                    self.ax.plot(
                        np.arange(0, len(ecg_data[t_lead]) * step, step) + x_offset,
                        ecg_data[t_lead] + y_offset,
                        linewidth=self.line_width * display_factor,
                        color=color_line
                    )

    def setup_grid(self, columns=4, row_height=6):
        color_major = (1, 0, 0)
        color_minor = (1, 0.7, 0.7)

        x_min = 0
        x_max = columns * self.sections
        y_min = row_height / 4 - (self.rows / 2) * row_height
        y_max = row_height / 4

        self.ax.set_xticks(np.arange(x_min, x_max, 0.2))
        self.ax.set_yticks(np.arange(y_min, y_max, 0.5))

        self.ax.minorticks_on()

        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', linestyle='-', linewidth=0.5 * self.display_factor, color=color_major)
        self.ax.grid(which='minor', linestyle='-', linewidth=0.5 * self.display_factor, color=color_minor)

        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlim(x_min, x_max)