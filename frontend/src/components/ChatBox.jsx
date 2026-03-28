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
        <h2>Clinic AI Assistant</h2>
        <button type="button" className="btn btn-ghost" onClick={onClear}>
          Clear Conversation
        </button>
      </div>

      <div className="chatbox-messages" ref={listRef}>
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Start the conversation. Ask about appointments, services, pricing, or timings.</p>
          </div>
        )}
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isLoading && <LoadingSpinner label="Clinic assistant is typing..." />}
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <form className="chatbox-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type your message..."
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
