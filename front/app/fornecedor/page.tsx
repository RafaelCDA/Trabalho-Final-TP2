'use client';

import axios from "axios";
import { useEffect, useState } from "react";

export default function Fornecedores() {

  // ➜ Fornecedores de teste
  const [fornecedores, setFornecedores] = useState([]);

  const [selected, setSelected] = useState<any | null>(null);

  async function fetchFornecedores() {
    try {
      const response = await axios.get("http://localhost:3000/suppliers");
      setFornecedores(response.data);
    } catch (error) {
      console.error("Erro ao buscar fornecedores:", error);
    }
  }

  useEffect(() => {
    fetchFornecedores();
  }, []);

  return (
    <main className="max-w-7xl mx-auto px-6 py-6">

      <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] mb-6">
        Lista de Fornecedores
      </h2>

      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {fornecedores.map((f: any, i: number) => (
          <div key={i} className="border p-4 rounded-xl shadow-sm hover:shadow-md transition">
            <h3 className="text-lg font-semibold">{f.nome}</h3>
            <p className="text-gray-600">{f.cidade}</p>
            <p className="text-gray-500 text-sm mt-1">{f.descricao}</p>

            <button
              onClick={() => setSelected(f)}
              className="mt-3 bg-[var(--color-shop_light_green)] text-white px-4 py-2 rounded-lg hover:opacity-90"
            >
              Ver detalhes
            </button>
          </div>
        ))}
      </section>

      {/* Modal com fundo BLUR */}
      {selected && (
        <div className="fixed inset-0 backdrop-blur-sm bg-black/10 flex items-center justify-center">
          <div className="bg-white p-6 rounded-xl w-80 shadow-xl">

            <h3 className="text-xl font-bold">{selected.nome}</h3>
            <p className="text-gray-700 mt-2">{selected.cidade}</p>
            <p className="text-gray-500 mt-2">{selected.descricao}</p>

            <button
              onClick={() => setSelected(null)}
              className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg w-full"
            >
              Fechar
            </button>

          </div>
        </div>
      )}

    </main>
  );
}
