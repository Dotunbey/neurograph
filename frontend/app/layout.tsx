import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NeuroGraph",
  description: "AI Graph Neural Network Visualizer",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
