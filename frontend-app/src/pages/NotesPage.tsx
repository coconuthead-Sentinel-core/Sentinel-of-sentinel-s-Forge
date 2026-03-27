import { FormEvent, useEffect, useState } from "react";
import { listNotes, upsertNote, type NoteItem } from "../lib/api";

export default function NotesPage() {
  const [notes, setNotes] = useState<NoteItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [text, setText] = useState("");
  const [tag, setTag] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("");

  async function loadNotes() {
    try {
      const data = await listNotes();
      setNotes(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load notes");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadNotes();
  }, []);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!text.trim() || !tag.trim() || saving) return;
    setError("");
    setSaving(true);
    try {
      await upsertNote({ text: text.trim(), tag: tag.trim() });
      setText("");
      setTag("");
      await loadNotes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save note");
    } finally {
      setSaving(false);
    }
  }

  const tags = [...new Set(notes.map((n) => n.tag))];
  const filtered = filter ? notes.filter((n) => n.tag === filter) : notes;

  return (
    <section className="panel">
      <h2>Notes</h2>
      <p>Create and manage knowledge notes in the Sentinel memory lattice.</p>

      {/* Create Note */}
      <form onSubmit={onSubmit} className="note-form">
        <div className="note-form-row">
          <label>
            Tag
            <input
              type="text"
              value={tag}
              onChange={(e) => setTag(e.target.value)}
              placeholder="e.g. research, todo, idea"
              required
              maxLength={50}
            />
          </label>
        </div>
        <label>
          Content
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write your note..."
            rows={3}
            required
          />
        </label>
        <button type="submit" disabled={saving || !text.trim() || !tag.trim()}>
          {saving ? "Saving..." : "Save Note"}
        </button>
      </form>

      {error && <p className="error-msg">{error}</p>}

      {/* Filter */}
      {tags.length > 0 && (
        <div className="note-filters">
          <button
            type="button"
            className={!filter ? "filter-active" : ""}
            onClick={() => setFilter("")}
          >
            All ({notes.length})
          </button>
          {tags.map((t) => (
            <button
              key={t}
              type="button"
              className={filter === t ? "filter-active" : ""}
              onClick={() => setFilter(t)}
            >
              {t} ({notes.filter((n) => n.tag === t).length})
            </button>
          ))}
        </div>
      )}

      {/* Notes List */}
      {loading ? (
        <p className="text-muted">Loading notes...</p>
      ) : filtered.length === 0 ? (
        <p className="text-muted">
          {notes.length === 0
            ? "No notes yet. Create your first note above."
            : "No notes matching this filter."}
        </p>
      ) : (
        <div className="notes-list">
          {filtered.map((note) => (
            <article key={note.id} className="note-card">
              <div className="note-header">
                <span className="note-tag">{note.tag}</span>
                <span className="note-id mono">{note.id.slice(0, 8)}</span>
              </div>
              <p className="note-text">{note.text}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
