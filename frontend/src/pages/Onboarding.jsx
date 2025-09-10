export default function Onboarding() {
  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-semibold mb-2">Welcome to Astrooverz</h1>
      <p className="opacity-80 mb-6">Let's set up your profile to personalize your guidance.</p>
      
      <div className="space-y-4">
        <div className="form-control">
          <label className="label">
            <span className="label-text">Full Name</span>
          </label>
          <input type="text" placeholder="Enter your full name" className="input input-bordered" />
        </div>
        
        <div className="form-control">
          <label className="label">
            <span className="label-text">Date of Birth</span>
          </label>
          <input type="date" className="input input-bordered" />
        </div>
        
        <div className="form-control">
          <label className="label">
            <span className="label-text">Time of Birth</span>
          </label>
          <input type="time" className="input input-bordered" />
        </div>
        
        <div className="form-control">
          <label className="label">
            <span className="label-text">Birth Location</span>
          </label>
          <input type="text" placeholder="City, Country" className="input input-bordered" />
        </div>
        
        <button className="btn btn-primary w-full">
          Complete Setup
        </button>
      </div>
    </div>
  );
}
