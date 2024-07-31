from flask import Blueprint, request, jsonify, abort
from sqlalchemy.ext.automap import automap_base
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def new_bp(plugin_folder, core_ep, store_ep, db, Base):
    # Create a new Blueprint
    bp = Blueprint("bp_evaluator", __name__)

    # Function to calculate hash
    def calculate_hash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    # Ensure application context is available
    Evaluations = Base.classes.evaluations

    # Endpoint to submit evaluation request (Client)
    @bp.route("/submit_evaluation", methods=["POST"])
    def submit_evaluation():
        """Create a new evaluation request"""
        print("Headers: ", request.headers)
        print("Body: ", request.get_data(as_text=True))
        print("JSON: ", request.request.get_data(as_text=True).get_json())
        print("Args: ", request.args)
        print("Form: ", request.form)
        print("Files: ", request.files)
        try:
            content = request.json
            print("contrent: ", content)
            
            required_fields = ['client_id', 'data', 'window_size']

            # Validate input data
            for field in required_fields:
                if field not in content:
                    return jsonify({"error": f"Missing field: {field}"}), 400

            client_id = content['client_id']
            data = content['data']  # Expecting data to be a JSON string
            window_size = content['window_size']
            data_hash = calculate_hash(data)  # Calculate hash of the JSON string
            print("Hashes calculated")
            new_evaluation = Evaluations(
                client_id=client_id,
                data=data,  # Store JSON string
                window_size=window_size,
                evaluation_status='pending',
                data_hash=data_hash
            )
            print("Evaluation object created")
            db.session.add(new_evaluation)
            db.session.commit()
            print("Evaluation committed")
            evaluation_id = new_evaluation.id
            return jsonify({"evaluation_id": evaluation_id}), 201
        except Exception as e:
            logger.error(f"Error submitting evaluation: {e}")
            abort(500)

    # Endpoint for evaluator to fetch next pending evaluation
    @bp.route("/fetch_evaluation", methods=["GET"])
    def fetch_evaluation():
        try:
            evaluation = db.session.query(Evaluations).filter_by(evaluation_status='pending').first()
            if evaluation:
                return jsonify({
                    "evaluation_id": evaluation.id,
                    "client_id": evaluation.client_id,
                    "data": evaluation.data,  # Return JSON string
                    "window_size": evaluation.window_size,
                    "data_hash": evaluation.data_hash
                }), 200
            else:
                return jsonify({"message": "No pending evaluations available"}), 204
        except Exception as e:
            logger.error(f"Error fetching evaluation: {e}")
            abort(500)

    # Endpoint for evaluator to submit results
    @bp.route("/submit_result", methods=["POST"])
    def submit_result():
        """Submit the result of an evaluation"""
        try:
            content = request.json
            required_fields = ['evaluation_id', 'json_result', 'data_hash', 'feature_extracted_data_hash', 'feature_extractor_hash', 'champion_genome_hash', 'neat_config_hash']

            # Validate input data
            for field in required_fields:
                if field not in content:
                    return jsonify({"error": f"Missing field: {field}"}), 400

            evaluation_id = content['evaluation_id']
            json_result = content['json_result']  # Expecting result to be a JSON string
            data_hash = content['data_hash']
            feature_extracted_data_hash = content['feature_extracted_data_hash']
            feature_extractor_hash = content['feature_extractor_hash']
            champion_genome_hash = content['champion_genome_hash']
            neat_config_hash = content['neat_config_hash']
            result_hash = calculate_hash(json_result)  # Calculate hash of the JSON string

            evaluation = db.session.query(Evaluations).filter_by(id=evaluation_id).first()

            if not evaluation:
                return jsonify({"error": "Evaluation not found"}), 404

            if evaluation.evaluation_status != 'pending':
                return jsonify({"error": "Evaluation already completed"}), 400

            # TODO: Verify hashes
            #if evaluation.data_hash != data_hash:
            #    return jsonify({"error": "Data hash mismatch"}), 400

            evaluation.json_result = json_result  # Store JSON string
            evaluation.feature_extracted_data_hash = feature_extracted_data_hash
            evaluation.feature_extractor_hash = feature_extractor_hash
            evaluation.champion_genome_hash = champion_genome_hash
            evaluation.neat_config_hash = neat_config_hash
            evaluation.result_hash = result_hash
            evaluation.evaluation_status = 'completed'
            db.session.commit()
            return jsonify({"message": "Result submitted successfully"}), 200
        except Exception as e:
            logger.error(f"Error submitting result: {e}")
            abort(500)

    # Endpoint for client to check evaluation result
    @bp.route("/check_result/<int:evaluation_id>", methods=["GET"])
    def check_result(evaluation_id):
        try:
            evaluation = db.session.query(Evaluations).filter_by(id=evaluation_id).first()

            if not evaluation:
                return jsonify({"error": "Evaluation not found"}), 404

            if evaluation.evaluation_status == 'pending':
                return jsonify({"message": "Evaluation is still pending"}), 202

            return jsonify({
                "json_result": evaluation.json_result,  # Return JSON string
                "result_hash": evaluation.result_hash
            }), 200
        except Exception as e:
            logger.error(f"Error checking result: {e}")
            abort(500)

    return bp
