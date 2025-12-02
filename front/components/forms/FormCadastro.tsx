// EU009, EU010, EU011 - Formulário Único de Cadastro
'use client';

import { useState } from 'react';
import axios from 'axios';

type TipoCadastro = 'fornecedor' | 'banca' | 'produto';

interface FormData {
  // Fornecedor (EU009)
  nome?: string;
  email?: string;
  cidade?: string;
  descricao?: string;
  
  // Banca (EU010)
  endereco?: string;
  latitude?: string;
  longitude?: string;
  horario_abertura?: string;
  horario_fechamento?: string;
  fornecedor_id?: string;
  
  // Produto (EU011)
  description?: string;
  price_in?: string;
  category?: string;
  unit_of_measurement?: string;
  bar_shelf_id?: string;
}

export default function FormCadastro() {
  const [tipo, setTipo] = useState<TipoCadastro>('fornecedor');
  const [formData, setFormData] = useState<FormData>({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleTipoChange = (novoTipo: TipoCadastro) => {
    setTipo(novoTipo);
    setFormData({}); // Limpa campos ao trocar de aba
    setMessage({ type: '', text: '' });
  };

  const validarCampos = (): boolean => {
    if (tipo === 'fornecedor') {
      return !!(formData.nome && formData.email && formData.cidade);
    } else if (tipo === 'banca') {
      return !!(
        formData.nome && 
        formData.endereco && 
        formData.latitude && 
        formData.longitude && 
        formData.horario_abertura && 
        formData.horario_fechamento
      );
    } else if (tipo === 'produto') {
      return !!(
        formData.description && 
        formData.price_in && 
        formData.category && 
        formData.unit_of_measurement
      );
    }
    return false;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validarCampos()) {
      setMessage({ type: 'error', text: 'Preencha todos os campos obrigatórios' });
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      let endpoint = '';
      let data = {};

      if (tipo === 'fornecedor') {
        endpoint = 'http://localhost:3000/suppliers';
        data = {
          nome: formData.nome,
          email: formData.email,
          cidade: formData.cidade,
          descricao: formData.descricao || ''
        };
      } else if (tipo === 'banca') {
        endpoint = 'http://localhost:3000/bancas';
        data = {
          nome: formData.nome,
          descricao: formData.descricao || '',
          endereco: formData.endereco,
          latitude: parseFloat(formData.latitude!),
          longitude: parseFloat(formData.longitude!),
          horario_abertura: formData.horario_abertura,
          horario_fechamento: formData.horario_fechamento,
          fornecedor_id: formData.fornecedor_id ? parseInt(formData.fornecedor_id) : undefined
        };
      } else if (tipo === 'produto') {
        endpoint = 'http://localhost:3000/produtos';
        data = {
              nome: formData.nome,
          description: formData.description,
          price_in: parseFloat(formData.price_in!),
          category: formData.category,
          unit_of_measurement: formData.unit_of_measurement,
          bar_shelf_id: formData.bar_shelf_id ? parseInt(formData.bar_shelf_id) : undefined
        };
      }

      await axios.post(endpoint, data);

      const mensagens = {
        fornecedor: 'Fornecedor cadastrado com sucesso!',
        banca: 'Banca cadastrada com sucesso!',
        produto: 'Produto cadastrado com sucesso!'
      };

      setMessage({ type: 'success', text: mensagens[tipo] });
      setFormData({});
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Erro ao cadastrar. Tente novamente.' 
      });
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
          setMessage({ type: 'success', text: 'Localização obtida com sucesso!' });
        },
        () => {
          setMessage({ type: 'error', text: 'Erro ao obter localização' });
        }
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow-md rounded-lg p-8">
          
          {/* Tabs */}
          <div className="flex gap-2 mb-8">
            <button
              role="button"
              onClick={() => handleTipoChange('fornecedor')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
                tipo === 'fornecedor'
                  ? 'bg-[var(--color-shop_light_green)] text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Fornecedor
            </button>
            <button
              role="button"
              onClick={() => handleTipoChange('banca')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
                tipo === 'banca'
                  ? 'bg-[var(--color-shop_light_green)] text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Banca
            </button>
            <button
              role="button"
              onClick={() => handleTipoChange('produto')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
                tipo === 'produto'
                  ? 'bg-[var(--color-shop_light_green)] text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Produto
            </button>
          </div>

          {/* Título */}
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            {tipo === 'fornecedor' && 'Cadastro de Fornecedor'}
            {tipo === 'banca' && 'Cadastro de Banca'}
            {tipo === 'produto' && 'Cadastro de Produto'}
          </h1>

          {/* Mensagens */}
          {message.text && (
            <div
              className={`mb-6 p-4 rounded-md ${
                message.type === 'success'
                  ? 'bg-green-50 text-green-800 border border-green-200'
                  : 'bg-red-50 text-red-800 border border-red-200'
              }`}
            >
              {message.text}
            </div>
          )}

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* FORNECEDOR (EU009) */}
            {tipo === 'fornecedor' && (
              <>
                <div>
                  <label htmlFor="nome" className="block text-sm font-medium text-gray-700 mb-2">
                    Nome *
                  </label>
                  <input
                    type="text"
                    id="nome"
                    name="nome"
                    value={formData.nome || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Nome do fornecedor"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="email@exemplo.com"
                  />
                </div>

                <div>
                  <label htmlFor="cidade" className="block text-sm font-medium text-gray-700 mb-2">
                    Cidade *
                  </label>
                  <input
                    type="text"
                    id="cidade"
                    name="cidade"
                    value={formData.cidade || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Cidade do fornecedor"
                  />
                </div>

                <div>
                  <label htmlFor="descricao" className="block text-sm font-medium text-gray-700 mb-2">
                    Descrição
                  </label>
                  <textarea
                    id="descricao"
                    name="descricao"
                    value={formData.descricao || ''}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Descrição do fornecedor"
                  />
                </div>
              </>
            )}

            {/* BANCA (EU010) */}
            {tipo === 'banca' && (
              <>
                <div>
                  <label htmlFor="nome" className="block text-sm font-medium text-gray-700 mb-2">
                    Nome da Banca *
                  </label>
                  <input
                    type="text"
                    id="nome"
                    name="nome"
                    value={formData.nome || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Nome da banca"
                  />
                </div>

                <div>
                  <label htmlFor="endereco" className="block text-sm font-medium text-gray-700 mb-2">
                    Endereço *
                  </label>
                  <input
                    type="text"
                    id="endereco"
                    name="endereco"
                    value={formData.endereco || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Endereço completo"
                  />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <label className="block text-sm font-medium text-gray-700">
                      Localização GPS *
                    </label>
                    <button
                      type="button"
                      onClick={obterLocalizacao}
                      className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                    >
                      📍 Obter localização atual
                    </button>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="latitude" className="block text-xs text-gray-600 mb-1">
                        Latitude *
                      </label>
                      <input
                        type="number"
                        step="any"
                        id="latitude"
                        name="latitude"
                        value={formData.latitude || ''}
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="-15.7801"
                      />
                    </div>
                    <div>
                      <label htmlFor="longitude" className="block text-xs text-gray-600 mb-1">
                        Longitude *
                      </label>
                      <input
                        type="number"
                        step="any"
                        id="longitude"
                        name="longitude"
                        value={formData.longitude || ''}
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="-47.9292"
                      />
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="horario_abertura" className="block text-sm font-medium text-gray-700 mb-2">
                      Horário Abertura *
                    </label>
                    <input
                      type="time"
                      id="horario_abertura"
                      name="horario_abertura"
                      value={formData.horario_abertura || ''}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label htmlFor="horario_fechamento" className="block text-sm font-medium text-gray-700 mb-2">
                      Horário Fechamento *
                    </label>
                    <input
                      type="time"
                      id="horario_fechamento"
                      name="horario_fechamento"
                      value={formData.horario_fechamento || ''}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="descricao" className="block text-sm font-medium text-gray-700 mb-2">
                    Descrição
                  </label>
                  <textarea
                    id="descricao"
                    name="descricao"
                    value={formData.descricao || ''}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Descrição da banca"
                  />
                </div>
              </>
            )}

            {/* PRODUTO (EU011) */}
            {tipo === 'produto' && (
            <>
                <div>
                <label htmlFor="nome" className="block text-sm font-medium text-gray-700 mb-2">
                    Nome do Produto *
                </label>
                <input
                    type="text"
                    id="nome"
                    name="nome"
                    value={formData.nome || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Nome do produto"
                />
                </div>

                <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                    Descrição *
                </label>
                <textarea
                    id="description"
                    name="description"
                    value={formData.description || ''}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Descrição detalhada do produto"
                />
                </div>

                <div>
                <label htmlFor="price_in" className="block text-sm font-medium text-gray-700 mb-2">
                    Preço *
                </label>
                <input
                    type="number"
                    step="0.01"
                    id="price_in"
                    name="price_in"
                    value={formData.price_in || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="0.00"
                />
                </div>

                <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                    Categoria *
                </label>
                <select
                    id="category"
                    name="category"
                    value={formData.category || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                    <option value="">Selecione uma categoria</option>
                    <option value="Dispositivos">Dispositivos</option>
                    <option value="Eletrodomésticos">Eletrodomésticos</option>
                    <option value="Refrigeradores">Refrigeradores</option>
                    <option value="Outros">Outros</option>
                </select>
                </div>

                <div>
                <label htmlFor="unit_of_measurement" className="block text-sm font-medium text-gray-700 mb-2">
                    Unidade de Medida *
                </label>
                <input
                    type="text"
                    id="unit_of_measurement"
                    name="unit_of_measurement"
                    value={formData.unit_of_measurement || ''}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Ex: unidade, kg, litro"
                />
                </div>
            </>
            )}


            {/* Botão Submit */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-md font-medium text-white transition-colors ${
                loading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-[var(--color-shop_light_green)] hover:bg-green-600'
              }`}
            >
              {loading ? 'Cadastrando...' : 'Cadastrar'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}