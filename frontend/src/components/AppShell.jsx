import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import NavBar from "./NavBar";

const employeeNav = [
  { to: "/employee", label: "Dashboard", icon: "D", end: true },
  { to: "/employee/tickets", label: "My tickets", icon: "T" },
  { to: "/employee/tickets/new", label: "New ticket", icon: "+" },
];

const supportNav = [
  { to: "/support", label: "Dashboard", icon: "D", end: true },
  { to: "/support/tickets", label: "All tickets", icon: "T" },
];

export default function AppShell() {
  const { user, isEmployee, logout } = useAuth();
  const navigate = useNavigate();
  const items = isEmployee ? employeeNav : supportNav;

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            ST
          </span>
          <div>
            <strong>TicketDesk</strong>
            <span>Employee Support</span>
          </div>
        </div>

        <NavBar items={items} />

        <div className="sidebar-note">
          <span className="note-dot" aria-hidden="true" />
          <p>
            {isEmployee
              ? "Need help? Raise a ticket and track it from your dashboard."
              : "Review requests and move each ticket one step forward."}
          </p>
        </div>
      </aside>

      <div className="main-column">
        <header className="topbar">
          <div className="topbar-heading">
            <span className="eyebrow">Signed in as</span>
            <strong>{user?.full_name}</strong>
          </div>
          <div className="topbar-actions">
            <span className={`role-pill${isEmployee ? "" : " support"}`}>{user?.role}</span>
            <button type="button" className="button ghost" onClick={handleLogout}>
              Log out
            </button>
          </div>
        </header>

        <main className="page">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
