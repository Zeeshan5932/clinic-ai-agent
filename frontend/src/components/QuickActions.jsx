const QUICK_ACTIONS = [
  { label: "Book Appointment", message: "I want to book an appointment for a skin consultation." },
  { label: "Reschedule Appointment", message: "I need to reschedule my appointment. My appointment ID is 1." },
  { label: "Cancel Appointment", message: "Please cancel my appointment. My appointment ID is 1." },
  { label: "Ask Clinic Timings", message: "What are your clinic working hours?" },
];

function QuickActions({ onAction }) {
  return (
    <section className="quick-actions card">
      <h3>Quick Actions</h3>
      <div className="quick-actions-grid">
        {QUICK_ACTIONS.map((action) => (
          <button
            key={action.label}
            type="button"
            className="btn btn-secondary"
            onClick={() => onAction(action.message)}
          >
            {action.label}
          </button>
        ))}
      </div>
    </section>
  );
}

export default QuickActions;
