// export const API_BASE = "http://localhost:8000";
// export const API_BASE = `${process.env.REACT_APP_DOMAIN_NAME}:${process.env.REACT_APP_PORT}` || 'http://localhost:8000';
export const API_BASE = process.env.REACT_APP_API_ORIGIN || 'http://localhost:8000';


export async function listSessions(token) {
  const res = await fetch(`${API_BASE}/api/sessions`, {headers: {Authorization: `Bearer ${token}`}});
  if (!res.ok) throw new Error("Failed to fetch sessions");
  return res.json();
}

export async function createSession(token) {
  const res = await fetch(`${API_BASE}/api/sessions`, 
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    }
  });
  if (!res.ok) throw new Error("Failed to create session");
  return res.json();
}

export async function deleteSession(token, sessionId) {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}`, {method: "DELETE", headers: { Authorization: `Bearer ${token}` }});
  if (!res.ok) throw new Error("Failed to delete session");
}

export async function getSession(token, sessionId) {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}`, {headers: {Authorization: `Bearer ${token}`}});
  if (!res.ok) throw new Error("Failed to fetch session");
  return res.json();
}
