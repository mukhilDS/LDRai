"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Login() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    const res = await api.login(form.email, form.password);
    if (res.access_token) {
      localStorage.setItem("token", res.access_token);
      router.push("/dashboard");
    } else {
      setError(res.detail || "Invalid credentials");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <h1 className="text-3xl font-bold mb-2">Welcome back</h1>
        <p className="text-gray-400 text-sm mb-8">Login to your LDRai account</p>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <input className="w-full bg-gray-800 rounded-lg px-4 py-3 mb-3 text-sm outline-none"
          placeholder="Email" type="email" value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })} />
        <input className="w-full bg-gray-800 rounded-lg px-4 py-3 mb-6 text-sm outline-none"
          placeholder="Password" type="password" value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })} />

        <button onClick={handleSubmit} disabled={loading}
          className="w-full bg-pink-600 hover:bg-pink-700 py-3 rounded-lg font-medium transition disabled:opacity-50">
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-gray-500 text-sm text-center mt-4">
          No account? <Link href="/signup" className="text-pink-400">Sign up</Link>
        </p>
      </div>
    </main>
  );
}