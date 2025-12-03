"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios, { AxiosError } from "axios";


export default function Login() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    const response = await axios.post(process.env.NEXT_PUBLIC_API_URL + "/auth/login", 
      {
        "email": email,
        "password": senha  
      }
    ).then((r) => {
      const user = {
        id: r.data.id,
        name: r.data.email,
        email: r.data.email,
        type: r.data.type
      };
      sessionStorage.setItem("user", JSON.stringify(user));

      // sinaliza outras partes da app (mesma aba) que o usuário mudou
      window.dispatchEvent(new Event("userChanged"));

      // navega para a home
      router.push("/");
    }).catch(e =>  {
      if (e.status !== 500){
        setError(e.response.data.detail)
      }
    });
  };

  return (
    <div className="w-full max-w-sm mx-auto py-12">
      <h1 className="text-2xl font-semibold text-center mb-8 text-gray-800">
        Login
      </h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white shadow rounded-lg px-6 py-8 space-y-5"
      >
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            E-mail
          </label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:outline-none"
            placeholder="********"
          />
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
          Entrar
        </button>

        <p className="text-center text-sm text-gray-600 pt-2">
          Não tem conta?{" "}
          <button
            type="button"
            onClick={() => router.push("/register")}
            className="text-blue-600 hover:underline"
          >
            Criar conta
          </button>
        </p>
      </form>
    </div>
  );
}
