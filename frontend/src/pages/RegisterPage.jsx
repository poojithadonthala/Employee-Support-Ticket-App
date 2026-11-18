import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import Alert from "../components/Alert";
import { useAuth } from "../auth/AuthContext";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { user, register } = useAuth();
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (user) {
    return <Navigate to={user.role === "Support Staff" ? "/support" : "/employee"} replace />;
  }

  const update = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }));
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register(form);
      navigate("/login", { replace: true, state: { registered: true } });
    } catch (err) {
      setError(err.message || "Unable to create account.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page single">
      <section className="auth-card">
        <div className="auth-brand compact">
          <span className="brand-mark" aria-hidden="true">
            ST
          </span>
          <div>
            <p className="eyebrow">Employee registration</p>
            <h1>Create your account</h1>
            <p className="muted">
              Register as an employee to submit and track support tickets. Support staff accounts are
              created by administrators.
            </p>
          </div>
        </div>

        {error && (
          <Alert type="error" title="Registration failed">
            {error}
          </Alert>
        )}

        <form className="form-grid two" onSubmit={onSubmit}>
          <label className="field span-2">
            <span>Full name</span>
            <input
              type="text"
              name="full_name"
              autoComplete="name"
              value={form.full_name}
              onChange={update("full_name")}
              placeholder="Your full name"
              required
            />
          </label>

          <label className="field span-2">
            <span>Email address</span>
            <input
              type="text"
              name="email"
              autoComplete="email"
              value={form.email}
              onChange={update("email")}
              placeholder="name@company.com"
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              name="password"
              autoComplete="new-password"
              value={form.password}
              onChange={update("password")}
              placeholder="At least 8 characters"
              required
            />
          </label>

          <label className="field">
            <span>Confirm password</span>
            <input
              type="password"
              name="confirm_password"
              autoComplete="new-password"
              value={form.confirm_password}
              onChange={update("confirm_password")}
              placeholder="Re-enter password"
              required
            />
          </label>

          <div className="form-actions span-2">
            <button type="submit" className="button primary" disabled={submitting}>
              {submitting ? "Creating account..." : "Create account"}
            </button>
            <Link to="/login" className="button ghost">
              Back to sign in
            </Link>
          </div>
        </form>
      </section>
    </div>
  );
}
