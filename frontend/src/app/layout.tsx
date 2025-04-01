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
        <main className="w-full pt-20">
          {children}
        </main>
        
        <footer className="bg-gray-800 text-white py-6">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center">
              <p>© {new Date().getFullYear()} S&F Detailing</p>
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