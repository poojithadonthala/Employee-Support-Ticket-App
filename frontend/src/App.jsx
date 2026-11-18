import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./auth/ProtectedRoute";
import { useAuth } from "./auth/AuthContext";
import AppShell from "./components/AppShell";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import EmployeeTickets from "./pages/EmployeeTickets";
import Forbidden from "./pages/Forbidden";
import LoginPage from "./pages/LoginPage";
import NotFound from "./pages/NotFound";
import RegisterPage from "./pages/RegisterPage";
import SupportDashboard from "./pages/SupportDashboard";
import SupportTickets from "./pages/SupportTickets";
import TicketDetail from "./pages/TicketDetail";
import TicketForm from "./pages/TicketForm";

function HomeRedirect() {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="center-screen">
        <div className="spinner" aria-hidden="true" />
        <p>Loading your workspace...</p>
      </div>
    );
  }
  if (!user) return <Navigate to="/login" replace />;
  return <Navigate to={user.role === "Support Staff" ? "/support" : "/employee"} replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/forbidden" element={<Forbidden />} />
      <Route path="*" element={<NotFound />} />

      <Route element={<ProtectedRoute roles={["Employee"]} />}>
        <Route element={<AppShell />}>
          <Route path="/employee" element={<EmployeeDashboard />} />
          <Route path="/employee/tickets" element={<EmployeeTickets />} />
          <Route path="/employee/tickets/new" element={<TicketForm />} />
          <Route path="/employee/tickets/:id/edit" element={<TicketForm />} />
          <Route path="/employee/tickets/:id" element={<TicketDetail />} />
        </Route>
      </Route>

      <Route element={<ProtectedRoute roles={["Support Staff"]} />}>
        <Route element={<AppShell />}>
          <Route path="/support" element={<SupportDashboard />} />
          <Route path="/support/tickets" element={<SupportTickets />} />
          <Route path="/support/tickets/:id" element={<TicketDetail />} />
        </Route>
      </Route>
    </Routes>
  );
}
