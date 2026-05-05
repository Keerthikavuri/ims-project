const BASE_URL = "http://localhost:8000";

export const getIncidents = async () => {
  const res = await fetch(`${BASE_URL}/incidents`);
  return res.json();
};

export const getIncident = async (id) => {
  const res = await fetch(`${BASE_URL}/incidents/${id}`);
  return res.json();
};

export const getIncidentSignals = async (id) => {
  const res = await fetch(`${BASE_URL}/incidents/${id}/signals`);
  return res.json();
};

export const updateStatus = async (id, new_status) => {
  const res = await fetch(`${BASE_URL}/incidents/${id}/status?new_status=${new_status}`, {
    method: "PATCH",
  });
  return res.json();
};

export const submitRCA = async (id, rcaData) => {
  const res = await fetch(`${BASE_URL}/incidents/${id}/rca`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(rcaData),
  });
  return res.json();
};

export const getHealth = async () => {
  const res = await fetch(`${BASE_URL}/health`);
  return res.json();
};