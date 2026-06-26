import pytest
from unittest.mock import MagicMock, Mock, patch, mock_open
from vapory.io import render_povstring, ppm_to_numpy

def test_render_povstring_without_numpy():
    with patch('vapory.io.numpy_found', True), \
         patch('vapory.io.numpy') as mock_np, \
         patch('vapory.io.subprocess.Popen') as mock_popen, \
         patch('vapory.io.os.remove') as mock_remove, \
         patch('builtins.open', mock_open()):

        process_mock = Mock()
        process_mock.communicate.return_value = (b'P5\n2 2\n255\n\x00\x00\x00\x01\x01\x01', b'')
        process_mock.returncode = 0
        mock_popen.return_value = process_mock

        # Create a mock numpy array that has .reshape()
        mock_array = MagicMock()
        mock_array.reshape.return_value = [[[0,0,0],[1,1,1]]]  # whatever shape
        mock_np.frombuffer.return_value = mock_array
        mock_np.uint8 = 'uint8'

        _result = render_povstring("scene", height=100, width=200)

        # Verify reshape was called with correct dimensions
        mock_array.reshape.assert_called_once_with((2, 2, 3))
        mock_remove.assert_called_once()

def test_render_povstring_output_file():
    with patch('vapory.io.subprocess.Popen') as mock_popen, \
         patch('vapory.io.os.remove') as mock_remove, \
         patch('builtins.open', mock_open()):
        process_mock = Mock()
        process_mock.communicate.return_value = (b'', b'')
        process_mock.returncode = 0
        mock_popen.return_value = process_mock

        render_povstring("scene", outfile='output.png', height=300)

        cmd_args = mock_popen.call_args[0][0]
        assert 'Output_File_Type=N' in cmd_args
        assert '+Ooutput.png' in cmd_args
        mock_remove.assert_called_once()

def test_render_povstring_ipython():
    with patch('vapory.io.ipython_found', True), \
         patch('vapory.io.Image') as mock_image, \
         patch('vapory.io.subprocess.Popen') as mock_popen, \
         patch('vapory.io.os.remove') as mock_remove, \
         patch('builtins.open', mock_open()):

        process_mock = Mock()
        process_mock.communicate.return_value = (b'', b'')
        process_mock.returncode = 0
        mock_popen.return_value = process_mock

        render_povstring("scene", outfile='ipython')

        mock_image.assert_called_once_with('__temp_ipython__.png')
        mock_remove.assert_called_once()

def test_ppm_to_numpy_with_buffer():
    header = b'P6\n2 2\n255\n'
    data = b'\x00\x00\x00\x01\x01\x01\x02\x02\x02\x03\x03\x03'
    buffer = header + data

    with patch('vapory.io.numpy_found', True), \
         patch('vapory.io.numpy') as mock_np:
        mock_array = MagicMock()
        mock_array.reshape.return_value = None
        mock_np.frombuffer.return_value = mock_array
        mock_np.uint8 = 'uint8'

        _result = ppm_to_numpy(buffer=buffer)

        # Verify reshape with correct shape
        mock_array.reshape.assert_called_once_with((2, 2, 3))