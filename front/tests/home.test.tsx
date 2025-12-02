// EU001 – Teste do título da Home
import { render, screen } from "@testing-library/react";
import Home from "./../app/page";
import '@testing-library/jest-dom';


// jest.mock("axios");    //Precisa mockar o axios para nao ficar poluido na saida(por ultimo)
describe("Home Page", () => {
  test("exibe o título principal", () => {
    render(<Home />);

    expect(
    screen.getByRole("heading", { name: /Garanta 50% de desconto/i })
    ).toBeInTheDocument();

  });
});
