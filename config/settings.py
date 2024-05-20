# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SET_NUM_DRIVER_TO_SCAN: int = 6
    SET_NUM_DRIVER_TO_GET_MAX_SPEED: int = 3
    DEFAULT_SPEED: int = 60
    KEY_GRAPH: list[str] = [
        "0dc4f299-a491-452f-97e0-515c296c9453",
        "LijBPDQGfu7Iiq80w3HzwB4RUDJbMbhs6BU0dEnn",
        "a948c182-388d-48eb-889f-01131bbce681",
        "8fcdb3be-5de1-46db-b97f-a76370ca35b8",
        "a3d9f382-aa47-49b2-bcc2-fda39e4c1dcc"
    ]

    class Config:
        env_file = ".env"
