"use client";
import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function Pair() {
  const router = useRouter();
  const [token, setToken] = useState("");
  const [inviteCode, setInviteCode] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) { router.push("/login"); return; }
    setToken(t);
    checkStatus(t);
  }, []);

  const checkStatus = async (t: string) => {
    const res = await api.getCoupleStatus(t);
    if (res.has_partner) {
      router.push("/dashboard");
    } else if (res.has_couple) {
      setInviteCode(res.invite_code);
    }
  };

  const handleCreate = async () => {
    setLoading(true);
    const res = await api.createCouple(token);
    if (res.invite_code) setInviteCode(res.invite_code);
    else setMessage(res.detail);
    setLoading(false);
  };

  const handleJoin = async () => {
    setLoading(true);
    const res = await api.joinCouple(token, joinCode);
    if (res.message === "Joined couple") {
      router.push("/dashboard");
    } else {
      setMessage(res.detail || res.message);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold mb-2">Pair with your partner</h1>
        <p className="text-gray-400 text-sm mb-8">
          Connect with your partner to start sharing check-ins and daily questions.
        </p>

        {message && <p className="text-red-400 text-sm mb-4">{message}</p>}

        {inviteCode ? (
          <div className="bg-gray-900 border border-pink-900 rounded-xl p-6 mb-6 text-center">
            <p className="text-gray-400 text-sm mb-3">Share this code with your partner</p>
            <p className="text-3xl font-bold text-pink-400 tracking-widest mb-4">{inviteCode}</p>
            <button onClick={() => navigator.clipboard.writeText(inviteCode)}
              className="text-sm border border-gray-700 hover:border-pink-500 px-4 py-2 rounded-lg transition">
              Copy code
            </button>
            <p className="text-gray-500 text-xs mt-4">Waiting for your partner to join...</p>
          </div>
        ) : (
          <button onClick={handleCreate} disabled={loading}
            className="w-full bg-pink-600 hover:bg-pink-700 py-3 rounded-lg font-medium transition mb-6 disabled:opacity-50">
            {loading ? "Creating..." : "Create invite code"}
          </button>
        )}

        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 h-px bg-gray-800"></div>
          <span className="text-gray-500 text-sm">or</span>
          <div className="flex-1 h-px bg-gray-800"></div>
        </div>

        <p className="text-sm font-medium mb-3">I have a code from my partner</p>
        <div className="flex gap-2">
          <input className="flex-1 bg-gray-800 rounded-lg px-4 py-3 text-sm outline-none uppercase"
            placeholder="Enter code" value={joinCode}
            onChange={e => setJoinCode(e.target.value.toUpperCase())} />
          <button onClick={handleJoin} disabled={loading || !joinCode}
            className="bg-pink-600 hover:bg-pink-700 px-6 rounded-lg text-sm font-medium transition disabled:opacity-50">
            Pair now
          </button>
        </div>
      </div>
    </main>
  );
}