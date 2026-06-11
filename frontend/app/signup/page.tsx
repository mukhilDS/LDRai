"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Signup() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    const res = await api.signup(form.email, form.password, form.name);
    if (res.user_id) {
      router.push("/login");
    } else {
      setError(res.detail || "Something went wrong");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <h1 className="text-3xl font-bold mb-2">Create account</h1>
        <p className="text-gray-400 text-sm mb-8">Start your LDRai journey</p>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <input className="w-full bg-gray-800 rounded-lg px-4 py-3 mb-3 text-sm outline-none"
          placeholder="Your name" value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })} />
        <input className="w-full bg-gray-800 rounded-lg px-4 py-3 mb-3 text-sm outline-none"
          placeholder="Email" type="email" value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })} />
        <input className="w-full bg-gray-800 rounded-lg px-4 py-3 mb-6 text-sm outline-none"
          placeholder="Password" type="password" value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })} />

        <button onClick={handleSubmit} disabled={loading}
          className="w-full bg-pink-600 hover:bg-pink-700 py-3 rounded-lg font-medium transition disabled:opacity-50">
          {loading ? "Creating..." : "Create Account"}
        </button>

        <p className="text-gray-500 text-sm text-center mt-4">
          Already have an account? <Link href="/login" className="text-pink-400">Login</Link>
        </p>
      </div>
    </main>
  );
}