'use client';

import Image from "next/image";
import { useState, useEffect } from "react";
import axios from "axios";

interface Produto {
  id: number;
  banca_id: number;
  nome: string;
  preco: number;
  imagem: string;
  created_at: string;
  updated_at: string;
}

interface Banca {
  id: number;
  nome: string;
  descricao: string;
  horario_funcionamento: string;
}

export default function Home() {

  // --- categorias da UI ---
  const categories = ["todos", "produtos", "bancas"];

  // --- estados principais ---
  const [activeCategory, setActiveCategory] = useState("todos");
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [bancas, setBancas] = useState<Banca[]>([]);
  const [search, setSearch] = useState("");

  // --- filtros locais ---
  const [precoMax, setPrecoMax] = useState<number | undefined>(undefined);
  const [distancia, setDistancia] = useState<number | undefined>(undefined);
  const [orderBy, setOrderBy] = useState<"preco" | "distancia" | undefined>(undefined);

  // --- filtros enviados ao backend ---
  const [filtros, setFiltros] = useState({
    termo: "",
    tipo: "all",
    preco_max: undefined as number | undefined,
    distancia_max_metros: undefined as number | undefined,
    order_by: undefined as "preco" | "distancia" | undefined,
    lat_user: -25.425704,
    lon_user: -49.273300,
    lat_ref: -25.425704,
    lon_ref: -49.273300,
  });

  // ============================================================
  // CONSULTA CENTRAL AO BACKEND
  // ============================================================
  async function fetchSearch(params: typeof filtros) {
    try {
      const url = new URL("http://localhost:80/pesquisa");

      // parâmetros obrigatórios
      url.searchParams.set("termo", params.termo);
      url.searchParams.set("tipo", params.tipo);

      // filtros opcionais
      if (params.preco_max !== undefined)
        url.searchParams.set("preco_max", String(params.preco_max));

      if (params.distancia_max_metros !== undefined)
        url.searchParams.set("distancia_max_metros", String(params.distancia_max_metros));

      if (params.order_by !== undefined)
        url.searchParams.set("order_by", params.order_by);

      // localização
      url.searchParams.set("lat_user", String(params.lat_user));
      url.searchParams.set("lon_user", String(params.lon_user));
      url.searchParams.set("lat_ref", String(params.lat_ref));
      url.searchParams.set("lon_ref", String(params.lon_ref));

      const res = await axios.get(url.toString());

      setProdutos(res.data.produtos || []);
      setBancas(res.data.bancas || []);

    } catch (err) {
      console.error("Erro na pesquisa:", err);
      setProdutos([]);
      setBancas([]);
    }
  }

  // dispara busca sempre que filtros mudarem
  useEffect(() => {
    fetchSearch(filtros);
  }, [filtros]);

  // ============================================================
  // HANDLERS DE FILTROS
  // ============================================================

  function handleSearch(text: string) {
    setSearch(text);
    setFiltros(f => ({ ...f, termo: text }));
  }

  function handleCategory(cat: string) {
    setActiveCategory(cat);

    const tipo =
      cat === "todos"
        ? "all"
        : cat === "produtos"
        ? "produto"
        : "banca";

    setFiltros(f => ({ ...f, tipo }));
  }

  function handlePreco(value: number) {
    setPrecoMax(value);
    setFiltros(f => ({ ...f, preco_max: value }));
  }

  function handleDistancia(value: number) {
    setDistancia(value);
    setFiltros(f => ({ ...f, distancia_max_metros: value }));
  }

  function handleOrder(value: "preco" | "distancia" | "") {
    const val = value === "" ? undefined : value;
    setOrderBy(val as any);
    setFiltros(f => ({ ...f, order_by: val }));
  }

  // ============================================================
  // RENDERIZAÇÃO
  // ============================================================

  return (
    <main className="max-w-7xl mx-auto mb-10 px-6 py-6">

      {/* --- barra de pesquisa --- */}
      <section className="mb-10 flex justify-center">
        <div className="w-full max-w-xl flex items-center gap-3 px-5 py-3 
            bg-white rounded-full shadow-md border border-gray-200">

          <svg xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 text-gray-500"
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
              d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z" />
          </svg>

          <input
            type="text"
            placeholder="Buscar..."
            value={search}
            onChange={(e) => handleSearch(e.target.value)}
            className="flex-1 bg-transparent focus:outline-none text-base"
          />
        </div>
      </section>

      {/* --- categorias --- */}
      <section className="mt-10 flex items-center gap-4">
        {categories.map((cat) => (
          <button key={cat} onClick={() => handleCategory(cat)}
            className={`px-5 py-2 rounded-full border transition ${
              activeCategory === cat
                ? "bg-[var(--color-shop_light_green)] text-white border-[var(--color-shop_light_green)]"
                : "border-gray-300 text-gray-700 hover:bg-gray-100"
            }`}>
            {cat}
          </button>
        ))}
      </section>

      {/* --- layout principal --- */}
      <section className="mt-12 grid grid-cols-1 lg:grid-cols-[250px_1fr] gap-10">

        {/* --- sidebar de filtros --- */}
        <aside className="hidden lg:block border rounded-lg p-5 h-fit sticky top-20 bg-white shadow-sm">

          <h3 className="text-lg font-semibold mb-3">Filtros</h3>

          {/* preço */}
          <div className="mb-6">
            <h4 className="font-medium mb-2">Preço máximo</h4>

            <input
              type="range"
              min={0}
              max={200}
              value={precoMax ?? 0}
              onChange={(e) => handlePreco(Number(e.target.value))}
              className="w-full"
            />

            <p className="text-sm text-gray-600">
              Até: <strong>R${precoMax ?? 0}</strong>
            </p>
          </div>

          {/* distância */}
          <div className="mb-6">
            <h4 className="font-medium mb-2">Distância máxima (m)</h4>

            <input
              type="range"
              min={0}
              max={2000}
              value={distancia ?? 0}
              onChange={(e) => handleDistancia(Number(e.target.value))}
              className="w-full"
            />

            <p className="text-sm text-gray-600">
              Até: <strong>{distancia ?? 0}m</strong>
            </p>
          </div>

          {/* ordenação */}
          <div className="mb-6">
            <h4 className="font-medium mb-2">Ordenar por</h4>

            <select
              className="w-full border rounded p-2"
              value={orderBy ?? ""}
              onChange={(e) => handleOrder(e.target.value as any)}
            >
              <option value="">Nenhum</option>
              <option value="preco">Menor preço</option>
              <option value="distancia">Menor distância</option>
            </select>
          </div>

        </aside>

        {/* --- grid de resultados --- */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">

          {/* produtos */}
          {(activeCategory === "produtos" || activeCategory === "todos") &&
            produtos.map((p) => (
              <div key={p.id}
                className="rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md transition">
                <div className="w-full h-40 flex items-center justify-center">
                  <Image
                    src="/fire (1).png"
                    alt={p.nome}
                    width={140}
                    height={140}
                    className="object-contain"
                  />
                </div>
                <h3 className="mt-3 text-sm font-medium text-gray-700">
                  {p.nome}
                </h3>
                <span className="text-lg font-bold text-[var(--color-shop_dark_green)]">
                  R${p.preco}
                </span>
              </div>
            ))}

          {/* bancas */}
          {(activeCategory === "bancas" || activeCategory === "todos") &&
            bancas.map((b) => (
              <div key={b.id}
                className="rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md transition">
                <h3 className="text-md font-bold">{b.nome}</h3>
                <p className="text-sm text-gray-600">{b.descricao}</p>
                <p className="text-sm text-gray-500 mt-2">
                  Horário: {b.horario_funcionamento}
                </p>
              </div>
            ))}

        </div>
      </section>
    </main>
  );
}
