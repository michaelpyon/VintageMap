import { useState, useEffect, useImperativeHandle, forwardRef } from "react";
import type { Significance } from "../../types";
import "./DateInput.css";

interface Props {
  onSubmit: (year: number, significance: string) => void;
  loading: boolean;
}

export interface DateInputHandle {
  setYearAndSubmit: (year: number) => void;
}

const SIGNIFICANCES: { value: Significance; label: string }[] = [
  { value: "birthday", label: "Birthday" },
  { value: "anniversary", label: "Anniversary" },
  { value: "wedding", label: "Wedding" },
  { value: "graduation", label: "Graduation" },
  { value: "retirement", label: "Retirement" },
  { value: "memorial", label: "Memorial" },
  { value: "other", label: "Just Curious" },
];

const LEGENDARY_YEARS = new Set([1945, 1961, 1982, 1990, 2000, 2005, 2009, 2010, 2015, 2016, 2019]);

const DateInput = forwardRef<DateInputHandle, Props>(function DateInput({ onSubmit, loading }, ref) {
  const [year, setYear] = useState("");
  const [significance, setSignificance] = useState<Significance>("birthday");
  const [yearError, setYearError] = useState("");
  const [yearHint, setYearHint] = useState("");

  useImperativeHandle(ref, () => ({
    setYearAndSubmit(y: number) {
      setYear(String(y));
      setYearError("");
      onSubmit(y, significance);
    },
  }));

  // Live validation + legendary hint
  useEffect(() => {
    if (!year) {
      setYearError("");
      setYearHint("");
      return;
    }
    const y = parseInt(year, 10);
    if (isNaN(y)) {
      setYearError("");
      setYearHint("");
      return;
    }
    if (year.length >= 4 && (y < 1970 || y > 2023)) {
      setYearError("Please enter a year between 1970 and 2023");
      setYearHint("");
    } else {
      setYearError("");
      setYearHint(LEGENDARY_YEARS.has(y) ? "⭐ Legendary vintage" : "");
    }
  }, [year]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const y = parseInt(year, 10);
    if (isNaN(y) || y < 1970 || y > 2023) {
      setYearError("Please enter a year between 1970 and 2023");
      return;
    }
    setYearError("");
    onSubmit(y, significance);
  };

  return (
    <form className="date-input" onSubmit={handleSubmit}>
      <div className="date-input-row">
        <div className="field">
          <label htmlFor="year-input">Year <span className="field-hint">(1970 – 2023)</span></label>
          <input
            id="year-input"
            type="number"
            min={1970}
            max={2023}
            placeholder="e.g. 1990"
            value={year}
            onChange={(e) => setYear(e.target.value)}
          />
          {yearError && <span className="field-error">{yearError}</span>}
          {!yearError && yearHint && <span className="field-legendary-hint">{yearHint}</span>}
        </div>

        <div className="field">
          <label htmlFor="significance-select">Occasion <span className="field-hint">(shapes your pick)</span></label>
          <select
            id="significance-select"
            value={significance}
            onChange={(e) => setSignificance(e.target.value as Significance)}
          >
            {SIGNIFICANCES.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button type="submit" className="submit-btn" disabled={loading}>
        {loading ? <span className="spinner" /> : "Discover Your Vintage"}
      </button>
    </form>
  );
});

export default DateInput;
