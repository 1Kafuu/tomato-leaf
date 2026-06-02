type StepCardProps = {
  step: string;
  title: string;
  desc: string;
  icon: React.ReactNode;
};

export default function StepCard({ step, title, desc, icon }: StepCardProps) {
  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white p-6 relative">
      <div className="flex items-start gap-4">
        <div className="shrink-0 w-12 h-12 rounded-2xl bg-surface-default text-icon-default border border-border-default flex items-center justify-center">
          {icon}
        </div>
        <div className="flex-1">
          <p className="xs-semibold text-text-action uppercase tracking-wider mb-1">
            {step}
          </p>
          <h1 className="md-semibold text-text-heading mb-2">{title}</h1>
          <p className="sm-default text-text-placeholder leading-relaxed">{desc}</p>
        </div>
      </div>
    </div>
  );
}
