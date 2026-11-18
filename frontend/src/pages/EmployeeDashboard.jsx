import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import Alert from "../components/Alert";
import StatCard from "../components/StatCard";
import TicketTable from "../components/TicketTable";

export default function EmployeeDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      setData(await api.employeeDashboard());
    } catch (err) {
      setError(err.message || "Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="page-stack">
      <section className="page-header">
        <div>
          <p className="eyebrow">Employee workspace</p>
          <h1>Dashboard</h1>
          <p className="muted">Track your requests and see the latest updates at a glance.</p>
        </div>
        <div className="header-actions">
          <Link to="/employee/tickets/new" className="button primary">
            Create ticket
          </Link>
          <button type="button" className="button ghost" onClick={load}>
            Refresh
          </button>
        </div>
      </section>

      {error && (
        <Alert type="error" title="Could not load dashboard">
          {error}
        </Alert>
      )}

      {loading ? (
        <div className="panel loading-panel">Loading dashboard...</div>
      ) : (
        data && (
          <>
            <section className="stats-grid" aria-label="Ticket summary">
              <StatCard label="Total tickets" value={data.total} tone="primary" />
              <StatCard label="Open" value={data.open} tone="open" />
              <StatCard label="In progress" value={data.in_progress} tone="progress" />
              <StatCard label="Resolved" value={data.resolved} tone="resolved" />
              <StatCard label="Closed" value={data.closed} tone="closed" />
            </section>

            <section className="panel">
              <div className="panel-header">
                <div>
                  <h2>Recent tickets</h2>
                  <p className="muted">Your latest 5 tickets by created date, newest first.</p>
                </div>
                <Link to="/employee/tickets" className="button secondary">
                  View all tickets
                </Link>
              </div>
              <TicketTable tickets={data.recent_tickets} mode="employee" />
            </section>
          </>
        )
      )}
    </div>
  );
}
