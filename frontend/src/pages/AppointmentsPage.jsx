import { useEffect, useState } from "react";
import AppointmentCard from "../components/AppointmentCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { API_BASE_URL } from "../services/api";

function AppointmentsPage() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    async function fetchAppointments() {
      setLoading(true);
      setError("");

      // Prefer v1 route and fallback to root route if backend differs.
      const endpoints = ["/api/v1/appointments", "/appointments"];

      for (const endpoint of endpoints) {
        try {
          const response = await fetch(`${API_BASE_URL}${endpoint}`);
          if (!response.ok) {
            throw new Error("Unable to fetch appointments.");
          }
          const data = await response.json();
          if (mounted) {
            setAppointments(Array.isArray(data) ? data : []);
          }
          setLoading(false);
          return;
        } catch (err) {
          setError(err.message || "Could not load appointments.");
        }
      }

      setLoading(false);
    }

    fetchAppointments();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <section className="page-stack">
      <div className="page-title">
        <h1>Appointments</h1>
        <p>Review upcoming and historical patient bookings.</p>
      </div>

      {loading ? <LoadingSpinner label="Loading appointments..." /> : null}
      {error ? <p className="error-text">{error}</p> : null}

      {!loading && appointments.length === 0 ? (
        <div className="empty-state card">
          <p>No appointments found yet.</p>
          <p>Use the chat page to create your first appointment.</p>
        </div>
      ) : null}

      <div className="appointments-grid">
        {appointments.map((appointment) => (
          <AppointmentCard key={appointment.id} appointment={appointment} />
        ))}
      </div>
    </section>
  );
}

export default AppointmentsPage;
