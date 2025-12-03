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
      const data = sessionStorage.getItem("user");
      console.log(data);
      setUserData(JSON.parse(data) || null);
    } catch (error) {
      console.error("Erro ao buscar fornecedores:", error);
    }
  }

  useEffect(() => {
    fetchUserData();
  }, []);


  const handleEmailChange = async (e) => {
    e.preventDefault();
    if (newEmail.trim() === "") return;
    const response = await axios.put(process.env.NEXT_PUBLIC_API_URL + `/users/${userData.id}`, 
      {
        "email": newEmail
      }
    ).then((r) => {
      alert("Email alterado com sucesso!");
      sessionStorage.setItem("user", JSON.stringify({...userData, email: newEmail}));
      setUserData({ ...userData, email: newEmail });
      setNewEmail("");
    }).catch(e =>  {
      if (e.status !== 500){
        alert("Erro ao alterar email: " + e.response.data.detail);
      }
    });
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
  );
}
