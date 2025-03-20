import Navbar from "@/components/ui/Navbar";
import Hero from '@/components/ui/Hero';
import Services from '@/components/ui/Services';
import CTA from '@/components/ui/CTA';
import Footer from '@/components/ui/Footer';

export default function Home() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <Hero />
      <Services />
      <CTA />
      <Footer />
    </main>
  );
}