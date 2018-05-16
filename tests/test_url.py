from marlin.util.url import scheme_to_port


def test_schema_to_port():
    schemes = {"http": 80, "https": 443}
    for scheme in schemes:
        port = scheme_to_port(scheme)
        assert port == schemes[scheme]
