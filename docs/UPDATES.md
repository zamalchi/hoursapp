<a name="updates"></a>
### UPDATES
- **added back and forward arrows for navigating day to day**
- dependency: `markdown` python package
- bugfix: adjacent-record overlap fixed (was adding instead of subtracting)
- bugfix: start/end time popup suppressed for entries w/o a leading 0 (ex. 830, 8:30)
- An alert will popup if a start or end time exceeds its logical limit (can't exceed an entire adjacent record)
- Check added for ensuring a record has a positive duration (will refresh the page on submit if invalid)
- Trying to submit a record with invalid times will refresh the page and insert the notes into the notes form field
- Deleting a record will copy its notes into the record form at that index (useful for adjusting an existing record)
- Pattern regex added for labels (only labels in the list can be used)
- New file `config/settings`
- Billable/Emergency elements can now be focused and toggled with space/enter
- Each record now has an anchor tag : editing a record will reload the page anchored at the record

