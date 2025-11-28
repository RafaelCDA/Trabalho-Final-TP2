'use client';
import Image from "next/image";
import { Heart } from "lucide-react";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {

  const categories = ["Dispositivos", "Eletrodomésticos", "Refrigeradores", "Outros"];
  const [activeCategory, setActiveCategory] = useState("Dispositivos");

  const [products, setProducts] = useState([]);

  async function fetchProducts(category: string) {
    try {
      // Exemplo de rota (ve oque implementaram no back)
      const response = await axios.get(
        `http://localhost:3000/products?category=${category}`
      );

      setProducts(response.data); // salva na variável que o map usa
    } catch (error) {
      console.error("Erro ao buscar produtos:", error);
    }
  }

  useEffect(() => {
    fetchProducts(activeCategory);
  }, []);

  useEffect(() => {
    fetchProducts(activeCategory);
  }, [activeCategory]);

  return (

  //TODAS AS IMAGENS DEVEM SER COLOCADAS NA PASTA 'public' PARA FUNCIONAREM CORRETAMENTE 
  //E SEREM COLOCADAS POSTERIORMENTE
  <main className="max-w-7xl mx-auto px-6 py-6">


      <section className="w-full bg-[var(--color-shop-light-pink)] rounded-xl flex items-center justify-between px-10 py-10">
        <div className="flex flex-col gap-4 max-w-md">
          <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] leading-snug">
            Garanta 50% de desconto <br /> Selecione o produto hoje!
          </h2>

          <button className="bg-[var(--color-shop_btn_dark_green)] text-white px-6 py-2 rounded-lg w-fit hover:opacity-90">
            Compre Agora
          </button>
        </div>

        <div className="w-[300px] h-[300px] relative flex items-center justify-center">
          <Image
            src="/headphone.png" 
            alt="Headphone"
            fill
            className="object-contain scale-[1.2]"
          />
        </div>
      </section>

      <section className="mt-10 flex items-center justify-between">
        <div className="flex gap-4">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-5 py-2 rounded-full border transition ${
                activeCategory === cat
                  ? "bg-[var(--color-shop_light_green)] text-white border-[var(--color-shop_light_green)]"
                  : "border-gray-300 text-gray-700 hover:bg-gray-100"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <button className="border px-4 py-2 rounded-full text-gray-700 hover:bg-gray-100">
          Veja todos
        </button>
      </section>

      <section className="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

        {[
          {
            name: "Apple AirPods 3rd generation",
            price: 1700,
            oldPrice: 1870,
            stock: 10,
            img: "/fire (1).png",
          },
          {
            name: "Canon EOS 250D Camera",
            price: 750,
            oldPrice: 900,
            stock: 9,
            img: "/fire (1).png",
          },
          {
            name: "HP Laptop AMD Ryzen 5",
            price: 1659,
            oldPrice: 1907,
            stock: 17,
            img: "/fire (1).png",
          },
          {
            name: "Mpow – CHE2S On-Ear Headphone",
            price: 550,
            oldPrice: 605,
            stock: 5,
            img: "/fire (1).png",
          },
        ].map((p, i) => (
          <div
            key={i}
            className="rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md transition relative"
          >
            <button className="absolute top-3 right-3 text-gray-500 hover:text-red-500">
              <Heart size={18} />
            </button>

            <div className="w-full h-40 flex items-center justify-center">
              <Image
                src={p.img}
                alt={p.name}
                width={140}
                height={140}
                className="object-contain"
              />
            </div>

            <div className="mt-3 flex flex-col gap-1">
              <h3 className="text-sm text-gray-700 font-medium line-clamp-2">
                {p.name}
              </h3>

              <p className="text-sm text-gray-500">Em estoque {p.stock}</p>

              <div className="flex items-center gap-2">
                <span className="text-lg font-bold text-[var(--color-shop_dark_green)]">
                  R${p.price}
                </span>
                <span className="text-sm line-through text-gray-400">
                  R${p.oldPrice}
                </span>
              </div>

              <button className="mt-2 bg-[var(--color-shop_light_green)] text-white py-2 rounded-lg hover:opacity-90">
                Compre
              </button>
            </div>
          </div>
        ))}

      </section>
    </main>
  );
}
