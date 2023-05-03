#include<math.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<openssl/pem.h>
#include<openssl/err.h>
#include<openssl/bio.h>
#include<openssl/x509.h>

int main(int argc, char **argv)
{
    int ret;
    if (argc != 2)
        return (printf("ERROR: Invalid arguments.\n"));

    OpenSSL_add_all_algorithms();
    ERR_load_BIO_strings();
    ERR_load_crypto_strings();
    EVP_PKEY    *pkey = NULL;
    BIO         *outbio = NULL;
    BIO         *certbio = BIO_new(BIO_s_file());
    RSA         *cert = NULL;
    outbio  = BIO_new_fp(stdout, BIO_NOCLOSE);
    if ((ret = BIO_read_filename(certbio, argv[1])) == 0)
        return (printf("ERROR: Invalid certificate or corrupted.\n"));
    if (!(cert = PEM_read_bio_RSA_PUBKEY(certbio, NULL, 0, NULL)))
        return (BIO_printf(outbio, "ERROR: Loading cert into memory\n"));
    RSA_get0_key(cert, NULL, NULL, NULL);
    BIO_printf(certbio, "%d Key\n\n", EVP_PKEY_bits(pkey));
    if(!PEM_write_bio_PUBKEY(outbio, pkey))
        BIO_printf(outbio, "ERROR: Writing public key data in PEM format");
    EVP_PKEY_free(pkey);
    RSA_free(cert);
    BIO_free_all(certbio);
    BIO_free_all(outbio);
    return (0);pip list