"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="fixed top-0 z-50 w-full bg-white shadow-md">
      <div className="container mx-auto">
        <div className="flex h-20 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="pl-0">
            <Image
              src="/images/grayscale.png"
              alt="SF Detailing Logo"
              className="h-10 w-auto object-cover"
              width={60}
              height={60}
            />
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:block">
            <ul className="flex space-x-8">
              <li>
                <Link
                  href="/"
                  className="text-gray-700 transition hover:text-purple-700"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/services"
                  className="text-gray-700 transition hover:text-purple-700"
                >
                  Services
                </Link>
              </li>
              <li>
                <Link
                  href="/gallery"
                  className="text-gray-700 transition hover:text-purple-700"
                >
                  Gallery
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-gray-700 transition hover:text-purple-700"
                >
                  Contact
                </Link>
              </li>
              <li>
                <Link
                  href="/booking"
                  className="rounded-full bg-purple-700 px-6 py-2 text-white transition hover:bg-purple-800"
                >
                  Book Now
                </Link>
              </li>
            </ul>
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={toggleMenu}
            className="block md:hidden"
            aria-label="Toggle menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="h-6 w-6"
            >
              {isMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <ul className="space-y-4 pb-6 pt-2">
              <li>
                <Link
                  href="/"
                  className="block py-2 text-gray-700 transition hover:text-purple-700"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/services"
                  className="block py-2 text-gray-700 transition hover:text-purple-700"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Services
                </Link>
              </li>
              <li>
                <Link
                  href="/gallery"
                  className="block py-2 text-gray-700 transition hover:text-purple-700"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Gallery
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="block py-2 text-gray-700 transition hover:text-purple-700"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Contact
                </Link>
              </li>
              <li>
                <Link
                  href="/booking"
                  className="inline-block rounded-full bg-purple-700 px-6 py-2 text-white transition hover:bg-purple-800"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Book Now
                </Link>
              </li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
}
