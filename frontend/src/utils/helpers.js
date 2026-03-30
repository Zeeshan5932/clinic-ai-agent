export function formatDateTime(value) {
  if (!value) return "Not available";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString();
}

export function getStatusClass(status) {
  const normalized = (status || "").toLowerCase();
  if (normalized === "scheduled") return "status status-scheduled";
  if (normalized === "booked") return "status status-scheduled";
  if (normalized === "pending") return "status status-pending";
  if (normalized === "cancelled") return "status status-cancelled";
  if (normalized === "completed") return "status status-completed";
  return "status";
}

export function createMessage(role, content) {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    role,
    content,
    createdAt: new Date().toISOString(),
  };
}
