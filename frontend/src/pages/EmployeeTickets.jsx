import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import Alert from "../components/Alert";
import TicketTable from "../components/TicketTable";

export default function EmployeeTickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      setTickets(await api.employeeTickets());
    } catch (err) {
      setError(err.message || "Unable to load tickets.");
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
          <h1>My tickets</h1>
          <p className="muted">View and manage all tickets you have created.</p>
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
        <Alert type="error" title="Could not load tickets">
          {error}
        </Alert>
      )}

      <section className="panel">
        {loading ? <div className="loading-panel">Loading tickets...</div> : <TicketTable tickets={tickets} mode="employee" />}
      </section>
    </div>
  );
}
