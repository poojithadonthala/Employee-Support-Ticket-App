export default function Alert({ type = "info", title, children, onClose }) {
  return (
    <div className={`alert alert-${type}`} role="status">
      <div className="alert-content">
        {title && <strong>{title}</strong>}
        {children && <span>{children}</span>}
      </div>
      {onClose && (
        <button type="button" className="alert-close" onClick={onClose} aria-label="Dismiss message">
          ×
        </button>
      )}
    </div>
  );
}
