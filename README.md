# S&F Detailing

A full-stack web application for a western massachusetts car detailing business that allows customers to book detailing services online. The application features a user-friendly booking system, authentication, and service management.

## Tech Stack

### Backend
- **Django**: REST API backend
- **Django REST Framework**: API development
- **PostgreSQL**: Database
- **JWT Authentication**: Secure user authentication
- **Simple JWT**: Token-based authentication

### Frontend
- **Next.js**: React framework for the frontend
- **React**: UI library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Hook Form**: Form validation
- **Zod**: Schema validation
- **Axios**: HTTP client
- **date-fns**: Date utility library

## Project Structure

### Backend

```
backend/
├── api/                  # Django project settings
├── booking/              # Booking application
│   ├── migrations/       # Database migrations
│   ├── models.py         # Data models
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # URL routing
│   ├── permissions.py    # Custom permissions
│   └── services.py       # Business logic services
├── users/                # User authentication app
│   ├── migrations/       # Database migrations
│   ├── models.py         # Custom user model
│   ├── serializers.py    # User serializers
│   ├── views.py          # Authentication views
│   └── authentication.py # Custom JWT authentication
└── templates/            # Email templates
```

### Frontend

```
frontend/
├── public/               # Static assets
├── src/
│   ├── api/              # API client and service functions
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   │   ├── booking/      # Booking form components
│   │   └── ui/           # Reusable UI components
│   └── hooks/            # Custom React hooks
```

## Features

- **User Authentication**
  - Registration
  - Login with two-factor authentication
  - Password reset
  - JWT-based authentication using HTTPOnly Cookies

- **Booking System**
  - Service package selection
  - Date and time selection based on business hours
  - Address information for mobile services
  - Email confirmation workflow

- **Admin Features**
  - Manage bookings
  - Update service packages
  - Configure business hours

## Setup Instructions

### Prerequisites

- Dev Containers Extension for VSCode
- Docker
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tomdion/sf-detailing.git
   cd sf-detailing
   ```

2. **Create environment file**
   Create a `.env` file in the root directory with the following variables:
   ```
   # Django settings
   SECRET_KEY=your_secret_key
   DEBUG=1
   DJANGO_ALLOWED_HOSTS=your_port
   
   # Database settings
   POSTGRES_DB=your_db
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=db
   POSTGRES_PORT=your_db_port
   
   # Email settings
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_app_password
   DEFAULT_FROM_EMAIL=email@example.com
   
   # Frontend settings
   FRONTEND_URL=http://localhost:3000
   NEXT_PUBLIC_API_URL=http://localhost:8001
   ```

3. **Start the development container**
   ```bash
   # Using VS Code Dev Containers
   code .
   # Select "Reopen in Container" when prompted or in the command palette
   
   ```

4. **Run migrations and create a superuser**
   ```bash
   # Inside the container
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start the development servers**
   ```bash
   # For the backend (inside the container)
   cd backend
   python manage.py runserver 0.0.0.0:8001
   
   # For the frontend (in a new terminal inside the container)
   cd frontend
   npm install
   npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - Django Admin: http://localhost:8001/admin

## API Endpoints

### Authentication
- `POST /api/users/register/`: Register a new user
- `POST /api/users/login/`: Log in (triggers 2FA email)
- `POST /api/users/verify-2fa/`: Verify 2FA code
- `POST /api/users/logout/`: Log out user
- `GET /api/users/user-info/`: Get current user information
- `POST /api/users/refresh/`: Refresh JWT token
- `POST /api/users/password-reset/`: Request password reset
- `POST /api/users/password-reset/confirm/`: Confirm password reset

### Booking
- `GET /api/bookings/booking-list/`: List all bookings (admin only)
- `POST /api/bookings/booking-list/`: Create a new booking
- `DELETE /api/bookings/booking-list/<id>/`: Delete a booking
- `GET /api/bookings/user-bookings/`: Get bookings for authenticated user
- `POST /api/bookings/guest-bookings/`: Get bookings for a guest by email
- `GET /api/bookings/confirm/?token=<token>`: Confirm a booking
- `GET /api/bookings/business-hours/`: Get business hours
- `GET /api/bookings/packages/`: Get service packages
- `GET /api/bookings/addons/`: Get service add-ons

## License

This software is proprietary and is the property of S&F Detailing. Unauthorized use, distribution, or modification of this software is strictly prohibited.
