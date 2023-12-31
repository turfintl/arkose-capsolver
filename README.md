# arkose-capsolver                                                                                                                            
[>>>ENGLISH<<<](README.en.md)  
一个简单的利用CapSolver API获取arkose token的http服务器。  
支持并发向公共token服务发送请求，以增强冗余性和响应速度。  
<br />注：CapSolver收费，$2 / 1000 token  
注2：本项目用于OpenAI ChatGPT提问时所需arkose token  
注3：因CapSolver实际体验识别率有时并不高，等待时间可能会较长，不推荐用于token需求量大的场景

## 安装

```
pip3 install capsolver
git clone https://github.com/turfintl/arkose-capsolver.git
```
编辑`main.py`填入你的API key  
（可选）在`get_first_result`函数中取消注释并赋值`public_pool_urlx`以启用公共token池的支持  
~~（进一步）如果注释掉capsolver，添加多个公共token池，甚至能变成一个较稳定的本地白嫖token服务，但我不推荐这么搞~~

## 运行
```
python3 main.py
```

## 获取arkose token
访问 http://127.0.0.1:8999/token


## 支持

如果觉得本项目对您有帮助，欢迎使用下方邀请链接进行注册使用  
[CapSolver注册链接](https://dashboard.capsolver.com/passport/register?inviteCode=lhn2_FmvyM-N)
