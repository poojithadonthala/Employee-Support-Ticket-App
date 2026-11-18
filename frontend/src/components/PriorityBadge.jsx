const classByPriority = {
  Low: "low",
  Medium: "medium",
  High: "high",
};

export default function PriorityBadge({ priority }) {
  return <span className={`badge priority-${classByPriority[priority] || "low"}`}>{priority}</span>;
}
