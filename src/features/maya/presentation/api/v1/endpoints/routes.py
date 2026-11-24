from flask import request, jsonify, current_app, g
from http import HTTPStatus
from uuid import UUID
from src.features.maya.presentation.api.v1.endpoints import maya_bp
from src.features.auth.presentation.api.v1.dependencies.auth_deps import token_required
from src.features.beehive.presentation.api.v1.schemas.beehive_schemas import BeehiveResponseSchema
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError
from src.features.apiaries.presentation.api.v1.schemas.apiary_schemas import ApiaryResponseSchema
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException


FORBIDDEN_MESSAGE = "No tienes permiso para acceder a este recurso"


def _user_owns_apiary(apiary) -> bool:
    """True si el apiario pertenece al usuario autenticado (token)."""
    current_user_id = getattr(g, 'current_user_id', None)
    return bool(current_user_id) and str(apiary.user_id).lower() == str(current_user_id).lower()


def _check_hive_access(hive_uuid: UUID):
    """
    Verifica que la colmena exista y que su apiario pertenezca al usuario del token.
    Devuelve None si tiene acceso; si no, una tupla (response, status) lista para retornar.
    """
    try:
        hive = current_app.container.get_beehive_by_id_use_case().execute(hive_uuid)
        apiary = current_app.container.get_apiary_by_id_use_case().execute(hive.apiary_id)
    except (BeehiveNotFoundException, ApiaryNotFoundError) as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    if not _user_owns_apiary(apiary):
        return jsonify({"error": FORBIDDEN_MESSAGE}), HTTPStatus.FORBIDDEN
    return None


@maya_bp.route("/apiaries", methods=['GET', 'OPTIONS'])
@token_required()
def obtener_apiarios_del_usuario():
    """
    Devuelve TODOS los apiarios del usuario autenticado, sin paginar.
    El usuario sale del token, no se recibe por parámetro, así que solo se
    pueden consultar apiarios propios. Es el primer paso del monitoreo:
    el usuario elige un apiario y luego se piden sus colmenas con
    GET /api/v1/maya/apiary/<apiary_id>/hives.
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        current_user_id = getattr(g, 'current_user_id', None)
        if not current_user_id:
            return jsonify({"error": FORBIDDEN_MESSAGE}), HTTPStatus.FORBIDDEN

        use_case = current_app.container.get_apiaries_by_user_id_use_case()
        apiaries = use_case.execute(current_user_id)

        return jsonify({
            "apiaries": [ApiaryResponseSchema.model_validate(a).model_dump(mode="json") for a in apiaries],
            "total": len(apiaries)
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@maya_bp.route("/apiary/<uuid:apiary_id>/hives", methods=['GET', 'OPTIONS'])
@token_required()
def obtener_colmenas_del_apiario(apiary_id: UUID):
    """
    Devuelve TODAS las colmenas de un apiario, sin paginar, ordenadas por
    hive_number. Es el punto de entrada del monitoreo, que trabaja a nivel de
    apiario y necesita recorrer todas las colmenas.

    Para listados normales de la app usar GET /api/v1/beehives/apiary/<id>,
    que sí está paginado.
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        # El apiario debe existir y pertenecer al usuario del token
        get_apiary = current_app.container.get_apiary_by_id_use_case()
        apiary = get_apiary.execute(apiary_id)

        if not _user_owns_apiary(apiary):
            return jsonify({"error": FORBIDDEN_MESSAGE}), HTTPStatus.FORBIDDEN

        use_case = current_app.container.get_all_beehives_by_apiary_id_use_case()
        beehives = use_case.execute(apiary_id)

        return jsonify({
            "apiary_id": str(apiary_id),
            "hives": [BeehiveResponseSchema.model_validate(b).model_dump(mode="json") for b in beehives],
            "total": len(beehives)
        }), HTTPStatus.OK

    except ApiaryNotFoundError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


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

        # La colmena debe pertenecer a un apiario del usuario del token
        denied = _check_hive_access(hive_uuid)
        if denied:
            return denied

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

        hive_uuid = UUID(hive_id)

        # Preparar datos para el batch (se valida todo antes de guardar nada)
        answers_data = []
        for ans in answers:
            if 'hive_question_id' not in ans:
                return jsonify({"error": "Cada respuesta debe tener hive_question_id"}), HTTPStatus.BAD_REQUEST

            answers_data.append({
                "hive_question_id": UUID(ans['hive_question_id']),
                "answer": ans.get('answer', ''),
                "score": ans.get('score', 0),
            })

        # La colmena debe pertenecer a un apiario del usuario del token
        denied = _check_hive_access(hive_uuid)
        if denied:
            return denied

        # Cada pregunta debe existir y pertenecer a esa misma colmena
        question_repository = current_app.container.question_repository()
        for item in answers_data:
            hive_question = question_repository.get_hive_question_by_id(item["hive_question_id"])
            if not hive_question:
                return jsonify({"error": f"Pregunta {item['hive_question_id']} no encontrada"}), HTTPStatus.NOT_FOUND
            if str(hive_question.hive_id).lower() != str(hive_uuid).lower():
                return jsonify({"error": FORBIDDEN_MESSAGE}), HTTPStatus.FORBIDDEN

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
