import datetime

import arrow
import numpy as np
import pandas as pd
from dateutil import tz


class CalendarHeatmap:

    week_index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    time_columns = ["09:00", "09:15", "09:30", "09:45", "10:00",
                    "10:15", "10:30", "10:45", "11:00", "11:15",
                    "11:30", "11:45", "12:00", "12:15", "12:30",
                    "12:45", "13:00", "13:15", "13:30", "13:45",
                    "14:00", "14:15", "14:30", "14:45", "15:00",
                    "15:15", "15:30", "15:45", "16:00", "16:15",
                    "16:30", "16:45", "17:00", "17:15", "17:30",
                    "17:45", "18:00", "18:15", "18:30", "18:45",
                    "19:00", "19:15", "19:30", "19:45", "20:00"]

    def __init__(self, timezone, start_date, end_date, user_schedule):
        self.timezone = timezone
        self.start_date = str(start_date.date())
        self.start_date_day = self.week_index[start_date.isoweekday()]
        self.end_date = str(end_date.date())
        self.user_schedule = user_schedule

    def is_weeklong(self, start_date, end_date):
        if start_date == end_date:
            return False
        return True

    def get_increments(self, hours, minutes):
        fifteen_minute_increments = 0
        if minutes:
            fifteen_minute_increments += minutes / 15
        if hours:
            fifteen_minute_increments += hours * 4
        return fifteen_minute_increments

    def round_time(self, non_rounded_time, base=15):
        minutes = non_rounded_time[-2:]
        rounded_minutes = str(int(base * round(float(minutes) / base)))
        if rounded_minutes == "0":
            rounded_minutes = "00"
        rounded_time = non_rounded_time[0:3] + rounded_minutes
        return rounded_time

    def formatter(self, list_events):
        for user_event in list_events:

            start_time = arrow.get(user_event["startTime"] / 1000)
            start_time = start_time.to(tz.gettz(self.timezone))

            end_time = arrow.get(user_event["endTime"] / 1000)
            end_time = end_time.to(tz.gettz(self.timezone))

            diff = end_time - start_time
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            increments = self.get_increments(hours, minutes)
            weekday = start_time.weekday()
            military_time = start_time.strftime("%H:%M")
            if military_time[-2:] not in set(["00", "15", "30", "45"]):
                military_time = self.round_time(military_time)

            if military_time not in set(self.time_columns) or weekday not in range(0, 5):
                continue

            yield int(weekday), str(military_time), int(increments)

    def build_heatmap(self):
        is_weekly = self.is_weeklong(self.start_date, self.end_date)

        df = self.build_dataframe(self.user_schedule, is_weekly)
        heatmap_figure = self.graph_data(df)
        return heatmap_figure

    def build_dataframe(self, user_event, is_weekly):
        matrix = self.build_matrix(user_event, is_weekly)
        if is_weekly:
            df = pd.DataFrame(matrix, columns=self.time_columns, index=self.week_index[:5])
        else:
            df = pd.DataFrame(matrix,
                              columns=self.time_columns,
                              index=[", ".join([self.start_date_day, self.start_date])])
        return df

    def build_matrix(self, list_events, is_weekly):
        if is_weekly:
            matrix = np.zeros((5, 45))
            for weekday, military_time, increments in self.formatter(list_events):
                time_idx = self.time_columns.index(military_time)
                matrix[weekday][time_idx:time_idx + increments] = 1
            return matrix
        else:
            matrix = np.zeros((1, 45))
            for weekday, military_time, increments in self.formatter(list_events):
                time_idx = self.time_columns.index(military_time)
                matrix[0][time_idx:time_idx + increments] = 1
            return matrix

    def graph_data(self, dataframe):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns

        figure, ax = plt.subplots(figsize=(15, 3))
        sns.heatmap(dataframe, linewidths=0, square=True, cbar=False, cmap=["#f7f7d7", "#923192"], ax=ax, xticklabels=2)
        ax.hlines([1, 2, 3, 4], *ax.get_xlim(), colors='w', linestyles='solid')
        ax.yaxis.set_ticks_position('none')
        plt.yticks(rotation=0)
        plt.xticks(rotation=45)
        return figure

    def save_as_image(self, figure):
        format_now = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
        image_filepath = f'/tmp/{format_now}.png'
        figure.savefig(image_filepath, bbox_inches='tight')
        self.image_filepath = image_filepath
        return None
