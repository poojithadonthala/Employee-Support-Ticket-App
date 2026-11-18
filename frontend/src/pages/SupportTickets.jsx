import { useEffect, useState } from "react";
import { api } from "../api/client";
import Alert from "../components/Alert";
import TicketTable from "../components/TicketTable";

const EMPTY_FILTERS = { search: "", status: "", category: "", priority: "" };

export default function SupportTickets() {
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [applied, setApplied] = useState(EMPTY_FILTERS);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");

  const load = async (nextFilters = applied) => {
    setLoading(true);
    setError("");
    try {
      setTickets(await api.supportTickets(nextFilters));
    } catch (err) {
      setError(err.message || "Unable to load tickets.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load(EMPTY_FILTERS);
  }, []);

  const update = (field) => (event) => {
    setFilters((current) => ({ ...current, [field]: event.target.value }));
  };

  const apply = (event) => {
    event.preventDefault();
    setApplied(filters);
    load(filters);
  };

  const clear = () => {
    setFilters(EMPTY_FILTERS);
    setApplied(EMPTY_FILTERS);
    load(EMPTY_FILTERS);
  };

  const advance = async (id, nextStatus) => {
    setActionError("");
    try {
      await api.updateStatus(id, nextStatus);
      await load(applied);
    } catch (err) {
      setActionError(err.message || "Unable to update status.");
    }
  };

  return (
    <div className="page-stack">
      <section className="page-header">
        <div>
          <p className="eyebrow">Support staff workspace</p>
          <h1>All tickets</h1>
          <p className="muted">Search, filter, and advance tickets one step at a time.</p>
        </div>
        <div className="header-actions">
          <button type="button" className="button ghost" onClick={() => load(applied)}>
            Refresh
          </button>
        </div>
      </section>

      {error && (
        <Alert type="error" title="Could not load tickets">
          {error}
        </Alert>
      )}
      {actionError && (
        <Alert type="error" title="Status update failed">
          {actionError}
        </Alert>
      )}

      <section className="panel">
        <form className="filter-bar" onSubmit={apply}>
          <label className="field compact-field">
            <span>Search</span>
            <input
              type="search"
              value={filters.search}
              onChange={update("search")}
              placeholder="Title, description, or creator"
            />
          </label>
          <label className="field compact-field">
            <span>Status</span>
            <select value={filters.status} onChange={update("status")}>
              <option value="">All statuses</option>
              <option value="Open">Open</option>
              <option value="In Progress">In Progress</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
          </label>
          <label className="field compact-field">
            <span>Category</span>
            <select value={filters.category} onChange={update("category")}>
              <option value="">All categories</option>
              <option value="Hardware">Hardware</option>
              <option value="Software">Software</option>
              <option value="Network">Network</option>
              <option value="Access">Access</option>
              <option value="Other">Other</option>
            </select>
          </label>
          <label className="field compact-field">
            <span>Priority</span>
            <select value={filters.priority} onChange={update("priority")}>
              <option value="">All priorities</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </label>
          <div className="filter-actions">
            <button type="submit" className="button primary">
              Apply filters
            </button>
            <button type="button" className="button ghost" onClick={clear}>
              Clear
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        {loading ? (
          <div className="loading-panel">Loading tickets...</div>
        ) : (
          <TicketTable tickets={tickets} mode="support" onAdvance={advance} />
        )}
      </section>
    </div>
  );
}
