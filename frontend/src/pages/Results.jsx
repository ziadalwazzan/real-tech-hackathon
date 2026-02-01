import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import PrimaryButton from "../components/PrimaryButton";
import { MonthlyBarChart } from "../components/SeasonalBarChart";
import { SeasonalPriceCard } from "../components/SeasonalPriceCard";
import {
  fetchFrontierComparables,
  fetchRiskAssessment,
  fetchSeasonalPrices,
} from "../services/api";

export default function Results() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);
  const [comparables, setComparables] = useState([]);
  const [comparablesError, setComparablesError] = useState("");
  const [seasonalData, setSeasonalData] = useState([]);
  const [seasonalError, setSeasonalError] = useState("");

  const payload = useMemo(() => {
    if (!state?.query || !state?.locationType) return null;
    return { query: state.query, location_type: state.locationType };
  }, [state]);

  useEffect(() => {
    if (!payload) {
      setLoading(false);
      setError("Missing location input. Please start a new search.");
      return;
    }

    let isActive = true;
    setLoading(true);
    fetchRiskAssessment(payload)
      .then((response) => {
        if (!isActive) return;
        setData(response);
        setError("");
      })
      .catch((err) => {
        if (!isActive) return;
        setError(err.message || "Unable to load results");
      })
      .finally(() => {
        if (isActive) setLoading(false);
      });

    return () => {
      isActive = false;
    };
  }, [payload]);

  useEffect(() => {
    if (!state?.query || state?.locationType !== "city") {
      setComparables([]);
      setComparablesError("Quick facts available for city searches only.");
      return;
    }

    const rawQuery = state.query.trim();
    const normalizedCity = rawQuery.includes("(")
      ? rawQuery
      : rawQuery.includes(",")
        ? `${rawQuery.split(",")[0].trim()} (${rawQuery.split(",")[1].trim().toUpperCase()})`
        : rawQuery;

    let isActive = true;
    fetchFrontierComparables(normalizedCity, 3)
      .then((response) => {
        if (!isActive) return;
        setComparables(response.results || []);
        setComparablesError("");
      })
      .catch((err) => {
        if (!isActive) return;
        setComparables([]);
        setComparablesError(err.message || "Unable to load quick facts");
      });

    return () => {
      isActive = false;
    };
  }, [state?.query, state?.locationType]);

  useEffect(() => {
    if (!state?.query || state?.locationType !== "city") {
      setSeasonalData([]);
      setSeasonalError("Seasonality is available for city searches only.");
      return;
    }

    const rawQuery = state.query.trim();
    const normalizedCity = rawQuery.includes("(")
      ? rawQuery
      : rawQuery.includes(",")
        ? `${rawQuery.split(",")[0].trim()} (${rawQuery.split(",")[1].trim().toUpperCase()})`
        : rawQuery;

    let isActive = true;
    fetchSeasonalPrices(normalizedCity)
      .then((response) => {
        if (!isActive) return;
        setSeasonalData(response.monthly || []);
        setSeasonalError("");
      })
      .catch((err) => {
        if (!isActive) return;
        setSeasonalData([]);
        setSeasonalError(err.message || "Unable to load seasonal prices");
      });

    return () => {
      isActive = false;
    };
  }, [state?.query, state?.locationType]);

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <div className="glass-panel flex w-full max-w-lg flex-col gap-4 rounded-3xl p-8 text-center">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Analyzing</p>
          <p className="font-display text-3xl text-ink">Running the risk model...</p>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
            <div className="h-full w-2/3 animate-pulse rounded-full bg-ink/70" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <div className="glass-panel flex w-full max-w-lg flex-col gap-4 rounded-3xl p-8 text-center">
          <p className="font-display text-3xl text-ink">We hit a snag</p>
          <p className="text-sm text-slate-600">{error}</p>
          <PrimaryButton onClick={() => navigate("/")}>Start new search</PrimaryButton>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const quickFacts = comparables.map((entry, index) => ({
    city: entry.city,
    risk: `${entry.risk_score.toFixed(2)}`,
    returnFactor: `${entry.return_score.toFixed(2)}`,
    isCurrent: index === 0,
  }));

  return (
    <section className="flex flex-1 flex-col gap-8">
      <div className="flex flex-col justify-between gap-4 rounded-3xl p-4 sm:p-8">
        <div className="space-y-3">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Location</p>
          <h2 className="font-display text-3xl text-ink sm:text-4xl">{data.location}</h2>
        </div>
      </div>

      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xs uppercase tracking-[0.3em] text-slate-500">Risk Return Analysis</h3>
        </div>
        {comparablesError ? (
          <div className="rounded-3xl border border-slate-200 bg-white/70 p-5 text-sm text-slate-600">
            {comparablesError}
          </div>
        ) : (
          <div className="flex gap-4 overflow-x-auto pb-4">
            {quickFacts.map((city) => (
              <div
                key={city.city}
                className={`min-w-[220px] rounded-3xl border p-5 ${
                  city.isCurrent
                    ? "border-ink bg-ink text-white shadow-glow"
                    : "border-slate-200 bg-white/70 text-slate-700"
                }`}
              >
                <p className="text-xs uppercase tracking-[0.3em] opacity-70">City</p>
                <p className="mt-2 text-lg font-semibold">{city.city}</p>
                <div className="mt-4 flex flex-col gap-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className={city.isCurrent ? "text-white/70" : "text-slate-500"}>
                      Risk factor %
                    </span>
                    <span className="font-semibold">{city.risk}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className={city.isCurrent ? "text-white/70" : "text-slate-500"}>
                      Return factor %
                    </span>
                    <span className="font-semibold">{city.returnFactor}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
        {seasonalError ? (
          <div className="rounded-3xl border border-slate-200 bg-white/70 p-5 text-sm text-slate-600">
            {seasonalError}
          </div>
        ) : (
          <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]">
            <SeasonalPriceCard data={seasonalData} />
            <MonthlyBarChart data={seasonalData} />
          </div>
        )}
      </section>

      <section className="glass-panel rounded-3xl p-6">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Next Actions</p>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row">
          <PrimaryButton onClick={() => navigate("/")}>Search Another Location</PrimaryButton>
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-full border border-slate-300 px-6 py-3 text-sm font-semibold text-slate-700 transition hover:border-ink hover:text-ink"
          >
            Share Results
          </button>
        </div>
      </section>
    </section>
  );
}
