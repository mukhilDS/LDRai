"use client";
import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const [token, setToken] = useState("");
  const [feed, setFeed] = useState<any>(null);
  const [question, setQuestion] = useState("");
  const [checkin, setCheckin] = useState({ mood: 3, stress: 3, miss_you: 3 });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [inviteCode, setInviteCode] = useState("");
  const [joinCode, setJoinCode] = useState("");

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) { router.push("/login"); return; }
    setToken(t);
    loadFeed(t);
    loadQuestion(t);
  }, []);

  const loadFeed = async (t: string) => {
    const res = await api.getFeed(t);
    if (!res.detail) setFeed(res);
  };

  const loadQuestion = async (t: string) => {
    const res = await api.getDailyQuestion(t);
    if (res.question) setQuestion(res.question);
  };

  const handleCheckin = async () => {
    setLoading(true);
    const res = await api.checkin(token, checkin.mood, checkin.stress, checkin.miss_you);
    setMessage(res.message || res.detail || "Done");
    setLoading(false);
  };

  const handleCreateCouple = async () => {
    const res = await api.createCouple(token);
    if (res.invite_code) setMessage(`Your invite code: ${res.invite_code}`);
    else setMessage(res.detail);
  };

  const handleJoinCouple = async () => {
    const res = await api.joinCouple(token, joinCode);
    setMessage(res.message || res.detail);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10 max-w-xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">LDRai 💌</h1>
        <button onClick={() => { localStorage.removeItem("token"); router.push("/"); }}
          className="text-gray-500 text-sm hover:text-white">Logout</button>
      </div>

      {question && (
        <div className="bg-gray-800 rounded-xl p-5 mb-6 border border-pink-900">
          <p className="text-xs text-pink-400 mb-2 font-medium">TODAY'S QUESTION</p>
          <p className="text-gray-200">{question}</p>
        </div>
      )}

      <div className="bg-gray-900 rounded-xl p-5 mb-6">
        <h2 className="font-semibold mb-4">Daily Check-in</h2>
        {(["mood", "stress", "miss_you"] as const).map((key) => (
          <div key={key} className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-400 capitalize">{key.replace("_", " ")}</span>
              <span className="text-pink-400 font-medium">{checkin[key]}/5</span>
            </div>
            <input type="range" min={1} max={5} value={checkin[key]}
              onChange={e => setCheckin({ ...checkin, [key]: parseInt(e.target.value) })}
              className="w-full accent-pink-500" />
          </div>
        ))}
        <button onClick={handleCheckin} disabled={loading}
          className="w-full bg-pink-600 hover:bg-pink-700 py-2.5 rounded-lg text-sm font-medium transition disabled:opacity-50">
          {loading ? "Saving..." : "Submit Check-in"}
        </button>
        {message && <p className="text-green-400 text-sm mt-3 text-center">{message}</p>}
      </div>

      {feed && feed.checkins?.length > 0 && (
        <div className="bg-gray-900 rounded-xl p-5 mb-6">
          <h2 className="font-semibold mb-3">{feed.partner_name}'s Recent Check-ins</h2>
          {feed.checkins.slice(0, 3).map((c: any, i: number) => (
            <div key={i} className="flex justify-between text-sm py-2 border-b border-gray-800 last:border-0">
              <span className="text-gray-500">{c.date}</span>
              <span>Mood {c.mood} · Stress {c.stress} · Miss {c.miss_you}</span>
            </div>
          ))}
        </div>
      )}

      <div className="bg-gray-900 rounded-xl p-5 mb-6">
        <h2 className="font-semibold mb-3">Partner Connection</h2>
        <button onClick={handleCreateCouple}
          className="w-full border border-gray-700 hover:border-pink-500 py-2.5 rounded-lg text-sm mb-3 transition">
          Create Couple & Get Invite Code
        </button>
        <div className="flex gap-2">
          <input className="flex-1 bg-gray-800 rounded-lg px-3 py-2.5 text-sm outline-none"
            placeholder="Enter invite code" value={joinCode}
            onChange={e => setJoinCode(e.target.value)} />
          <button onClick={handleJoinCouple}
            className="bg-pink-600 hover:bg-pink-700 px-4 rounded-lg text-sm transition">Join</button>
        </div>
      </div>

      <button onClick={() => router.push("/report")}
        className="w-full border border-gray-700 hover:border-pink-500 py-3 rounded-lg text-sm transition">
        View Weekly Report →
      </button>
    </main>
  );
}
