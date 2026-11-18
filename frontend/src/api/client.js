const API_BASE = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export async function apiRequest(path, { method = "GET", body, headers = {} } = {}) {
  const options = {
    method,
    credentials: "include",
    headers: { ...headers },
  };

  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(`${API_BASE}/api${path}`, options);
  } catch (error) {
    throw new Error("Unable to reach the server. Check that the backend is running.");
  }

  if (response.status === 204) {
    return null;
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const message = data?.detail || `Request failed with status ${response.status}.`;
    const error = new Error(message);
    error.status = response.status;
    if (response.status === 401 && !path.startsWith("/auth/login")) {
      window.dispatchEvent(new CustomEvent("auth:unauthorized"));
    }
    throw error;
  }

  return data;
}

export const api = {
  health: () => apiRequest("/health"),
  register: (payload) => apiRequest("/auth/register", { method: "POST", body: payload }),
  login: (payload) => apiRequest("/auth/login", { method: "POST", body: payload }),
  me: () => apiRequest("/auth/me"),
  logout: () => apiRequest("/auth/logout", { method: "POST" }),
  employeeDashboard: () => apiRequest("/employee/dashboard"),
  employeeTickets: () => apiRequest("/employee/tickets"),
  supportDashboard: () => apiRequest("/support/dashboard"),
  supportTickets: (params = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) query.set(key, value);
    });
    const suffix = query.toString();
    return apiRequest(`/support/tickets${suffix ? `?${suffix}` : ""}`);
  },
  createTicket: (payload) => apiRequest("/tickets", { method: "POST", body: payload }),
  ticket: (id) => apiRequest(`/tickets/${id}`),
  comments: (id) => apiRequest(`/tickets/${id}/comments`),
  addComment: (id, content) =>
    apiRequest(`/tickets/${id}/comments`, { method: "POST", body: { content } }),
  updateTicket: (id, payload) => apiRequest(`/tickets/${id}`, { method: "PATCH", body: payload }),
  updateStatus: (id, status) =>
    apiRequest(`/tickets/${id}/status`, { method: "POST", body: { status } }),
};
