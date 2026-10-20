import { NavLink, Outlet } from 'react-router-dom';
import { Icon, IconMark, Text } from '../primitives';
import './AppShell.css';

const NAV = [
  { to: '/', label: 'Home', end: true },
  { to: '/performance', label: 'Performance' },
  { to: '/live', label: 'Live' },
  { to: '/review', label: 'Review' },
  { to: '/records', label: 'Records' },
] as const;

export function AppShell() {
  return (
    <div className="ln-shell">
      <a className="ln-skip-link" href="#main">
        Skip to main content
      </a>

      <header className="ln-shell__header">
        <div className="ln-shell__brand">
          <Icon size={18} label="BMRG">
            <IconMark />
          </Icon>
          <div>
            <Text as="div" variant="title" className="ln-shell__wordmark">
              BMRG
            </Text>
            <Text as="div" variant="micro" tone="faint">
              Kyoto Ledger
            </Text>
          </div>
        </div>

        <nav className="ln-shell__nav" aria-label="Primary">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={'end' in item ? item.end : false}
              className={({ isActive }) =>
                ['ln-shell__link', isActive ? 'is-active' : ''].filter(Boolean).join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main className="ln-shell__stage" id="main" tabIndex={-1}>
        <Outlet />
      </main>

      <footer className="ln-shell__footer">
        <Text as="div" variant="micro" tone="faint">
          BMRG · Kyoto Ledger · read-first console
        </Text>
      </footer>
    </div>
  );
}
