const API_URL = "https://ldrai-production.up.railway.app";

export const api = {
  signup: async (email: string, password: string, name: string) => {
    const res = await fetch(`${API_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, name }),
    });
    return res.json();
  },

  login: async (email: string, password: string) => {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return res.json();
  },

  createCouple: async (token: string) => {
    const res = await fetch(`${API_URL}/couples/create`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.json();
  },

  joinCouple: async (token: string, code: string) => {
    const res = await fetch(`${API_URL}/couples/join/${code}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.json();
  },

  checkin: async (token: string, mood: number, stress: number, miss_you: number) => {
    const res = await fetch(`${API_URL}/checkins/`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ mood, stress, miss_you }),
    });
    return res.json();
  },

  getFeed: async (token: string) => {
    const res = await fetch(`${API_URL}/checkins/feed`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.json();
  },

  getDailyQuestion: async (token: string) => {
    const res = await fetch(`${API_URL}/ai/daily-question`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.json();
  },

  getWeeklyReport: async (token: string) => {
    const res = await fetch(`${API_URL}/ai/weekly-report`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.json();
  },

  getDashboard: async (token: string) => {
    const res = await fetch(`${API_URL}/dashboard/stats`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.json();
  },
};