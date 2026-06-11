import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center px-6">
      <div className="max-w-lg text-center">
        <h1 className="text-5xl font-bold mb-4">LDRai 💌</h1>
        <p className="text-gray-400 text-lg mb-2">
          An AI relationship companion for long-distance couples.
        </p>
        <p className="text-gray-500 text-sm mb-10">
          Daily check-ins. Shared feeds. Personalized AI insights.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/signup" className="bg-pink-600 hover:bg-pink-700 px-6 py-3 rounded-lg font-medium transition">
            Get Started
          </Link>
          <Link href="/login" className="border border-gray-600 hover:border-gray-400 px-6 py-3 rounded-lg font-medium transition">
            Login
          </Link>
        </div>
      </div>
    </main>
  );
}