# Gooseberry 基于时间表叠加的约时间工具
#### 此项目为thu2017soa课程大作业

## 运行说明
#### 操作步骤
0. 配置环境（mysql数据库，python2.7及引用的各种工具）
1. 在mysql中创建数据库 gooseberry
2. 命令行中输入 python dabaseIni.py
3. 命令行输入python hello.py
4. 在浏览器打开localhost:5000
#### 技术说明
+ 后端框架 flask
+ 后端开发语言 python 2.7
+ 前端开发使用 jquery bootstrap
+ 数据库 mysql

## 使用流程说明
1. 注册/登录
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/hello.jpg)
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/tutorial.jpg)
  + 首页右上角有tutorial，可以看到我们的课程提交poster
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/signup.jpg)
  + 注册需要填写用户名与注册id
  + 登录时只需填写注册id与密码
2. 编辑自己的时间表
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/index.jpg)
  + 登陆后首先看到自己的时间表，一列表示一天，一共7天，一行是半个小时
  + 可以用shift辅助来选择多个连续格子，然后点击左下角的新增事件即可，也可以选中需要删除的部分点击删除事件（一个事件只要有一部分被选中即会全部删除该时间）
  + clear是清空当前的操作
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/tags.jpg)
  + 另，invitation标签页是用户创建的邀请的列表
  + events是用户加入的活动的列表
3. 添加好友
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/friends.jpg)
  + 在goose标签页里，点击add contact即可打开搜索模态框
  + 将你要搜索的一个或多个用户的id以;分割输入到搜索框中，点击搜索即可显示结果
  + 搜索结果分为三类：好友用户，陌生人用户，不存在的用户（我们的好友概念是单向的）
    + 好友用户可以在他的名字旁边编辑备注名，之后的朋友列表都会以备注名显示，如果备注名为空则显示他自己的用户名；点击删除按钮可以删除他
    + 陌生人用户右边的添加按钮可以点击添加好友。
    + 不存在的用户会用红色显示。
    + 关闭模态框
4. 查看叠加的时间表
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/impose.jpg)
  + 此时左边的列表里有你自己（第一行）和所有的好友
  + 选择你需要查看时间的所有人，然后点击下面的superimpose按钮即可在时间表中看到结果（颜色越深表示此时有事的人越多）
5. 选择时间创建邀请（如果所有参与者时间表都是准确的，那么其实之后的步骤可以不进行，或者不在本平台进行）
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/create.jpg)
  + 然后可以选择你想要举办活动的备选时间，并点击创建活动按钮，在弹出的对话框中填写活动的基本信息提交即可。
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/invs.jpg)
  + 此时你可以在invitation标签下看到刚刚创建的活动，点击打开活动的页面，把网址发给你想要邀请的人即可。
6. 邀请界面的操作
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/info.jpg)
  + 左上角是活动的基本信息，右边是已经投票了的人数。
  + 图中颜色深浅表示投票给这个时间的人数的多少（所以深色表示可以参加的人比较多的时间）
  + 图中的圆圈表示活动创建者选定的时间范围，灰色为你没有选择的部分，黑色是你选择了的部分。点击它可以选中或取消。
  + 图中的对勾表示活动发起者最终敲定的时间。
  ![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/btn.jpg)
  + 作为创建者你可以在右上角删除活动或者敲定活动时间（set按钮），敲定前你需要在图中选定（文字变为黑色）你想要敲定的时间。
  + 任何人都可以先选定一些时间段，然后点击Join加入活动
  + 如果你已经加入了活动，那么打开这个页面的时候时间表○的状态就是你之前的选择，你可以退出活动或者修改你的选择

## 项目idea
#### 痛点与竞品分析
在我们日常生活中，想要组织什么活动时，“约时间”总是一件非常麻烦的事情。目前市面上有着不少面向活动发起或者日程管理的网站和应用，但我们小组在进行前期调研的时候发现，搜索并试用了近二十个产品，没有一个能满足我们的需要--足够简单。（下图为概览）
![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/ppt.jpg)
总结后的痛点有：
+ 直接交流约时间：
  1. 需要反复询问：多人活动更是很难敲定一个时间。
+ 采用问卷或者其他工具的问题
  2. 反复填写相同信息：被邀请者如果要参加很多个活动则需要填写很多次问卷，而时间表几乎是相同的
  3. 选项盲目：邀请者创建活动备选时间的时候比较盲目，需要创建很多条
  4. 选项过多：创建选项的时间很不灵活，比如一整个下午4个小时都可以用来举办一场一个小时的活动，发起者需要手动创建4甚至8个备选项。

#### 核心idea
![](https://github.com/WangQianEve/Gooseberry/tree/master/docs/images
/impose.jpg)
因此，我们提出了基于日程叠加的活动发起的概念。
1. 每个用户对自己的日程表进行一次的设置（后期可同步第三方日程管理工具），所有人都可以查看，从而解决了痛点2。
  + 当然，这不等同于暴露日程表。因为其他人只能查看别人是“有空”还是“没空”，没有更多信息，从而保证了用户隐私。
2. 活动发起者可以将多个人的日程表进行叠加，从而直观地看到可以发起活动的时间。这样可以大大提升约时间的**精准度**，解决了痛点1，痛点3。
3. 采用日程表的图像化形式，不仅直观，而且可以连续选择大片时间，投票时间也很灵活，不需要与备选时间完全重合（本质是时间分片更小，甚至可以小到分钟，因为大片选择非常方便，demo是30min一格）。解决了痛点4，痛点3

#### 扩充idea（未实现）
1. 跨时区功能，并在时间表左部绘制时间轴辅助查看
2. 显示活动每个事件的投票者都是谁
3. 同步第三方日程管理工具。
