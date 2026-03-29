import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar-wrap">
      <div className="container navbar">
        <NavLink to="/" className="brand">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 64 64" role="img" focusable="false">
              <circle cx="32" cy="32" r="30" fill="rgba(255,255,255,0.15)" />
              <path
                d="M10 35h10l5-10 8 18 7-14 4 6h10"
                fill="none"
                stroke="white"
                strokeWidth="4"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>
          <div>
            <strong>VitaPulse CareOS</strong>
            <small>AI Reception and Scheduling Suite</small>
          </div>
        </NavLink>

        <nav className="nav-links">
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/chat">Chat</NavLink>
          <NavLink to="/appointments">Appointments</NavLink>
          <NavLink to="/guide">User Guide</NavLink>
          <NavLink to="/faq">FAQ</NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
