import { Heart, Search, ShoppingBag } from "lucide-react";
import {anton} from '@/app/layout';

export default function Header() {
    return (
    <header className="w-full bg-white">
      <div className="max-w-7xl mx-auto flex items-center justify-between py-4 px-6">

        <h1 className={`${anton.className} text-4xl tracking-wider`} style={{ color: "var(--color-shop_dark_green)" }}>
          LET'S GO_BUY
        </h1>

        <nav className="hidden md:flex space-x-8 text-gray-700 font-medium">
          <a href="#" className="hover:text-green-600 border-b-2 border-green-600 pb-1">
            Home
          </a>
          <a href="#" className="hover:text-green-600">Fornecedor</a>
          <a href="#" className="hover:text-green-600">Produtos</a>
          <a href="#" className="hover:text-green-600">Bancas</a>
        </nav>

        <div className="btext-gray-700">

          <button className="font-medium hover:text-green-600">
            Login
          </button>
        </div>
      </div>
    </header>
    );
}