'use client';

import { useState } from 'react';
import axios from 'axios';

type TipoCadastro = 'fornecedor' | 'banca' | 'produto';

interface FormData {
  // Comuns
  nome?: string;
  descricao?: string;

  // Fornecedor (EU009)
  email?: string;
  cidade?: string; // Cidade do fornecedor (string simples)
  
  // Banca (EU010) - Backend exige endereço estruturado
  supplier_id?: string;
  horario_funcionamento?: string;
  // Endereço da Banca
  street?: string;
  number?: string;
  district?: string;
  city_banca?: string;
  state?: string;
  zip_code?: string;
  latitude?: string;
  longitude?: string;
  
  // Produto (EU011)
  preco?: string;
  imagem?: string;
  banca_id?: string;
}

export default function FormCadastro() {
  const [tipo, setTipo] = useState<TipoCadastro>('fornecedor');
  const [formData, setFormData] = useState<FormData>({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  // Reset do formulário ao trocar de aba
  const handleTipoChange = (novoTipo: TipoCadastro) => {
    setTipo(novoTipo);
    setFormData({});
    setMessage({ type: '', text: '' });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Validação básica antes de enviar
  const validarCampos = (): boolean => {
    if (tipo === 'fornecedor') {
      return !!(formData.nome && formData.email && formData.cidade);
    } else if (tipo === 'banca') {
      return !!(
        formData.nome && 
        formData.supplier_id && 
        formData.street && 
        formData.city_banca && 
        formData.state && 
        formData.zip_code
      );
    } else if (tipo === 'produto') {
      return !!(formData.nome && formData.preco && formData.banca_id);
    }
    return false;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validarCampos()) {
      setMessage({ type: 'error', text: 'Preencha todos os campos obrigatórios (*)' });
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      let url = '';
      let payload = {};

      // --- Lógica de Envio para Fornecedor ---
      if (tipo === 'fornecedor') {
        url = 'http://localhost:8000/suppliers/';
        payload = {
          nome: formData.nome,
          email: formData.email,
          cidade: formData.cidade,
          descricao: formData.descricao
        };
      } 
      // --- Lógica de Envio para Banca ---
      else if (tipo === 'banca') {
        url = 'http://localhost:8000/bancas/';
        payload = {
          nome: formData.nome,
          descricao: formData.descricao,
          horario_funcionamento: formData.horario_funcionamento,
          supplier_id: formData.supplier_id,
          // O Backend exige um objeto 'address' aninhado
          address: {
            street: formData.street,
            number: formData.number,
            district: formData.district,
            city: formData.city_banca,
            state: formData.state,
            zip_code: formData.zip_code,
            latitude: formData.latitude ? parseFloat(formData.latitude) : null,
            longitude: formData.longitude ? parseFloat(formData.longitude) : null
          }
        };
      } 
      // --- Lógica de Envio para Produto ---
      else if (tipo === 'produto') {
        url = 'http://localhost:8000/produtos/';
        payload = {
          nome: formData.nome,
          preco: parseFloat(formData.preco || '0'),
          imagem: formData.imagem,
          banca_id: parseInt(formData.banca_id || '0')
        };
      }

      await axios.post(url, payload);

      setMessage({ type: 'success', text: `Cadastro de ${tipo} realizado com sucesso!` });
      setFormData({}); // Limpar formulário após sucesso

    } catch (error: any) {
      console.error(error);
      const errorMsg = error.response?.data?.detail || 'Erro ao conectar com o servidor.';
      setMessage({ type: 'error', text: `Erro: ${errorMsg}` });
    } finally {
      setLoading(false);
    }
  };

  const obterLocalizacao = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude.toString(),
            longitude: position.coords.longitude.toString()
          }));
          setMessage({ type: 'success', text: 'Localização GPS obtida!' });
        },
        () => setMessage({ type: 'error', text: 'Permissão de localização negada.' })
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow-lg rounded-xl p-8 border border-gray-100">
          
          {/* Navegação entre Abas */}
          <div className="flex gap-2 mb-8 bg-gray-100 p-1 rounded-lg">
            {(['fornecedor', 'banca', 'produto'] as TipoCadastro[]).map((t) => (
              <button
                key={t}
                onClick={() => handleTipoChange(t)}
                className={`flex-1 py-2 px-4 rounded-md font-medium text-sm transition-all ${
                  tipo === t
                    ? 'bg-white text-[var(--color-shop_dark_green)] shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>

          <h1 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">
            {tipo === 'fornecedor' && 'Novo Fornecedor'}
            {tipo === 'banca' && 'Nova Banca'}
            {tipo === 'produto' && 'Novo Produto'}
          </h1>

          {/* Feedback Visual */}
          {message.text && (
            <div className={`mb-6 p-4 rounded-lg text-sm font-medium ${
              message.type === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'
            }`}>
              {message.text}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            
            {/* ================= FORNECEDOR ================= */}
            {tipo === 'fornecedor' && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="label-form">Nome *</label>
                    <input name="nome" value={formData.nome || ''} onChange={handleChange} className="input-form" placeholder="Ex: João da Silva" />
                  </div>
                  <div>
                    <label className="label-form">Email *</label>
                    <input name="email" type="email" value={formData.email || ''} onChange={handleChange} className="input-form" placeholder="joao@email.com" />
                  </div>
                </div>
                <div>
                  <label className="label-form">Cidade *</label>
                  <input name="cidade" value={formData.cidade || ''} onChange={handleChange} className="input-form" placeholder="Brasília" />
                </div>
                <div>
                  <label className="label-form">Descrição</label>
                  <textarea name="descricao" value={formData.descricao || ''} onChange={handleChange} rows={3} className="input-form" placeholder="Biografia ou detalhes..." />
                </div>
              </>
            )}

            {/* ================= BANCA ================= */}
            {tipo === 'banca' && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="label-form">Nome da Banca *</label>
                    <input name="nome" value={formData.nome || ''} onChange={handleChange} className="input-form" placeholder="Ex: Banca do João" />
                  </div>
                  <div>
                    <label className="label-form">ID do Fornecedor *</label>
                    <input name="supplier_id" value={formData.supplier_id || ''} onChange={handleChange} className="input-form" placeholder="UUID do fornecedor" />
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 space-y-4">
                  <h3 className="font-semibold text-gray-700 text-sm">Endereço da Banca</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="md:col-span-2">
                      <label className="label-form">Logradouro (Rua) *</label>
                      <input name="street" value={formData.street || ''} onChange={handleChange} className="input-form" placeholder="Av. Principal" />
                    </div>
                    <div>
                      <label className="label-form">Número</label>
                      <input name="number" value={formData.number || ''} onChange={handleChange} className="input-form" placeholder="123" />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="label-form">Bairro</label>
                      <input name="district" value={formData.district || ''} onChange={handleChange} className="input-form" />
                    </div>
                    <div>
                      <label className="label-form">CEP *</label>
                      <input name="zip_code" value={formData.zip_code || ''} onChange={handleChange} className="input-form" placeholder="00000-000" />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="label-form">Cidade *</label>
                      <input name="city_banca" value={formData.city_banca || ''} onChange={handleChange} className="input-form" />
                    </div>
                    <div>
                      <label className="label-form">Estado (UF) *</label>
                      <input name="state" value={formData.state || ''} onChange={handleChange} className="input-form" maxLength={2} placeholder="DF" />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-2 border-t">
                    <div>
                      <label className="label-form">Latitude</label>
                      <input name="latitude" type="number" step="any" value={formData.latitude || ''} onChange={handleChange} className="input-form text-xs" />
                    </div>
                    <div>
                      <label className="label-form">Longitude</label>
                      <input name="longitude" type="number" step="any" value={formData.longitude || ''} onChange={handleChange} className="input-form text-xs" />
                    </div>
                  </div>
                  <button type="button" onClick={obterLocalizacao} className="text-xs text-blue-600 hover:underline font-medium">
                    📍 Pegar minha localização atual
                  </button>
                </div>

                <div>
                  <label className="label-form">Horário de Funcionamento</label>
                  <input name="horario_funcionamento" value={formData.horario_funcionamento || ''} onChange={handleChange} className="input-form" placeholder="Ex: 08:00 - 18:00" />
                </div>
                
                <div>
                  <label className="label-form">Descrição</label>
                  <textarea name="descricao" value={formData.descricao || ''} onChange={handleChange} className="input-form" rows={2} />
                </div>
              </>
            )}

            {/* ================= PRODUTO ================= */}
            {tipo === 'produto' && (
              <>
                <div>
                  <label className="label-form">Nome do Produto *</label>
                  <input name="nome" value={formData.nome || ''} onChange={handleChange} className="input-form" placeholder="Ex: Maçã Gala" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="label-form">Preço (R$) *</label>
                    <input name="preco" type="number" step="0.01" value={formData.preco || ''} onChange={handleChange} className="input-form" placeholder="0.00" />
                  </div>
                  <div>
                    <label className="label-form">ID da Banca *</label>
                    <input name="banca_id" type="number" value={formData.banca_id || ''} onChange={handleChange} className="input-form" placeholder="ID numérico" />
                  </div>
                </div>

                <div>
                  <label className="label-form">URL da Imagem</label>
                  <input name="imagem" value={formData.imagem || ''} onChange={handleChange} className="input-form" placeholder="https://..." />
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-bold text-white transition-all transform active:scale-95 ${
                loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-[var(--color-shop_light_green)] hover:bg-green-600 shadow-md'
              }`}
            >
              {loading ? 'Processando...' : 'Cadastrar'}
            </button>

          </form>
        </div>
      </div>

      <style jsx>{`
        .label-form {
          @apply block text-sm font-semibold text-gray-700 mb-1;
        }
        .input-form {
          @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[var(--color-shop_light_green)] focus:border-transparent outline-none transition-shadow;
        }
      `}</style>
    </div>
  );
}