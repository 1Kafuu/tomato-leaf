type StatCardProps = {
  title: string;
  date: string;
  volume: string;
  desc: string;
};

export default function StatCard({ title, date, volume, desc }: StatCardProps) {
  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white desktop:flex-1">
      <div className="p-6">
        <h1 className="md-semibold text-text-heading">{title}</h1>
        <p className="sm-default text-text-placeholder mt-1">{date}</p>
      </div>
      <div className="py-10 rounded-2xl border-t-2 border-border-default border-dashed desktop:border-solid bg-surface-default">
        <h1 className="text-[40px] md:text-[48px] leading-none text-text-action font-bold w-fit mx-auto">
          {volume}
        </h1>
        <p className="md-default text-text-placeholder text-center mt-2">{desc}</p>
      </div>
    </div>
  );
}
