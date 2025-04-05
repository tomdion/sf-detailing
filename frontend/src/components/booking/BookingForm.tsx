"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { format } from "date-fns";
import { createBooking } from "@/api/bookings";
import { useAuth } from "@/hooks/useAuth";
import { AxiosError } from 'axios';
import PersonalInfo from "./PersonalInfo";
import ServiceDetails from "./ServiceDetails";
import Location from "./Location";

export const bookingSchema = z.object({
  first_name: z.string().min(2, "First name is required"),
  last_name: z.string().min(2, "Last name is required"),
  email: z.string().email("Please enter a valid email"),
  phone_number: z.string().min(10, "Please enter a valid phone number"),
  date: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: "Please select a valid date",
  }),
  time: z.string().min(1, "Please select a time"),
  package: z.number().min(1, "Please select a package"),
  vehicle: z.enum(["car", "suv", "truck"], {
    errorMap: () => ({ message: "Please select a vehicle type" }),
  }),
  address: z.object({
    street_address: z.string().min(5, "Street address is required"),
    city: z.string().min(2, "City is required"),
    state: z.string().min(2, "State is required"),
    zip_code: z.string().min(5, "ZIP code is required"),
  }),
});

export type BookingFormData = z.infer<typeof bookingSchema>;

interface BookingFormProps {
  packages: Package[];
  businessHours: BusinessHour[];
  onSuccess: () => void;
}

export interface VehiclePrice {
  id: number;
  vehicle_type: string;
  vehicle_type_display: string;
  price: number;
}

export interface Package {
  id: number;
  name: string;
  display_name: string;
  price: number;
  description: string;
  vehicle_prices: VehiclePrice[];
}

export interface BusinessHour {
  id: number;
  day: number;
  day_name: string;
  opening_time: string;
  closing_time: string;
  is_open: boolean;
}

const BookingForm = ({ packages, businessHours, onSuccess }: BookingFormProps) => {
  const [availableTimes, setAvailableTimes] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const { user, isLoggedIn } = useAuth();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    setValue,
    reset,
  } = useForm<BookingFormData>({
    resolver: zodResolver(bookingSchema),
    defaultValues: {
      vehicle: "car",
      address: {
        street_address: "",
        city: "",
        state: "",
        zip_code: "",
      },
    },
  });

  const selectedDate = watch("date");

  // Fill user data if logged in
  useEffect(() => {
    if (isLoggedIn && user) {
      setValue("first_name", user.username.split(" ")[0] || "");
      setValue("last_name", user.username.split(" ")[1] || "");
      setValue("email", user.email);
    }
  }, [isLoggedIn, user, setValue]);

  // Generate available time slots when date changes
  useEffect(() => {
    if (!selectedDate || !businessHours.length) return;

    const date = new Date(selectedDate);
    const dayOfWeek = date.getDay();
    // Convert 0 (Sunday) to 6, and 1-6 (Monday-Saturday) to 0-5
    const adjustedDay = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    
    const dayHours = businessHours.find(hour => hour.day === adjustedDay);
    
    if (!dayHours || !dayHours.is_open) {
      setAvailableTimes([]);
      return;
    }

    const openingTime = new Date(`1970-01-01T${dayHours.opening_time}`);
    const closingTime = new Date(`1970-01-01T${dayHours.closing_time}`);
    
    const timeSlots = [];
    const currentTime = new Date(openingTime);
    
    // Generate 30-minute intervals
    while (currentTime < closingTime) {
      timeSlots.push(format(currentTime, "HH:mm"));
      currentTime.setMinutes(currentTime.getMinutes() + 30);
    }
    
    setAvailableTimes(timeSlots);
  }, [selectedDate, businessHours]);

  const onSubmit = async (data: BookingFormData) => {
    setIsSubmitting(true);
    setSubmitError("");
    
    try {
      await createBooking(data);
      reset();
      window.scrollTo(0, 0);
      onSuccess();
    } catch (error) {
      console.error("Error creating booking:", error);
      const axiosError = error as AxiosError<{message?: string}>;
      setSubmitError(
        axiosError.response?.data?.message || 
        "An error occurred while creating your booking. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  // Get minimum date (tomorrow)
  const getMinDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return format(tomorrow, "yyyy-MM-dd");
  };

  return (
    <div className="mx-auto max-w-4xl rounded-lg bg-white p-8 shadow-lg">
      {submitError && (
        <div className="mb-6 rounded-md bg-red-100 p-4 text-red-700">
          {submitError}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {/* Personal Information */}
          <PersonalInfo 
            register={register} 
            errors={errors} 
          />

          {/* Service Details */}
          <ServiceDetails 
            register={register}
            watch={watch}
            errors={errors}
            packages={packages}
            selectedDate={selectedDate}
            availableTimes={availableTimes}
            getMinDate={getMinDate}
          />
        </div>

        {/* Location Section */}
        <Location 
          register={register}
          errors={errors}
        />

        <div className="flex justify-center pt-6">
          <button
            type="submit"
            disabled={isSubmitting}
            className="rounded-full bg-purple-700 px-8 py-3 text-lg font-semibold text-white transition hover:bg-purple-800 disabled:bg-purple-400"
          >
            {isSubmitting ? "Processing..." : "Book Now"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BookingForm;