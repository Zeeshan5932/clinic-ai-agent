import HeroSection from "../components/HeroSection";
import QuickActions from "../components/QuickActions";
import DashboardPanel from "../components/DashboardPanel";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  function handleQuickAction(message) {
    navigate("/chat", { state: { starterMessage: message } });
  }

  return (
    <div className="page-stack">
      <HeroSection />
      <DashboardPanel />
      <QuickActions onAction={handleQuickAction} />
    </div>
  );
}

export default Home;
