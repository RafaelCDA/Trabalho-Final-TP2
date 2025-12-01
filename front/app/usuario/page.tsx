'use client';

import axios from "axios";
import { useEffect, useState } from "react";

interface UserData {
  id: number;
  name: string;
  email: string;
}

export default function Perfil() {

  const [userData, setUserData]  = useState<UserData>({id: 0, name: "Usuário de Exemplo", email: "usuario@example.com"});
  const [newEmail, setNewEmail] = useState("");
  const [passwordData, setPasswordData] = useState({
    current: "",
    new: "",
    confirm: "",
  });

  async function fetchUserData() {
    try {
      const response = await axios.get(process.env.API_URL + "/user/1");
      setUserData(response.data);
    } catch (error) {
      console.error("Erro ao buscar fornecedores:", error);
    }
  }

  useEffect(() => {
    fetchUserData();
  }, []);


  const handleEmailChange = (e) => {
    e.preventDefault();
    if (newEmail.trim() === "") return;
    setUserData({ ...userData, email: newEmail });
    setNewEmail("");
  };

  const handlePasswordChange = (e) => {
    e.preventDefault();
    if (passwordData.new !== passwordData.confirm) {
      alert("A nova senha e a confirmação não conferem.");
      return;
    }
    alert("Senha alterada com sucesso!");
    setPasswordData({ current: "", new: "", confirm: "" });
  };

  return (
  <main className="max-w-lg mx-auto p-6 bg-white shadow rounded-lg mt-10">
      <h1 className="text-2xl font-bold mb-4">Informações do Usuário</h1>

      <div className="mb-6">
        <p><span className="font-semibold">Nome:</span> {userData.name} </p>
        <p><span className="font-semibold">Email:</span> {userData.email} </p>
      </div>

      <form
        onSubmit={handleEmailChange}
        className="mb-8 p-4 border rounded-lg bg-gray-50"
      >
        <h2 className="text-lg font-semibold mb-2">Alterar Email</h2>
        <input
          type="email"
          className="w-full border p-2 rounded mb-3"
          placeholder="Novo email"
          value={newEmail}
          onChange={(e) => setNewEmail(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Atualizar Email
        </button>
      </form>

      <form
        onSubmit={handlePasswordChange}
        className="p-4 border rounded-lg bg-gray-50"
      >
        <h2 className="text-lg font-semibold mb-2">Alterar Senha</h2>

        <input
          type="password"
          className="w-full border p-2 rounded mb-3"
          placeholder="Senha atual"
          value={passwordData.current}
          onChange={(e) =>
            setPasswordData({ ...passwordData, current: e.target.value })
          }
        />

        <input
          type="password"
          className="w-full border p-2 rounded mb-3"
          placeholder="Nova senha"
          value={passwordData.new}
          onChange={(e) =>
            setPasswordData({ ...passwordData, new: e.target.value })
          }
        />

        <input
          type="password"
          className="w-full border p-2 rounded mb-3"
          placeholder="Confirmar nova senha"
          value={passwordData.confirm}
          onChange={(e) =>
            setPasswordData({ ...passwordData, confirm: e.target.value })
          }
        />

        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Atualizar Senha
        </button>
      </form>
    </main>
    // <main className="max-w-7xl mx-auto px-6 py-6">
    //
    //   <h2 className="text-3xl font-bold text-[var(--color-shop_dark_green)] mb-6">
    //     Lista de Fornecedores
    //   </h2>
    //
    //   <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    //     {fornecedores.map((f: any, i: number) => (
    //       <div key={i} className="border p-4 rounded-xl shadow-sm hover:shadow-md transition">
    //
    //         <h3 className="text-lg font-semibold">{f.nome}</h3>
    //         <p className="text-gray-600">{f.cidade}</p>
    //
    //         {/* Descrição truncada com ... e quebrando palavras longas */}
    //         <p
    //           className="text-gray-500 text-sm mt-1 whitespace-nowrap overflow-hidden text-ellipsis break-all"
    //           style={{ width: "100%" }}
    //         >
    //           {f.descricao}
    //         </p>
    //
    //         <button
    //           onClick={() => setSelected(f)}
    //           className="mt-3 bg-[var(--color-shop_light_green)] text-white px-4 py-2 rounded-lg hover:opacity-90"
    //         >
    //           Ver detalhes
    //         </button>
    //
    //       </div>
    //     ))}
    //   </section>
    //
    //   {/* Modal com fundo blur + descrição completa */}
    //   {selected && (
    //     <div className="fixed inset-0 backdrop-blur-sm bg-black/10 flex items-center justify-center">
    //       <div className="bg-white p-6 rounded-xl w-80 shadow-xl">
    //
    //         <h3 className="text-xl font-bold">{selected.nome}</h3>
    //         <p className="text-gray-700 mt-2">{selected.cidade}</p>
    //
    //         {/* Aqui mostra a descrição INTEIRA */}
    //         <p className="text-gray-500 mt-2 whitespace-normal">
    //           {selected.descricao}
    //         </p>
    //
    //         <button
    //           onClick={() => setSelected(null)}
    //           className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg w-full"
    //         >
    //           Fechar
    //         </button>
    //
    //       </div>
    //     </div>
    //   )}
    //
    // </main>
  );
}
