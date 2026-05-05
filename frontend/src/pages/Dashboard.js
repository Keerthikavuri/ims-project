import { useState, useEffect } from "react";
import { getIncidents, getHealth } from "../api/client";
import IncidentCard from "../components/IncidentCard";

const Dashboard = ({ onSelectIncident }) => {
  const [incidents, setIncidents] = useState([]);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [inc, h] = await Promise.all([getIncidents(), getHealth()]);
      setIncidents(inc);
      setHealth(h);
    } catch (e) {
      console.error("Fetch failed:", e);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    // Every 5 seconds auto refresh
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const counts = {
    OPEN: incidents.filter(i => i.status === "OPEN").length,
    INVESTIGATING: incidents.filter(i => i.status === "INVESTIGATING").length,
    RESOLVED: incidents.filter(i => i.status === "RESOLVED").length,
    CLOSED: incidents.filter(i => i.status === "CLOSED").length,
  };

  return (
    <div style={{ padding: "24px", maxWidth: "900px", margin: "0 auto" }}>

      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <div>
          <h1 style={{ color: "#cdd6f4", fontSize: "24px", margin: 0 }}>
            🚨 Incident Management System
          </h1>
          <p style={{ color: "#6c7086", fontSize: "13px", marginTop: "4px" }}>
            Zeotap Infrastructure · Live Dashboard
          </p>
        </div>
        {health && (
          <div style={{
            background: health.status === "ok" ? "#1a2e1a" : "#2e1a1a",
            border: `1px solid ${health.status === "ok" ? "#16a34a" : "#dc2626"}`,
            borderRadius: "8px", padding: "8px 16px", textAlign: "center"
          }}>
            <div style={{ color: health.status === "ok" ? "#4ade80" : "#f87171", fontWeight: "700", fontSize: "13px" }}>
              {health.status === "ok" ? "✅ System Healthy" : "⚠️ Degraded"}
            </div>
            <div style={{ color: "#6c7086", fontSize: "11px" }}>
              Queue: {health.queue_size} · Uptime: {Math.round(health.uptime_seconds)}s
            </div>
          </div>
        )}
      </div>

      {/* Stats Row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px", marginBottom: "24px" }}>
        {[
          { label: "OPEN", count: counts.OPEN, color: "#dc2626", bg: "#fee2e2" },
          { label: "INVESTIGATING", count: counts.INVESTIGATING, color: "#d97706", bg: "#fef3c7" },
          { label: "RESOLVED", count: counts.RESOLVED, color: "#2563eb", bg: "#dbeafe" },
          { label: "CLOSED", count: counts.CLOSED, color: "#16a34a", bg: "#dcfce7" },
        ].map(s => (
          <div key={s.label} style={{
            background: "#1e1e2e", border: "1px solid #313244",
            borderRadius: "10px", padding: "16px", textAlign: "center"
          }}>
            <div style={{ fontSize: "28px", fontWeight: "800", color: s.color }}>{s.count}</div>
            <div style={{ fontSize: "11px", color: "#6c7086", marginTop: "4px" }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Incidents List */}
      <h2 style={{ color: "#a6adc8", fontSize: "14px", marginBottom: "12px", textTransform: "uppercase" }}>
        All Incidents
      </h2>

      {loading ? (
        <div style={{ color: "#6c7086", textAlign: "center", padding: "40px" }}>
          Loading incidents...
        </div>
      ) : incidents.length === 0 ? (
        <div style={{ color: "#6c7086", textAlign: "center", padding: "40px" }}>
          No incidents yet. Run mock_signals.py to generate some!
        </div>
      ) : (
        incidents.map(incident => (
          <IncidentCard
            key={incident.id}
            incident={incident}
            onClick={onSelectIncident}
          />
        ))
      )}
    </div>
  );
};

export default Dashboard;