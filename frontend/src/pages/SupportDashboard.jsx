import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import Alert from "../components/Alert";
import StatCard from "../components/StatCard";

export default function SupportDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      setData(await api.supportDashboard());
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
          <p className="eyebrow">Support staff workspace</p>
          <h1>Dashboard</h1>
          <p className="muted">Review all employee requests and keep statuses moving forward.</p>
        </div>
        <div className="header-actions">
          <Link to="/support/tickets" className="button primary">
            Manage tickets
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
          <section className="stats-grid" aria-label="Ticket summary">
            <StatCard label="Total tickets" value={data.total} tone="primary" />
            <StatCard label="Open" value={data.open} tone="open" />
            <StatCard label="In progress" value={data.in_progress} tone="progress" />
            <StatCard label="Resolved" value={data.resolved} tone="resolved" />
            <StatCard label="Closed" value={data.closed} tone="closed" />
          </section>
        )
      )}
    </div>
  );
}
