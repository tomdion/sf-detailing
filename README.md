# S&F Detailing

A full-stack web application for S&F Auto Detailing, a mobile car detailing business based in western massachusettes, that allows customers to book detailing services online. The application features a user-friendly booking system, authentication, and service management.

## Tech Stack

### Backend
- **Django**: Python Web Development Framwork
- **Django REST Framework**: RESTful API framwork fo Django
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


## License

This software is proprietary and is the property of S&F Detailing. Unauthorized use, distribution, or modification of this software is strictly prohibited.
