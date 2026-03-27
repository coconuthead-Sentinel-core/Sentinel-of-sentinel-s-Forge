import { FormEvent, useRef, useState } from "react";
import { sendChat, type ChatMessage } from "../lib/api";

type DisplayMessage = ChatMessage & { id: number };

let nextId = 0;

export default function ChatPage() {
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;

    setError("");
    const userMsg: DisplayMessage = { id: nextId++, role: "user", content: text };
    const updated = [...messages, userMsg];
    setMessages(updated);
    setInput("");
    setSending(true);

    try {
      const apiMessages: ChatMessage[] = updated.map(({ role, content }) => ({ role, content }));
      const resp = await sendChat(apiMessages);
      const aiContent = resp.choices?.[0]?.message?.content ?? "(no response)";
      const aiMsg: DisplayMessage = { id: nextId++, role: "assistant", content: aiContent };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Chat failed");
    } finally {
      setSending(false);
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }

  return (
    <section className="panel chat-panel">
      <h2>AI Chat</h2>
      <p>Interact with the Sentinel Forge cognitive engine.</p>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-empty">
            Send a message to start a conversation. The AI will process your input
            through the cognitive pipeline and respond.
          </div>
        )}
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-bubble chat-${msg.role}`}>
            <span className="chat-role">{msg.role === "user" ? "You" : "Sentinel"}</span>
            <div className="chat-content">{msg.content}</div>
          </div>
        ))}
        {sending && (
          <div className="chat-bubble chat-assistant">
            <span className="chat-role">Sentinel</span>
            <div className="chat-content chat-typing">Thinking...</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {error && <p className="error-msg">{error}</p>}

      <form onSubmit={onSubmit} className="chat-input-bar">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={sending}
          autoFocus
        />
        <button type="submit" disabled={sending || !input.trim()}>
          Send
        </button>
      </form>
    </section>
  );
}
