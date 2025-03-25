import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "S&F Detailing",
  description: "Auto Detailing Service Based in Western Mass",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="bg-purple-700 text-white">
          <div className="container mx-auto p-4">
            <div className="flex items-center justify-between">
              <Link href="/" className="text-xl font-bold">
                SF Detailing
              </Link>
              <nav>
                <ul className="flex space-x-6">
                  <li>
                    <Link href="/" className="hover:text-gray-300">
                      Home
                    </Link>
                  </li>
                  <li>
                    <Link href="/book" className="hover:text-gray-300">
                      Book Now
                    </Link>
                  </li>
                  <li>
                    <Link href="/dashboard" className="hover:text-gray-300">
                      Dashboard
                    </Link>
                  </li>
                  <li>
                    <Link href="/login" className="hover:text-gray-300">
                      Login
                    </Link>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </header>
        <main className="w-full">{children}</main>
        <footer className="bg-gray-800 text-white py-6">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center">
              <p>© {new Date().getFullYear()} SF Detailing</p>
              <div className="flex space-x-4">
                <Link href="/terms" className="hover:text-gray-300">
                  Terms
                </Link>
                <Link href="/privacy" className="hover:text-gray-300">
                  Privacy
                </Link>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}