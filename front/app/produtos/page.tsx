// EU011 - Listagem de Produtos
'use client';

import axios from "axios";
import { useEffect, useState } from "react";
import Image from "next/image";
import { Heart } from "lucide-react";

interface Produto {
  id?: number;
  bar_shelf_id: number;
  category: string;
  description: string;
  price_in: number;
  unit_of_measurement: string;
}

export default function Produtos() {

  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [selected, setSelected] = useState<Produto | null>(null);

  // Categorias para filtro (baseado no diagrama)
  const categories = ["Dispositivos", "Eletrodomésticos", "Refrigeradores", "Outros"];
  const [activeCategory, setActiveCategory] = useState("Dispositivos");

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
    // COMENTADO ATÉ O BACKEND ESTAR PRONTO
    // fetchProdutos(activeCategory);
    
    // DADOS DE TESTE - REMOVER QUANDO O BACKEND ESTIVER PRONTO
    setProdutos([
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
      }
    ]);
  }, []);

  // Filtrar produtos por categoria
  const produtosFiltrados = produtos.filter(p => p.category === activeCategory);

  return (
    <main className="max-w-7xl mx-auto px-6 py-6">

      <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] mb-6">
        Lista de Produtos
      </h2>

      {/* Filtros de Categoria */}
      <section className="mb-10 flex items-center justify-between">
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

      {/* Grid de Produtos */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {produtosFiltrados.length === 0 ? (
          <div className="col-span-full text-center py-10 text-gray-500">
            <p className="text-lg">Nenhum produto encontrado nesta categoria.</p>
            <p className="text-sm mt-2">Tente selecionar outra categoria.</p>
          </div>
        ) : (
          produtosFiltrados.map((p: Produto, i: number) => (
            <div
              key={i}
              className="rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md transition relative"
            >
              <button className="absolute top-3 right-3 text-gray-500 hover:text-red-500">
                <Heart size={18} />
              </button>

              <div className="w-full h-40 flex items-center justify-center bg-gray-50 rounded-lg">
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

                <p className="text-xs text-gray-500">
                  Categoria: {p.category}
                </p>

                <p className="text-xs text-gray-500">
                  Unidade: {p.unit_of_measurement}
                </p>

                <div className="flex items-center gap-2 mt-2">
                  <span className="text-lg font-bold text-[var(--color-shop_dark_green)]">
                    R$ {p.price_in.toFixed(2)}
                  </span>
                </div>

                <button
                  onClick={() => setSelected(p)}
                  className="mt-2 bg-[var(--color-shop_light_green)] text-white py-2 rounded-lg hover:opacity-90"
                >
                  Ver detalhes
                </button>
              </div>
            </div>
          ))
        )}
      </section>

      {/* Modal de Detalhes */}
      {selected && (
        <div className="fixed inset-0 backdrop-blur-sm bg-black/10 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl w-96 shadow-xl">

            <div className="w-full h-48 flex items-center justify-center bg-gray-50 rounded-lg mb-4">
              <Image
                src="/fire (1).png"
                alt={selected.description}
                width={180}
                height={180}
                className="object-contain"
              />
            </div>

            <h3 className="text-xl font-bold">{selected.description}</h3>

            <div className="mt-4 space-y-2">
              <p className="text-gray-600">
                <span className="font-semibold">Categoria:</span> {selected.category}
              </p>
              
              <p className="text-gray-600">
                <span className="font-semibold">Unidade:</span> {selected.unit_of_measurement}
              </p>

              <p className="text-gray-600">
                <span className="font-semibold">ID da Prateleira:</span> {selected.bar_shelf_id}
              </p>

              <div className="pt-4 border-t">
                <p className="text-2xl font-bold text-[var(--color-shop_dark_green)]">
                  R$ {selected.price_in.toFixed(2)}
                </p>
              </div>
            </div>

            <button
              onClick={() => setSelected(null)}
              className="mt-6 px-4 py-2 bg-red-500 text-white rounded-lg w-full hover:bg-red-600"
            >
              Fechar
            </button>

          </div>
        </div>
      )}

    </main>
  );
}