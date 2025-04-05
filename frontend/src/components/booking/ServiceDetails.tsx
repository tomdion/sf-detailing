import { UseFormRegister, FieldErrors, UseFormWatch } from "react-hook-form";
import { BookingFormData, Package } from "./BookingForm";

interface ServiceDetailsSectionProps {
  register: UseFormRegister<BookingFormData>;
  watch: UseFormWatch<BookingFormData>;
  errors: FieldErrors<BookingFormData>;
  packages: Package[];
  selectedDate: string;
  availableTimes: string[];
  getMinDate: () => string;
}

const ServiceDetails = ({ 
  register, 
  watch,
  errors, 
  packages, 
  selectedDate, 
  availableTimes,
  getMinDate 
}: ServiceDetailsSectionProps) => {
  const selectedVehicle = watch("vehicle");
  const selectedPackageId = watch("package");

  const selectedPackage = packages.find(pkg => pkg.id === selectedPackageId);
  
  const getVehiclePrice = (pkg: Package, vehicleType: string) => {
    const vehiclePrice = pkg?.vehicle_prices?.find(
      vp => vp.vehicle_type === vehicleType
    );
    return vehiclePrice?.price || pkg?.price || 0;
  };

  return (
    <div>
      <h2 className="mb-4 text-xl font-semibold text-gray-800">Service Details</h2>
      
      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Vehicle Type
        </label>
        <select
          {...register("vehicle")}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        >
          <option value="car">Car</option>
          <option value="suv">SUV</option>
          <option value="truck">Truck</option>
        </select>
        {errors.vehicle && (
          <p className="mt-1 text-sm text-red-600">{errors.vehicle.message}</p>
        )}
      </div>
      
      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Select Date
        </label>
        <input
          type="date"
          {...register("date")}
          min={getMinDate()}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        />
        {errors.date && (
          <p className="mt-1 text-sm text-red-600">{errors.date.message}</p>
        )}
      </div>

      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Select Time
        </label>
        <select
          {...register("time")}
          disabled={!selectedDate || availableTimes.length === 0}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        >
          <option value="">Select a time slot</option>
          {availableTimes.map((time) => (
            <option key={time} value={time}>
              {time}
            </option>
          ))}
        </select>
        {errors.time && (
          <p className="mt-1 text-sm text-red-600">{errors.time.message}</p>
        )}
        {selectedDate && availableTimes.length === 0 && (
          <p className="mt-1 text-sm text-yellow-600">
            No available times for the selected date. Please choose another date.
          </p>
        )}
      </div>

      <div className="mb-4">
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Service Package
        </label>
        <select
          {...register("package", { valueAsNumber: true })}
          className="w-full rounded-md border border-gray-300 p-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
        >
          <option value="">Select a package</option>
          {packages.map((pkg) => {
            const price = getVehiclePrice(pkg, selectedVehicle);
            return (
              <option key={pkg.id} value={pkg.id}>
                {pkg.display_name} - ${price}
              </option>
            );
          })}
        </select>
        {errors.package && (
          <p className="mt-1 text-sm text-red-600">{errors.package.message}</p>
        )}
      </div>

      {selectedPackage && (
        <div className="mt-4 rounded-md bg-gray-50 p-4">
          <h3 className="mb-2 font-semibold">Selected Package Details:</h3>
          <p><span className="font-medium">Package:</span> {selectedPackage.display_name}</p>
          <p><span className="font-medium">Vehicle:</span> {selectedVehicle.charAt(0).toUpperCase() + selectedVehicle.slice(1)}</p>
          <p><span className="font-medium">Price:</span> ${getVehiclePrice(selectedPackage, selectedVehicle)}</p>
          {selectedPackage.description && (
            <p className="mt-1 text-sm text-gray-600">{selectedPackage.description}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default ServiceDetails;