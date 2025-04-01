import { UseFormRegister, FieldErrors } from "react-hook-form";
import { BookingFormData } from "./BookingForm";

interface LocationSectionProps {
  register: UseFormRegister<BookingFormData>;
  errors: FieldErrors<BookingFormData>;
}

const Location = ({ register, errors }: LocationSectionProps) => {
  return (
    <div className="pt-4">
      <h2 className="mb-4 text-xl font-semibold text-gray-800">Service Location</h2>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            Street Address
          </label>
          <input
            type="text"
            {...register("address.street_address")}
            className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
          />
          {errors.address?.street_address && (
            <p className="mt-1 text-sm text-red-600">
              {errors.address.street_address.message}
            </p>
          )}
        </div>
        
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            City
          </label>
          <input
            type="text"
            {...register("address.city")}
            className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
          />
          {errors.address?.city && (
            <p className="mt-1 text-sm text-red-600">
              {errors.address.city.message}
            </p>
          )}
        </div>
        
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            State
          </label>
          <input
            type="text"
            {...register("address.state")}
            className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
          />
          {errors.address?.state && (
            <p className="mt-1 text-sm text-red-600">
              {errors.address.state.message}
            </p>
          )}
        </div>
        
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">
            ZIP Code
          </label>
          <input
            type="text"
            {...register("address.zip_code")}
            className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
          />
          {errors.address?.zip_code && (
            <p className="mt-1 text-sm text-red-600">
              {errors.address.zip_code.message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Location;