import { useNavigate } from "react-router-dom";

const CONSULTATION = {
  doctor: "Dermatologist Consultation",
  fee: "PKR 2,500",
  followUp: "PKR 1,500 (within 14 days)",
};

const SKIN_TREATMENTS = [
  { name: "Hydra Facial", fee: "PKR 6,500", duration: "45 min" },
  { name: "Acne Treatment Session", fee: "PKR 4,000", duration: "30 min" },
  { name: "Chemical Peel", fee: "PKR 7,500", duration: "40 min" },
  { name: "Laser Hair Removal", fee: "From PKR 5,000", duration: "20-60 min" },
  { name: "Skin Brightening Therapy", fee: "PKR 8,500", duration: "50 min" },
  { name: "Microneedling", fee: "PKR 9,000", duration: "45 min" },
];

function FeesPage() {
  const navigate = useNavigate();

  function askAssistant(message) {
    navigate("/chat", { state: { starterMessage: message } });
  }

  return (
    <section className="page-stack">
      <div className="page-title">
        <h1>Fees and Treatments</h1>
        <p>Review consultation and treatment pricing, then ask assistant for personalized guidance.</p>
      </div>

      <div className="fees-grid">
        <article className="card fee-highlight">
          <p className="hero-kicker">Doctor Appointment Fee</p>
          <h3>{CONSULTATION.doctor}</h3>
          <p className="fee-price">{CONSULTATION.fee}</p>
          <p className="fee-note">Follow-up: {CONSULTATION.followUp}</p>
          <div className="hero-actions">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => askAssistant("What is your dermatologist consultation fee and what is included?")}
            >
              Ask Assistant About Consultation
            </button>
          </div>
        </article>

        <article className="card">
          <h3>Skin Treatment Fee List</h3>
          <p className="guide-sub">Estimated starting prices. Final fee depends on assessment and treatment plan.</p>
          <div className="fee-list">
            {SKIN_TREATMENTS.map((treatment) => (
              <div className="fee-item" key={treatment.name}>
                <div>
                  <h4>{treatment.name}</h4>
                  <p>{treatment.duration}</p>
                </div>
                <strong>{treatment.fee}</strong>
              </div>
            ))}
          </div>
        </article>
      </div>

      <article className="card fee-guide-card">
        <h3>Need Agent Guidance?</h3>
        <p>Use one of these prompts and assistant will guide user to the right package.</p>
        <div className="fee-prompt-row">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => askAssistant("Suggest best treatment for acne and tell me fee range.")}
          >
            Acne Treatment Fees
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => askAssistant("Compare hydra facial and chemical peel fees and sessions.")}
          >
            Compare Skin Treatment Fees
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => askAssistant("I want to book skin consultation. What will be total estimated cost?")}
          >
            Get Cost Estimate in Chat
          </button>
        </div>
      </article>
    </section>
  );
}

export default FeesPage;