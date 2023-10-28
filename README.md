# blockutpl

Modificaciones en archivos base:


blockutpl/venv/lib/python3.8/site-packages/cert_tools/helpers.py

def create_iso8601_tz():
    ret = datetime.now(timezone.utc).isoformat()[:-13]+'Z'
    return ret.isoformat()

def create_iso8601_tz():
    return datetime.now(timezone.utc).isoformat()[:-13]+'Z'

blockutpl/venv/lib/python3.8/site-packages/cert_tools/instantiate_v3_certificate_batch.py
def instantiate_recipient(cert, recipient, additional_fields):
    cert['credentialSubject']['id'] = recipient.pubkey
    cert['credentialSubject']['name'] = recipient.name +++
    cert['credentialSubject']['email'] = recipient.identity +++