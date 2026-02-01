import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Results from "./pages/Results";
import ExploreCities from "./pages/ExploreCities";

export default function App() {
  return (
    <div className="min-h-screen gradient-shell text-ink">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-6 sm:px-6 lg:px-10">
        <header className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-ink text-white shadow-glow">
              📈
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Real Estate Risk Analysis</p>
              <p className="font-display text-lg">INSITE</p>
            </div>
          </div>
          <div className="hidden items-center gap-3 text-xs text-slate-500 sm:flex">
            <span className="rounded-full border border-slate-200 px-3 py-1">Mobile-first UI</span>
            <span className="rounded-full border border-slate-200 px-3 py-1">Mock API</span>
          </div>
        </header>

        <main className="flex flex-1 flex-col py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results" element={<Results />} />
            <Route path="/explore" element={<ExploreCities />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <footer className="text-xs text-slate-500 flex justify-center">
          <p>UCL CSRI Hackathon {new Date().getFullYear()} • Copyright </p>
        </footer>
      </div>
    </div>
  );
}
