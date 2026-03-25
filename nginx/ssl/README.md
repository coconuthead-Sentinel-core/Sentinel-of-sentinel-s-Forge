# TLS Bootstrap Certificates

`fullchain.pem` and `privkey.pem` are generated locally for nginx TLS bootstrapping.

- Generate them with `python scripts/generate_dev_tls_cert.py`
- The generated certificate is self-signed for `localhost`, `127.0.0.1`, and `::1`
- Replace these files with CA-issued certificates before any public deployment
