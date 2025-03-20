import Link from 'next/link';

export default function CTA() {
    return (
      <section className="py-16 bg-gray-900 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Vehicle?</h2>
          <p className="max-w-2xl mx-auto mb-8">
            Book your appointment today and experience the SF Detailing difference. 
            Our professional team is ready to make your car look its absolute best.
          </p>
          <Link 
            href="/booking" 
            className="inline-block rounded-full bg-purple-700 px-8 py-4 text-lg font-semibold transition hover:bg-purple-800"
          >
            Book Now
          </Link>
        </div>
      </section>
    );
  }