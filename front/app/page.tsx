'use client';
import Image from "next/image";
import { Heart } from "lucide-react";
import { useState, useEffect } from "react";
import axios from "axios";

interface Produto {
  id?: number;
  bar_shelf_id: number;
  category: string;
  description: string;
  price_in: number;
  unit_of_measurement: string;
}

export default function Home() {

  const categories = ["Dispositivos", "Eletrodomésticos", "Refrigeradores", "Outros"];
  const [activeCategory, setActiveCategory] = useState("Dispositivos");
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [produtosOriginais, setProdutosOriginais] = useState<Produto[]>([]);

  async function fetchProdutos(category?: string) {
    try {
      const url = category 
        ? `http://localhost:3000/produtos?category=${category}`
        : `http://localhost:3000/produtos`;

      const response = await axios.get(url);

      setProdutos(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error("Erro ao buscar produtos:", error);
      setProdutos([]);
    }
  }
  useEffect(() => {
    const mock = [
      {
        id: 1,
        bar_shelf_id: 1,
        category: "Dispositivos",
        description: "Apple AirPods 3rd generation - Fones sem fio com cancelamento de ruído",
        price_in: 1700.00,
        unit_of_measurement: "unidade"
      },
      {
        id: 2,
        bar_shelf_id: 1,
        category: "Dispositivos",
        description: "Canon EOS 250D Camera - Câmera DSLR profissional com lente 18-55mm",
        price_in: 750.00,
        unit_of_measurement: "unidade"
      },
      {
        id: 3,
        bar_shelf_id: 2,
        category: "Eletrodomésticos",
        description: "HP Laptop AMD Ryzen 5 - Notebook com 8GB RAM e SSD 256GB",
        price_in: 1659.00,
        unit_of_measurement: "unidade"
      },
      {
        id: 4,
        bar_shelf_id: 3,
        category: "Dispositivos",
        description: "Mpow CHE2S On-Ear Headphone - Fones de ouvido com microfone",
        price_in: 550.00,
        unit_of_measurement: "unidade"
      },
      {
        id: 5,
        bar_shelf_id: 2,
        category: "Refrigeradores",
        description: "Geladeira Frost Free Brastemp 375L - Eficiência energética A",
        price_in: 2899.00,
        unit_of_measurement: "unidade"
      },
      {
        id: 6,
        bar_shelf_id: 3,
        category: "Eletrodomésticos",
        description: "Micro-ondas Electrolux 31L - Com função grill e timer digital",
        price_in: 599.00,
        unit_of_measurement: "unidade"
      },
      {
        id: 7,
        bar_shelf_id: 1,
        category: "Dispositivos",
        description: "Apple AirPods 4rd generation - Fones sem fio com cancelamento de ruído",
        price_in: 2000.00,
        unit_of_measurement: "unidade"
      }
    ];

    setProdutos(mock);
    setProdutosOriginais(mock);
  }, []);



  const minPrice = Math.min(...produtos.map(p => p.price_in));
  const maxPrice = Math.max(...produtos.map(p => p.price_in));
  const [preco, setPreco] = useState(0);
  const [precoAlterado, setPrecoAlterado] = useState(false);
  const produtosFiltrados = produtos
    .filter((p) => {
      // se o preço NÃO foi alterado → mostra todos
      if (!precoAlterado) return true;

      // se o preço foi alterado → filtra até o valor
      return p.price_in <= preco;
    })
    .filter((p) => {
      // quando o preço for alterado, a categoria vira Outros
      if (activeCategory === "Outros") return true;
      return p.category === activeCategory;
    });


  const [search, setSearch] = useState("");


  function filterBySearch(text: string) {
    setSearch(text);

    if (!text.trim()) {
      // volta ao original
      setProdutos(produtosOriginais);
      return;
    }

    const lower = text.toLowerCase();

    const filtrados = produtosOriginais.filter((p) =>
      p.description.toLowerCase().includes(lower)
    );

    setProdutos(filtrados);
  }

  useEffect(() => {
    setPreco(maxPrice);
  }, [produtos]);

  function handleCategory(cat: string) {
    setActiveCategory(cat);
    setPrecoAlterado(false); // volta o preço ao normal
    setProdutos(produtosOriginais); // reseta produtos
  }




  return (
  <main className="max-w-7xl mx-auto mb-10 px-6 py-6">
      <section className="mb-10 flex justify-center">
        <div className="w-full max-w-xl flex items-center gap-3 px-5 py-3 
            bg-white rounded-full shadow-md border border-gray-200">

          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z"
            />
          </svg>

          <input
            type="text"
            placeholder="Buscar produtos..."
            value={search}
            onChange={(e) => filterBySearch(e.target.value)}
            className="flex-1 bg-transparent focus:outline-none text-base"
          />
        </div>
      </section>

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
              onClick={() => handleCategory(cat)}
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
      </section>

    <section className="mt-12 grid grid-cols-1 lg:grid-cols-[250px_1fr] gap-10">

      <aside className="hidden lg:block border rounded-lg p-5 h-fit sticky top-20 bg-white shadow-sm">

        <h3 className="text-lg font-semibold mb-3">Filtrar por</h3>
        <div className="mb-6">
          <h4 className="font-medium mb-2">Preço</h4>
          <input
            type="range"
            min={minPrice}
            max={maxPrice}
            value={preco}
            onChange={(e) => {
              setPreco(Number(e.target.value));
              setPrecoAlterado(true);
              setActiveCategory("Outros");
            }}

            className="
              w-full
              h-2
              appearance-none
              bg-transparent

              [&::-webkit-slider-runnable-track]:bg-[var(--color-shop_dark_green)]
              [&::-webkit-slider-runnable-track]:h-2
              [&::-webkit-slider-runnable-track]:rounded-lg

              [&::-webkit-slider-thumb]:appearance-none
              [&::-webkit-slider-thumb]:h-4
              [&::-webkit-slider-thumb]:w-4
              [&::-webkit-slider-thumb]:rounded-full
              [&::-webkit-slider-thumb]:bg-[var(--color-shop_light_green)]
              [&::-webkit-slider-thumb]:cursor-pointer
              [&::-webkit-slider-thumb]:mt-[-6px]
            "
          />

          <p className="text-sm text-gray-600 mt-1">
            Até: <span className="font-bold text-[var(--color-shop_dark_green)]">R${preco}</span>
          </p>
        </div>

        <div>
          <h4 className="font-medium mb-2">Localização</h4>
          <select className="w-full border rounded p-2">
            <option>Qualquer lugar</option>
            <option>Brasília</option>
            <option>Goiânia</option>
            <option>São Paulo</option>
          </select>
        </div>

      </aside>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">

        {produtosFiltrados.length === 0 && (
          <p className="col-span-full text-center text-gray-500">
            Nenhum produto encontrado nesta categoria.
          </p>
        )}

        {produtosFiltrados.map((p) => (
          <div
            key={p.id}
            className="rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md transition relative"
          >

            <div className="w-full h-40 flex items-center justify-center">
              <Image
                src="/fire (1).png"
                alt={p.description}
                width={140}
                height={140}
                className="object-contain"
              />
            </div>

            <div className="mt-3 flex flex-col gap-1">
              <h3 className="text-sm text-gray-700 font-medium line-clamp-2">
                {p.description}
              </h3>

              <p className="text-sm text-gray-500">
                Categoria: {p.category}
              </p>

              <span className="text-lg font-bold text-[var(--color-shop_dark_green)]">
                R${p.price_in}
              </span>

              <button className="mt-2 bg-[var(--color-shop_dark_green)] text-white py-2 rounded-lg hover:opacity-90">
                Compre
              </button>
            </div>
          </div>
        ))}

      </div>
    </section>

  </main>
  );
}
