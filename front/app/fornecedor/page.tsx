'use client';

import { useState, useEffect } from "react";
import axios from "axios";

// --- Interface alinhada com o DTO SupplierRead do Backend ---
interface Fornecedor {
  id: string; // UUID vindo do backend é string
  nome: string;
  email: string;
  cidade: string;
  descricao?: string;
  created_at?: string;
  updated_at?: string;
}

export default function FornecedoresPage() {
  // --- Estados ---
  const [fornecedores, setFornecedores] = useState<Fornecedor[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<Fornecedor | null>(null);
  const [error, setError] = useState<string | null>(null);

  // --- Busca de Dados ---
  async function fetchFornecedores() {
    try {
      setLoading(true);
      setError(null);
      
      // Endpoint do backend (acessível via localhost:8000 se mapeado no docker)
      const url = "http://localhost:8000/suppliers/";
      
      const response = await axios.get<Fornecedor[]>(url);
      setFornecedores(response.data);
    } catch (err) {
      console.error("Erro ao buscar fornecedores:", err);
      setError("Não foi possível carregar a lista. Verifique a conexão com o backend.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchFornecedores();
  }, []);

  // --- Filtro Local (Nome, Cidade ou Descrição) ---
  const filteredFornecedores = fornecedores.filter((f) =>
    f.nome.toLowerCase().includes(search.toLowerCase()) ||
    f.cidade.toLowerCase().includes(search.toLowerCase()) ||
    (f.descricao && f.descricao.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <main className="max-w-7xl mx-auto px-6 py-6 min-h-screen bg-gray-50">
      
      {/* --- Cabeçalho e Busca --- */}
      <section className="mb-8">
        <div className="flex flex-col md:flex-row justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] text-center lg:text-left">
            Lista de Fornecedores
          </h2>
          <button 
            onClick={fetchFornecedores}
            className="mt-4 md:mt-0 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition shadow-sm text-sm"
          >
            Atualizar Lista
          </button>
        </div>

        <div className="flex justify-center lg:justify-start">
          <div className="w-full max-w-xl flex items-center gap-3 px-5 py-3 bg-white rounded-full shadow-md border border-gray-200">
            {/* Ícone de Lupa */}
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z" />
            </svg>
            <input
              type="text"
              placeholder="Buscar por nome, cidade ou descrição..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 bg-transparent focus:outline-none text-base text-gray-700"
            />
          </div>
        </div>
      </section>

      {/* --- Loading e Erro --- */}
      {loading && (
        <div className="flex justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded shadow-sm">
          <p className="font-bold">Ops!</p>
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && (
        /* --- Grid de Cards --- */
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredFornecedores.length === 0 ? (
            <div className="col-span-full text-center py-16 bg-white rounded-xl shadow-sm border border-gray-100">
              <p className="text-xl text-gray-600">Nenhum fornecedor encontrado.</p>
              <p className="text-sm text-gray-400 mt-2">Tente buscar por outro termo.</p>
            </div>
          ) : (
            filteredFornecedores.map((f) => (
              <div key={f.id} className="bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-lg transition duration-300 flex flex-col h-full">
                
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-bold text-gray-800 line-clamp-1" title={f.nome}>
                    {f.nome}
                  </h3>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">Ativo</span>
                </div>
                
                <div className="flex-1 space-y-3 mb-4">
                  {/* Cidade */}
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <span className="flex-shrink-0">📍</span>
                    <p className="font-medium">{f.cidade}</p>
                  </div>

                  {/* Email */}
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <span className="flex-shrink-0">✉️</span>
                    <p className="truncate" title={f.email}>{f.email}</p>
                  </div>

                  {/* Descrição */}
                  <p className="text-sm text-gray-500 line-clamp-3 bg-gray-50 p-3 rounded mt-2 italic border-l-2 border-gray-200">
                    "{f.descricao || "Sem descrição disponível."}"
                  </p>
                </div>

                <button
                  onClick={() => setSelected(f)}
                  className="w-full bg-[var(--color-shop_light_green)] text-white px-4 py-2 rounded-lg hover:opacity-90 transition font-medium mt-auto"
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
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden animate-in fade-in zoom-in duration-200">
            
            {/* Header do Modal */}
            <div className="bg-[var(--color-shop_dark_green)] p-6 text-white relative">
              <button
                onClick={() => setSelected(null)}
                className="absolute top-4 right-4 text-white/80 hover:text-white transition text-2xl leading-none"
              >
                &times;
              </button>
              <h3 className="text-2xl font-bold">{selected.nome}</h3>
              <p className="text-green-100 text-sm mt-1">Fornecedor Parceiro</p>
            </div>

            {/* Corpo do Modal */}
            <div className="p-6 space-y-5">
              
              <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl border border-gray-100">
                <div>
                  <label className="text-xs font-bold text-gray-400 uppercase tracking-wide block mb-1">Cidade</label>
                  <p className="text-gray-800 font-medium flex items-center gap-1">
                    📍 {selected.cidade}
                  </p>
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-400 uppercase tracking-wide block mb-1">Contato</label>
                  <p className="text-gray-800 font-medium break-all text-sm">
                    ✉️ {selected.email}
                  </p>
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wide block mb-2">Sobre o Fornecedor</label>
                <div className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap bg-white p-1">
                  {selected.descricao || "Este fornecedor não forneceu uma descrição detalhada."}
                </div>
              </div>

              <div className="pt-4 border-t border-gray-100 flex justify-between items-center text-xs text-gray-400">
                <span>ID: <span className="font-mono">{selected.id.slice(0, 8)}...</span></span>
                {selected.created_at && (
                  <span>Cadastro: {new Date(selected.created_at).toLocaleDateString()}</span>
                )}
              </div>
            </div>
            
            {/* Rodapé do Modal */}
            <div className="p-4 bg-gray-50 text-right border-t">
              <button
                onClick={() => setSelected(null)}
                className="px-6 py-2 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition"
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