-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 12-Fev-2025 às 19:58
-- Versão do servidor: 10.4.27-MariaDB
-- versão do PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `sistema_teste`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `cotas`
--

CREATE TABLE `cotas` (
  `id` int(11) NOT NULL,
  `produto_id` int(11) NOT NULL,
  `fornecedor_id` int(11) NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  `quantidade` decimal(10,2) NOT NULL,
  `data_cotacao` date NOT NULL,
  `rel_un_peso` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `cotas`
--

INSERT INTO `cotas` (`id`, `produto_id`, `fornecedor_id`, `preco_unitario`, `quantidade`, `data_cotacao`, `rel_un_peso`) VALUES
(1, 1, 1, '4.50', '50.00', '2024-09-15', 0),
(2, 1, 2, '5.00', '50.00', '2024-09-15', 0),
(3, 2, 2, '10.90', '20.00', '2024-09-15', 0),
(4, 3, 3, '15.00', '10.00', '2024-09-15', 0),
(5, 1, 1, '4.50', '50.00', '2024-09-15', 0),
(7, 2, 2, '10.90', '20.00', '2024-09-15', 0),
(8, 3, 3, '15.00', '10.00', '2024-09-15', 0),
(9, 1, 2, '4.00', '50.00', '2024-10-20', 0),
(10, 2, 2, '20.00', '50.00', '2024-11-05', 0),
(11, 14, 2, '20.00', '5.00', '2024-12-03', 200),
(12, 2, 6, '120.00', '20.00', '2024-12-03', 3000);

-- --------------------------------------------------------

--
-- Estrutura da tabela `produtos`
--

CREATE TABLE `produtos` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `data_criacao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `produtos`
--

INSERT INTO `produtos` (`id`, `nome`, `categoria`, `data_criacao`) VALUES
(1, 'Maçã', 'Verduras', '2024-09-18 01:39:26'),
(2, 'Frango', 'Carnes', '2024-09-18 01:39:26'),
(3, 'Sabão em Pó', 'Limpeza', '2024-09-18 01:39:26'),
(7, 'Absorvente', 'Higiene Pessoal', '2024-11-06 11:37:29'),
(8, 'Achocolatado em pó', 'Alimenticios', '2024-11-06 11:42:20'),
(9, 'Creme Dental', 'Higiene Pessoal', '2024-11-06 11:43:36'),
(10, 'Detergente', 'Limpeza', '2024-11-06 11:44:02'),
(11, 'Farinha de Trigo', 'Alimenticios', '2024-11-06 11:44:20'),
(12, 'Mussarela', 'Frios', '2024-11-06 11:44:47'),
(13, 'Pães Frances', 'Outros', '2024-11-06 11:45:33'),
(14, 'Banana', 'Frutas', '2024-11-06 11:46:58');

-- --------------------------------------------------------

--
-- Estrutura da tabela `totalidade_produtos`
--

CREATE TABLE `totalidade_produtos` (
  `id` int(11) NOT NULL,
  `produto_id` int(11) DEFAULT NULL,
  `nome_produto` varchar(255) DEFAULT NULL,
  `categoria_produto` varchar(255) DEFAULT NULL,
  `preco_unitario` decimal(10,2) DEFAULT NULL,
  `quantidade` int(11) DEFAULT NULL,
  `data_cotacao` date DEFAULT NULL,
  `preco_total` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `totalidade_produtos`
--

INSERT INTO `totalidade_produtos` (`id`, `produto_id`, `nome_produto`, `categoria_produto`, `preco_unitario`, `quantidade`, `data_cotacao`, `preco_total`) VALUES
(1, 1, 'Maçã', 'Verduras', '4.50', 50, '2024-09-15', '225.00'),
(2, 1, 'Maçã', 'Verduras', '5.00', 50, '2024-09-15', '250.00'),
(3, 2, 'Frango', 'Carnes', '10.90', 20, '2024-09-15', '218.00'),
(4, 3, 'Sabão em Pó', 'Limpeza', '15.00', 10, '2024-09-15', '150.00'),
(5, 1, 'Maçã', 'Verduras', '4.50', 50, '2024-09-15', '225.00'),
(6, 2, 'Frango', 'Carnes', '10.90', 20, '2024-09-15', '218.00'),
(7, 3, 'Sabão em Pó', 'Limpeza', '15.00', 10, '2024-09-15', '150.00'),
(8, 1, 'Maçã', 'Verduras', '4.00', 50, '2024-10-20', '200.00'),
(9, 2, 'Frango', 'Carnes', '20.00', 50, '2024-11-05', '1000.00'),
(10, 14, 'Banana', 'Frutas', '20.00', 5, '2024-12-03', '100.00'),
(11, 2, 'Frango', 'Carnes', '120.00', 20, '2024-12-03', '2400.00');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `cotas`
--
ALTER TABLE `cotas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `produto_id` (`produto_id`),
  ADD KEY `fornecedor_id` (`fornecedor_id`);

--
-- Índices para tabela `produtos`
--
ALTER TABLE `produtos`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `totalidade_produtos`
--
ALTER TABLE `totalidade_produtos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `cotas`
--
ALTER TABLE `cotas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `produtos`
--
ALTER TABLE `produtos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de tabela `totalidade_produtos`
--
ALTER TABLE `totalidade_produtos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `cotas`
--
ALTER TABLE `cotas`
  ADD CONSTRAINT `cotas_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cotas_ibfk_2` FOREIGN KEY (`fornecedor_id`) REFERENCES `fornecedores` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
