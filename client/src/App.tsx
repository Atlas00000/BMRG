import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './api/AuthContext';
import { AppShell } from './components/shells';
import { Home } from './routes/Home';
import { Live } from './routes/Live';
import { Performance } from './routes/Performance';
import { Records } from './routes/Records';
import { Review } from './routes/Review';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppShell />}>
            <Route index element={<Home />} />
            <Route path="performance" element={<Performance />} />
            <Route path="live" element={<Live />} />
            <Route path="review" element={<Review />} />
            <Route path="records" element={<Records />} />
          </Route>
          {/* Outside the layout so it cannot outrank real pages */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
