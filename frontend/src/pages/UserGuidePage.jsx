import { useState } from "react";

const GUIDE_STEPS = [
  {
    title: "Open Chat",
    detail: "Go to Chat and start with a clear intent like booking, cancel, reschedule, or clinic info.",
  },
  {
    title: "Share Core Details",
    detail: "For booking, send service + date/time first, then share patient name and any notes.",
  },
  {
    title: "Respond to Follow-up",
    detail: "If bot asks one missing item, provide only that item to complete the flow quickly.",
  },
  {
    title: "Verify in Appointments",
    detail: "Open Appointments page to confirm status and check if calendar sync completed.",
  },
];

const EXAMPLES = [
  "Book appointment for skin consultation on 2026-03-31 at 11:30 am.",
  "My name is Ali and note acne follow-up.",
  "Please reschedule my appointment ID 7 to 2026-04-02 05:00 pm.",
  "Cancel my appointment with ID 5.",
  "What are your clinic working hours and address?",
];

function UserGuidePage() {
  const [copiedText, setCopiedText] = useState("");

  async function handleCopy(value) {
    try {
      await navigator.clipboard.writeText(value);
      setCopiedText(value);
      setTimeout(() => setCopiedText(""), 1300);
    } catch {
      setCopiedText("");
    }
  }

  return (
    <section className="page-stack guide-page">
      <div className="page-title">
        <h1>User Guide</h1>
        <p>Simple workflow for staff and reception teams to use VitaPulse smoothly.</p>
      </div>

      <div className="guide-grid">
        <article className="card guide-card">
          <h3>How To Use</h3>
          <div className="guide-steps">
            {GUIDE_STEPS.map((step, index) => (
              <div className="guide-step" key={step.title}>
                <span>{index + 1}</span>
                <div>
                  <h4>{step.title}</h4>
                  <p>{step.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className="card guide-card">
          <h3>Copy-Ready Prompts</h3>
          <p className="guide-sub">Use these messages directly in chat for faster operations.</p>
          <div className="guide-examples">
            {EXAMPLES.map((example) => (
              <button
                key={example}
                type="button"
                className="guide-example"
                onClick={() => handleCopy(example)}
              >
                <span>{example}</span>
                <strong>{copiedText === example ? "Copied" : "Copy"}</strong>
              </button>
            ))}
          </div>
        </article>
      </div>
    </section>
  );
}

export default UserGuidePage;