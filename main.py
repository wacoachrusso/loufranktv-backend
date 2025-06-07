import pathlib
import dotenv
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware  # Add this import

dotenv.load_dotenv()




# def get_router_config() -> dict:
#     try:
#         # Note: This file is not available to the agent
#         cfg = json.loads(open("routers.json").read())
#     except:
#         return False
#     return cfg


# def is_auth_disabled(router_config: dict, name: str) -> bool:
#     return router_config["routers"][name]["disableAuth"]


def import_api_routers() -> APIRouter:
    """Create top level router including all user defined endpoints."""
    routes = APIRouter(prefix="/routes")

    src_path = pathlib.Path(__file__).parent

    # Import API routers from "src/app/apis/*/__init__.py"
    apis_path = src_path / "app" / "apis"

    api_names = [
        p.relative_to(apis_path).parent.as_posix()
        for p in apis_path.glob("*/__init__.py")
    ]

    api_module_prefix = "app.apis."

    for name in api_names:
        print(f"Importing API: {name}")
        try:
            api_module = __import__(api_module_prefix + name, fromlist=[name])
            api_router = getattr(api_module, "router", None)
            if isinstance(api_router, APIRouter):
                routes.include_router(
                    api_router,
                    # Authentication dependencies removed as requested
                )
            else:
                print(f"API '{name}' does not have a valid APIRouter object.")
        except Exception as e:
            print(f"Error importing API {name}: {e}")
            continue

    print(routes.routes)

    return routes


def create_app() -> FastAPI:
    """Create the app. This is called by uvicorn with the factory option to construct the app object."""
    app = FastAPI()

    # --- ADD THIS CORS CONFIGURATION BLOCK ---
    origins = [
        "http://localhost:5173",  # Your local frontend development server
        "https://www.loufranktv.com", # Your primary live domain
        "https://loufranktv.com",     # Your root live domain (if you use it)
        "https://loufranktv-frontend.netlify.app", # Your Netlify temporary domain
        # Add any other Netlify preview/branch domains if needed, e.g.:
        # "https://your-preview-xxxx.netlify.app",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allows all headers
    )
    # --- END CORS CONFIGURATION BLOCK ---

    app.include_router(import_api_routers())

    for route in app.routes:
        if hasattr(route, "methods"):
            for method in route.methods:
                print(f"{method} {route.path}")

    # Removed DataButton Firebase integration and related auth config logic
    app.state.auth_config = None

    return app


app = create_app()
