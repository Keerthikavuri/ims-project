import { StatusBadge, PriorityBadge } from "./StatusBadge";

const IncidentCard = ({ incident, onClick }) => {
  return (
    <div
      onClick={() => onClick(incident.id)}
      style={{
        background: "#1e1e2e",
        border: "1px solid #313244",
        borderRadius: "10px",
        padding: "16px",
        marginBottom: "12px",
        cursor: "pointer",
        transition: "border 0.2s",
      }}
      onMouseEnter={e => e.currentTarget.style.border = "1px solid #89b4fa"}
      onMouseLeave={e => e.currentTarget.style.border = "1px solid #313244"}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <div style={{ color: "#cdd6f4", fontWeight: "700", fontSize: "15px" }}>
            {incident.component_id}
          </div>
          <div style={{ color: "#6c7086", fontSize: "12px", marginTop: "4px" }}>
            {new Date(incident.created_at).toLocaleString()}
          </div>
        </div>
        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
          <PriorityBadge priority={incident.priority} />
          <StatusBadge status={incident.status} />
        </div>
      </div>
      <div style={{ marginTop: "10px", display: "flex", gap: "16px" }}>
        <span style={{ color: "#a6adc8", fontSize: "13px" }}>
          🔔 Signals: <b style={{ color: "#cdd6f4" }}>{incident.signal_count}</b>
        </span>
        {incident.mttr_seconds && (
          <span style={{ color: "#a6adc8", fontSize: "13px" }}>
            ⏱ MTTR: <b style={{ color: "#a6e3a1" }}>{Math.round(incident.mttr_seconds)}s</b>
          </span>
        )}
      </div>
    </div>
  );
};

export default IncidentCard;