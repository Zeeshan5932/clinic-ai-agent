import { useEffect, useState } from "react";
import AppointmentCard from "../components/AppointmentCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { API_BASE_URL } from "../services/api";

function AppointmentsPage() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

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

  const normalizedQuery = query.trim().toLowerCase();

  const filteredAppointments = appointments.filter((item) => {
    const status = (item.status || "").toLowerCase();
    const patient = (item.patient_name || "").toLowerCase();
    const service = (item.service || "").toLowerCase();

    const matchesStatus = statusFilter === "all" || status === statusFilter;
    const matchesQuery = !normalizedQuery
      || patient.includes(normalizedQuery)
      || service.includes(normalizedQuery)
      || String(item.id || "").includes(normalizedQuery);

    return matchesStatus && matchesQuery;
  });

  const metrics = {
    total: appointments.length,
    scheduled: appointments.filter((item) => (item.status || "").toLowerCase() === "scheduled").length,
    completed: appointments.filter((item) => (item.status || "").toLowerCase() === "completed").length,
    cancelled: appointments.filter((item) => (item.status || "").toLowerCase() === "cancelled").length,
  };

  return (
    <section className="page-stack">
      <div className="page-title">
        <h1>Appointments</h1>
        <p>Review upcoming and historical bookings at VitaPulse Clinic.</p>
      </div>

      <section className="dashboard-metrics appointments-metrics">
        <article className="dashboard-metric">
          <h3>Total</h3>
          <p>{metrics.total} records</p>
        </article>
        <article className="dashboard-metric">
          <h3>Scheduled</h3>
          <p>{metrics.scheduled} active</p>
        </article>
        <article className="dashboard-metric">
          <h3>Completed</h3>
          <p>{metrics.completed} finished</p>
        </article>
        <article className="dashboard-metric">
          <h3>Cancelled</h3>
          <p>{metrics.cancelled} cancelled</p>
        </article>
      </section>

      <section className="card appointments-toolbar" aria-label="Appointment filters">
        <div className="appointments-toolbar-group">
          <label htmlFor="appointment-search">Search</label>
          <input
            id="appointment-search"
            type="search"
            placeholder="Search by ID, patient, or service"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>

        <div className="appointments-toolbar-group">
          <label htmlFor="appointment-status">Status</label>
          <select
            id="appointment-status"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="all">All</option>
            <option value="scheduled">Scheduled</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </section>

      {loading ? <LoadingSpinner label="Loading appointments..." /> : null}
      {error ? <p className="error-text card">{error}</p> : null}

      {!loading && appointments.length === 0 ? (
        <div className="empty-state card">
          <p>No appointments found yet.</p>
          <p>Use the chat page to create your first appointment.</p>
        </div>
      ) : null}

      {!loading && appointments.length > 0 && filteredAppointments.length === 0 ? (
        <div className="empty-state card">
          <p>No appointments match your current filters.</p>
          <p>Try clearing search text or changing the status filter.</p>
        </div>
      ) : null}

      <div className="appointments-grid">
        {filteredAppointments.map((appointment) => (
          <AppointmentCard key={appointment.id} appointment={appointment} />
        ))}
      </div>
    </section>
  );
}

export default AppointmentsPage;
