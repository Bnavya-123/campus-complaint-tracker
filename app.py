"""Campus Complaint Tracker: ticketing, duplicate suggestions, history and open summary."""
import sys
import re
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import Store, form, heading, note, table, run

CATEGORIES = ["Electrical", "Water", "Network", "Other"]
STATUSES = ["Pending", "In progress", "Resolved"]
store = Store(Path(__file__).with_name("data.json"), {"tickets": []})


def duplicates(candidate, tickets):
    """Suggest unresolved tickets with same category/location and >= 40% word overlap."""
    words = set(re.findall(r"\w+", candidate["description"].lower()))
    results = []
    for ticket in tickets:
        if ticket["status"] == "Resolved":
            continue
        if any(ticket[key].lower() != candidate[key].lower() for key in ("category", "location")):
            continue
        other = set(re.findall(r"\w+", ticket["description"].lower()))
        union = words | other
        score = len(words & other) / len(union) if union else 0
        if score >= 0.4:
            results.append([ticket["id"], ticket["description"], f"{score:.0%} word overlap"])
    return results


def view():
    out = note("Use sample maintenance complaints. Each status update is added to the ticket history.")
    out += form("add", [
        ("category", "Category", "select", CATEGORIES),
        ("location", "Location", "text", "Block A"),
        ("description", "Complaint description", "textarea", "Fan is not working in room 12"),
        ("assignee", "Assigned technician (extension)", "text", "Not assigned"),
    ], "Submit complaint")
    out += form("search", [("query", "Search location or complaint text", "text", "fan")], "Search")
    out += form("update", [
        ("id", "Ticket number", "number", "1"),
        ("status", "Status", "select", STATUSES),
        ("comment", "Update comment", "text", "Assigned to technician"),
        ("assignee", "Assigned technician (extension)", "text", "Not assigned"),
    ], "Record update")
    out += form("history", [("id", "Ticket number", "number", "1")], "View history")
    out += form("assignee_search", [("assignee", "Filter by technician", "text", "Not assigned")],
                "Filter by technician")

    tickets = store.data["tickets"]
    rows = [[t["id"], t["category"], t["location"], t["description"], t["status"],
             t["assignee"], t["created"]] for t in tickets]
    out += heading("All complaints")
    out += table(["Ticket", "Category", "Location", "Description", "Status", "Technician", "Created"], rows)

    out += heading("Open complaint summary")
    summary = {}
    for ticket in tickets:
        if ticket["status"] != "Resolved":
            category = ticket["category"]
            age = (date.today() - date.fromisoformat(ticket["created"])).days
            count, oldest = summary.get(category, (0, 0))
            summary[category] = (count + 1, max(oldest, age))
    out += table(["Category", "Open tickets", "Oldest age in days"],
                 [[category, *values] for category, values in sorted(summary.items())])
    return out


def handle(data):
    tickets = store.data["tickets"]
    action = data.get("action")

    if action == "add":
        category = data["category"]
        location = data["location"].strip()
        description = data["description"].strip()
        assignee = data.get("assignee", "").strip() or "Not assigned"
        if category not in CATEGORIES or not location or not description:
            raise ValueError("Enter a valid category, location and complaint.")
        ticket = {
            "id": max((t["id"] for t in tickets), default=0) + 1,
            "category": category,
            "location": location,
            "description": description,
            "status": "Pending",
            "created": date.today().isoformat(),
            "assignee": assignee,
            "history": [[datetime.now().isoformat(timespec="seconds"), "Pending", "Ticket created"]],
        }
        possible = duplicates(ticket, tickets)
        tickets.append(ticket)
        store.save()
        return heading("Possible earlier complaints") + table(["Ticket", "Description", "Similarity"], possible)

    if action == "search":
        query = data["query"].strip().lower()
        if not query:
            raise ValueError("Enter a word or location to search.")
        rows = [[t["id"], t["location"], t["description"], t["status"]] for t in tickets
                if query in (t["location"] + " " + t["description"]).lower()]
        return heading("Search results") + table(["Ticket", "Location", "Description", "Status"], rows)

    if action == "assignee_search":
        query = data["assignee"].strip().lower()
        rows = [[t["id"], t["category"], t["location"], t["description"], t["status"], t["assignee"]]
                for t in tickets if query in t.get("assignee", "").lower()]
        return heading("Technician filter results") + table(
            ["Ticket", "Category", "Location", "Description", "Status", "Technician"], rows)

    try:
        ticket_id = int(data.get("id", ""))
    except ValueError:
        raise ValueError("Ticket number must be an integer.")
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if ticket is None:
        raise ValueError("Ticket does not exist.")

    if action == "history":
        return heading(f"History for ticket {ticket_id}") + table(
            ["Time", "Status", "Comment"], ticket["history"])

    if action == "update":
        status = data["status"]
        comment = data["comment"].strip()
        assignee = data.get("assignee", "").strip() or "Not assigned"
        if status not in STATUSES or not comment:
            raise ValueError("Choose a valid status and enter a comment.")
        ticket["status"] = status
        ticket["assignee"] = assignee
        ticket["history"].append([datetime.now().isoformat(timespec="seconds"), status, comment])
        store.save()
        return None

    raise ValueError("Unknown action.")


if __name__ == "__main__":
    run("Campus Complaint Tracker", view, handle)
