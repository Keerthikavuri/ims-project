import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import IncidentDetail from "./pages/IncidentDetail";

function App() {
  const [selectedIncident, setSelectedIncident] = useState(null);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#11111b",
      fontFamily: "'Segoe UI', sans-serif",
    }}>
      {selectedIncident ? (
        <IncidentDetail
          incidentId={selectedIncident}
          onBack={() => setSelectedIncident(null)}
        />
      ) : (
        <Dashboard onSelectIncident={setSelectedIncident} />
      )}
    </div>
  );
}

export default App;