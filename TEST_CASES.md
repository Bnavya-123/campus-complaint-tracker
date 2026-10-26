# Test Cases — Campus Complaint Tracker

| No. | Test | Expected result |
|---|---|---|
| 1 | Add a valid complaint | A new ticket is created with Pending status and a creation-history entry. |
| 2 | Add the same unresolved complaint in the same category and location | Possible earlier ticket appears with 100% overlap. |
| 3 | Add same words but a different location | No duplicate suggestion. |
| 4 | Update a ticket twice | Both timestamped updates remain in its history. |
| 5 | Resolve a ticket | It disappears from open summary and future duplicate suggestions. |
| 6 | Enter an unknown ticket number | A readable “Ticket does not exist” error appears. |
| 7 | Restart the app | Tickets and history are loaded from data.json. |
| 8 | Filter by technician | Only tickets assigned to the matching technician appear. |
