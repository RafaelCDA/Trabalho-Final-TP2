import { render, screen } from "@testing-library/react";
import Produtos from "../app/produtos/page";
import '@testing-library/jest-dom';

describe("Página de Produtos", () => {
  test("exibe o título principal", () => {
    render(<Produtos />);

    expect(
      screen.getByRole("heading", { name: /Lista de Produtos/i })
    ).toBeInTheDocument();
  });
});
