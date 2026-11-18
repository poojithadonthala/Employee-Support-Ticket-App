const classByStatus = {
  Open: "open",
  "In Progress": "progress",
  Resolved: "resolved",
  Closed: "closed",
};

export default function StatusBadge({ status }) {
  return <span className={`badge status-${classByStatus[status] || "open"}`}>{status}</span>;
}
