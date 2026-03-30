function ChatMessage({ message }) {
  const isUser = message.role === "user";
  const roleLabel = isUser ? "You" : "Assistant";

  const timeLabel = message.createdAt
    ? new Date(message.createdAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    : "";

  return (
    <div className={`chat-row ${isUser ? "chat-row-user" : "chat-row-assistant"}`}>
      <div className={`chat-bubble ${isUser ? "chat-bubble-user" : "chat-bubble-assistant"}`}>
        <div className="chat-bubble-meta">
          <span>{roleLabel}</span>
          {timeLabel ? <span>{timeLabel}</span> : null}
        </div>
        <p>{message.content}</p>
      </div>
    </div>
  );
}

export default ChatMessage;
