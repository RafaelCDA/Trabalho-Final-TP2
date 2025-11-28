import type { Metadata } from "next";
import "./globals.css";
import Header from "../components/Header";
import { Orbitron } from 'next/font/google';
import { Bangers } from 'next/font/google';
import { Anton } from 'next/font/google';


export const metadata: Metadata = {
  title: {
    template: "%s - Let's Goo Buy",
    default: "Let's Goo Buy Online Store",
  },
  description: "Let's Goo Buy, Sua loja online favorita para tudo que precisa",
};

export const orbitron = Orbitron({
  subsets: ['latin'],
  weight: ['400', '700'],
});


export const bangers = Bangers({
  subsets: ['latin'],
  weight: ['400'],
});


export const anton = Anton({
  subsets: ['latin'],
  weight: ['400'],
});


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-poppins antialiased ">
        <Header/>
        {children}
      </body>
    </html>
  );
}
