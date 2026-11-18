import { Link } from "react-router-dom";
import PriorityBadge from "./PriorityBadge";
import StatusBadge from "./StatusBadge";

const NEXT_STATUS = {
  Open: "In Progress",
  "In Progress": "Resolved",
  Resolved: "Closed",
  Closed: null,
};

export default function TicketTable({ tickets, mode = "employee", onAdvance }) {
  if (!tickets.length) {
    return (
      <div className="empty-state">
        <span aria-hidden="true">◎</span>
        <strong>No tickets to display</strong>
        <p>Try a different filter or create a new ticket.</p>
      </div>
    );
  }

  const basePath = mode === "support" ? "/support/tickets" : "/employee/tickets";

  return (
    <div className="table-wrap">
      <table className="ticket-table">
        <thead>
          <tr>
            <th scope="col">Ticket</th>
            <th scope="col">Category</th>
            <th scope="col">Priority</th>
            <th scope="col">Status</th>
            {mode === "support" && <th scope="col">Created by</th>}
            <th scope="col">Created</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((ticket) => {
            const next = NEXT_STATUS[ticket.status];
            return (
              <tr key={ticket.id}>
                <td data-label="Ticket">
                  <div className="ticket-cell">
                    <Link to={`${basePath}/${ticket.id}`} className="ticket-link">
                      {ticket.title}
                    </Link>
                    <span className="ticket-id">#{ticket.id}</span>
                  </div>
                </td>
                <td data-label="Category">{ticket.category}</td>
                <td data-label="Priority">
                  <PriorityBadge priority={ticket.priority} />
                </td>
                <td data-label="Status">
                  <StatusBadge status={ticket.status} />
                </td>
                {mode === "support" && <td data-label="Created by">{ticket.created_by}</td>}
                <td data-label="Created">{ticket.created_at}</td>
                <td data-label="Actions">
                  <div className="row-actions">
                    <Link to={`${basePath}/${ticket.id}`} className="button tiny">
                      View
                    </Link>
                    {mode === "employee" && ticket.status !== "Closed" && (
                      <Link to={`${basePath}/${ticket.id}/edit`} className="button tiny secondary">
                        Edit
                      </Link>
                    )}
                    {mode === "support" && next && onAdvance && (
                      <button
                        type="button"
                        className="button tiny accent"
                        onClick={() => onAdvance(ticket.id, next)}
                      >
                        Move to {next}
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
