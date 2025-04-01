"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/ui/Navbar";
import Footer from "@/components/ui/Footer";
import { getBusinessHours, getPackages } from "@/api/bookings";
import BookingForm, { Package, BusinessHour } from "@/components/booking/BookingForm";
import BookingSuccess from "@/components/booking/BookingSuccess";

export default function BookingPage() {
  const [packages, setPackages] = useState<Package[]>([]);
  const [businessHours, setBusinessHours] = useState<BusinessHour[]>([]);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const router = useRouter();

  // Fetch packages and business hours
  useEffect(() => {
    const fetchData = async () => {
      try {
        const packagesData = await getPackages();
        setPackages(packagesData);

        const hoursData = await getBusinessHours();
        setBusinessHours(hoursData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleSuccess = () => {
    setSubmitSuccess(true);
    setTimeout(() => {
      router.push("/booking/confirmation");
    }, 3000);
  };

  return (
    <main className="min-h-screen bg-gray-100">
      <Navbar />
      
      <div className="container mx-auto px-4 py-12">
        <div className="mb-8 text-center">
          <h1 className="mb-4 text-4xl font-bold text-gray-800">Book Your Detailing Service</h1>
          <p className="mx-auto max-w-2xl text-lg text-gray-600">
            Schedule your appointment with S&F Detailing. We offer professional
            auto detailing services for cars, SUVs, and trucks.
          </p>
        </div>

        {submitSuccess ? (
          <BookingSuccess />
        ) : (
          <BookingForm 
            packages={packages}
            businessHours={businessHours}
            onSuccess={handleSuccess}
          />
        )}
      </div>

      <div className="mt-16">
        <Footer />
      </div>
    </main>
  );
}