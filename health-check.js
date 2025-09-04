// Simple health check script for debugging
const endpoints = [
  'http://localhost:8000/',
  'http://localhost:8000/healthz',
  'http://localhost:8000/api/healthz',
  'http://localhost:80/',
  'https://astrooverz.com/',
  'https://astrooverz.com/healthz',
  'https://astrooverz.com/api/healthz'
];

async function checkEndpoint(url) {
  try {
    const response = await fetch(url);
    const status = response.status;
    const ok = response.ok;
    console.log(`✅ ${url} - Status: ${status} ${ok ? 'OK' : 'ERROR'}`);
    if (ok) {
      try {
        const data = await response.text();
        console.log(`   Response: ${data.substring(0, 100)}...`);
      } catch (e) {
        console.log(`   Response: [Could not read response]`);
      }
    }
  } catch (error) {
    console.log(`❌ ${url} - Error: ${error.message}`);
  }
}

async function runHealthChecks() {
  console.log('🔍 Running health checks...\n');
  
  for (const endpoint of endpoints) {
    await checkEndpoint(endpoint);
    console.log(''); // Empty line for readability
  }
  
  console.log('🏁 Health checks complete!');
}

// Run health checks
runHealthChecks().catch(console.error);
