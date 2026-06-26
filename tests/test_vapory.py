from unittest.mock import patch

import pytest
from vapory import (
    Scene, Camera, Sphere, Box, LightSource, POVRayElement,
    Background, Pigment, Finish, Texture
)
from vapory.helpers import vectorize

def test_povray_element_str_simple():
    # Test that a simple element produces correct POV-Ray syntax
    sphere = Sphere([0,0,0], 1)
    expected = "sphere {\n<0,0,0>\n1 \n}"
    assert str(sphere) == expected

    # With additional args
    sphere2 = Sphere([1,2,3], 2, 'texture', Texture('pigment', Pigment('color', [1,0,0])))
    # It will format texture as a string; we just check that it's in the output
    out = str(sphere2)
    assert 'sphere {' in out
    assert '<1,2,3>' in out
    assert '2' in out
    assert 'texture' in out

def test_camera():
    cam = Camera('perspective', 'location', [0,0,0], 'look_at', [0,0,1])
    out = str(cam)
    assert 'camera {' in out
    assert 'perspective' in out
    assert 'location' in out
    assert '<0,0,0>' in out
    assert 'look_at' in out
    assert '<0,0,1>' in out

def test_scene_str():
    cam = Camera('perspective', 'location', [0,0,0])
    sphere = Sphere([0,0,0], 1)
    light = LightSource([-10,10,-10], [1,1,1])
    scene = Scene(cam, objects=[sphere], atmospheric=[light])
    out = str(scene)
    # Order: included, declares, objects, camera, atmospheric, global_settings
    # Objects come before camera, so sphere should appear before camera
    assert str(sphere) in out
    assert str(cam) in out
    assert str(light) in out
    # Check that global_settings is present even if empty
    assert 'global_settings{' in out

def test_scene_render(mocker):
    # Mock render_povstring to check it gets correct arguments
    mock_render = mocker.patch('vapory.vapory.render_povstring')
    cam = Camera('perspective')
    scene = Scene(cam)
    scene.render(outfile='test.png', height=100, width=200)
    mock_render.assert_called_once()
    # First arg should be str(scene)
    args = mock_render.call_args[0]
    assert args[0] == str(scene)
    assert args[1] == 'test.png'
    assert args[2] == 100
    assert args[3] == 200
    # other defaults
    assert args[4] is None  # quality
    assert args[5] is None  # antialiasing
    assert args[6] is True  # remove_temp
    assert args[7] is False # show_window
    assert args[8] is None  # tempfile
    assert args[9] is None  # includedirs
    assert args[10] is False # output_alpha

def test_scene_auto_camera_angle():
    # When auto_camera_angle=True and width given, it should add a 'right' argument
    cam = Camera('perspective')
    scene = Scene(cam)
    # Capture the camera after render call
    with patch('vapory.vapory.render_povstring') as mock_render:
        scene.render(height=300, width=400, auto_camera_angle=True)
        # The camera should have an extra arg: ['right', [1.333..., 0, 0]]
        # We can't easily inspect the modified camera, but we can check the string
        # Instead, we check that render_povstring is called with a string that includes 'right'
        call_args = mock_render.call_args[0]
        scene_str = call_args[0]
        assert 'right' in scene_str
        assert '<1.3333333333333333,0,0>' in scene_str or '<1.33333,0,0>' in scene_str

def test_macro():
    from vapory import Macro
    macro = Macro('MyMacro', 1, 2, 'hello')
    assert str(macro) == 'MyMacro( 1 , 2 , hello)'

def test_background():
    bg = Background([1,0,0])
    assert str(bg) == 'background {\n<1,0,0> \n}'

def test_light_source():
    ls = LightSource([0,0,0], [1,1,1])
    assert 'light_source' in str(ls)
    assert '<0,0,0>' in str(ls)
    assert '<1,1,1>' in str(ls)