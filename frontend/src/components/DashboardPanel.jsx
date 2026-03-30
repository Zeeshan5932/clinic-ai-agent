import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { API_BASE_URL, fetchHealthStatus } from "../services/api";

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
  const [appointments, setAppointments] = useState([]);
  const [healthState, setHealthState] = useState({ type: "", message: "" });

  const todayLabel = useMemo(
    () => new Intl.DateTimeFormat("en-PK", { dateStyle: "full" }).format(new Date()),
    []
  );

  const metrics = useMemo(() => {
    const total = appointments.length;
    const scheduled = appointments.filter((item) => (item.status || "").toLowerCase() === "scheduled").length;
    const cancelled = appointments.filter((item) => (item.status || "").toLowerCase() === "cancelled").length;
    const completed = appointments.filter((item) => (item.status || "").toLowerCase() === "completed").length;

    return { total, scheduled, cancelled, completed };
  }, [appointments]);

  useEffect(() => {
    let mounted = true;

    async function loadAppointments() {
      const endpoints = ["/api/v1/appointments", "/appointments"];

      for (const endpoint of endpoints) {
        try {
          const response = await fetch(`${API_BASE_URL}${endpoint}`);
          if (!response.ok) {
            throw new Error("Could not load appointment metrics.");
          }

          const data = await response.json();
          if (mounted) {
            setAppointments(Array.isArray(data) ? data : []);
          }
          return;
        } catch {
          // Try next endpoint fallback.
        }
      }
    }

    loadAppointments();

    return () => {
      mounted = false;
    };
  }, []);

  async function handleHealthCheck() {
    try {
      const result = await fetchHealthStatus();
      const status = result?.status || "healthy";
      setHealthState({ type: "success", message: `System status: ${status}` });
    } catch {
      setHealthState({ type: "error", message: "System status check failed. Please try again." });
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
          <h3>Live Appointments</h3>
          <p>{metrics.total} total records</p>
        </article>
        <article className="dashboard-metric">
          <h3>Scheduled</h3>
          <p>{metrics.scheduled} active bookings</p>
        </article>
        <article className="dashboard-metric">
          <h3>Completed</h3>
          <p>{metrics.completed} finished visits</p>
        </article>
        <article className="dashboard-metric">
          <h3>Cancelled</h3>
          <p>{metrics.cancelled} cancelled bookings</p>
        </article>
        <article className="dashboard-metric">
          <h3>Need a walkthrough?</h3>
          <p>Use the step-by-step user guide for your staff onboarding.</p>
          <Link className="dashboard-guide-link" to="/guide">
            Open User Guide
          </Link>
        </article>
      </div>

      {healthState.message ? (
        <p className={`dashboard-health ${healthState.type === "error" ? "dashboard-health-error" : "dashboard-health-success"}`}>
          {healthState.message}
        </p>
      ) : null}

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