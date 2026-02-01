import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import PrimaryButton from "../components/PrimaryButton";
import SegmentedToggle from "../components/SegmentedToggle";

const ZIP_REGEX = /^\d{5}(-\d{4})?$/;

export default function Home() {
  const [locationType, setLocationType] = useState("city");
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const placeholder = locationType === "zip" ? "e.g. 90210" : "e.g. Austin";

  const handleSubmit = (event) => {
    event.preventDefault();
    const trimmed = query.trim();

    if (!trimmed) {
      setError("Enter a location to continue.");
      return;
    }

    if (locationType === "zip" && !ZIP_REGEX.test(trimmed)) {
      setError("Enter a valid ZIP code (12345 or 12345-6789).");
      return;
    }

    setError("");
    navigate("/results", {
      state: { query: trimmed, locationType },
    });
  };

  return (
    <section className="flex flex-1 flex-col items-center justify-center gap-10 text-center">
      <div className="space-y-4">
        <h1 className="font-display text-4xl text-ink sm:text-5xl">
          Know the risk before you invest
        </h1>
        <p className="mx-auto max-w-xl text-sm text-slate-600 sm:text-base">
          Run a fast, mobile-first risk check on any zip code or city. Get an
          investor-ready summary in seconds.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="glass-panel w-full max-w-xl rounded-3xl p-6 text-left sm:p-8"
      >
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-3">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Location Type</p>
            <div className="flex justify-center sm:justify-start">
              <SegmentedToggle value={locationType} onChange={setLocationType} />
            </div>
          </div>

          <label className="flex flex-col gap-2 text-sm text-slate-600">
            <span className="font-semibold text-ink">Location</span>
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder={placeholder}
              className="h-12 rounded-2xl border-slate-200 bg-white/80 px-4 text-sm focus:border-ink focus:ring-ink"
            />
          </label>

          {error && (
            <div className="rounded-2xl border border-rose-100 bg-rose-50 px-4 py-3 text-xs text-rose-600">
              {error}
            </div>
          )}

          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <PrimaryButton type="submit">Continue</PrimaryButton>
          </div>
          <div className="flex justify-center sm:justify-end">
            <Link
              to="/explore"
              className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-500 underline decoration-2 underline-offset-4 transition hover:text-ink"
            >
              explore cities
            </Link>
          </div>
        </div>
      </form>
    </section>
  );
}
