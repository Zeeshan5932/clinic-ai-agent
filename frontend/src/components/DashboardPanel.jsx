import { useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { fetchHealthStatus } from "../services/api";

const FLOW_STEPS = [
  {
    title: "Start Booking",
    detail: "Open chat and share service with preferred date and time.",
    starter: "Book appointment for skin consultation tomorrow at 6 pm.",
  },
  {
    title: "Confirm Details",
    detail: "Assistant fills missing fields and confirms schedule.",
    starter: "My name is Ahmed and note acne follow-up.",
  },
  {
    title: "Track Appointments",
    detail: "Visit dashboard to review status and calendar sync.",
    route: "/appointments",
  },
];

function DashboardPanel() {
  const navigate = useNavigate();

  const todayLabel = useMemo(
    () => new Intl.DateTimeFormat("en-PK", { dateStyle: "full" }).format(new Date()),
    []
  );

  async function handleHealthCheck() {
    try {
      const result = await fetchHealthStatus();
      const status = result?.status || "healthy";
      window.alert(`System status: ${status}`);
    } catch {
      window.alert("System status check failed. Please try again.");
    }
  }

  function handleStep(step) {
    if (step.starter) {
      navigate("/chat", { state: { starterMessage: step.starter } });
      return;
    }

    if (step.route) {
      navigate(step.route);
    }
  }

  return (
    <section className="dashboard-panel card">
      <div className="dashboard-panel-head">
        <div>
          <p className="dashboard-kicker">Operations Dashboard</p>
          <h2>Reception Control Center</h2>
          <p>Monitor system readiness, guide patient flow, and move faster through daily bookings.</p>
        </div>
        <button type="button" className="btn btn-secondary" onClick={handleHealthCheck}>
          Check System Health
        </button>
      </div>

      <div className="dashboard-metrics">
        <article className="dashboard-metric">
          <h3>Today</h3>
          <p>{todayLabel}</p>
        </article>
        <article className="dashboard-metric">
          <h3>Assistant Mode</h3>
          <p>Live and ready for booking, cancel, and FAQ workflows.</p>
        </article>
        <article className="dashboard-metric">
          <h3>Need a walkthrough?</h3>
          <p>Use the step-by-step user guide for your staff onboarding.</p>
          <Link className="dashboard-guide-link" to="/guide">
            Open User Guide
          </Link>
        </article>
      </div>

      <div className="dashboard-flow">
        {FLOW_STEPS.map((step, index) => (
          <button
            key={step.title}
            type="button"
            className="dashboard-step"
            onClick={() => handleStep(step)}
          >
            <span className="dashboard-step-index">0{index + 1}</span>
            <div>
              <h4>{step.title}</h4>
              <p>{step.detail}</p>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}

export default DashboardPanel;