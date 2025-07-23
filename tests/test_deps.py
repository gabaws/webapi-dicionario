def test_get_settings():
    from app.api.deps import get_settings
    settings = get_settings()
    assert settings is not None
    assert hasattr(settings, "settings") or hasattr(settings, "__file__") 