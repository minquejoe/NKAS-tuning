# FROM

https://github.com/takagisanmie/NIKKEAutoScript

# NIKKEAutoScript

胜利女神：NIKKE 自动日常脚本

### 鸣谢

------

Alas的所有开发者，到现在我还是觉得Alas的源码不明觉厉  
让我学到了，'草，Python还能这么写？'  
然后想到了自己写的最初版代码，那写的是什么shit😅😅😅  
虽然现在写的NKAS依旧是shit😅😅😅

### 如何使用

------
-1.可以加入qq划水群 823265807  
1.https://www.bluestacks.cn/ 在此页面下载并安装 蓝叠模拟器5.20.101.6503  
2.模拟器`显示`设置竖屏，720*1280，240DPI，`图像`设置图像渲染器为Vulkan，界面渲染器为软件，`高级`打开Android调试  
3.下载脚本和依赖，运行`updater.bat`(一般要开代理)，打开`NKAS\win-unpacked\NikkeAutoScript.exe`，在脚本设置中将`Serial`改为模拟器设置`高级 => Android调试`给出的127.0.0.1:xxxx  
4.NIKKE画面设置如图(`光晕效果`和`颜色分级`一定要打开)，然后可以运行脚本了  
![image](https://github.com/user-attachments/assets/5a8e340a-0736-4073-a1dc-b2d7c1fe13f0)

### 依赖相关

------

由于用到的依赖文件过大，所以将依赖和本体分开   
如果是第一次使用，请下载python-3.9.13-embed-amd64.7z   
并且解压在与updater.bat的同一级，保持文件夹名称为‘python-3.9.13-embed-amd64’

### 常见问题 （目前拥有的功能并非全部完善，在遇到问题时，还麻烦来github反馈 或者 在QQ群反馈）
------
#### Q1： 运行NikkeAutoScript.exe 提示  ‘Failed to load resource’
#### A1： 可能是运行updater.bat时，没有完全更新成功，可以尝试重新解压后再次运行 updater.bat
------
#### Q2：主程序没有内容，只有顶部栏
#### A2： 可能是缺失了某个依赖，可以通过CMD手动安装 requirements.txt 中的依赖
------
#### Q3：updater.bat 在运行后一闪而过
#### A3： 这应该是无法访问Github时会出现的情况，可以在 config/deploy.yaml 的 GitProxy 字段中填写代理，或者更改hosts等
------
#### Q4：在咨询任务中，无法咨询任何NIKKE
#### A4：请检查NIKKE的画质设置，确保选项拥有‘光晕效果’和‘颜色分级’两个选项，以及在游戏中收藏了想咨询的NIKKE
------
#### Q5：在运行某个任务时，没有正确点击
#### A5：可能是模拟器的分辨率为1280 * 720，但在运行NIKKE时是以竖屏运行的，这样会导致点击到错误位置，请设置为720 * 1280后，再次尝试
------
#### Q6：更新界面只有None
#### A6：这是因为没有初始化Git，请运行 updater.bat
------
#### Q7：主程序更新时，一直在转圈圈
#### A7：同A3
------
#### Q8：运行调度器时出现'BaseError: /data/app/com.proximabeta.nikke-.......apk: no such file or directory'
#### A8：这是因为模拟器的NIKKE是通过Google Play下载的，可以卸载后在QooApp下载，可以解决这个问题
------
#### Q9：进入付费商店时，提示'网络异常，读取商店结账资讯失败'
#### A9：这很可能是因为模拟器的 Google Play 未登录账号，可以登录账号后再尝试
------
#### 推荐画面设置
<img src="https://s2.loli.net/2024/05/06/Rjcx7EwWXlbKBot.png" alt="1.png" style="zoom: 50%;" />

### 预览

------

![](https://profile-counter.glitch.me/takagisanmie-NIKKEAutoScript/count.svg)
