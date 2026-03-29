import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import ChatBox from "../components/ChatBox";
import QuickActions from "../components/QuickActions";
import { useChat } from "../hooks/useChat";
import { createMessage } from "../utils/helpers";

function ChatPage() {
  const location = useLocation();
  const processedStarterRef = useRef(null);

  const {
    messages,
    input,
    setInput,
    isLoading,
    error,
    listRef,
    canSend,
    submitMessage,
    clearConversation,
  } = useChat([
    createMessage(
      "assistant",
      "Welcome to VitaPulse Clinic Assistant. How can I help you today?"
    ),
  ]);

  useEffect(() => {
    const starterMessage = location.state?.starterMessage;
    if (!starterMessage) return;
    if (processedStarterRef.current === starterMessage) return;

    processedStarterRef.current = starterMessage;
    submitMessage(starterMessage);
    window.history.replaceState({}, document.title);
  }, [location.state?.starterMessage, submitMessage]);

  return (
    <div className="page-grid-chat">
      <ChatBox
        messages={messages}
        input={input}
        onInputChange={setInput}
        onSend={submitMessage}
        onClear={clearConversation}
        isLoading={isLoading}
        error={error}
        listRef={listRef}
        canSend={canSend}
      />
      <QuickActions onAction={submitMessage} />
    </div>
  );
}

export default ChatPage;
