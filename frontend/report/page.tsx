"use client";
import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function Report() {
  const router = useRouter();
  const [report, setReport] = useState<any>(null);
  const [dashboard, setDashboard] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) { router.push("/login"); return; }
    Promise.all([api.getWeeklyReport(t), api.getDashboard(t)]).then(([r, d]) => {
      if (!r.detail) setReport(r);
      if (!d.detail) setDashboard(d);
      setLoading(false);
    });
  }, []);

  if (loading) return (
    <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
      <p className="text-gray-400">Loading report...</p>
    </main>
  );

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10 max-w-xl mx-auto">
      <button onClick={() => router.push("/dashboard")}
        className="text-gray-500 text-sm hover:text-white mb-6 block">← Back</button>

      <h1 className="text-2xl font-bold mb-6">Weekly Report</h1>

      {report && (
        <div className="bg-gray-900 rounded-xl p-5 mb-6 border border-pink-900">
          <p className="text-xs text-pink-400 mb-2 font-medium">AI INSIGHT</p>
          <p className="text-gray-200 leading-relaxed">{report.week_summary}</p>
        </div>
      )}

      {dashboard && (
        <>
          <div className="bg-gray-900 rounded-xl p-5 mb-6">
            <h2 className="font-semibold mb-4">This Week's Stats</h2>
            <p className="text-gray-400 text-sm mb-4">{dashboard.insight}</p>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: "Your Avg Mood", value: dashboard.summary.my_avg_mood },
                { label: `${dashboard.summary.partner_name || "Partner"} Avg Mood`, value: dashboard.summary.partner_avg_mood },
                { label: "Your Avg Stress", value: dashboard.summary.my_avg_stress },
                { label: `${dashboard.summary.partner_name || "Partner"} Avg Stress`, value: dashboard.summary.partner_avg_stress },
              ].map((stat, i) => (
                <div key={i} className="bg-gray-800 rounded-lg p-3 text-center">
                  <p className="text-2xl font-bold text-pink-400">{stat.value}</p>
                  <p className="text-xs text-gray-400 mt-1">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gray-900 rounded-xl p-5">
            <h2 className="font-semibold mb-3">Check-in Count</h2>
            <div className="flex justify-around text-center">
              <div>
                <p className="text-3xl font-bold text-pink-400">{dashboard.summary.my_total_checkins}</p>
                <p className="text-xs text-gray-400 mt-1">Your check-ins</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-pink-400">{dashboard.summary.partner_total_checkins}</p>
                <p className="text-xs text-gray-400 mt-1">Partner's check-ins</p>
              </div>
            </div>
          </div>
        </>
      )}
    </main>
  );
}