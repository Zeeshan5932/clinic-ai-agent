import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { sendChatMessage } from "../services/api";
import { createMessage } from "../utils/helpers";

export function useChat(initialMessages = []) {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const listRef = useRef(null);
  const inFlightRef = useRef(false);

  const canSend = useMemo(() => input.trim().length > 0 && !isLoading, [input, isLoading]);

  useEffect(() => {
    if (!listRef.current) return;
    listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [messages, isLoading]);

  const submitMessage = useCallback(async (text) => {
    const cleanText = (text || "").trim();
    if (!cleanText || inFlightRef.current) return;

    inFlightRef.current = true;

    setError("");
    setInput("");
    setIsLoading(true);

    const userMsg = createMessage("user", cleanText);
    setMessages((prev) => [...prev, userMsg]);

    try {
      const data = await sendChatMessage(cleanText);
      const assistantText = data?.response || "I could not generate a response.";
      const assistantMsg = createMessage("assistant", assistantText);
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorText = err?.message || "Failed to contact backend.";
      setError(errorText);
      const assistantMsg = createMessage(
        "assistant",
        "I am having trouble connecting right now. Please try again in a moment."
      );
      setMessages((prev) => [...prev, assistantMsg]);
    } finally {
      inFlightRef.current = false;
      setIsLoading(false);
    }
  }, []);

  const clearConversation = useCallback(() => {
    setMessages([]);
    setError("");
    setInput("");
  }, []);

  return {
    messages,
    input,
    setInput,
    isLoading,
    error,
    listRef,
    canSend,
    submitMessage,
    clearConversation,
  };
}
