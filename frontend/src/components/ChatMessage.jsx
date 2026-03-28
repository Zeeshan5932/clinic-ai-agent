function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`chat-row ${isUser ? "chat-row-user" : "chat-row-assistant"}`}>
      <div className={`chat-bubble ${isUser ? "chat-bubble-user" : "chat-bubble-assistant"}`}>
        <p>{message.content}</p>
      </div>
    </div>
  );
}

export default ChatMessage;
