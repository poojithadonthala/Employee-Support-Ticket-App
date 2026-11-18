import { Link } from "react-router-dom";

export default function Forbidden() {
  return (
    <div className="center-screen status-screen">
      <span className="status-code">403</span>
      <h1>Access denied</h1>
      <p className="muted">You do not have permission to view this page.</p>
      <Link to="/" className="button primary">
        Go to my dashboard
      </Link>
    </div>
  );
}
