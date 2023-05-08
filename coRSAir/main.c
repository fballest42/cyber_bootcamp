#include<math.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<stdbool.h>
#include<fcntl.h>
#include<openssl/pem.h>
#include<openssl/err.h>
#include<openssl/bio.h>
#include<openssl/rsa.h>
#include<openssl/bn.h>

void print_bignum_calc(const BIGNUM *tp, const BIGNUM *tq, const BIGNUM *rem, const BIGNUM *rem2) 
{
    printf("\n*************************************************\n");
    printf("*************************************************\n");
    printf("PRIMO P-1 ---> \t");
    BN_print_fp(stdout, tp);
    printf("\nPRIMO Q-1 ---> \t");
    BN_print_fp(stdout, tq);
    printf("\nREM ---> \t\t");
    BN_print_fp(stdout, rem);
    printf("\nREM2 --->\t\t");
    BN_print_fp(stdout, rem2);
    printf("\n");
}

void print_bignum_primes(const BIGNUM *p, const BIGNUM *q, const BIGNUM *z) 
{
    printf("\n*************************************************\n");
    printf("PRIMO P ---> \t");
    BN_print_fp(stdout, p);
    printf("\nPRIMO Q ---> \t");
    BN_print_fp(stdout, q);
    printf("\nZ ---> \t\t");
    BN_print_fp(stdout, z);
    printf("\n");
}

void mod_exp_print(BIGNUM *n, BIGNUM *k, int i, char **argv) 
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

void	decrypt(char **argv, int i, RSA* privkey)
{
	unsigned char	*out;
	unsigned char	*in;
	size_t			inlen;
	char			*file;
	char			c;
	int				fd;
	int				z;
	int				x;

	file = malloc(sizeof(char) * (strlen(argv[i + 1]) + 1));
	z = 0;
	while (z < strlen(argv[i + 1]) - 3)
	{
		file[z] = argv[i + 1][z];
		z++;
	}
	file[z++] = 'b';
	file[z++] = 'i';
	file[z++] = 'n';
	file[z] = '\0';
	inlen = 0;
	fd = open(file, O_RDONLY);
	if (fd <= 0)
		exit(printf("ERROR: No encrypted file associated.\n"));
	while (read(fd, &c, 1))
		inlen++;
	close(fd);
	in = (unsigned char *)malloc(sizeof(unsigned char) * (inlen));
	fd = open(file, O_RDONLY);
	if (read(fd, in, inlen) < 0)
		exit(1);
	close(fd);
	out = malloc(RSA_size(privkey));
	RSA_private_decrypt(RSA_size(privkey), in, out, privkey, RSA_PKCS1_PADDING);
	x = 0;
	while (out[x] != '\n' && out[x] != '\0')
		x++;
    printf("\n*************************************************\n");
	printf("Encrypted message of file %s:\n", file);
	printf("%s\n\n", in);
	printf("Decrypted message of file %s:\n", file);
	printf("%s\n\n", out);
    printf("\n*************************************************\n");
	free(file);
	free(in);
	free(out);
}

void create_prikey(BIGNUM *p, BIGNUM *n, BIGNUM *k, int i, int argc, char **argv)
{
    BIGNUM  *tq = BN_new();
    BIGNUM  *tp = BN_new();
    BIGNUM  *dq = BN_new();
    BIGNUM  *dp = BN_new();
    BIGNUM  *q = BN_new();
    BIGNUM  *z = BN_new();
    BIGNUM  *rem = BN_new();
    BIGNUM  *rem2 = BN_new();;
    BN_CTX  *ct = BN_CTX_new();
    RSA     *privkey;
    char    *res;

    BN_div(q, NULL, n, p, ct);
    BN_sub(tq, q, BN_value_one());
    BN_sub(tp, p, BN_value_one());
    BN_mul(z, tp, tq, ct);
    BN_mod_inverse(rem, k, z, ct);
    res = BN_bn2dec(rem);
    // print_bignum_primes(p, q, z);
    if (strcmp(res, "1\0") != 0)
    {
        BN_mod(dp, rem, tp, ct);
	    BN_mod(dq, rem, tq, ct);
        BN_mod_inverse(rem2, q, p, ct);
        // print_bignum_calc(tp, tq, rem, rem2);
        privkey = RSA_new();
        RSA_set0_key(privkey, BN_dup(n), BN_dup(k), rem);
        RSA_set0_factors(privkey, p, q);
        RSA_set0_crt_params(privkey, dp, dq, rem2);
        // privkey = RSAPrivateKey_dup(privkey);
        if (RSA_check_key(privkey) != 1)
		    printf("ERROR: OpenSSL reports internal inconsistency in generated RSA key!\n");
        else
        {
            // RSA_print_fp(stdout, privkey, 5);
            // PEM_write_RSAPrivateKey(stdout, privkey, NULL, NULL, 0, 0, NULL);
            decrypt(argv, i, privkey);
        }
    }
    BN_CTX_free(ct);
    BN_free(tp);
    BN_free(tq);
    BN_free(z);
    RSA_free(privkey);
}

void check_gcd(BIGNUM **n, BIGNUM **k, BIGNUM **p, int argc, char **argv)
{
    BIGNUM      *tp;
    BN_CTX      *ct = BN_CTX_new();
    char        *res;

    for (int i = 0; i < argc - 2; i++)
    {
        for (int j = i + 1; j < argc - 1; j++)
        {
            tp = BN_new();
            BN_gcd(tp, n[j], n[i], ct);
            res = BN_bn2dec(tp);
			if (strcmp(res, "1\0") != 0)
            {
                p[i] = BN_dup(tp);
                p[j] = BN_dup(tp);
                create_prikey(p[i], n[i], k[i], i, argc, argv);
                create_prikey(p[j], n[j], k[j], j, argc, argv);
            }
            free(res);
            BN_free(tp);
        }
    }
    BN_CTX_free(ct);
}

void free_BN(BIGNUM **n, BIGNUM **k, char **file, int argc)
{
    for (int i = 0; i < argc - 1; i++)
    {
        BN_free(n[i]);
        BN_free(k[i]);
        free(file[i]);
    }
}

int main(int argc, char **argv)
{
    EVP_PKEY        *pkey[argc];
    BIO             *outbio = BIO_new_fp(stdout, BIO_NOCLOSE);
    BIO             *certbio[argc];
    BIGNUM          *n[argc];
    BIGNUM          *k[argc];
    const BIGNUM    *tn[argc];
    const BIGNUM    *tk[argc];
    BIGNUM          **p;
    RSA             *cert[argc];
    char            *file[argc];
    int             i;

    p = malloc(sizeof(BIGNUM*) * argc);
    OpenSSL_add_all_algorithms();
    ERR_load_crypto_strings();
    if (argc < 2)
        return (printf("ERROR: Invalid arguments.\n"));
    for (i = 0; i < argc - 1; i++)
    {
        certbio[i] = BIO_new(BIO_s_file());
        pkey[i] = NULL;
        file[i] = strdup(argv[i + 1]);
        if (!(BIO_read_filename(certbio[i], argv[i + 1])))
            return (printf("ERROR: Invalid certificate or corrupted.\n"));
        if (!(cert[i] = PEM_read_bio_RSA_PUBKEY(certbio[i], NULL, 0, NULL)))
            return (printf("ERROR: Loading cert into memory.\n"));
        RSA_get0_key(cert[i], &tn[i], &tk[i], NULL);
        // mod_exp_print(tn[i], tk[i], i, argv);
        n[i] = BN_dup(tn[i]);
        k[i] = BN_dup(tk[i]);
        EVP_PKEY_free(pkey[i]);
        RSA_free(cert[i]);
        BIO_free_all(certbio[i]);
    }
    check_gcd(n, k, p, argc, argv);
    free_BN(n, k, file, argc);
    BIO_free_all(outbio);
    system("leaks corsair");
    return (0);
}
