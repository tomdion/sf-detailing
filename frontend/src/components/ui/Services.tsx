export default function Services() {
    const servicePackages = [
      {
        name: "Interior Detailing",
        description: "Complete interior cleaning and conditioning, including seats, carpet, and dashboard.",
        price: "$50",
        features: [
          "Vacuuming",
          "Steam Cleaning",
          "Leather Cleaning and Conditioning",
          "Dashboard and Console Cleaning",
          "Air Vent Cleaning",
          "Door Panel Cleaning",
          "Glass and Window Cleaning",
          "Odor Removal",
          "Stain Removal (Optional)",
          "Pet Hair Removal (Optional)",
          
        ]
      },
      {
        name: "Exterior Detailing",
        description: "Hand wash, wax, and polish to restore your vehicle's shine and protect the paint.",
        price: "$60",
        features: [
          "Exterior Wash",
          "Wheel and Tire Cleaning",
          "Tire Dressing",
          "Exterior Glass Cleaning",
          "Door Jamb Cleaning",
          "Clay Bar Treatment (Optional)",
          "Paint Polishing and Correction (Optional)",
          "Wax Application (Optional)",
          "Trim and Plastic Restoration (Optional)",
        ]
      },
      {
        name: "Complete Package",
        description: "Comprehensive interior and exterior detailing for the ultimate clean.",
        price: "$100",
        features: [
          "Everything included in the Interior and Exterior Detail Packages",
        ]
      }
    ];
  
    return (
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Our Detailing Services</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              We offer premium detailing packages tailored to your needs. Each service is performed with professional-grade products and meticulous attention to detail.
            </p>
          </div>
  
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {servicePackages.map((service, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
                <div className="p-6">
                  <h3 className="text-xl font-bold mb-2">{service.name}</h3>
                  <p className="text-gray-600 mb-4">{service.description}</p>
                  <p className="text-2xl font-bold text-purple-700 mb-4">Starting at {service.price}</p>
                  <ul className="space-y-2">
                    {service.features.map((feature, fIndex) => (
                      <li key={fIndex} className="flex items-center">
                        <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }