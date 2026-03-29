import { Link } from "react-router-dom";

function HeroSection() {
  return (
    <section className="hero card">
      <div className="hero-content">
        <p className="hero-kicker">VitaPulse Smart Reception</p>
        <h1>Your front desk, elevated with AI</h1>
        <p>
          VitaPulse Clinic assists patients instantly, keeps appointment workflows smooth,
          and helps your team stay focused on care.
        </p>
        <div className="hero-actions">
          <Link className="btn btn-primary" to="/chat">Open Assistant</Link>
          <Link className="btn btn-secondary" to="/chat">Book Appointment</Link>
          <Link className="btn btn-ghost" to="/appointments">View Appointments</Link>
        </div>
      </div>
      <div className="hero-aside">
        <div className="metric-card">
          <h3>Fast Patient Replies</h3>
          <p>Deliver clear answers in seconds with assistant-guided conversations.</p>
        </div>
        <div className="metric-card">
          <h3>Unified Scheduling Flow</h3>
          <p>Book, reschedule, and cancel appointments in one consistent experience.</p>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
