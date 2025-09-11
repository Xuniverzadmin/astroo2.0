export default function GetStartedCTA() {
  console.log("GetStartedCTA: Component rendering");
  
  const handleClick = () => {
    console.log("GetStartedCTA: Button clicked, navigating to onboarding");
    // Use hash-based navigation to match the app's routing system
    window.location.hash = "onboarding";
  };
  
  return (
    <button
      className="btn btn-accent"
      onClick={handleClick}
    >
      Get Started
    </button>
  );
}
