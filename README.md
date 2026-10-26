# Campus Complaint Tracker — DAA Project

This project follows the Campus Complaint Tracker requirements in the RGUKT Ongole DAA Project Assignment.

## Features
- Add maintenance complaints with automatic ticket IDs.
- Suggest possible duplicates only when category and location match and word-set similarity is at least 40%.
- Search complaints by location or description.
- Update ticket status and preserve a timestamped history of every update.
- Display open complaint counts by category and the age of the oldest open complaint.
- **Extension:** assign a technician and filter tickets by technician.
- Saves records in `07_complaint_tracker/data.json`.

## Requirements
- Python 3.10 or later
- A modern browser
- No third-party packages required

## Run on Ubuntu / Linux
Open a terminal in the `Campus_Complaint_Tracker` folder and run:

```bash
python3 07_complaint_tracker/app.py
```

Keep the terminal open and open `http://127.0.0.1:8000` in your browser. Stop the app with `Ctrl+C`.

If port 8000 is busy:

```bash
PORT=8001 python3 07_complaint_tracker/app.py
```

Then open `http://127.0.0.1:8001`.

## Example
1. Submit `Electrical`, `Block A`, `Fan is not working in room 12`.
2. Submit the same category, location, and description again. The app should suggest the earlier ticket.
3. Update ticket 1 to `In progress` with comment `Assigned to technician`.
4. Update it to `Resolved` with comment `Fan repaired`.
5. View ticket 1 history to see the creation and both updates.

## Tests to document
1. Valid complaint creates a ticket with Pending status.
2. Same category/location and identical description suggests a duplicate.
3. Same description in a different location does not suggest a duplicate.
4. Two updates remain in history.
5. Resolved tickets are omitted from the open summary and duplicate suggestions.
6. Unknown ticket number shows a readable error.
7. Restart the app and confirm tickets/history remain in `data.json`.
8. Technician filter shows only matching assignees.

## Notes
This is a local single-operator classroom prototype, not a multi-user campus service. Use fictional sample data.
