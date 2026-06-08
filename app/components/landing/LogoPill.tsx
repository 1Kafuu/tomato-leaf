import Image from "next/image";

type LogoPillProps = {
  text: string;
  iconOnly?: boolean;
};

export default function LogoPill({ text, iconOnly = false }: LogoPillProps) {
  return (
    <div className="flex gap-2.5 bg-neutral-100 w-fit py-3 pr-5 pl-4 rounded-3xl items-center">
      <Image
        src="/images/logo.svg"
        alt="TomaCheck logo"
        width={20}
        height={20}
        className="h-5 w-auto"
      />
      {!iconOnly && <p className="sm-semibold text-text-label whitespace-nowrap">{text}</p>}
    </div>
  );
}
