#应用的唯一标识
client_id = "DigitalPioneerDev"
#应用的唯一标识
client_secret="b5e617f1fff228aea8216d467cdfa37dea694432"
# 固定值 code
response_type = "code"
#固定值 read
scope = "read"
#用来维护请求和回调状态的附加字符串，在授权完成回调时会附加此参数，应用可以根据此字符串来判断上下文关系
state = ""
#仅仅限于车联网系统使用
clw_vin=""
#固定值 authorization_code
grant_type = "authorization_code"
#获取当前账号的域账号信息，若是需要填写固定值 isAdUser=1 即可
isAdUser = 1


#用户授权完成后的回调地址，应用需要通过此回调地址获得用户的授权结果。注意请将参数做URLEncode
redirect_uri_vue = "http://xxc.saicmotor.com/sso/token"
# 用户登陆跳转接口,登陆成功后返回code
sso_uri_code = "https://host/sso/authorize"
# 根据 code 获取 token
sso_uri_token = "https://host/sso/token"
# 根据 token 获取用户信息
sso_uri_user = "https://host/sso/user/get"

