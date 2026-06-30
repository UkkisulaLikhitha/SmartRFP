import requests

BASE_URL = "http://127.0.0.1:8000"

# def upload_rfp(
#     file,
#     deal_name="",
#     client_name="",
#     region="",
#     deadline="",
#     assigned_role="",
#     use_web_search=True,
# ):
#     files = {
#         "file": (
#             file.name,
#             file.getvalue(),
#             file.type or "application/octet-stream",
#         )
#     }

#     data = {
#         "deal_name": deal_name,
#         "client_name": client_name,
#         "region": region,
#         "deadline": deadline,
#         "assigned_role": assigned_role,
#         "use_web_search": str(use_web_search).lower(),
#     }

#     response = requests.post(
#         f"{BASE_URL}/upload-rfp",
#         files=files,
#         data=data,
#     )

#     response.raise_for_status()

#     return response.json()

import requests

BASE_URL = "http://127.0.0.1:8000"

def upload_rfp(
    uploaded_file,
    deal_name="",
    client_name="",
    region="",
    deadline="",
    assigned_role="",
    use_web_search=True,
):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "application/octet-stream",
        )
    }

    data = {
        "deal_name": deal_name,
        "client_name": client_name,
        "region": region,
        "deadline": deadline,
        "assigned_role": assigned_role,
        "use_web_search": str(use_web_search).lower(),
    }

    response = requests.post(
        f"{BASE_URL}/upload-rfp",
        files=files,
        data=data,
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    response.raise_for_status()

    return response.json()

def regenerate(rfp_id):
    response = requests.post(
        f"{BASE_URL}/regenerate/{rfp_id}"
    )
    response.raise_for_status()
    return response.json()

