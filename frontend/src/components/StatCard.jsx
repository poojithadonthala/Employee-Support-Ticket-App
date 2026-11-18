export default function StatCard({ label, value, tone = "primary" }) {
  return (
    <article className={`stat-card stat-${tone}`}>
      <span className="stat-label">{label}</span>
      <strong className="stat-value">{value}</strong>
      <span className="stat-bar" aria-hidden="true" />
    </article>
  );
}
