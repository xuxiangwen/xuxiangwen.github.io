

- **SSL** 的全名是Secure Sockets Layer. 即“安全套接层”。发明SSL协议的初衷，是为了解决HTTP明文传输不安全的问题。
- **TLS**  将SSL协议标准化之后的名称，全称Transport Layer Security，即“传输层安全协议”。因此SSL和TLS可以看作同一个东西，在不同阶段的不同名称。因此，经常有人将其并列称为SSL/TLS。SSL/TLS依靠SSL证书验证身份，对传输数据进行加密。
- **HTTPS**  HTTPS=HTTP+SSL/TLS，即HTTPS超文本传输协议，实际上是HTTP和SSL/TLS的组合。也可以说，HTTPS，是安全版的HTTP，即在HTTP下加入了SSL层。可有效避免信息在传输中被窃听、篡改、劫持。HTTP与HTTPS所用端口有区别，HTTP的端口是80，HTTPS的端口是443。
- **SSL/TLS证书** 一种数据证书，也称为SSL服务器证书。由受信任的颁发机构，以验证服务器身份，提供数据传输加密功能。SSL证书内包含网站信息和颁发者，以及有效期。