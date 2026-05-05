import { useState, useEffect, useCallback } from "react";
import { getIncident, getIncidentSignals } from "../api/client";
import { StatusBadge, PriorityBadge } from "../components/StatusBadge";
import RCAForm from "../components/RCAForm";

const IncidentDetail = ({ incidentId, onBack }) => {
  const [incident, setIncident] = useState(null);
  const [signals, setSignals] = useState([]);
  const [showRCA, setShowRCA] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const [inc, sigs] = await Promise.all([
        getIncident(incidentId),
        getIncidentSignals(incidentId),
      ]);
      setIncident(inc);
      setSignals(sigs);
    } catch (e) {
      console.error("Fetch failed:", e);
    }
    setLoading(false);
  }, [incidentId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleStatusUpdate = async (newStatus) => {
    try {
      const res = await fetch(
        `http://localhost:8000/incidents/${incidentId}/status?new_status=${newStatus}`,
        { method: "PATCH" }
      );
      const data = await res.json();
      if (data.detail) alert(data.detail);
      fetchData();
    } catch (e) {
      alert("Failed: " + e.message);
    }
  };

  const NEXT_STATUS = {
    OPEN: "INVESTIGATING",
    INVESTIGATING: "RESOLVED",
    RESOLVED: "CLOSED",
  };

  if (loading) return <div style={{ color: "#6c7086", textAlign: "center", padding: "60px" }}>Loading...</div>;
  if (!incident) return <div style={{ color: "#f38ba8", textAlign: "center", padding: "60px" }}>Incident not found.</div>;

  return (
    <div style={{ padding: "24px", maxWidth: "900px", margin: "0 auto" }}>
      <button onClick={onBack} style={{
        background: "transparent", border: "1px solid #313244",
        color: "#a6adc8", borderRadius: "6px", padding: "6px 16px",
        cursor: "pointer", marginBottom: "20px", fontSize: "13px"
      }}>← Back to Dashboard</button>

      <div style={{ background: "#1e1e2e", border: "1px solid #313244", borderRadius: "10px", padding: "20px", marginBottom: "16px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ color: "#cdd6f4", margin: 0, fontSize: "20px" }}>{incident.component_id}</h2>
          <div style={{ display: "flex", gap: "8px" }}>
            <PriorityBadge priority={incident.priority} />
            <StatusBadge status={incident.status} />
          </div>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", marginTop: "16px" }}>
          {[
            { label: "Started", value: new Date(incident.start_time).toLocaleString() },
            { label: "Signals", value: incident.signal_count },
            { label: "MTTR", value: incident.mttr_seconds ? `${Math.round(incident.mttr_seconds)}s` : "In Progress" },
          ].map(item => (
            <div key={item.label}>
              <div style={{ color: "#6c7086", fontSize: "11px", textTransform: "uppercase" }}>{item.label}</div>
              <div style={{ color: "#cdd6f4", fontSize: "15px", fontWeight: "600", marginTop: "4px" }}>{item.value}</div>
            </div>
          ))}
        </div>
      </div>

      {incident.status !== "CLOSED" && (
        <div style={{ marginBottom: "16px", display: "flex", gap: "10px" }}>
          <button onClick={() => handleStatusUpdate(NEXT_STATUS[incident.status])} style={{
            background: "#89b4fa", color: "#1e1e2e", border: "none",
            borderRadius: "6px", padding: "10px 20px", fontWeight: "700",
            cursor: "pointer", fontSize: "13px"
          }}>Move to {NEXT_STATUS[incident.status]}</button>

          {incident.status === "RESOLVED" && (
            <button onClick={() => setShowRCA(!showRCA)} style={{
              background: "#cba6f7", color: "#1e1e2e", border: "none",
              borderRadius: "6px", padding: "10px 20px", fontWeight: "700",
              cursor: "pointer", fontSize: "13px"
            }}>{showRCA ? "Hide RCA Form" : "📋 Submit RCA"}</button>
          )}
        </div>
      )}

      {showRCA && <RCAForm incident={incident} onSuccess={() => { setShowRCA(false); fetchData(); }} />}

      <h3 style={{ color: "#a6adc8", fontSize: "13px", textTransform: "uppercase", marginBottom: "10px" }}>
        Raw Signals ({signals.length})
      </h3>
      <div style={{ maxHeight: "300px", overflowY: "auto" }}>
        {signals.map((sig, i) => (
          <div key={i} style={{ background: "#181825", border: "1px solid #313244", borderRadius: "6px", padding: "10px 14px", marginBottom: "8px" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ color: "#f38ba8", fontSize: "12px", fontWeight: "600" }}>{sig.error_type}</span>
              <span style={{ color: "#6c7086", fontSize: "11px" }}>{sig.received_at}</span>
            </div>
            <div style={{ color: "#a6adc8", fontSize: "12px", marginTop: "4px" }}>{sig.message}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default IncidentDetail;