import { useEffect, useState } from "react";
import { api } from "../api/client";
import Alert from "./Alert";

function initials(name) {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join("");
}

export default function CommentSection({ ticketId }) {
  const [comments, setComments] = useState([]);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      setComments(await api.comments(ticketId));
    } catch (err) {
      setError(err.message || "Unable to load comments.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [ticketId]);

  const submit = async (event) => {
    event.preventDefault();
    const trimmed = content.trim();
    if (!trimmed) {
      setError("Comment cannot be empty.");
      return;
    }

    setSubmitting(true);
    setError("");
    try {
      const created = await api.addComment(ticketId, trimmed);
      setComments((current) => [...current, created]);
      setContent("");
    } catch (err) {
      setError(err.message || "Unable to add comment.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="panel comment-section">
      <div className="panel-header">
        <div>
          <h2>Comments</h2>
          <p className="muted">
            Visible to the ticket owner and Support Staff. Closed tickets can still receive comments.
          </p>
        </div>
        <span className="comment-count" aria-label={`${comments.length} comments`}>
          {comments.length}
        </span>
      </div>

      {error && (
        <Alert type="error" title="Comment error">
          {error}
        </Alert>
      )}

      {loading ? (
        <div className="loading-panel">Loading comments...</div>
      ) : comments.length === 0 ? (
        <div className="comment-empty">
          <span aria-hidden="true">&#128172;</span>
          <strong>No comments yet</strong>
          <p>Add the first update for this ticket.</p>
        </div>
      ) : (
        <ol className="comment-list">
          {comments.map((comment) => (
            <li className="comment-item" key={comment.id}>
              <div className="comment-avatar" aria-hidden="true">
                {initials(comment.author)}
              </div>
              <div className="comment-body">
                <div className="comment-meta">
                  <span className="comment-author">{comment.author}</span>
                  <span className="comment-role">{comment.author_role}</span>
                  <time className="comment-time">{comment.created_at}</time>
                </div>
                <p className="comment-content">{comment.content}</p>
              </div>
            </li>
          ))}
        </ol>
      )}

      <form className="comment-form" onSubmit={submit}>
        <label className="field">
          <span>Add a comment</span>
          <textarea
            value={content}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Write an update or ask a question..."
            rows={3}
          />
        </label>
        <div className="comment-actions">
          <span className="comment-hint">Surrounding whitespace is removed automatically.</span>
          <button
            type="submit"
            className="button primary"
            disabled={submitting || !content.trim()}
          >
            {submitting ? "Posting..." : "Add comment"}
          </button>
        </div>
      </form>
    </section>
  );
}
