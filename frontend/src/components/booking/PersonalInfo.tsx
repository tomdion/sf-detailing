import { UseFormRegister, FieldErrors } from "react-hook-form";
import { BookingFormData } from "./BookingForm";

interface PersonalInfoSectionProps {
  register: UseFormRegister<BookingFormData>;
  errors: FieldErrors<BookingFormData>;
}

const PersonalInfo = ({ register, errors }: PersonalInfoSectionProps) => {
  return (
    <div>
      <h2 className="mb-4 text-xl font-semibold text-gray-800">Personal Information</h2>
      
      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          First Name
        </label>
        <input
          type="text"
          {...register("first_name")}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        />
        {errors.first_name && (
          <p className="mt-1 text-sm text-red-600">{errors.first_name.message}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Last Name
        </label>
        <input
          type="text"
          {...register("last_name")}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        />
        {errors.last_name && (
          <p className="mt-1 text-sm text-red-600">{errors.last_name.message}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          type="email"
          {...register("email")}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Phone Number
        </label>
        <input
          type="tel"
          {...register("phone_number")}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        />
        {errors.phone_number && (
          <p className="mt-1 text-sm text-red-600">{errors.phone_number.message}</p>
        )}
      </div>
    </div>
  );
};

export default PersonalInfo;