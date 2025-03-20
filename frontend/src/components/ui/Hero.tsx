import Link from 'next/link';

export default function Hero() {
  return (
    <section className="relative min-h-screen w-full bg-neutral-800 bg-opacity-20 bg-[url('/images/hero-bg.jpg')] bg-cover bg-center bg-blend-soft-light">      
      <div className="container mx-auto flex min-h-screen flex-col items-center justify-center px-4 py-32 text-center">
        <h1 className="mb-4 text-4xl font-bold text-white md:text-5xl lg:text-6xl">
          Professional Auto Detailing
        </h1>
        <p className="mb-8 max-w-2xl text-xl text-gray-200">
          Transforming your vehicle with premium detailing services in Western Massachusetts
        </p>
        <div className="flex flex-col gap-4 sm:flex-row">
          <Link 
            href="/booking" 
            className="rounded-full bg-purple-700 px-8 py-4 text-lg font-semibold text-white transition hover:bg-purple-800"
          >
            Book Now
          </Link>
          <Link 
            href="/services" 
            className="rounded-full border-2 border-white bg-transparent px-8 py-4 text-lg font-semibold text-white transition hover:bg-white hover:text-gray-900"
          >
            Our Services
          </Link>
        </div>
      </div>
    </section>
  );
}