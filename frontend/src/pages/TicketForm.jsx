import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client";
import Alert from "../components/Alert";

const CATEGORIES = ["Hardware", "Software", "Network", "Access", "Other"];
const PRIORITIES = ["Low", "Medium", "High"];
const EMPTY = { title: "", description: "", category: "Hardware", priority: "Low" };

export default function TicketForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [form, setForm] = useState(EMPTY);
  const [loading, setLoading] = useState(isEdit);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [ticketStatus, setTicketStatus] = useState("");

  useEffect(() => {
    if (!isEdit) return;
    let active = true;
    setLoading(true);
    api
      .ticket(id)
      .then((ticket) => {
        if (!active) return;
        setForm({
          title: ticket.title,
          description: ticket.description,
          category: ticket.category,
          priority: ticket.priority,
        });
        setTicketStatus(ticket.status);
      })
      .catch((err) => {
        if (active) setError(err.message || "Unable to load ticket.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [id, isEdit]);

  const closed = ticketStatus === "Closed";
  const canSubmit = useMemo(() => !submitting && !closed, [submitting, closed]);

  const update = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }));
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      if (isEdit) {
        await api.updateTicket(id, form);
        navigate(`/employee/tickets/${id}`, { replace: true });
      } else {
        const created = await api.createTicket(form);
        navigate(`/employee/tickets/${created.id}`, { replace: true });
      }
    } catch (err) {
      setError(err.message || "Unable to save ticket.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="panel loading-panel">Loading ticket...</div>;
  }

  return (
    <div className="page-stack narrow">
      <section className="page-header">
        <div>
          <p className="eyebrow">Employee workspace</p>
          <h1>{isEdit ? "Edit ticket" : "Create ticket"}</h1>
          <p className="muted">
            {isEdit
              ? "Update the title, description, category, or priority. Closed tickets cannot be edited."
              : "Provide clear details so support staff can help quickly."}
          </p>
        </div>
        <div className="header-actions">
          <Link to={isEdit ? `/employee/tickets/${id}` : "/employee"} className="button ghost">
            Cancel
          </Link>
        </div>
      </section>

      {error && (
        <Alert type="error" title="Could not save ticket">
          {error}
        </Alert>
      )}
      {closed && (
        <Alert type="warning" title="Closed ticket">
          This ticket is closed and cannot be edited.
        </Alert>
      )}

      <section className="panel">
        <form className="form-grid" onSubmit={onSubmit}>
          <label className="field">
            <span>Title</span>
            <input
              type="text"
              value={form.title}
              onChange={update("title")}
              maxLength={100}
              placeholder="Brief summary of the issue"
              required
              disabled={closed}
            />
            <small className="hint">{form.title.trim().length}/100 characters</small>
          </label>

          <label className="field">
            <span>Description</span>
            <textarea
              rows={7}
              value={form.description}
              onChange={update("description")}
              maxLength={2000}
              placeholder="Describe what happened, what you expected, and any details that help."
              required
              disabled={closed}
            />
            <small className="hint">{form.description.trim().length}/2,000 characters</small>
          </label>

          <div className="form-grid two">
            <label className="field">
              <span>Category</span>
              <select value={form.category} onChange={update("category")} disabled={closed} required>
                {CATEGORIES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>Priority</span>
              <select value={form.priority} onChange={update("priority")} disabled={closed} required>
                {PRIORITIES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="form-actions">
            <button type="submit" className="button primary" disabled={!canSubmit}>
              {submitting ? "Saving..." : isEdit ? "Save changes" : "Create ticket"}
            </button>
            <Link to={isEdit ? `/employee/tickets/${id}` : "/employee/tickets"} className="button ghost">
              Back
            </Link>
          </div>
        </form>
      </section>
    </div>
  );
}
