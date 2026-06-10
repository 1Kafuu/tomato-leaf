import Navbar from "../components/landing/Navbar";
import Footer from "../components/landing/Footer";

export default function MarketingLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Navbar variant="marketing" />
      <main className="flex-1">{children}</main>
      <Footer variant="marketing" />
    </>
  );
}
