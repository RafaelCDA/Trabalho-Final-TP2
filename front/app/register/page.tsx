"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function RegisterForm() {
  const router = useRouter();

  const [form, setForm] = useState({
    nome: "",
    email: "",
    senha: "",
    confirmarSenha: "",
    tipo: "user", // 'user' ou 'supplier'
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (form.senha !== form.confirmarSenha) {
      setError("As senhas não coincidem!");
      return;
    }

    const response = await axios.post(process.env.NEXT_PUBLIC_API_URL + "/users/", 
      {
        "name": form.nome,
        "email": form.email,
        "password": form.senha,
        "type": form.tipo
      }
    ).then((r) => {
      alert("Conta criada com sucesso! Faça login para continuar.");
      router.push("/login");
    }).catch(e =>  {
      if (e.status !== 500){
        alert("Erro ao criar conta: " + e.response.data.detail);
      }
    });

  };

  return (
    <div className="w-full max-w-sm mx-auto py-12">
      <h1 className="text-2xl font-semibold text-center mb-8 text-gray-800">
        Criar Conta
      </h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white shadow rounded-lg px-6 py-8 space-y-5"
      >
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Nome
          </label>
          <input
            type="text"
            name="nome"
            required
            value={form.nome}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:outline-none"
            placeholder="Seu nome"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            E-mail
          </label>
          <input
            type="email"
            name="email"
            required
            value={form.email}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:outline-none"
            placeholder="seuemail@email.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Senha
          </label>
          <input
            type="password"
            name="senha"
            required
            value={form.senha}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:outline-none"
            placeholder="********"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Confirmar Senha
          </label>
          <input
            type="password"
            name="confirmarSenha"
            required
            value={form.confirmarSenha}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:outline-none"
            placeholder="********"
          />
        </div>

        <div>
          <span className="block text-sm font-medium text-gray-700 mb-2">
            Tipo de Conta
          </span>
          <div className="flex items-center gap-4">
            <label className="inline-flex items-center gap-2">
              <input
                type="radio"
                name="tipo"
                value="user"
                checked={form.tipo === "user"}
                onChange={handleChange}
                className="h-4 w-4 text-green-600"
              />
              <span>Usuário</span>
            </label>

            <label className="inline-flex items-center gap-2">
              <input
                type="radio"
                name="tipo"
                value="supplier"
                checked={form.tipo === "supplier"}
                onChange={handleChange}
                className="h-4 w-4 text-green-600"
              />
              <span>Fornecedor</span>
            </label>
          </div>
        </div>

        {error ? (
          <div className="flex items-center">
            <p className="text-red-400 font-bold text-lg">
              {error}
            </p>
          </div>
        ):(<></>)}

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-md transition"
        >
          Criar Conta
        </button>

        <p className="text-center text-sm text-gray-600 pt-2">
          Já tem conta?{" "}
          <button
            type="button"
            onClick={() => router.push("/login")}
            className="text-blue-600 hover:underline"
          >
            Entrar
          </button>
        </p>
      </form>
    </div>
  );
}
