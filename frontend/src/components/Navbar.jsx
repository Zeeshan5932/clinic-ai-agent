import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar-wrap">
      <div className="container navbar">
        <NavLink to="/" className="brand">
          <span className="brand-mark">+</span>
          <div>
            <strong>VitaPulse Clinic</strong>
            <small>Digital Reception Dashboard</small>
          </div>
        </NavLink>

        <nav className="nav-links">
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/chat">Chat</NavLink>
          <NavLink to="/appointments">Appointments</NavLink>
          <NavLink to="/faq">FAQ</NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
