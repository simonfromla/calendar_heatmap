# Calendar_heatmap
Graph a collection of UNIX timestamped calendar events into a weekly heatmap.  

# Usage  
Script requires user to feed a JSON list of objects with `startTime` and `endTime` containing values in 13-digit UNIX timestamp format.  
See `test/mock_user_events.json` for an example.  

Provide a timezone, `start_date` and `end_date` UNIX timestamp, and the JSON list of events to the `CalendarHeatmap` object.  

### Example
```
calendarheatmap = CalendarHeatmap("Asia/Seoul", start_date, end_date, user_events)
figure = calendarheatmap.build_heatmap()
calendarheatmap.save_as_image(figure)
filepath = calendarheatmap.image_filepath
```

![Example 1](https://imgur.com/Iqc3swa.png)
![Example](https://imgur.com/yMbl4aG.png)
