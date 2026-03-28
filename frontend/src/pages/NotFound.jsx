import { Link } from "react-router-dom";

function NotFound() {
  return (
    <section className="card not-found">
      <h1>404</h1>
      <p>The page you are looking for does not exist.</p>
      <Link to="/" className="btn btn-primary">Go Home</Link>
    </section>
  );
}

export default NotFound;
