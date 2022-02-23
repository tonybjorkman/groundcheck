== Testing ==

Make sure the python virtual environment is active

For running tests in all files starting named 'test_*' and testmethods named 'test_*':
`pytest -s`


For running single test method in specific file:
`pytest test_all.py::test_bouncer_tcp_response -s  `
