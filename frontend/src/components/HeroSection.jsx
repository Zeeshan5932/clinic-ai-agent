import { Link } from "react-router-dom";

function HeroSection() {
  return (
    <section className="hero card">
      <div className="hero-content">
        <p className="hero-kicker">Smart Front Desk Experience</p>
        <h1>Clinic AI Receptionist</h1>
        <p>
          Handle appointments, answer patient questions, and streamline clinic communication
          with a professional AI assistant.
        </p>
        <div className="hero-actions">
          <Link className="btn btn-primary" to="/chat">Start Chat</Link>
          <Link className="btn btn-secondary" to="/chat">Book Appointment</Link>
          <Link className="btn btn-ghost" to="/appointments">View Appointments</Link>
        </div>
      </div>
      <div className="hero-aside">
        <div className="metric-card">
          <h3>Fast Response</h3>
          <p>Answer patient queries in seconds with AI-powered chat support.</p>
        </div>
        <div className="metric-card">
          <h3>Unified Workflow</h3>
          <p>Book, reschedule, and cancel appointments from a single interface.</p>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
