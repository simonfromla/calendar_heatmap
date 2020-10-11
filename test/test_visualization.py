import json
import os
import unittest
from datetime import datetime

import arrow

from calendar_heatmap.calendar_heatmap import CalendarHeatmap


class CalendarHeatmapTests(unittest.TestCase):

    def setUp(self):
        with open('test/mock_user_events.json', 'r') as fp:
            self.mock_user_events_response = json.loads(fp.read())

    def test_calendarheatmap(self):
        user_events, start_date, end_date = self.mock_user_events_response, arrow.get(datetime(2018, 7, 30, 10, 20)), arrow.get(datetime(2018, 8, 5, 10, 20))
        calendarheatmap = CalendarHeatmap("Asia/Seoul", start_date, end_date, user_events)
        figure = calendarheatmap.build_heatmap()
        calendarheatmap.save_as_image(figure)
        filepath = calendarheatmap.image_filepath
        self.assertTrue(os.path.isfile(filepath))

if __name__ == '__main__':
    unittest.main()