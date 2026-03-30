import ChatMessage from "./ChatMessage";
import LoadingSpinner from "./LoadingSpinner";

function ChatBox({
  messages,
  input,
  onInputChange,
  onSend,
  onClear,
  isLoading,
  error,
  listRef,
  canSend,
}) {
  function handleSubmit(event) {
    event.preventDefault();
    onSend(input);
  }

  return (
    <section className="chatbox card">
      <div className="chatbox-head">
        <div>
          <h2>VitaPulse AI Assistant</h2>
          <p className="chatbox-subtitle">
            Ask about booking, rescheduling, cancellations, fees, and clinic information.
          </p>
        </div>
        <div className="chatbox-head-actions">
          <button type="button" className="btn btn-ghost" onClick={onClear}>
            Clear Conversation
          </button>
        </div>
      </div>

      <div className="chatbox-messages" ref={listRef}>
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Start a conversation about appointments, services, fees, or working hours.</p>
          </div>
        )}
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isLoading && <LoadingSpinner label="VitaPulse assistant is typing..." />}
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <form className="chatbox-form" onSubmit={handleSubmit}>
        <label className="sr-only" htmlFor="assistant-message-input">
          Message for assistant
        </label>
        <input
          id="assistant-message-input"
          type="text"
          placeholder="Type a patient request, for example: Book skin consultation tomorrow at 4 PM"
          value={input}
          onChange={(event) => onInputChange(event.target.value)}
          disabled={isLoading}
        />
        <button type="submit" className="btn btn-primary" disabled={!canSend}>
          Send
        </button>
      </form>
    </section>
  );
}

export default ChatBox;
