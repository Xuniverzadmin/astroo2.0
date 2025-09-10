import { useNavigate } from "react-router-dom";

export default function GetStartedCTA() {
  const nav = useNavigate();
  
  return (
    <button
      className="btn btn-accent"
      onClick={() => nav("/onboarding")}
    >
      Get Started
    </button>
  );
}
