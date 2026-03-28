import { formatDateTime, getStatusClass } from "../utils/helpers";

function AppointmentCard({ appointment }) {
  return (
    <article className="appointment-card card">
      <div className="appointment-card-head">
        <h3>Appointment #{appointment.id}</h3>
        <span className={getStatusClass(appointment.status)}>{appointment.status || "unknown"}</span>
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
    </article>
  );
}

export default AppointmentCard;
