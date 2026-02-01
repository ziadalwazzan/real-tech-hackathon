const icons = {
  "trending-up": "M6 16l4-5 4 3 4-6",
  shield: "M12 3l7 4v5c0 4-3 7-7 9-4-2-7-5-7-9V7l7-4z",
  briefcase: "M9 6h6m-8 4h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2z",
  droplet: "M12 4s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z",
  map: "M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2V6z",
  sparkles: "M12 3l1.2 3.6L17 8l-3.8 1.4L12 13l-1.2-3.6L7 8l3.8-1.4L12 3z",
  "shield-check": "M12 3l7 4v5c0 4-3 7-7 9-4-2-7-5-7-9V7l7-4zM9 12l2 2 4-4",
  rocket: "M12 3l5 5-4 1-1 4-1-4-4-1 5-5z",
  info: "M12 6v1m0 3v5m0 8a9 9 0 1 0 0-18 9 9 0 0 0 0 18z",
};

export default function Icon({ name, className = "" }) {
  const path = icons[name];
  if (!path) return null;
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={`h-5 w-5 ${className}`}
      aria-hidden="true"
    >
      <path d={path} />
    </svg>
  );
}
