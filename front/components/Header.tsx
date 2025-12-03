"use client"
import { Heart, Search, ShoppingBag } from "lucide-react";
import {anton} from '@/app/fonts';
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";


export default function Header() {

    const pathname = usePathname(); // rota atual

    const links = [
        { name: "Home", href: "/" },
        { name: "Fornecedor", href: "/fornecedor" },
        { name: "Produtos", href: "/produtos" },
        { name: "Bancas", href: "/bancas" },
    ];

    const [user, setUser] = useState<any>(null);

    // carregar usuário salvo e reagir a mudanças (login/logout/redirecionamento)
    useEffect(() => {
        const load = () => {
            const data = sessionStorage.getItem("user");
            setUser(data ? JSON.parse(data) : null);
        };

        // carregar ao montar / quando pathname muda
        load();

        // quando outra aba alterar sessionStorage
        const onStorage = (e: StorageEvent) => {
            if (e.key === "user") load();
        };

        // evento custom para mesma aba (disparado no login)
        const onUserChanged = () => load();

        window.addEventListener("storage", onStorage);
        window.addEventListener("userChanged", onUserChanged);

        return () => {
            window.removeEventListener("storage", onStorage);
            window.removeEventListener("userChanged", onUserChanged);
        };
    }, [pathname]);

    function logout() {
        sessionStorage.removeItem("user");
        setUser(null);
    }
    
    return (
    <header className="w-full bg-white">
      <div className="max-w-7xl mx-auto flex items-center justify-between py-4 px-6">

        <div className="flex-1">
          <h1
            className={`${anton.className} text-4xl tracking-wider`}
            style={{ color: "var(--color-shop_dark_green)" }}
          >
            LET'S GO_BUY
          </h1>
        </div>

        <nav className="flex-1 flex justify-center space-x-10 text-gray-700 font-medium">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`pb-1 transition ${
                  isActive
                    ? "border-b-2 border-green-600 text-green-700"
                    : "hover:text-green-600"
                }`}
              >
                {link.name}
              </Link>
            );
          })}
        </nav>

        <div className="flex-1 flex justify-end">
          {user ? (
            <div className="flex items-center gap-6">
              <Link
                href={"/perfil"}
                className="font-medium text-green-700 cursor-pointer hover:text-green-800"
              >
                Perfil
              </Link>

              <button
                onClick={logout}
                className="text-red-600 font-medium hover:text-red-800"
              >
                Sair
              </button>
            </div>
          ) : (
            <Link
              href={"/login"}
              className="font-medium text-green-700 cursor-pointer hover:text-green-800"
            >
              Login
            </Link>
          )}
        </div>

      </div>
    </header>
    );
}
