'use client';

import { useState, useEffect } from "react";
import axios from "axios";

// --- Tipagem alinhada com o Backend (BancaRead + AddressRead) ---
interface Endereco {
  id: string;
  street: string;
  number?: string;
  complement?: string;
  district?: string;
  city: string;
  state: string;
  zip_code: string;
  latitude?: number;
  longitude?: number;
}

interface Banca {
  id: number;
  nome: string;
  descricao?: string;
  horario_funcionamento?: string;
  supplier_id: string;
  address: Endereco; // Objeto aninhado vindo da API
  created_at: string;
}

export default function BancasPage() {
  // --- Estados ---
  const [bancas, setBancas] = useState<Banca[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<Banca | null>(null);

  // --- Busca de Dados ---
  async function fetchBancas() {
    try {
      setLoading(true);
      // O frontend Next.js (client) acessa o backend na porta 8000 do host
      const url = "http://localhost:8000/bancas/"; 
      
      const response = await axios.get<Banca[]>(url);
      setBancas(response.data);
    } catch (error) {
      console.error("Erro ao buscar bancas:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchBancas();
  }, []);

  // --- Filtro Local (pelo nome ou descrição) ---
  const filteredBancas = bancas.filter((b) =>
    b.nome.toLowerCase().includes(search.toLowerCase()) ||
    (b.descricao && b.descricao.toLowerCase().includes(search.toLowerCase()))
  );

  // --- Helper de Endereço ---
  const formatarEndereco = (end: Endereco) => {
    const numero = end.number ? `, ${end.number}` : '';
    return `${end.street}${numero} - ${end.district || ''}, ${end.city}/${end.state}`;
  };

  return (
    <main className="max-w-7xl mx-auto px-6 py-6 min-h-screen bg-gray-50">
      
      {/* --- Cabeçalho e Busca --- */}
      <section className="mb-8">
        <div className="flex flex-col md:flex-row justify-between items-center mb-6">
            <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] text-center lg:text-left">
            Feira Virtual - Bancas
            </h2>
            <button 
                onClick={fetchBancas}
                className="mt-4 md:mt-0 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition shadow-sm text-sm"
            >
                Atualizar Lista
            </button>
        </div>

        <div className="flex justify-center lg:justify-start">
          <div className="w-full max-w-xl flex items-center gap-3 px-5 py-3 bg-white rounded-full shadow-md border border-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z" />
            </svg>
            <input
              type="text"
              placeholder="Buscar banca por nome..."
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
        /* --- Grid de Bancas --- */
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredBancas.length === 0 ? (
            <div className="col-span-full text-center py-16 bg-white rounded-xl shadow-sm border border-gray-100">
              <p className="text-xl text-gray-600">Nenhuma banca encontrada.</p>
              <p className="text-sm text-gray-400 mt-2">Verifique se o backend está rodando em localhost:8000</p>
            </div>
          ) : (
            filteredBancas.map((b) => (
              <div key={b.id} className="bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-lg transition duration-300 flex flex-col h-full">
                
                <h3 className="text-lg font-bold text-gray-800 mb-2">{b.nome}</h3>
                
                <div className="flex-1 space-y-2 mb-4">
                  <div className="flex items-start gap-2 text-sm text-gray-600">
                    <span className="flex-shrink-0">📍</span>
                    <p className="line-clamp-2">{formatarEndereco(b.address)}</p>
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <span className="flex-shrink-0">🕒</span>
                    <p>{b.horario_funcionamento || "Horário não informado"}</p>
                  </div>

                  <p className="text-sm text-gray-500 line-clamp-3 bg-gray-50 p-2 rounded mt-2">
                    {b.descricao || "Sem descrição."}
                  </p>
                </div>

                <button
                  onClick={() => setSelected(b)}
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
            
            <div className="bg-[var(--color-shop_dark_green)] p-6 text-white relative">
              <button
                onClick={() => setSelected(null)}
                className="absolute top-4 right-4 text-white/80 hover:text-white transition text-2xl leading-none"
              >
                &times;
              </button>
              <h3 className="text-2xl font-bold">{selected.nome}</h3>
              <p className="text-green-100 text-sm mt-1">{selected.address.city} - {selected.address.state}</p>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wide">Localização</label>
                <p className="text-gray-800 font-medium">{formatarEndereco(selected.address)}</p>
                {selected.address.complement && (
                  <p className="text-gray-500 text-sm mt-1">Comp: {selected.address.complement}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-gray-400 uppercase tracking-wide">Horário</label>
                  <p className="text-gray-800">{selected.horario_funcionamento || "—"}</p>
                </div>
                {selected.address.latitude && (
                  <div>
                    <label className="text-xs font-bold text-gray-400 uppercase tracking-wide">GPS</label>
                    <p className="text-gray-800 text-sm">{selected.address.latitude.toFixed(4)}, {selected.address.longitude?.toFixed(4)}</p>
                  </div>
                )}
              </div>

              <div>
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wide">Sobre</label>
                <p className="text-gray-600 text-sm mt-1 leading-relaxed whitespace-pre-wrap">
                  {selected.descricao || "Nenhuma descrição disponível."}
                </p>
              </div>

              {/* Botão Mapa */}
              {selected.address.latitude && selected.address.longitude ? (
                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${selected.address.latitude},${selected.address.longitude}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl transition mt-4 shadow-md"
                >
                  🗺️ Ver no Google Maps
                </a>
              ) : (
                <div className="mt-4 p-3 bg-gray-100 text-gray-500 text-center rounded-lg text-sm">
                  Localização GPS não disponível
                </div>
              )}
            </div>
            
            <div className="p-4 bg-gray-50 text-right border-t">
              <button
                onClick={() => setSelected(null)}
                className="px-6 py-2 text-gray-600 hover:text-gray-900 font-medium transition"
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