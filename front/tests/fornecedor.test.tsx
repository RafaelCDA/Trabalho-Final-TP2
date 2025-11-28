import { render, screen } from "@testing-library/react";
import Fornecedor from "../app/fornecedor/page";
import '@testing-library/jest-dom';

describe("Tela de Fornecedor", () => {

  test("deve exibir o título 'Cadastro de Fornecedores'", () => {
    render(<Fornecedor />);

    expect(
      screen.getByRole("heading", { name: /Lista de Fornecedores/i })
    ).toBeInTheDocument();

  });
});
