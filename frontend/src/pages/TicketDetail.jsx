import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import Alert from "../components/Alert";
import PriorityBadge from "../components/PriorityBadge";
import StatusBadge from "../components/StatusBadge";

const NEXT_STATUS = {
  Open: "In Progress",
  "In Progress": "Resolved",
  Resolved: "Closed",
  Closed: null,
};

export default function TicketDetail() {
  const { id } = useParams();
  const { isEmployee } = useAuth();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [advancing, setAdvancing] = useState(false);

  const basePath = isEmployee ? "/employee/tickets" : "/support/tickets";
  const workspacePath = isEmployee ? "/employee" : "/support";

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      setTicket(await api.ticket(id));
    } catch (err) {
      setError(err.message || "Unable to load ticket.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [id]);

  const advance = async () => {
    const next = NEXT_STATUS[ticket.status];
    if (!next) return;
    setActionError("");
    setAdvancing(true);
    try {
      setTicket(await api.updateStatus(id, next));
    } catch (err) {
      setActionError(err.message || "Unable to update status.");
    } finally {
      setAdvancing(false);
    }
  };

  if (loading) {
    return <div className="panel loading-panel">Loading ticket...</div>;
  }

  if (error || !ticket) {
    return (
      <div className="page-stack narrow">
        <Alert type="error" title="Ticket unavailable">
          {error}
        </Alert>
        <Link to={basePath} className="button secondary">
          Back to tickets
        </Link>
      </div>
    );
  }

  const next = NEXT_STATUS[ticket.status];

  return (
    <div className="page-stack">
      <section className="page-header">
        <div>
          <p className="eyebrow">Ticket #{ticket.id}</p>
          <h1>{ticket.title}</h1>
          <div className="detail-badges">
            <StatusBadge status={ticket.status} />
            <PriorityBadge priority={ticket.priority} />
            <span className="badge neutral">{ticket.category}</span>
          </div>
        </div>
        <div className="header-actions">
          <Link to={workspacePath} className="button ghost">
            Dashboard
          </Link>
          <Link to={basePath} className="button secondary">
            Back to tickets
          </Link>
          {isEmployee && ticket.status !== "Closed" && (
            <Link to={`${basePath}/${ticket.id}/edit`} className="button primary">
              Edit ticket
            </Link>
          )}
          {!isEmployee && next && (
            <button type="button" className="button primary" onClick={advance} disabled={advancing}>
              {advancing ? "Updating..." : `Move to ${next}`}
            </button>
          )}
        </div>
      </section>

      {actionError && (
        <Alert type="error" title="Status update failed">
          {actionError}
        </Alert>
      )}

      <section className="panel">
        <h2>Description</h2>
        <p className="description-text">{ticket.description}</p>
      </section>

      <section className="panel">
        <h2>Ticket details</h2>
        <dl className="detail-grid">
          <div>
            <dt>Category</dt>
            <dd>{ticket.category}</dd>
          </div>
          <div>
            <dt>Priority</dt>
            <dd>
              <PriorityBadge priority={ticket.priority} />
            </dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>
              <StatusBadge status={ticket.status} />
            </dd>
          </div>
          <div>
            <dt>Created by</dt>
            <dd>{ticket.created_by}</dd>
          </div>
          <div>
            <dt>Created date</dt>
            <dd>{ticket.created_at}</dd>
          </div>
          <div>
            <dt>Last updated date</dt>
            <dd>{ticket.updated_at}</dd>
          </div>
        </dl>
      </section>
    </div>
  );
}
