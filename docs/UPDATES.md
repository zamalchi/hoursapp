An alert will popup if a start or end time exceeds its logical limit (can't exceed an entire adjacent record)
Check added for ensuring a record has a positive duration (will refresh the page on submit if invalid)
Trying to submit a record with invalid times will refresh the page and insert the notes into the notes form field
Deleting a record will copy its notes into the record form at that index (useful for adjusting an existing record)
Pattern regex added for labels (only labels in the list can be used)
New file [config/settings] : newline-separated fields in the format [name=value]
Changeable server address:port fields added (sources address:port from [config/settings] : [loggingServerAddress=0.0.0.0] and [loggingServerPort=1234])
Emailing functionality added back (sources addresses from [config/settings] : [sender=foo] and [receivers=foo,bar])
Billable/Emergency elements can now be focused and toggled with space/enter
Each record now has an anchor tag : editing a record will reload the page anchored at the record
