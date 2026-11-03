 SELECT 
        -- pega o ano da data de atualizado_em
        YEAR(atualizado_em) AS ano, 

        -- pega o mes da data de atualizado_em
        MONTH(atualizado_em) AS mes,

        -- pega o valor total
        ROUND(SUM(valor_total) ,2) AS faturamento

        from pedidos 

        where year(atualizado_em) = 2026 
        
        -- agrupa os resultados por ano e mes
        GROUP BY
            YEAR(atualizado_em),
            MONTH(atualizado_em)
        -- ordena o resultado primeiro pelo ano e depois pelo mes
        ORDER BY
            ano,
            mes        
        ;