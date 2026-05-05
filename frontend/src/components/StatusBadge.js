export const STATUS_COLORS = {
  OPEN: { bg: "#fee2e2", color: "#dc2626", label: "OPEN" },
  INVESTIGATING: { bg: "#fef3c7", color: "#d97706", label: "INVESTIGATING" },
  RESOLVED: { bg: "#dbeafe", color: "#2563eb", label: "RESOLVED" },
  CLOSED: { bg: "#dcfce7", color: "#16a34a", label: "CLOSED" },
};

export const PRIORITY_COLORS = {
  P0: { bg: "#fee2e2", color: "#dc2626" },
  P1: { bg: "#ffedd5", color: "#ea580c" },
  P2: { bg: "#fef9c3", color: "#ca8a04" },
};

export const StatusBadge = ({ status }) => {
  const style = STATUS_COLORS[status] || STATUS_COLORS.OPEN;
  return (
    <span style={{
      backgroundColor: style.bg,
      color: style.color,
      padding: "2px 10px",
      borderRadius: "12px",
      fontWeight: "600",
      fontSize: "12px",
    }}>
      {style.label}
    </span>
  );
};

export const PriorityBadge = ({ priority }) => {
  const style = PRIORITY_COLORS[priority] || PRIORITY_COLORS.P2;
  return (
    <span style={{
      backgroundColor: style.bg,
      color: style.color,
      padding: "2px 10px",
      borderRadius: "12px",
      fontWeight: "700",
      fontSize: "12px",
    }}>
      {priority}
    </span>
  );
};