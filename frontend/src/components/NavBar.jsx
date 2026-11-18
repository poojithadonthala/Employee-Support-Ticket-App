import { NavLink } from "react-router-dom";

export default function NavBar({ items }) {
  return (
    <nav className="sidebar-nav" aria-label="Main navigation">
      <p className="nav-caption">Workspace</p>
      <ul className="nav-list">
        {items.map((item) => (
          <li key={item.to}>
            <NavLink
              to={item.to}
              end={item.end}
              className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}
            >
              <span className="nav-icon" aria-hidden="true">
                {item.icon}
              </span>
              <span>{item.label}</span>
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
