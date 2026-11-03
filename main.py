from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from datetime import date
from database import get_db_connection

app = FastAPI(
    title="API de Calendário de Corridas",
    description="API para gerenciar e buscar provas de corrida de rua.",
    version="1.0.0"
)

@app.get("/provas", summary="Listar e filtrar provas de corrida")
def listar_provas(
    cidade_id: Optional[int] = Query(None, description="Filtrar por ID da cidade específica"),
    estado_id: Optional[int] = Query(None, description="Filtrar por ID do estado"),
    apenas_capitais: Optional[bool] = Query(True, description="Se True, traz apenas provas nas capitais"),
    data_inicio: Optional[date] = Query(None, description="Filtrar a partir desta data (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(None, description="Filtrar até esta data (YYYY-MM-DD)")
):
    conn = get_db_connection()
    cursor = conn.cursor()

       try:
        query = """
            SELECT 
                p.id,
                p.nome AS prova_nome,
                p.data_hora,
                p.local_descricao,
                p.distancias,
                p.faixa_preco_inferior,
                p.link_inscricao,
                p.status,
                c.id AS cidade_id,
                c.nome AS cidade_nome,
                c.capital,
                e.sigla AS estado_sigla
            FROM provas p
            JOIN cidades c ON p.cidade_id =c.id
            JOIN estados e ON c.estado_id =e.id
            WHERE p.data_hora >= NOW()
        """
        
        # ADICIONAR ESTA LINHA QUE ESTAVA EM FALTA:
        params = []

        if apenas_capitais is True and cidade_id is None:
            query += " AND c.capital = TRUE"

        if cidade_id is not None:
            query += " AND p.cidade_id = %s"
            params.append(cidade_id)

        if estado_id is not None:
            query += " AND c.estado_id = %s"
            params.append(estado_id)

        if data_inicio is not None:
            query += " AND p.data_hora >= %s"
            params.append(data_inicio)

        if data_fim is not None:
            query += " AND p.data_hora <= %s"
            params.append(data_fim)

        query += " ORDER BY p.data_hora ASC;"

        cursor.execute(query, tuple(params))
        provas = cursor.fetchall()

        return {
            "total": len(provas),
            "provas": provas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
