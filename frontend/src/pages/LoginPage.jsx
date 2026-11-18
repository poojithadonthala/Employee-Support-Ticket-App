import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import Alert from "../components/Alert";
import { useAuth } from "../auth/AuthContext";

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, login } = useAuth();
  const registered = location.state?.registered;
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (user) {
    return <Navigate to={user.role === "Support Staff" ? "/support" : "/employee"} replace />;
  }

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const loggedIn = await login(email, password);
      navigate(loggedIn.role === "Support Staff" ? "/support" : "/employee", { replace: true });
    } catch (err) {
      setError(err.message || "Unable to sign in.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <section className="auth-card">
        <div className="auth-brand">
          <span className="brand-mark large" aria-hidden="true">
            ST
          </span>
          <div>
            <p className="eyebrow">Employee Support</p>
            <h1>Sign in to TicketDesk</h1>
            <p className="muted">
              Use your employee or support staff account to manage workplace and technical requests.
            </p>
          </div>
        </div>

        {registered && (
          <Alert type="success" title="Account created">
            Sign in with your new employee account.
          </Alert>
        )}

        {error && (
          <Alert type="error" title="Sign-in failed">
            {error}
          </Alert>
        )}

        <form className="form-grid" onSubmit={onSubmit}>
          <label className="field">
            <span>Email address</span>
            <input
              type="text"
              name="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@company.com"
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              name="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </label>

          <button type="submit" className="button primary full" disabled={submitting}>
            {submitting ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p className="auth-footer">
          New employee? <Link to="/register">Create an account</Link>
        </p>
      </section>

      <aside className="auth-aside" aria-hidden="true">
        <div className="aside-panel">
          <h2>Track every request clearly</h2>
          <ul>
            <li>Submit hardware, software, network, and access tickets.</li>
            <li>Follow progress from Open to Closed.</li>
            <li>Support staff can review and update all requests.</li>
          </ul>
        </div>
      </aside>
    </div>
  );
}
