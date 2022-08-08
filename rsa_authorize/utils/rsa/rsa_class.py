# -*- coding: utf-8 -*-
# date: 2022/7/18
# Author: YuChen

import logging
import os
import sys
import traceback
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Cryptodome.PublicKey import RSA

logger = logging.getLogger('debug')


class RSAUtil():
    filepath = "./rsa_temp.json"

    def __init__(self) -> None:
        self.code = "nooneknows"
        self.private_key = bytes
        self.public_key = bytes

        self.private_file = str
        self.public_file = str
    def new_keys(self, length: int = 2048):
        key = RSA.generate(length)
        self.private_key = key.exportKey(passphrase=self.code,  # 類似 RSA 本身的 password，在後面曲時需帶入
                                         pkcs=8,  # 處理創造所用的進程數
                                         protection="scryptAndAES128-CBC")
        self.public_key = key.publickey().exportKey()
        return True

    def load_key(self, key: str, filepath: str):
        if(os.path.isfile(filepath)):
            with open(filepath, "rb") as f:
                file_content = f.read()
            if(key == "private"):
                self.private_file = filepath
                raw_key = RSA.import_key(file_content, passphrase=self.code)
                self.private_key = raw_key.export_key().decode('utf-8')
            elif(key == "public"):
                self.public_file = filepath
                raw_key = RSA.import_key(file_content)
                self.public_key = raw_key.export_key().decode('utf-8')
            else:
                return False
        else:
            return False

    def save_key(self, key: str, filepath: str):
        if(not os.path.exists(os.path.dirname(filepath))):
            os.makedirs(os.path.dirname(filepath))
        # if(not os.path.exists(Path(filepath).parents[0])):os.mkdir(Path(filepath).parents[0])
        if(key == "private"):
            self.private_file = filepath
            with open(filepath, "wb") as f:
                f.write(self.private_key)
                return True
        elif(key == "public"):
            self.public_file = filepath
            with open(filepath, "wb") as f:
                f.write(self.public_key)
                return True
        else:
            return False

    def get_key(self, key: str):
        if(key == "private"):
            return self.private_key
        elif(key == "public"):
            return self.public_key
        else:
            return False

    def encrypt(self, data:str) -> str:
        try:
            data_bytes = str.encode(data, encoding="utf-8")

            with open(self.filepath, 'wb') as out_file:
                # 收件人密鑰 => 我的公鑰
                public_key = RSA.import_key(open(self.public_file).read())
                # 長度 16 字元的 session 密鑰
                session_key = get_random_bytes(16)
                # Encrypt the session key with the public RSA key
                cipher_rsa = PKCS1_OAEP.new(public_key)  # PKCS1_OAEP 最優非對稱加密填充
                out_file.write(cipher_rsa.encrypt(session_key))
                # Encrypt the data with the AES session key
                cipher_aes = AES.new(session_key, AES.MODE_EAX)  # 創建 AES
                ciphertext, tag = cipher_aes.encrypt_and_digest(data_bytes)  # AES 加密

                out_file.write(cipher_aes.nonce)  # 隨機數
                out_file.write(tag)  # 消息驗證碼
                out_file.write(ciphertext)  # 密文

            with open(self.filepath, 'rb') as f:
                data = f.read()

            return self.__convert_bytes2str(data)
        except:
            message = " encrypt Failed "
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

        finally:
            if(os.path.exists(self.filepath)):
                os.remove(self.filepath)

    def descrypt(self, data:str)-> str:
        try:
            data_bytes = self.__convert_str2bytes(data)

            with open(self.filepath, 'wb') as f:
                f.write(data_bytes)

            with open(self.filepath, 'rb') as fobj:
                # 導入私鑰
                private_key = RSA.import_key(
                    open(self.private_file).read(), passphrase=self.code)
                # 加密的 session 密鑰， 隨機數，消息驗證碼，密文
                enc_session_key, nonce, tag, ciphertext = [fobj.read(x)
                                                           for x in (private_key.size_in_bytes(),
                                                                     16, 16, -1)]
                cipher_rsa = PKCS1_OAEP.new(private_key)
                session_key = cipher_rsa.decrypt(enc_session_key)  # 用私鑰解密
                cipher_aes = AES.new(
                    session_key, AES.MODE_EAX, nonce)  # 重建 AES 密鑰
                data = cipher_aes.decrypt_and_verify(
                    ciphertext, tag)  # AES 解密出原

            return data.decode('utf-8')
        except ValueError:
            message = " Can,t be decoding, Please check the private key is right "
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
        except:
            message = " descrypt failed "
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            raise False

        finally:
            if(os.path.exists(self.filepath)):
                os.remove(self.filepath)

    def __convert_bytes2str(self, bytes_data: bytes):
        try:
            bytes_data_list = list(bytes_data)
            bytes_data_str = ','.join(str(v) for v in bytes_data_list)
            return (bytes_data_str)
        except:
            message = " convert_bytes2str failed "
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False

    def __convert_str2bytes(self, bytes_data: str):
        try:
            bytes_data_list = bytes_data.split(',')
            bytes_data_bytes = bytes(int(v) for v in bytes_data_list)
            return(bytes_data_bytes)
        except:
            message = " convert_bytes2str failed "
            logger.debug(message)
            logger.debug(sys.exc_info())
            logger.debug(traceback.format_exc(1))
            return False
