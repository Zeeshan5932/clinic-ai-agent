import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import ChatPage from "./pages/ChatPage";
import AppointmentsPage from "./pages/AppointmentsPage";
import FeesPage from "./pages/FeesPage";
import FAQPage from "./pages/FAQPage";
import UserGuidePage from "./pages/UserGuidePage";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="app-main container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/appointments" element={<AppointmentsPage />} />
          <Route path="/fees" element={<FeesPage />} />
          <Route path="/faq" element={<FAQPage />} />
          <Route path="/guide" element={<UserGuidePage />} />
          <Route path="/home" element={<Navigate to="/" replace />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
