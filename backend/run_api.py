from api.app import create_app

api = create_app()

api.run(host="0.0.0.0", port=9000, load_dotenv=False)