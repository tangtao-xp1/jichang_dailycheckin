# ikuuu每日签到

这个脚本只适合这一个机场😥😥😥😥，当时只是自己拿来用，就写个这一个机场的。我又写了一个通用的（机场只要Powered by SSPANEL就可以）请移步<a href = 'https://github.com/bighammer-link/jichang_checkin'>此处</a>
## 推送
  该脚本可选择采用<a href='https://sct.ftqq.com/'>server酱</a>和<a href = 'https://www.pushplus.plus/'>pushplus</a>的推送方式
  <br/>想使用哪一种推送方式就将密钥填入下方参数，并将另一参数赋值为 <b>1</b>
  <br/>如若不想使用推送，请假下面的SCKEY和TOKEN参数全部赋值为<b>1</b>
  

# 部署过程
 
1. 右上角Fork此仓库
2. 然后到`Settings`→`Secrets and variables`→`Actions` 新建以下参数：

| 参数   |  是否必填  | 内容  | 
| ------------ |  ------------ |  ------------ |
| BASE_URL  |  否  |  ikuuu的域名地址，不填写则默认为https://ikuuu.one  |
| EMAIL  |  是  |  账号邮箱  |
| PASSWD |  是  |  账号密码  |
| SCKEY  |  否  |  Server酱密钥，不填写则不会使用Server酱推送消息  |
| TOKEN  |  否  |  pushplus密钥，不填写则不会使用pushplus推送消息  |

3. 到`Actions`中创建一个workflow，运行一次，以后每天项目都会自动运行。
4. 最后，可以到Run sign查看签到情况，同时也会也会将签到详情推送到Sever酱。
