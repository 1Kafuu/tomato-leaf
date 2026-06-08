type ButtonProps = {
  text: string;
  inv?: boolean;
  icon?: boolean;
  onClick?: () => void;
  disabled?: boolean;
  fullWidth?: boolean;
  href?: string;
};

export default function Button({
  inv,
  text,
  icon = true,
  onClick,
  disabled,
  fullWidth,
  href,
}: ButtonProps) {
  const baseClass = `group ${inv ? "bg-surface-primary border border-border-action hover:bg-surface-primary-hover" : "bg-white border border-border-default hover:border-border-action-hover"} disabled:border-0 disabled:bg-surface-disabled ${fullWidth ? "w-full" : "w-full md:w-45"} h-11 md:h-14 flex items-center justify-between px-6 rounded-2xl transition-colors`;

  const content = (
    <>
      <h1
        className={`w-fit h-fit items-center font-bold label-semibold ${inv ? "text-neutral-white" : "text-text-action"} ${icon ? "" : "mx-auto"}`}
      >
        {text}
      </h1>
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={`${icon ? "block" : "hidden"} ${inv ? "" : "transition-transform group-hover:translate-x-0.5"}`}
      >
        <path
          d="M7.5 15L12.5 10L7.5 5"
          stroke={`${inv ? "#FFFFFF" : "#097315"}`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </>
  );

  if (href) {
    return (
      <a href={href} className={baseClass}>
        {content}
      </a>
    );
  }

  return (
    <button disabled={disabled} onClick={onClick} className={baseClass}>
      {content}
    </button>
  );
}
