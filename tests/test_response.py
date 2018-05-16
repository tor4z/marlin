from marlin.response import raw_response_to_header_body


def test_split_rawdata():
    with open("test_response.txt", "rb") as fp:
        rawdata = fp.read()
    header, body = raw_response_to_header_body(rawdata)
    assert header is not None
    assert body is not None
