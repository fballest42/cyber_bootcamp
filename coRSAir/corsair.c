#include<math.h>
#include<string.h>
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<fcntl.h>
#include<openssl/pem.h>
#include<openssl/err.h>
#include<openssl/bio.h>
#include<openssl/rsa.h>
#include<openssl/bn.h>
#include<openssl/x509.h>

void mod_exp_print(BIGNUM *n, BIGNUM *k, int i, char **argv) 
{
    //FUNTION TO PRINT THE DATA EXTRACTED FROM PUBLIC KEYS
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

    //CHANGING THE EXTENSION TO LOOK THE ASOCIATED FILE
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
	// CHECKING THE TEXT INSIDE THE BIN FILE
    inlen = 0;
	fd = open(file, O_RDONLY);
	if (fd <= 0)
		exit(printf("ERROR: No encrypted file associated.\n"));
	while (read(fd, &c, 1))
		inlen++;
	close(fd);
	in = (unsigned char *)malloc(sizeof(unsigned char) * (inlen + 1));
	fd = open(file, O_RDONLY);
	if (read(fd, in, inlen) < 0)
		exit(printf("ERROR: not possible to read the bin file.\n"));
	close(fd);
    in[inlen] = '\0';
    // DECRYPTING THE TEXT INSIDE THE BIN FILE
	out = malloc(RSA_size(privkey));
	RSA_private_decrypt(RSA_size(privkey), in, out, privkey, RSA_PKCS1_PADDING);
	x = 0;
	while (out[x] >= 32 && out[x] <= 126)
        x++;
    out[x] = '\0';
    // printf("\n\n******************************************************\n");
    // TO VIEW THE ENCRIPTED TEST IN THE FILE UNCOMMENT THIS LINES,
    // THIS CAN CAUSE ANOMALIES IN PRINTING CAUSED BY THE CHARACTERS INSIDE, DO NOT PANIC
	// printf("Encrypted message of file %s:\n", file);
	// printf("%s\n\n", in);
	printf("\nDecrypted message of the file: %s\n", file);
    printf("-------------------------------------------------------\n");
	printf("<< %s >>\n\n", out);
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
    BIGNUM  *rem2 = BN_new();
    BN_CTX  *ct = BN_CTX_new();
    RSA     *privkey = RSA_new();
    char    *res;
    FILE     *fd;

    // CALCULATE THE OTHER PRIME NUMBER, AND OTHER VALUES NEEDED
    BN_div(q, NULL, n, p, ct);
    BN_sub(tq, q, BN_value_one());
    BN_sub(tp, p, BN_value_one());
    BN_mul(z, tp, tq, ct);
    BN_mod_inverse(rem, k, z, ct);
    BN_mod(dp, rem, tp, ct);
	BN_mod(dq, rem, tq, ct);
    BN_mod_inverse(rem2, q, p, ct);

    // GENERATE THE NEW PRIVATE KEY WITH THE VALUES
    RSA_set0_key(privkey, BN_dup(n), BN_dup(k), rem);
    RSA_set0_factors(privkey, p, q);
    RSA_set0_crt_params(privkey, dp, dq, rem2);
    if (RSA_check_key(privkey) != 1)
	    printf("ERROR: OpenSSL reports internal inconsistency in generated RSA key!\n");
    else
    {
        decrypt(argv, i, privkey);
        //COMMENT OR UNCOMMENT THIS LINE TO WATCH ON SCREEN ALL THE PRIVATE KEY DATAS.
        // RSA_print_fp(stdout, privkey, 5);
        //COMMENT OR UNCOMMENT THIS 10 LINES TO WATCH ON SCREEN OR WRITE IN A FILE THE PRIVATE KEY.
        // IF YOU DON'T WANT TO SAVE ON A FILE YOU MUST OPEN AND CHANGE fd FOR THE FILE stdout.
        // char    *tmp = ".priv";
        // char    *f_priv;
        // f_priv = malloc(sizeof(char) * (strlen(tmp) + strlen(argv[i + 1] + 1)));
        // strcpy(f_priv, argv[i + 1]);
        // strcat(f_priv, tmp);
        // if (!(fd = fopen(f_priv, "w+")))
        //      printf("ERROR: Could not create the private key file.");
        // else
        //     PEM_write_RSAPrivateKey(fd, privkey, NULL, NULL, 0, 0, NULL);
        // free(f_priv);
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
    // LOOP TO CHECK IF ANY CERTIFICATE HAVE A COMMON PRIME NUMBER WITH OTHERS CERTIFICATES
    // AND IN THAT CASE CREATE A NEW ONE
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

int open_crt_files(int argc, char **argv, int j, BIO **certbio, EVP_PKEY **key, RSA **pubkey, const BIGNUM **tn, const BIGNUM **tk)
{
	X509        *cert[argc];
	char	    *n;
	char	    *e;
    BIO         *outbio = BIO_new_fp(stdout, BIO_NOCLOSE);
    certbio[j] = BIO_new(BIO_s_file());

	BIO_read_filename(certbio[j], argv[j + 1]);
    cert[j] = NULL;
	if (!(cert[j] = PEM_read_bio_X509(certbio[j], NULL, NULL, NULL)))
	{
		BIO_printf(outbio, "Error loading cert into memory\n");
		return(1);
	}
	key[j] = X509_get_pubkey(cert[j]);
    //TRYING TO CHANGE TO RSA TO GET THE MODULE AND EXPONENT
	if (!(pubkey[j] = EVP_PKEY_get1_RSA(key[j])))
	{
		printf("Couldn't convert to a RSA style key.\n");
		return (1);
	}
	tn[j] = RSA_get0_n(pubkey[j]);
	tk[j] = RSA_get0_e(pubkey[j]);
    n = BN_bn2dec(tn[j]);
    e = BN_bn2dec(tk[j]);
	printf("\nMODULUS:	%s\n\nEXPONENT:	%s\n\n", n, e);
	free(n);
    free(e);
	BIO_free_all(certbio[j]);
	BIO_free_all(outbio);
	X509_free(cert[j]);
	EVP_PKEY_free(key[j]);
	RSA_free(pubkey[j]);
    return (0);
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
    int             i, ii = 0;
    int             j = 0;

    p = malloc(sizeof(BIGNUM*) * argc);
    OpenSSL_add_all_algorithms();
    ERR_load_crypto_strings();
    if (argc < 2)
        return (printf("ERROR: Invalid arguments.\n"));
    //LOOP TO OPEN AND PRINT CRT CERTIFICATES AND TRY TO CONVERT TO RSA CERTIFICATE
    for (j = 0; j < argc - 1; j++)
    {
        if (strnstr(argv[j + 1], ".crt", 100) != NULL)
        {
            open_crt_files(argc, argv, j, &certbio[j], &pkey[j], &cert[j], &tn[j], &tk[j]);
            ii = j;
        }
    }
    //LOOP TO OPEN PEN CERTIFICATES AND STORE IT FOR COMPARATION
    for (i = ii; i < argc - 1; i++)
    {
        if (strnstr(argv[i + 1], ".pem", 100) != NULL)
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
        else
            return(printf("ERROR: Not valid certificate\n"));
    }
    //FUNTION TO LOOK FOR ONE PRIME EACH PAIR OF TWO CERTFICATES
    check_gcd(n, k, p, argc, argv);
    //THE NEXT LINES IS TO LIBERATE MEMORY AND AVOID LEAKS
    free_BN(n, k, file, argc);
    free(p);
    BIO_free_all(outbio);
    return (0);
}
