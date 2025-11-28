// EU010 - Listagem de Bancas
'use client';

import axios from "axios";
import { useEffect, useState } from "react";

interface Banca {
  id?: number;
  nome: string;
  descricao: string;
  endereco: string;
  latitude: number;
  longitude: number;
  horario_abertura: string;
  horario_fechamento: string;
  fornecedor_id?: number;
}

export default function Bancas() {

  const [bancas, setBancas] = useState<Banca[]>([]);

  const [selected, setSelected] = useState<Banca | null>(null);

  async function fetchBancas() {
    try {
      const response = await axios.get("http://localhost:3000/bancas");
      // Garante que sempre seja um array
      setBancas(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error("Erro ao buscar bancas:", error);
      setBancas([]); // Define array vazio em caso de erro
    }
  }

  useEffect(() => {
   // fetchBancas();
    
    // DADOS DE TESTE - REMOVER QUANDO O BACKEND ESTIVER PRONTO
    setBancas([
      {
        id: 1,
        nome: "Banca do João",
        descricao: "Frutas e verduras frescas, produtos orgânicos e sucos naturais. Atendimento de qualidade!",
        endereco: "SQN 308, Asa Norte, Brasília - DF",
        latitude: -15.7801,
        longitude: -47.9292,
        horario_abertura: "08:00",
        horario_fechamento: "18:00",
        fornecedor_id: 1
      },
      {
        id: 2,
        nome: "Empório da Maria",
        descricao: "Especializada em queijos artesanais, vinhos e produtos gourmet",
        endereco: "CLN 405, Asa Norte, Brasília - DF",
        latitude: -15.7501,
        longitude: -47.8892,
        horario_abertura: "09:00",
        horario_fechamento: "20:00",
        fornecedor_id: 2
      },
      {
        id: 3,
        nome: "Feira do Pedro",
        descricao: "Carnes, peixes e frutos do mar frescos diariamente",
        endereco: "SHIS QI 15, Lago Sul, Brasília - DF",
        latitude: -15.8301,
        longitude: -47.8592,
        horario_abertura: "07:00",
        horario_fechamento: "17:00",
        fornecedor_id: 3
      }
    ]);
  }, []);

  return (
    <main className="max-w-7xl mx-auto px-6 py-6">

      <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] mb-6">
        Lista de Bancas
      </h2>

      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {bancas.length === 0 ? (
          <div className="col-span-full text-center py-10 text-gray-500">
            <p className="text-lg">Nenhuma banca cadastrada ainda.</p>
            <p className="text-sm mt-2">Aguardando dados do backend...</p>
          </div>
        ) : (
          bancas.map((b: Banca, i: number) => (
            <div key={i} className="border p-4 rounded-xl shadow-sm hover:shadow-md transition">

              <h3 className="text-lg font-semibold">{b.nome}</h3>
              <p className="text-gray-600">{b.endereco}</p>

              {/* Horário de funcionamento */}
              <p className="text-gray-500 text-sm mt-1">
                🕐 {b.horario_abertura} - {b.horario_fechamento}
              </p>

              {/* Descrição truncada com ... e quebrando palavras longas */}
              <p
                className="text-gray-500 text-sm mt-1 whitespace-nowrap overflow-hidden text-ellipsis break-all"
                style={{ width: "100%" }}
              >
                {b.descricao}
              </p>

              <button
                onClick={() => setSelected(b)}
                className="mt-3 bg-[var(--color-shop_light_green)] text-white px-4 py-2 rounded-lg hover:opacity-90"
              >
                Ver detalhes
              </button>

            </div>
          ))
        )}
      </section>

      {/* Modal com fundo blur + descrição completa */}
      {selected && (
        <div className="fixed inset-0 backdrop-blur-sm bg-black/10 flex items-center justify-center">
          <div className="bg-white p-6 rounded-xl w-80 shadow-xl">

            <h3 className="text-xl font-bold">{selected.nome}</h3>
            <p className="text-gray-700 mt-2">📍 {selected.endereco}</p>

            {/* Localização GPS */}
            <p className="text-gray-600 text-sm mt-2">
              🌐 Lat: {selected.latitude}, Lng: {selected.longitude}
            </p>

            {/* Horário completo */}
            <p className="text-gray-600 text-sm mt-2">
              🕐 Funcionamento: {selected.horario_abertura} - {selected.horario_fechamento}
            </p>

            {/* Aqui mostra a descrição INTEIRA */}
            <p className="text-gray-500 mt-2 whitespace-normal">
              {selected.descricao}
            </p>

            {/* Link para Google Maps */}
            {selected.latitude && selected.longitude && (
              <a
                href={`https://www.google.com/maps?q=${selected.latitude},${selected.longitude}`}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 block text-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                🗺️ Ver no Mapa
              </a>
            )}

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