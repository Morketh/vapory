from vapory import config

def test_povray_binary():
    import os
    if os.name == 'nt':
        assert config.POVRAY_BINARY == 'povray.exe'
    else:
        assert config.POVRAY_BINARY == 'povray'

def test_global_scene_settings():
    settings = config.GLOBAL_SCENE_SETTINGS
    assert 'Radiosity' in settings
    assert settings['Radiosity']['count'] == 35
    assert 'Subsurface' in settings
    assert settings['Subsurface']['samples'] == (50, 50)