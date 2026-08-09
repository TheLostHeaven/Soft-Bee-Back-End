from flask import request, jsonify, current_app, g
from http import HTTPStatus
from uuid import UUID
from src.features.maya.presentation.api.v1.endpoints import maya_bp
from src.features.auth.presentation.api.v1.dependencies.auth_deps import token_required


@maya_bp.route("/iniciar-monitoreo", methods=['POST', 'OPTIONS'])
@token_required()
def iniciar_monitoreo():
    """
    Inicia el monitoreo por voz para una colmena.
    Retorna las preguntas activas de la colmena para que el frontend
    las presente al usuario en modo de voz.
    
    Una pregunta se considera activa si está activa tanto a nivel
    de la colmena (HiveQuestion.is_active) como a nivel del apiario
    (ApiaryQuestion.is_active).
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.json
        if not data or 'hive_id' not in data:
            return jsonify({"error": "hive_id es requerido"}), HTTPStatus.BAD_REQUEST

        hive_id = data['hive_id']
        hive_uuid = UUID(hive_id)

        # Obtener las preguntas de la colmena
        get_hive_questions = current_app.container.get_hive_questions_use_case()
        questions = get_hive_questions.execute(hive_uuid)

        # Formatear las preguntas para el monitoreo por voz
        # Una pregunta se considera activa si:
        # 1. HiveQuestion.is_active es True (activa a nivel colmena)
        # 2. ApiaryQuestion.is_active es True (activa a nivel apiario)
        formatted_questions = []
        for q in questions:
            if not q.is_active:
                continue
            if not q.apiary_question:
                continue
            if not q.apiary_question.is_active:
                continue

            question_data = {
                "hive_question_id": str(q.id),
                "question": q.apiary_question.question,
                "category": q.apiary_question.category,
                "type": q.apiary_question.type,
                "display_order": q.display_order,
                "is_required": q.apiary_question.is_required,
                "options": q.apiary_question.options,
                "min_value": q.apiary_question.min_value,
                "max_value": q.apiary_question.max_value,
            }
            formatted_questions.append(question_data)

        # Ordenar por display_order
        formatted_questions.sort(key=lambda x: x['display_order'])

        return jsonify({
            "hive_id": hive_id,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions)
        }), HTTPStatus.OK

    except ValueError as e:
        return jsonify({"error": "hive_id inválido"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@maya_bp.route("/guardar-respuestas", methods=['POST', 'OPTIONS'])
@token_required()
def guardar_respuestas():
    """
    Guarda las respuestas del monitoreo por voz.
    Recibe hive_id y una lista de answers con hive_question_id, answer y score.
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.json
        if not data:
            return jsonify({"error": "Body es requerido"}), HTTPStatus.BAD_REQUEST

        hive_id = data.get('hive_id')
        answers = data.get('answers')

        if not hive_id:
            return jsonify({"error": "hive_id es requerido"}), HTTPStatus.BAD_REQUEST

        if not answers or not isinstance(answers, list):
            return jsonify({"error": "answers debe ser una lista no vacía"}), HTTPStatus.BAD_REQUEST

        # Obtener user_id del contexto de autenticación
        user_id = getattr(g, 'current_user_id', None)

        # Preparar datos para el batch
        answers_data = []
        for ans in answers:
            if 'hive_question_id' not in ans:
                return jsonify({"error": "Cada respuesta debe tener hive_question_id"}), HTTPStatus.BAD_REQUEST

            answers_data.append({
                "hive_question_id": UUID(ans['hive_question_id']),
                "answer": ans.get('answer', ''),
                "score": ans.get('score', 0),
            })

        # Usar el caso de uso existente para guardar en batch
        create_batch = current_app.container.create_answers_batch_use_case()
        created_answers = create_batch.execute(answers_data, UUID(user_id) if user_id else None)

        return jsonify({
            "message": "Respuestas guardadas exitosamente",
            "hive_id": hive_id,
            "saved_count": len(created_answers)
        }), HTTPStatus.CREATED

    except ValueError as e:
        return jsonify({"error": f"Datos inválidos: {str(e)}"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
