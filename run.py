from app import create_app
import click

app = create_app()

@app.cli.command("list-routes")
def list_routes():
    """Lista todas las rutas registradas en la aplicación."""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = f"{rule.endpoint:50s} {methods:20s} {rule}"
        output.append(line)
    
    for line in sorted(output):
        print(line)

if __name__ == '__main__':
    # Utilizar el servidor de producción en lugar del servidor de desarrollo para mejor rendimiento
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True)

# if __name__ == '__main__':
#     app.run(debug=True)


# @app.cli.command("init-db")
# def init_db():
#     with app.app_context():
#         # Obtiene una conexión del engine
#         with db.engine.connect() as connection:
#             # Verifica si la tabla Usuario ya existe en PostgreSQL
#             result = connection.execute(text("SELECT to_regclass('public.usuario');"))
#             table_exists = result.first()[0] is not None

#             if not table_exists:
#                 db.drop_all()  # Esto eliminará todas las tablas existentes, ¡ten cuidado!
#                 db.create_all()
#                 print("Base de datos inicializada y tabla Usuario creada.")
#             else:
#                 print("La tabla Usuario ya existe.")



# @app.cli.command("create-test-user")
# @with_appcontext
# def create_test_user():
#     """Crea un usuario de prueba en la base de datos."""
#     from app.models import Usuario
#     if not Usuario.query.first():
#         user = Usuario(username="testuser", email="test@example.com")
#         user.set_password("testpassword")
#         db.session.add(user)
#         db.session.commit()
#         click.echo("Usuario de prueba creado.")
#     else:
#         click.echo("Ya existe un usuario en la base de datos.")


# @app.cli.command("check-db")
# @with_appcontext
# def check_db():
#     """Verifica la conexión a la base de datos y muestra las tablas."""
#     try:
#         # Intenta hacer una consulta simple
#         result = db.session.execute(text('SELECT 1'))
#         print("Conexión a la base de datos exitosa.")
#         print(f"Resultado de la consulta: {result.scalar()}")
        
#         # Muestra las tablas en la base de datos
#         inspector = db.inspect(db.engine)
#         tables = inspector.get_table_names()
#         print("Tablas en la base de datos:")
#         for table in tables:
#             print(f" - {table}")
            
#         # Muestra los usuarios (si existen)
#         users = Usuario.query.all()
#         if users:
#             print("\nUsuarios en la base de datos:")
#             for user in users:
#                 print(f" - {user.username} (ID: {user.id}, Email: {user.email})")
#         else:
#             print("\nNo hay usuarios en la base de datos.")
            
#     except Exception as e:
#         print(f"Error al conectar a la base de datos: {e}")





# import psycopg2

# @app.cli.command("psycopg2-check")
# def psycopg2_check():
#     try:
#         conn = psycopg2.connect(
#             dbname="testpsico",
#             user="testpsico_owner",
#             password="djopIrOs91vC",
#             host="ep-crimson-queen-a4isq2wz.us-east-1.aws.neon.tech",
#             sslmode='require'
#         )
#         print("Conexión exitosa usando psycopg2")
#         conn.close()
#     except Exception as e:
#         print(f"Error al conectar usando psycopg2: {e}")