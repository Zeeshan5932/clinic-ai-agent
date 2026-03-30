const QUICK_ACTIONS = [
  { label: "Book Appointment", message: "I want to book an appointment for a skin consultation." },
  { label: "Doctor Consultation Fee", message: "What is doctor consultation fee and follow-up fee?" },
  { label: "Skin Treatment Fees", message: "Show me skin treatment fees and suggest best option for acne." },
  { label: "Reschedule Appointment", message: "I need to reschedule my appointment. My appointment ID is 1." },
  { label: "Cancel Appointment", message: "Please cancel my appointment. My appointment ID is 1." },
  { label: "Check Clinic Hours", message: "What are your clinic working hours?" },
];

function QuickActions({ onAction }) {
  return (
    <section className="quick-actions card">
      <div className="quick-actions-head">
        <h3>Quick Actions</h3>
        <p>Use common requests to speed up daily reception tasks.</p>
      </div>
      <div className="quick-actions-grid">
        {QUICK_ACTIONS.map((action) => (
          <button
            key={action.label}
            type="button"
            className="btn btn-secondary"
            onClick={() => onAction(action.message)}
            title={action.message}
          >
            {action.label}
          </button>
        ))}
      </div>
    </section>
  );
}

export default QuickActions;
