import { Link } from "react-router-dom";

function HeroSection() {
  return (
    <section className="hero card">
      <div className="hero-content">
        <p className="hero-kicker">VitaPulse Smart Reception</p>
        <h1>Modern Clinic Reception. One Intelligent Dashboard.</h1>
        <p>
          Handle booking, follow-ups, and clinic queries in a polished workflow built for
          real front-desk teams. Faster responses for patients, fewer manual steps for staff.
        </p>
        <div className="hero-pill-row">
          <span className="hero-pill">Live scheduling assistant</span>
          <span className="hero-pill">Patient-ready responses</span>
          <span className="hero-pill">Unified dashboard view</span>
        </div>
        <div className="hero-actions">
          <Link className="btn btn-primary" to="/chat">Open Assistant</Link>
          <Link className="btn btn-secondary" to="/chat">Book Appointment</Link>
          <Link className="btn btn-ghost" to="/appointments">View Appointments</Link>
        </div>
      </div>
      <div className="hero-aside">
        <div className="metric-card">
          <h3>Faster Front Desk Operations</h3>
          <p>Deliver accurate responses in seconds with assistant-guided conversations.</p>
        </div>
        <div className="metric-card">
          <h3>Reliable Scheduling Control</h3>
          <p>Book, reschedule, and cancel appointments in one clear, consistent flow.</p>
        </div>
        <div className="metric-card metric-card-emphasis">
          <h3>Designed for Clinics</h3>
          <p>Clean, trustworthy UX tailored for patient communication and daily staff usage.</p>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
