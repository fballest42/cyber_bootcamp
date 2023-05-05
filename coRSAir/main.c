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

void BN_sqrt(BIGNUM *r, const BIGNUM *a, BN_CTX *ctx)
{
    BIGNUM *x0 = BN_new();
    BIGNUM *x1 = BN_new();
    BIGNUM *two = BN_new();
    BIGNUM *tmp = BN_new();

    int cmp; BN_set_word(x0, 1);
    BN_copy(x1, a);
    BN_add(x1, x1, x0);
    BN_rshift(x1, x1, 1);
    BN_set_word(two, 2); 
    do 
    {
        BN_copy(x0, x1);
        BN_div(tmp, NULL, a, x0, ctx);
        BN_add(x1, x0, tmp);
        BN_rshift(x1, x1, 1);
        cmp = BN_cmp(x0, x1);
    } 
    while (cmp != 0); BN_copy(r, x0); BN_free(x0); BN_free(x1); BN_free(two); BN_free(tmp);
} 

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
    const BIGNUM      *n = BN_new();
    const BIGNUM      *k = BN_new();
    char              *mod;
    outbio  = BIO_new_fp(stdout, BIO_NOCLOSE);
    if ((ret = BIO_read_filename(certbio, argv[1])) == 0)
        return (printf("ERROR: Invalid certificate or corrupted.\n"));
    if (!(cert = PEM_read_bio_RSA_PUBKEY(certbio, NULL, 0, NULL)))
        return (printf("ERROR: Loading cert into memory\n"));
    RSA_get0_key(cert, &n, &k, NULL);
    
    printf("MODULO:\n");
    BN_print_fp(stdout, n);
    printf("\n\nEXPONENTE:\n");
    BN_print_fp(stdout, k);
    printf("\n");
    mod = BN_bn2dec(n);
    printf("\nMODULO EN DECIMAL:%s\n", mod);
    size_t l = strlen(mod);
    size_t lp = l / 2;
    char pmax[lp + 1];
    char pmin[lp + 1];
    char pmed[lp + 1];
    printf("\nEL MODULO MIDE: %lu y los primos son de minimo %lu\n", l, lp);
    for (int i = 0; i < lp; i++)
    {
        if (i == 0 || i == lp - 1)
        {
            pmin[i] = '1';
            pmed[i] = '1';
        }
        else
        {
            pmin[i] = '0';
            pmed[i] = '0';
        }
        pmax[i] = '9';
        pmax[i+1] = '\0';
        pmin[i+1] = '\0';
        pmed[i+1] = '\0';
    }
    // printf("pmax %s\npmin %s\npmed %s\n", pmax, pmin, pmed);
    BIGNUM *bn_pmax = BN_new();
    BIGNUM *bn_pmin = BN_new();
    BIGNUM *bn_pmed = BN_new();
    BIGNUM *bn_one = BN_new();
    BIGNUM *bn_two = BN_new();
    BIGNUM *bn_root = BN_new();
    BIGNUM *rem = BN_new();
    BN_CTX *ctx = BN_CTX_new();
    // BN_dec2bn(&bn_pmax, pmax);
    // BN_dec2bn(&bn_pmin, pmin);

    BN_sqrt(bn_pmed, n, ctx);
    BN_dec2bn(&bn_one, "1");
    BN_dec2bn(&bn_two, "2");
    bn_pmin = BN_dup(bn_pmed);
    bn_pmax = BN_dup(bn_pmed);
    BN_print_fp(stdout, bn_pmin);
    printf("\n");
    BN_print_fp(stdout, bn_pmed);
    printf("\n");
    BN_print_fp(stdout, bn_pmax);
    printf("\n");
    BN_CTX_free(ctx);
    BN_GENCB *cb;
    int i = 0;
    while (1)
    {
        ctx = BN_CTX_new();
        cb = BN_GENCB_new();
        if (BN_is_prime_ex(bn_pmed, 1, ctx, cb))
        {
            printf("PRIMO: ");
            BN_print_fp(stdout, bn_pmed);
            printf("\n");
            BN_CTX_free(ctx);
            ctx = BN_CTX_new();
            BN_mod(rem, n, bn_pmed, ctx);
            if (BN_is_zero(rem))
            {
                BN_CTX_free(ctx);
                BN_GENCB_free(cb);
                break;
            }
            else
            {
                BN_CTX_free(ctx);
                BN_GENCB_free(cb);
            }
        }
        else
        {
            BN_CTX_free(ctx);
            BN_GENCB_free(cb);
        }
        BN_sub(bn_pmed, bn_pmed, bn_two);
        printf("%d\n", i++);
    }
    BN_print_fp(stdout, bn_pmin);
    EVP_PKEY_free(pkey);
    RSA_free(cert);
    BIO_free_all(certbio);
    BIO_free_all(outbio);
    return (0);
}
