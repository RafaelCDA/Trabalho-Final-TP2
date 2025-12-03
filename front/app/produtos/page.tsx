'use client';

import { useState, useEffect } from "react";
import axios from "axios";
import Image from "next/image";
import { Heart } from "lucide-react";

// --- Interface alinhada com o Backend (ProdutoRead) ---
interface Produto {
  id: number;
  nome: string;      // Backend usa 'nome', não 'description'
  preco: number;     // Backend usa 'preco', não 'price_in'
  imagem?: string;   // Backend pode retornar null
  banca_id: number;
}

export default function ProdutosPage() {
  // --- Estados ---
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<Produto | null>(null);

  // --- Busca de Dados ---
  async function fetchProdutos() {
    try {
      setLoading(true);
      // Acessa o backend na porta 8000 via localhost
      const url = "http://localhost:8000/produtos/"; 
      
      const response = await axios.get<Produto[]>(url);
      setProdutos(response.data);
    } catch (error) {
      console.error("Erro ao buscar produtos:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchProdutos();
  }, []);

  // --- Filtro Local (pelo nome) ---
  const filteredProdutos = produtos.filter((p) =>
    p.nome.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <main className="max-w-7xl mx-auto px-6 py-6 min-h-screen bg-gray-50">
      
      {/* --- Cabeçalho e Busca --- */}
      <section className="mb-8">
        <div className="flex flex-col md:flex-row justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] text-center lg:text-left">
            Lista de Produtos
          </h2>
          <button 
            onClick={fetchProdutos}
            className="mt-4 md:mt-0 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition shadow-sm text-sm"
          >
            Atualizar Lista
          </button>
        </div>

        {/* Barra de Pesquisa */}
        <div className="flex justify-center lg:justify-start">
          <div className="w-full max-w-xl flex items-center gap-3 px-5 py-3 bg-white rounded-full shadow-md border border-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z" />
            </svg>
            <input
              type="text"
              placeholder="Buscar produto..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 bg-transparent focus:outline-none text-base text-gray-700"
            />
          </div>
        </div>
      </section>

      {/* --- Loading --- */}
      {loading ? (
        <div className="flex justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      ) : (
        /* --- Grid de Produtos --- */
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredProdutos.length === 0 ? (
            <div className="col-span-full text-center py-16 bg-white rounded-xl shadow-sm border border-gray-100">
              <p className="text-xl text-gray-600">Nenhum produto encontrado.</p>
              <p className="text-sm text-gray-400 mt-2">Verifique se o backend está rodando em localhost:8000</p>
            </div>
          ) : (
            filteredProdutos.map((p) => (
              <div 
                key={p.id} 
                className="bg-white border border-gray-200 p-4 rounded-xl shadow-sm hover:shadow-lg transition duration-300 flex flex-col relative group"
              >
                {/* Botão de Favorito (Visual apenas) */}
                <button className="absolute top-3 right-3 text-gray-400 hover:text-red-500 transition z-10 bg-white/80 rounded-full p-1">
                  <Heart size={20} />
                </button>

                {/* Imagem do Produto */}
                <div className="w-full h-48 flex items-center justify-center bg-gray-50 rounded-lg mb-4 p-2">
                  {p.imagem ? (
                    <img 
                      src={p.imagem} 
                      alt={p.nome} 
                      className="max-h-full max-w-full object-contain mix-blend-multiply"
                      onError={(e) => (e.currentTarget.src = "/fire (1).png")} // Fallback se a imagem quebrar
                    />
                  ) : (
                    <Image
                      src="/fire (1).png"
                      alt={p.nome}
                      width={120}
                      height={120}
                      className="object-contain opacity-50"
                    />
                  )}
                </div>

                <div className="flex-1 flex flex-col">
                  <h3 className="text-md font-semibold text-gray-800 line-clamp-2 mb-1" title={p.nome}>
                    {p.nome}
                  </h3>
                  
                  {/* Preço com destaque */}
                  <div className="mt-auto pt-2 flex items-center justify-between">
                    <div className="flex flex-col">
                      <span className="text-xs text-gray-500">Preço</span>
                      <span className="text-xl font-bold text-[var(--color-shop_dark_green)]">
                        R$ {p.preco.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setSelected(p)}
                  className="mt-4 w-full bg-[var(--color-shop_light_green)] text-white py-2 rounded-lg hover:opacity-90 transition font-medium text-sm"
                >
                  Ver Detalhes
                </button>
              </div>
            ))
          )}
        </section>
      )}

      {/* --- Modal de Detalhes --- */}
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200 relative">
            
            {/* Botão Fechar no Topo */}
            <button
                onClick={() => setSelected(null)}
                className="absolute top-4 right-4 z-10 bg-black/20 text-white rounded-full p-1 hover:bg-black/40 transition"
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            {/* Imagem Grande no Modal */}
            <div className="w-full h-64 bg-gray-100 flex items-center justify-center p-6">
               {selected.imagem ? (
                    <img 
                      src={selected.imagem} 
                      alt={selected.nome} 
                      className="max-h-full max-w-full object-contain"
                    />
                  ) : (
                    <Image
                      src="/fire (1).png"
                      alt={selected.nome}
                      width={180}
                      height={180}
                      className="object-contain opacity-50"
                    />
                  )}
            </div>

            <div className="p-6">
              <h3 className="text-2xl font-bold text-gray-800 mb-2">{selected.nome}</h3>
              
              <div className="space-y-3 mt-4">
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-gray-500">ID do Produto</span>
                  <span className="font-mono text-gray-700">#{selected.id}</span>
                </div>
                
                <div className="flex justify-between items-center border-b pb-3">
                  <span className="text-gray-500">ID da Banca</span>
                  <span className="font-mono text-gray-700">#{selected.banca_id}</span>
                </div>

                <div className="pt-2">
                  <span className="block text-sm text-gray-500 mb-1">Preço Atual</span>
                  <span className="text-3xl font-bold text-[var(--color-shop_dark_green)]">
                    R$ {selected.preco.toFixed(2)}
                  </span>
                </div>
              </div>

              <button
                onClick={() => setSelected(null)}
                className="mt-6 w-full py-3 bg-red-500 text-white font-semibold rounded-xl hover:bg-red-600 transition"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}

    </main>
  );
}