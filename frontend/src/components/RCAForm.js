import { useState } from "react";
import { submitRCA } from "../api/client";

const RCAForm = ({ incident, onSuccess }) => {
  const [form, setForm] = useState({
    incident_start: incident.start_time?.slice(0, 16) || "",
    incident_end: new Date().toISOString().slice(0, 16),
    root_cause_category: "INFRA",
    fix_applied: "",
    prevention_steps: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async () => {
    if (!form.fix_applied || !form.prevention_steps) {
      setError("All fields are required!");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await submitRCA(incident.id, {
        work_item_id: incident.id,
        incident_start: form.incident_start + ":00",
        incident_end: form.incident_end + ":00",
        root_cause_category: form.root_cause_category,
        fix_applied: form.fix_applied,
        prevention_steps: form.prevention_steps,
      });
      if (res.id) {
        setSuccess(true);
        setTimeout(() => onSuccess(), 1000);
      } else {
        setError(JSON.stringify(res));
      }
    } catch (e) {
      setError("Failed: " + e.message);
    }
    setLoading(false);
  };

  const inputStyle = {
    width: "100%", background: "#181825", border: "1px solid #313244",
    borderRadius: "6px", color: "#cdd6f4", padding: "8px",
    marginTop: "4px", fontSize: "13px",
  };
  const labelStyle = {
    color: "#a6adc8", fontSize: "13px", marginTop: "12px", display: "block",
  };

  if (success) return (
    <div style={{
      background: "#1a2e1a", border: "1px solid #16a34a",
      borderRadius: "10px", padding: "20px", marginTop: "16px",
      color: "#4ade80", textAlign: "center", fontSize: "16px"
    }}>
      ✅ RCA Submitted Successfully!
    </div>
  );

  return (
    <div style={{ background: "#1e1e2e", borderRadius: "10px", padding: "20px", marginTop: "16px" }}>
      <h3 style={{ color: "#cba6f7", marginBottom: "12px" }}>📋 Submit RCA</h3>
      {error && <div style={{ color: "#f38ba8", marginBottom: "10px", fontSize: "13px" }}>⚠️ {error}</div>}

      <label style={labelStyle}>Incident Start</label>
      <input type="datetime-local" name="incident_start"
        value={form.incident_start}
        onChange={e => setForm({...form, incident_start: e.target.value})}
        style={inputStyle} />

      <label style={labelStyle}>Incident End</label>
      <input type="datetime-local" name="incident_end"
        value={form.incident_end}
        onChange={e => setForm({...form, incident_end: e.target.value})}
        style={inputStyle} />

      <label style={labelStyle}>Root Cause Category</label>
      <select value={form.root_cause_category}
        onChange={e => setForm({...form, root_cause_category: e.target.value})}
        style={inputStyle}>
        <option value="INFRA">INFRA</option>
        <option value="CODE">CODE</option>
        <option value="CONFIG">CONFIG</option>
        <option value="NETWORK">NETWORK</option>
        <option value="HUMAN">HUMAN</option>
      </select>

      <label style={labelStyle}>Fix Applied</label>
      <textarea rows={3} value={form.fix_applied}
        onChange={e => setForm({...form, fix_applied: e.target.value})}
        placeholder="What fix was applied?"
        style={{ ...inputStyle, resize: "vertical" }} />

      <label style={labelStyle}>Prevention Steps</label>
      <textarea rows={3} value={form.prevention_steps}
        onChange={e => setForm({...form, prevention_steps: e.target.value})}
        placeholder="How to prevent this in future?"
        style={{ ...inputStyle, resize: "vertical" }} />

      <button onClick={handleSubmit} disabled={loading} style={{
        marginTop: "16px", background: "#cba6f7", color: "#1e1e2e",
        border: "none", borderRadius: "6px", padding: "10px 24px",
        fontWeight: "700", cursor: "pointer", fontSize: "14px",
        opacity: loading ? 0.7 : 1,
      }}>
        {loading ? "Submitting..." : "Submit RCA"}
      </button>
    </div>
  );
};

export default RCAForm;