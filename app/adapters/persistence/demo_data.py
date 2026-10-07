def enderecos_de_demonstracao() -> list[dict[str, str]]:
    bairros = ["Centro", "Jardim das Flores", "Vila Nova", "Parque Central", "Boa Vista"]
    return [
        {
            "cep": f"01001{index:03d}",
            "logradouro": f"Rua de Demonstracao {index + 1}",
            "bairro": bairros[index % len(bairros)],
            "cidade": "Cidade Exemplo",
            "uf": "SP",
        }
        for index in range(50)
    ]