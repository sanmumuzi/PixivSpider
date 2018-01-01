# pixiv_spider 

## 基本功能: 输入画师ID,获取其作品

### 2017.09.17更新
**发现问题**:更改xpath内容,原有xpath可获取信息,但是需要经过正则提取以及拼接,而且经过测试发现通过该xpath获取的图片格式与实际图片格式不同,导致bug发生.

**思路**:每个具体作品页面有一个origin-image,这个链接直接为真正的图片url,获取这个origin-image需要访问具体作品页面,但是如果这么做的话,访问的页面数量几乎会增加一倍.另一种方法是访问的时候,对jpg和png两个都进行测试(**前提是P站只有png和jpg两种格式**),这样的话,获取的403数量将会很多...如果这样的话,是不是会有很大的被封风险....

**未测试方法**:如果每个画师的作品的格式都相同(**...假设...**),那么在爬第一副图片的时候进行试png和jpg,哪个成功的话,接下来所有的爬取都将采用该格式.

**最终处理方法**:选用思路中的第二种方法

### 2017.09.18更新

修复了格式转换的bug,并将其包装成函数.

将部分单独代码包装成函数.

**暂停使用**:P站于今日出现问题,貌似被qiang,重新开放后继续更新代码.

### 2017.10.25 Update

Because DNS contamination, we can only use a l_a_d_d_e_r.

Use ssr by requests\[socks\].

### 2017.10.26 Update

Added download log file to avoid duplication of downloads.
Increase the download interval option.

### 2018.1.1 Update

Rebuild code.

Use new_crawl.py now.

Only to achieve the most basic functions.
