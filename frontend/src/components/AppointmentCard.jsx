import { formatDateTime, getStatusClass } from "../utils/helpers";

function AppointmentCard({ appointment }) {
  const statusText = appointment.status || "unknown";

  return (
    <article className="appointment-card card">
      <div className="appointment-card-head">
        <div>
          <h3>Appointment #{appointment.id}</h3>
          <p className="appointment-subtitle">Patient scheduling record</p>
        </div>
        <span className={getStatusClass(appointment.status)}>{statusText}</span>
      </div>

      <dl className="appointment-grid">
        <div>
          <dt>Patient</dt>
          <dd>{appointment.patient_name || "Not provided"}</dd>
        </div>
        <div>
          <dt>Service</dt>
          <dd>{appointment.service || "Not provided"}</dd>
        </div>
        <div>
          <dt>Scheduled Time</dt>
          <dd>{formatDateTime(appointment.scheduled_time)}</dd>
        </div>
      </dl>

      <div className="appointment-foot">
        <span className="appointment-foot-label">Status</span>
        <span>{statusText}</span>
      </div>
    </article>
  );
}

export default AppointmentCard;
