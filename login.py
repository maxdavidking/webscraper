from lxml import html
import requests


def main():
    print "Running..."
    # Set up requests session
    client = requests.session()
    # Get csrf_token
    csrf_token = get_csrf(client)
    # Login with csrf_token
    data = login(client, csrf_token)
    tree = html.fromstring(data.content)
    # Output data as list of dicts
    headers = parse_headers(client, data, tree)
    parse_data(client, data, headers, tree)


def get_csrf(session):
    url = "http://quovotest.pythonanywhere.com"
    get_response = session.get(url)

    # Xpath to get csrf_token
    tree = html.fromstring(get_response.content)
    csrf = tree.xpath("//input[@name='csrf_token']/@value")
    return csrf


def login(session, csrf_token):
    # Pass that csrf_token value into the payload
    payload = {
        "email": "quovo@quovo.com",
        "password": "quovoquovo",
        "csrf_token": csrf_token}
    url = "http://quovotest.pythonanywhere.com/login"

    # Login to form
    login_response = session.post(url, data=payload)
    return login_response


def parse_headers(session, data, tree):
    # Get all header elements
    header_list = []
    headers = tree.xpath("//th")
    for header in headers:
        header_list.append(header.text)
    return header_list


def parse_data(session, data, headers, tree):
    # Master list for dicts
    list_of_dicts = []

    # Get all data elements and pair them with headers
    table_datum = tree.xpath("//tr/td")
    i = 0
    for table_data in table_datum:
        list_of_dicts.append({headers[i]: table_data.text})
        # Iterate through headers and start at 0 for new row
        if i < len(headers) - 1:
            i += 1
        else:
            i = 0
    print list_of_dicts
    return list_of_dicts


if __name__ == "__main__":
    main()
