import React from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `navbar__link${isActive ? " navbar__link--active" : ""}`;

  return (
    <header className="navbar">
      <div className="navbar__brand">
        <span role="img" aria-hidden="true">
          🧠
        </span>{" "}
        Memory Companion
      </div>
      <nav className="navbar__links">
        <NavLink to="/" className={linkClass} end>
          Predict
        </NavLink>
        <NavLink to="/chat" className={linkClass}>
          Chatbot
        </NavLink>
      </nav>
    </header>
  );
}
