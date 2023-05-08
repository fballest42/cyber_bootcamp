#include<math.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<openssl/pem.h>
#include<openssl/err.h>
#include<openssl/bio.h>
#include<openssl/rsa.h>
#include<openssl/bn.h>

void mod_exp_print(const BIGNUM *n, const BIGNUM *k, int i, char **argv) 
{
    printf("\n*************************************************\n");
    printf("FILE: \t\t\t%s\n", argv[i + 1]);
    printf("*************************************************\n");
    printf("MODULO ---> \t\t");
    BN_print_fp(stdout, n);
    printf("\nEXPONENTE ---> \t\t");
    BN_print_fp(stdout, k);
    printf("\n");
}

void create_prikey(BIGNUM *p, BIGNUM *n, BIGNUM *k, int argc)
{
    BIGNUM *q = BN_new();
    BIGNUM *z = BN_new();


}

void check_gcd(const BIGNUM **n, const BIGNUM **k, int argc, char **argv)
{
    BIGNUM      *tp;
    BIGNUM      *p[argc];
    BN_CTX      *ct;
    char        *res;
    int         key_num = 0;

    for (int i = 0; i < argc - 2; i++)
    {
        for (int j = i + 1; j < argc - 1; j++)
        {
            tp = BN_new();
            ct = BN_CTX_new();
            BN_gcd(p[i], n[j], n[i], ct);
            res = BN_bn2dec(p[i]);
			if (strncmp(res, "1\0", 2) != 0)
            {
                p[key_num] = BN_dup(tp);
                create_prikey(p[key_num], n[i], k[i], key_num);
                create_prikey(p[key_num], n[j], k[j], key_num);
                key_num++;
            }
            BN_free(p[i]);
            BN_CTX_free(ct);
        }
    }
}

int read_certificates(int argc, char **argv)
{
    
    return (0);
}

int main(int argc, char **argv)
{
    EVP_PKEY        *pkey[argc];
    BIO             *outbio = BIO_new_fp(stdout, BIO_NOCLOSE);
    BIO             *certbio[argc];
    const BIGNUM    *n[argc];
    const BIGNUM    *k[argc];
    BIGNUM          *p[argc;]
    RSA             *cert[argc];
    RSA             *prikey[argc];
    char            *mod[argc];
    char            *file[argc];
    int             i;

    OpenSSL_add_all_algorithms();
    ERR_load_BIO_strings();
    ERR_load_crypto_strings();

    if (argc < 2)
        return (printf("ERROR: Invalid arguments.\n"));
    for (i = 0; i < argc - 1; i++)
    {
        certbio[i] = BIO_new(BIO_s_file());
        n[i] = BN_new();
        k[i] = BN_new();
        pkey[i] = NULL;
        file[i] = strdup(argv[i + 1]);
        if (!(BIO_read_filename(certbio[i], argv[i + 1])))
            return (printf("ERROR: Invalid certificate or corrupted.\n"));
        if (!(cert[i] = PEM_read_bio_RSA_PUBKEY(certbio[i], NULL, 0, NULL)))
            return (printf("ERROR: Loading cert into memory.\n"));
        RSA_get0_key(cert[i], &n[i], &k[i], NULL);
        mod_exp_print(n[i], k[i], i, argv);
        mod[i] = BN_bn2dec(n[i]);
        n[i] = BN_dup(n[i]);
        k[i] = BN_dup(k[i]);
        EVP_PKEY_free(pkey[i]);
        RSA_free(cert[i]);
        BIO_free_all(certbio[i]);
    }
    check_gcd(n, k, argc, argv);

    BIO_free_all(outbio);

    return (0);
}
