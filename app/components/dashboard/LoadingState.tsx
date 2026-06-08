export default function LoadingState() {
  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white p-8 md:p-12 text-center">
      <div className="w-16 h-16 mx-auto rounded-2xl bg-surface-primary-light border-2 border-border-action flex items-center justify-center mb-4 text-icon-action">
        <svg
          className="animate-spin"
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
        >
          <circle
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="3"
            className="opacity-25"
          />
          <path
            d="M4 12a8 8 0 018-8"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
          />
        </svg>
      </div>
      <h3 className="md-semibold text-text-heading mb-1">
        Sedang Menganalisis...
      </h3>
      <p className="sm-default text-text-placeholder">
        Proses ini biasanya memakan waktu kurang dari 5 detik
      </p>
    </div>
  );
}
