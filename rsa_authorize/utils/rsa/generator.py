from rsa_class import RSAUtil

def main():
    # 寫入與真實使用的金鑰並不相同，因為檔案是有加入 passphrase 作保護
    RSA = RSAUtil()
    RSA.new_keys(2048)
    RSA.save_key("private","./keys/authorize_private.bin")
    RSA.save_key("public","./keys/authorize_public.pem")

if __name__ == "__main__":
    main()