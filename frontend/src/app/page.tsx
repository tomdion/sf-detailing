export default function Home() {
  return (
    <div className="mx-auto max-w-6xl">
      <section className="py-12 text-center">
        <h1 className="mb-4 text-4xl font-bold">SF Detailing</h1>
        <p className="mb-8 text-xl">Professional car detailing services in San Francisco</p>
        <div className="flex justify-center">
          <a
            href="/book"
            className="rounded bg-purple-700 px-6 py-3 text-white transition hover:bg-purple-800"
          >
            Book Now
          </a>
        </div>
      </section>

      <section className="grid gap-8 py-12 md:grid-cols-3">
        <div className="rounded-lg bg-white p-6 shadow-md">
          <h2 className="mb-3 text-xl font-semibold">Interior Detailing</h2>
          <p className="mb-4">Complete interior cleaning and conditioning, including seats, carpet, and dashboard.</p>
          <p className="font-semibold">Starting at $50</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-md">
          <h2 className="mb-3 text-xl font-semibold">Exterior Detailing</h2>
          <p className="mb-4">Hand wash, wax, and polish to restore your vehicle's shine and protect the paint.</p>
          <p className="font-semibold">Starting at $60</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-md">
          <h2 className="mb-3 text-xl font-semibold">Complete Package</h2>
          <p className="mb-4">Comprehensive interior and exterior detailing for the ultimate clean.</p>
          <p className="font-semibold">Starting at $100</p>
        </div>
      </section>
    </div>
  );
}
