// EU001 – Teste do título da Home
import { render, screen } from "@testing-library/react";
import Home from "@/app/page";
import '@testing-library/jest-dom';

describe("Home Page", () => {
  test("exibe o título principal", () => {
    render(<Home />);

    expect(
      screen.getByRole("heading", { name: /bem-vindo/i })
    ).toBeInTheDocument();
  });
});
