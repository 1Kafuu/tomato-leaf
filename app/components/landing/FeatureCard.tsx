type FeatureCardProps = {
  title: string;
  desc: string;
  icon: React.ReactNode;
};

export default function FeatureCard({ title, desc, icon }: FeatureCardProps) {
  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white p-6 desktop:flex-1 hover:border-border-action transition-colors">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-12 h-12 rounded-2xl bg-surface-default text-icon-default border border-border-default flex items-center justify-center">
          {icon}
        </div>
        <h1 className="md-semibold text-text-heading">{title}</h1>
      </div>
      <p className="sm-default text-text-placeholder leading-relaxed">{desc}</p>
    </div>
  );
}
