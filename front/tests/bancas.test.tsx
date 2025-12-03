import { render, screen } from "@testing-library/react";
import Bancas from "../app/bancas/page";
import '@testing-library/jest-dom';

describe("Página de Bancas", () => {
  test("exibe o título principal", () => {
    render(<Bancas />);

    expect(
      screen.getByRole("heading", { name: /Lista de Bancas/i })
    ).toBeInTheDocument();
  });
});
