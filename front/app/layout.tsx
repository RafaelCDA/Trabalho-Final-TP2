import type { Metadata } from "next";
import "./globals.css";
import Header from "../components/Header";
import { anton } from "./fonts";


export const metadata: Metadata = {
  title: {
    template: "%s - Let's Goo Buy",
    default: "Let's Goo Buy Online Store",
  },
  description: "Let's Goo Buy, Sua loja online favorita para tudo que precisa",
};


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
