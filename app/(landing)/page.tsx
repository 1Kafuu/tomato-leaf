import PageHeading from "../components/landing/PageHeading";
import Marquee from "../components/landing/Marquee";
import ProblemSection from "../components/landing/ProblemSection";
import Features from "../components/landing/Features";
import HowItWorks from "../components/landing/HowItWorks";
import DiseaseSection from "../components/landing/DiseaseSection";
import CTASection from "../components/landing/CTASection";
import FAQSection from "../components/landing/FAQSection";

export default function Home() {
  return (
    <>
      <PageHeading />
      <Marquee />
      <ProblemSection />
      <Features />
      <HowItWorks />
      <DiseaseSection />
      <CTASection />
      <FAQSection />
    </>
  );
}