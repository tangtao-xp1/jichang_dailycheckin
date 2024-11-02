# ikuuu每日自动签到

## 项目介绍
配合github actions每天定时触发脚本达到ikuuu签到。代码参考<a href = 'https://github.com/bighammer-link/jichang_dailycheckin'>bighammer-link/jichang_dailycheckin</a>，不过我在原代码基础进行了优化，可读性，易用性，维护性更高。

## 使用说明
 
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

## 推送说明
该脚本可选择采用<a href='https://sct.ftqq.com/'>Server酱</a>或<a href = 'https://www.pushplus.plus/'>pushplus</a>的推送方式
<br/>想使用哪一种推送方式就将密钥填入参数。例如要使用Server酱，只需要设置actions变量SCKEY，并为该变量填入Server酱密钥即可
<br/>如若不想使用推送，删除对应的actions变量即可。例如在actions中删除或不设置变量SCKEY，则不会使用Server酱推送
<br/>同时设置SCKEY和TOKEN，则会同时使用Server酱和pushplus进行推送
