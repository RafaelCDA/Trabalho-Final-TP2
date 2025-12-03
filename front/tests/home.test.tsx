// EU001 – Teste da Home Page
import { render, screen } from "@testing-library/react";
import Home from "../app/page";
import "@testing-library/jest-dom";
import axios from "axios";

jest.mock("axios");

describe("Home Page", () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Mock da resposta da API usada no useEffect
    (axios.get as jest.Mock).mockResolvedValue({
      data: {
        produtos: [],
        bancas: []
      }
    });
  });

  test("deve exibir o título principal da página", async () => {
    render(<Home />);

    expect(
      await screen.findByRole("heading", {
        name: /garanta 50% de desconto/i
      })
    ).toBeInTheDocument();
  });

  test("deve renderizar a barra de busca", async () => {
    render(<Home />);

    const searchInput = await screen.findByPlaceholderText("Buscar...");
    expect(searchInput).toBeInTheDocument();
  });

  test("deve renderizar as categorias principais", async () => {
    render(<Home />);

    expect(await screen.findByRole("button", { name: /todos/i })).toBeInTheDocument();
    expect(await screen.findByRole("button", { name: /produtos/i })).toBeInTheDocument();
    expect(await screen.findByRole("button", { name: /bancas/i })).toBeInTheDocument();
  });
});
