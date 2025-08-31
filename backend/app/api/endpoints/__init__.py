from .predict import router as predict_router
from .alerts import router as alerts_router
from .data import router as data_router
from .evacuation import router as evacuation_router
from .auth import router as auth_router

__all__ = ["predict_router", "alerts_router", "data_router", "evacuation_router", "auth_router"]