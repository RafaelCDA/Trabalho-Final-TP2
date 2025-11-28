// EU009, EU010, EU011 - Testes Completos do Formulário de Cadastro
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import FormCadastro from '../components/forms/FormCadastro';
import axios from 'axios';

// Mock do axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('FormCadastro - Testes Completos', () => {
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ===== TESTES DE RENDERIZAÇÃO INICIAL =====
  
  describe('Renderização Inicial', () => {
    it('deve renderizar o formulário com as 3 abas (Fornecedor, Banca, Produto)', () => {
      render(<FormCadastro />);
      
      expect(screen.getByText('Fornecedor')).toBeInTheDocument();
      expect(screen.getByText('Banca')).toBeInTheDocument();
      expect(screen.getByText('Produto')).toBeInTheDocument();
    });

    it('deve renderizar com aba Fornecedor ativa por padrão', () => {
      render(<FormCadastro />);
      
      const fornecedorTab = screen.getByRole('button', { name: /fornecedor/i });
      expect(fornecedorTab).toHaveClass('bg-[var(--color-shop_light_green)]');
    });

    it('deve exibir título correto para cada tipo de cadastro', () => {
      const { rerender } = render(<FormCadastro />);
      expect(screen.getByText(/Cadastro de Fornecedor/i)).toBeInTheDocument();
      
      // Simular clique na aba Banca
      fireEvent.click(screen.getByText('Banca'));
      expect(screen.getByText(/Cadastro de Banca/i)).toBeInTheDocument();
      
      // Simular clique na aba Produto
      fireEvent.click(screen.getByText('Produto'));
      expect(screen.getByText(/Cadastro de Produto/i)).toBeInTheDocument();
    });
  });

  // ===== TESTES DE ALTERNÂNCIA DE ABAS =====
  
  describe('Alternância de Abas', () => {
    it('deve alternar para aba Banca ao clicar', () => {
      render(<FormCadastro />);
      
      const bancaTab = screen.getByRole('button', { name: /banca/i });
      fireEvent.click(bancaTab);
      
      expect(bancaTab).toHaveClass('bg-[var(--color-shop_light_green)]');
      expect(screen.getByLabelText(/Nome da Banca/i)).toBeInTheDocument();
    });

    it('deve alternar para aba Produto ao clicar', () => {
      render(<FormCadastro />);
      
      const produtoTab = screen.getByRole('button', { name: /produto/i });
      fireEvent.click(produtoTab);
      
      expect(produtoTab).toHaveClass('bg-[var(--color-shop_light_green)]');
      expect(screen.getByLabelText(/Nome do Produto/i)).toBeInTheDocument();
    });

    it('deve limpar campos ao trocar de aba', () => {
      render(<FormCadastro />);
      
      // Preencher campo no Fornecedor
      const nomeInput = screen.getByLabelText(/Nome/i);
      fireEvent.change(nomeInput, { target: { value: 'João Silva' } });
      expect(nomeInput).toHaveValue('João Silva');
      
      // Trocar para Banca
      fireEvent.click(screen.getByText('Banca'));
      
      // Voltar para Fornecedor - campo deve estar limpo
      fireEvent.click(screen.getByText('Fornecedor'));
      const novoNomeInput = screen.getByLabelText(/Nome/i);
      expect(novoNomeInput).toHaveValue('');
    });
  });

  // ===== TESTES DE FORMULÁRIO FORNECEDOR (EU009) =====
  
  describe('EU009 - Cadastro de Fornecedor', () => {
    it('deve renderizar todos os campos obrigatórios do fornecedor', () => {
      render(<FormCadastro />);
      
      expect(screen.getByLabelText(/Nome \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Email \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Cidade \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Descrição/i)).toBeInTheDocument();
    });

    it('deve preencher os campos do fornecedor', () => {
      render(<FormCadastro />);
      
      fireEvent.change(screen.getByLabelText(/Nome \*/i), { 
        target: { value: 'Fornecedor Teste' } 
      });
      fireEvent.change(screen.getByLabelText(/Email \*/i), { 
        target: { value: 'teste@fornecedor.com' } 
      });
      fireEvent.change(screen.getByLabelText(/Cidade \*/i), { 
        target: { value: 'Brasília' } 
      });
      
      expect(screen.getByLabelText(/Nome \*/i)).toHaveValue('Fornecedor Teste');
      expect(screen.getByLabelText(/Email \*/i)).toHaveValue('teste@fornecedor.com');
      expect(screen.getByLabelText(/Cidade \*/i)).toHaveValue('Brasília');
    });

    it('deve validar campos obrigatórios do fornecedor', async () => {
      render(<FormCadastro />);
      
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Preencha todos os campos obrigatórios/i)).toBeInTheDocument();
      });
    });

    it('deve enviar dados do fornecedor para API com sucesso', async () => {
      mockedAxios.post.mockResolvedValueOnce({ data: { id: 1, nome: 'Fornecedor Teste' } });
      
      render(<FormCadastro />);
      
      fireEvent.change(screen.getByLabelText(/Nome \*/i), { 
        target: { value: 'Fornecedor Teste' } 
      });
      fireEvent.change(screen.getByLabelText(/Email \*/i), { 
        target: { value: 'teste@fornecedor.com' } 
      });
      fireEvent.change(screen.getByLabelText(/Cidade \*/i), { 
        target: { value: 'Brasília' } 
      });
      
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockedAxios.post).toHaveBeenCalledWith(
          'http://localhost:3000/suppliers',
          expect.objectContaining({
            nome: 'Fornecedor Teste',
            email: 'teste@fornecedor.com',
            cidade: 'Brasília'
          })
        );
      });
      
      expect(screen.getByText(/Fornecedor cadastrado com sucesso/i)).toBeInTheDocument();
    });
  });

  // ===== TESTES DE FORMULÁRIO BANCA (EU010) =====
  
  describe('EU010 - Cadastro de Banca', () => {
    beforeEach(() => {
      render(<FormCadastro />);
      fireEvent.click(screen.getByText('Banca'));
    });

    it('deve renderizar todos os campos obrigatórios da banca', () => {
      expect(screen.getByLabelText(/Nome da Banca \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Endereço \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Latitude \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Longitude \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Horário Abertura \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Horário Fechamento \*/i)).toBeInTheDocument();
    });

    it('deve preencher os campos da banca', () => {
      fireEvent.change(screen.getByLabelText(/Nome da Banca \*/i), { 
        target: { value: 'Banca do João' } 
      });
      fireEvent.change(screen.getByLabelText(/Endereço \*/i), { 
        target: { value: 'SQN 308, Brasília' } 
      });
      fireEvent.change(screen.getByLabelText(/Latitude \*/i), { 
        target: { value: '-15.7801' } 
      });
      fireEvent.change(screen.getByLabelText(/Longitude \*/i), { 
        target: { value: '-47.9292' } 
      });
      
      expect(screen.getByLabelText(/Nome da Banca \*/i)).toHaveValue('Banca do João');
      expect(screen.getByLabelText(/Latitude \*/i)).toHaveValue(-15.7801);
    });

    it('deve validar campos obrigatórios da banca', async () => {
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Preencha todos os campos obrigatórios/i)).toBeInTheDocument();
      });
    });

    it('deve enviar dados da banca para API com sucesso', async () => {
      mockedAxios.post.mockResolvedValueOnce({ data: { id: 1, nome: 'Banca do João' } });
      
      fireEvent.change(screen.getByLabelText(/Nome da Banca \*/i), { 
        target: { value: 'Banca do João' } 
      });
      fireEvent.change(screen.getByLabelText(/Endereço \*/i), { 
        target: { value: 'SQN 308' } 
      });
      fireEvent.change(screen.getByLabelText(/Latitude \*/i), { 
        target: { value: '-15.7801' } 
      });
      fireEvent.change(screen.getByLabelText(/Longitude \*/i), { 
        target: { value: '-47.9292' } 
      });
      fireEvent.change(screen.getByLabelText(/Horário Abertura \*/i), { 
        target: { value: '08:00' } 
      });
      fireEvent.change(screen.getByLabelText(/Horário Fechamento \*/i), { 
        target: { value: '18:00' } 
      });
      
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockedAxios.post).toHaveBeenCalledWith(
          'http://localhost:3000/bancas',
          expect.objectContaining({
            nome: 'Banca do João',
            endereco: 'SQN 308',
            latitude: -15.7801,
            longitude: -47.9292
          })
        );
      });
      
      expect(screen.getByText(/Banca cadastrada com sucesso/i)).toBeInTheDocument();
    });
  });

  // ===== TESTES DE FORMULÁRIO PRODUTO (EU011) =====
  
  describe('EU011 - Cadastro de Produto', () => {
    beforeEach(() => {
      render(<FormCadastro />);
      fireEvent.click(screen.getByText('Produto'));
    });

    it('deve renderizar todos os campos obrigatórios do produto', () => {
      expect(screen.getByLabelText(/Nome do Produto \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Descrição \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Preço \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Categoria \*/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Unidade de Medida \*/i)).toBeInTheDocument();
    });

    it('deve preencher os campos do produto', () => {
      fireEvent.change(screen.getByLabelText(/Nome do Produto \*/i), { 
        target: { value: 'Notebook Dell' } 
      });
      fireEvent.change(screen.getByLabelText(/Descrição \*/i), { 
        target: { value: 'Notebook i5 8GB RAM' } 
      });
      fireEvent.change(screen.getByLabelText(/Preço \*/i), { 
        target: { value: '2500.00' } 
      });
      
      expect(screen.getByLabelText(/Nome do Produto \*/i)).toHaveValue('Notebook Dell');
      expect(screen.getByLabelText(/Preço \*/i)).toHaveValue(2500);
    });

    it('deve validar campos obrigatórios do produto', async () => {
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Preencha todos os campos obrigatórios/i)).toBeInTheDocument();
      });
    });

    it('deve enviar dados do produto para API com sucesso', async () => {
      mockedAxios.post.mockResolvedValueOnce({ data: { id: 1, description: 'Notebook Dell' } });
      
      fireEvent.change(screen.getByLabelText(/Nome do Produto \*/i), { 
        target: { value: 'Notebook Dell' } 
      });
      fireEvent.change(screen.getByLabelText(/Descrição \*/i), { 
        target: { value: 'Notebook i5' } 
      });
      fireEvent.change(screen.getByLabelText(/Preço \*/i), { 
        target: { value: '2500.00' } 
      });
      fireEvent.change(screen.getByLabelText(/Categoria \*/i), { 
        target: { value: 'Eletrodomésticos' } 
      });
      fireEvent.change(screen.getByLabelText(/Unidade de Medida \*/i), { 
        target: { value: 'unidade' } 
      });
      
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(mockedAxios.post).toHaveBeenCalledWith(
          'http://localhost:3000/produtos',
          expect.objectContaining({
            description: 'Notebook i5',
            price_in: 2500,
            category: 'Eletrodomésticos'
          })
        );
      });
      
      expect(screen.getByText(/Produto cadastrado com sucesso/i)).toBeInTheDocument();
    });
  });

  // ===== TESTES DE TRATAMENTO DE ERROS =====
  
  describe('Tratamento de Erros', () => {
    it('deve exibir mensagem de erro quando API falhar', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Erro na API'));
      
      render(<FormCadastro />);
      
      fireEvent.change(screen.getByLabelText(/Nome \*/i), { 
        target: { value: 'Teste' } 
      });
      fireEvent.change(screen.getByLabelText(/Email \*/i), { 
        target: { value: 'teste@email.com' } 
      });
      fireEvent.change(screen.getByLabelText(/Cidade \*/i), { 
        target: { value: 'Brasília' } 
      });
      
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Erro ao cadastrar/i)).toBeInTheDocument();
      });
    });

    it('deve desabilitar botão durante envio', async () => {
      mockedAxios.post.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
      
      render(<FormCadastro />);
      
      fireEvent.change(screen.getByLabelText(/Nome \*/i), { 
        target: { value: 'Teste' } 
      });
      fireEvent.change(screen.getByLabelText(/Email \*/i), { 
        target: { value: 'teste@email.com' } 
      });
      fireEvent.change(screen.getByLabelText(/Cidade \*/i), { 
        target: { value: 'Brasília' } 
      });
      
      const submitButton = screen.getByRole('button', { name: /Cadastrar/i });
      fireEvent.click(submitButton);
      
      expect(submitButton).toBeDisabled();
      expect(screen.getByText(/Cadastrando.../i)).toBeInTheDocument();
    });
  });
});