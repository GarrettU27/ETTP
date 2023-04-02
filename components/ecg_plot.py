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
    line_width = 1

    def __init__(self, title='ECG 12'):
        super().__init__()

        self.fig, self.ax = plt.subplots()
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

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_ecg(self, ecg_data, sample_rate=500, number_of_columns=4, row_height=6):
        self.ax.cla()

        total_sections = len(ecg_data[0]) / sample_rate
        total_leads = len(ecg_data)
        total_rows = int(ceil(total_leads / number_of_columns))

        self.setup_grid(total_sections, total_rows, number_of_columns, row_height)

        color_line = (0, 0, 0)

        for current_column_number in range(0, number_of_columns):
            for current_row_number in range(0, total_rows):

                current_lead_number = current_column_number * total_rows + current_row_number
                if current_lead_number < total_leads:
                    y_offset = -(row_height / 2) * ceil(current_row_number % total_rows)
                    x_offset = 0
                    current_lead = ecg_data[current_lead_number]

                    if current_column_number > 0:
                        x_offset = total_sections * current_column_number
                        self.create_separator_line(x_offset, current_lead[0] + y_offset)

                    step = 1.0 / sample_rate
                    self.ax.text(x_offset + 0.07, y_offset - 0.5, self.lead_index[current_lead_number], fontsize=9)
                    self.ax.plot(
                        np.arange(0, len(current_lead) * step, step) + x_offset,
                        ecg_data[current_lead_number] + y_offset,
                        linewidth=self.line_width,
                        color=color_line
                    )

        self.canvas.draw()

    def setup_grid(self, total_sections, total_rows, total_columns=4, row_height=6):
        color_major = (1, 0, 0)
        color_minor = (1, 0.7, 0.7)

        x_min = 0
        x_max = total_columns * total_sections
        y_min = row_height / 4 - (total_rows / 2) * row_height
        y_max = row_height / 4

        self.ax.set_xticks(np.arange(x_min, x_max, 0.2))
        self.ax.set_yticks(np.arange(y_min, y_max, 0.5))

        self.ax.minorticks_on()

        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])

        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        self.ax.grid(which='major', linestyle='-', linewidth=0.5, color=color_major)
        self.ax.grid(which='minor', linestyle='-', linewidth=0.5, color=color_minor)

        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlim(x_min, x_max)

    def create_separator_line(self, x_offset, y_offset):
        separator_line_height = 0.6
        separator_color = (0, 0, 0)

        self.ax.plot([x_offset, x_offset],
                     [y_offset - separator_line_height / 2, y_offset + separator_line_height / 2],
                     linewidth=self.line_width, color=separator_color)
