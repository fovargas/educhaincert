import os.path
import sys
import logging

from cert_issuer import __main__

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __package__ is None and not hasattr(sys, 'frozen'):
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))


def cert_issuer_main(args=None):
    from cert_issuer import config
    parsed_config = config.get_config()
    import issue_certificates
    resultado = issue_certificates.main(parsed_config)
    
    print(resultado)
    

if __name__ == '__main__':
    cert_issuer_main()