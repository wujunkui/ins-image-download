import hashlib
import base64
import hmac


def generate_signature(data, secret_key):
    # 将字典的键排序并拼接成URL编码格式的字符串
    sorted_data = sorted(data.items())
    sorted_str = '&'.join(f"{key}={value}" for key, value in sorted_data)
    print(sorted_str)
    # 创建HMAC-SHA256哈希
    signed_hmac_sha256 = hmac.HMAC(secret_key.encode(), sorted_str.encode(), hashlib.sha256)

    # 将哈希值编码为Base64字符串
    signature = base64.b64encode(signed_hmac_sha256.digest()).decode()
    return signature


if __name__ == '__main__':
    # 示例数据和密钥
    data = {'url': 'https://www.instagram.com/reel/C5r1wgCSLLS/?igsh=MTFhcTV2eGpnNWRpeQ==', 't': 1713107028475}
    secret_key = 'bfa95f704ce74c5cba31820ea1c0da05'

    # 生成签名并打印
    print(generate_signature(data, secret_key))
