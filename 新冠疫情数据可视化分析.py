#!/usr/bin/env python
# coding: utf-8

# 数据采集

# In[1]:


#当前日期下的世界疫情情况
import requests
import pandas as pd
from lxml import etree

html='https://ncov.dxy.cn/ncovh5/view/pneumonia'
html_data=requests.get(html)
html_data.encoding='utf-8'
html_data = etree.HTML(html_data.text,etree.HTMLParser())
html_data = html_data.xpath('//*[@id="getListByCountryTypeService2true"]/text()')

ncov_world=html_data[0][49:-12]
ncov_world=ncov_world.replace('true','True')
ncov_world=ncov_world.replace('false','False')
ncov_world=eval(ncov_world)

country=[]
confirmed=[]
lived=[]
dead=[]

for i in ncov_world:
     # 分离国家名称，确诊人数，治愈人数和死亡人数并存入dataframe里备用
    country.append(i['provinceName'])
    confirmed.append(i['confirmedCount'])
    lived.append(i['curedCount'])
    dead.append(i['deadCount'])
    
data_world=pd.DataFrame()
data_world['国家名称']=country
data_world['确诊人数']=confirmed
data_world['治愈人数']=lived
data_world['死亡人数']=dead
data_world.head(5)


# In[2]:


#读取国内的经济数据（GDP）
data_economy = pd.read_csv("https://labfile.oss.aliyuncs.com/courses/2791/gpd_2016_2020.csv", index_col=0)
time_index = pd.date_range(start='2016', periods=18, freq='Q')
data_economy.index = time_index
data_economy


# In[3]:


#获取不同时间下的疫情数据
data_area = pd.read_csv('https://labfile.oss.aliyuncs.com/courses/2791/DXYArea.csv')
data_news = pd.read_csv('https://labfile.oss.aliyuncs.com/courses/2791/DXYNews.csv')


# 数据预处理

# In[4]:


data_area=data_area.loc[data_area['countryName']==data_area['provinceName']]
data_area_times=data_area[['countryName','province_confirmedCount','province_curedCount','province_deadCount','updateTime']]

time=pd.DatetimeIndex(data_area_times['updateTime'])#根据疫情的更新时间来生成时间序列
data_area_times.index=time #生成索引
data_area_times=data_area_times.drop('updateTime',axis=1)
data_area_times.head(5)

data_area_times.isnull().any()#查询是否有空值


# In[5]:


data_news_times = data_news[['pubDate', 'title', 'summary']]
time = pd.DatetimeIndex(data_news_times['pubDate'])
data_news_times.index = time  # 生成新闻数据的时间索引
data_news_times = data_news_times.drop('pubDate', axis=1)
data_news_times.head(5)


# In[6]:


#确认各个数据集是否空集
print(data_world.isnull().any())
print(data_economy.isnull().any())
print(data_area_times.isnull().any())
print(data_news_times.isnull().any())


# 疫情现状数据分析

# In[7]:


import matplotlib.pyplot as plt
import matplotlib
import os

get_ipython().run_line_magic('matplotlib', 'inline')
#绘图
data_world=data_world.sort_values(by='确诊人数',ascending=False)#按确诊人数进行分析
data_world_set=data_world[['确诊人数','治愈人数','死亡人数']]
data_world_set.index=data_world['国家名称']
data_world_set.head(10).plot(kind='bar',figsize=(15,10))#对排序前十的国家数据进行绘图

plt.rcParams['font.sans-serif']=['SimHei']#设置字体
plt.xlabel('国家名称')
plt.xticks()
plt.legend(fontsize=30)#设置图例


# In[9]:


import pyecharts
print(pyecharts.__version__)


# In[16]:


get_ipython().system('pip install pyecharts==1.7.1 ')


# In[8]:


from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig, NotebookType

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
name_map = {  # 世界各国数据的中英文对比
    'Singapore Rep.': '新加坡',
    'Dominican Rep.': '多米尼加',
    'Palestine': '巴勒斯坦',
    'Bahamas': '巴哈马',
    'Timor-Leste': '东帝汶',
    'Afghanistan': '阿富汗',
    'Guinea-Bissau': '几内亚比绍',
    "Côte d'Ivoire": '科特迪瓦',
    'Siachen Glacier': '锡亚琴冰川',
    "Br. Indian Ocean Ter.": '英属印度洋领土',
    'Angola': '安哥拉',
    'Albania': '阿尔巴尼亚',
    'United Arab Emirates': '阿联酋',
    'Argentina': '阿根廷',
    'Armenia': '亚美尼亚',
    'French Southern and Antarctic Lands': '法属南半球和南极领地',
    'Australia': '澳大利亚',
    'Austria': '奥地利',
    'Azerbaijan': '阿塞拜疆',
    'Burundi': '布隆迪',
    'Belgium': '比利时',
    'Benin': '贝宁',
    'Burkina Faso': '布基纳法索',
    'Bangladesh': '孟加拉国',
    'Bulgaria': '保加利亚',
    'The Bahamas': '巴哈马',
    'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
    'Belarus': '白俄罗斯',
    'Belize': '伯利兹',
    'Bermuda': '百慕大',
    'Bolivia': '玻利维亚',
    'Brazil': '巴西',
    'Brunei': '文莱',
    'Bhutan': '不丹',
    'Botswana': '博茨瓦纳',
    'Central African Rep.': '中非',
    'Canada': '加拿大',
    'Switzerland': '瑞士',
    'Chile': '智利',
    'China': '中国',
    'Ivory Coast': '象牙海岸',
    'Cameroon': '喀麦隆',
    'Dem. Rep. Congo': '刚果民主共和国',
    'Congo': '刚果',
    'Colombia': '哥伦比亚',
    'Costa Rica': '哥斯达黎加',
    'Cuba': '古巴',
    'N. Cyprus': '北塞浦路斯',
    'Cyprus': '塞浦路斯',
    'Czech Rep.': '捷克',
    'Germany': '德国',
    'Djibouti': '吉布提',
    'Denmark': '丹麦',
    'Algeria': '阿尔及利亚',
    'Ecuador': '厄瓜多尔',
    'Egypt': '埃及',
    'Eritrea': '厄立特里亚',
    'Spain': '西班牙',
    'Estonia': '爱沙尼亚',
    'Ethiopia': '埃塞俄比亚',
    'Finland': '芬兰',
    'Fiji': '斐',
    'Falkland Islands': '福克兰群岛',
    'France': '法国',
    'Gabon': '加蓬',
    'United Kingdom': '英国',
    'Georgia': '格鲁吉亚',
    'Ghana': '加纳',
    'Guinea': '几内亚',
    'Gambia': '冈比亚',
    'Guinea Bissau': '几内亚比绍',
    'Eq. Guinea': '赤道几内亚',
    'Greece': '希腊',
    'Greenland': '格陵兰',
    'Guatemala': '危地马拉',
    'French Guiana': '法属圭亚那',
    'Guyana': '圭亚那',
    'Honduras': '洪都拉斯',
    'Croatia': '克罗地亚',
    'Haiti': '海地',
    'Hungary': '匈牙利',
    'Indonesia': '印度尼西亚',
    'India': '印度',
    'Ireland': '爱尔兰',
    'Iran': '伊朗',
    'Iraq': '伊拉克',
    'Iceland': '冰岛',
    'Israel': '以色列',
    'Italy': '意大利',
    'Jamaica': '牙买加',
    'Jordan': '约旦',
    'Japan': '日本',
    'Kazakhstan': '哈萨克斯坦',
    'Kenya': '肯尼亚',
    'Kyrgyzstan': '吉尔吉斯斯坦',
    'Cambodia': '柬埔寨',
    'Korea': '韩国',
    'Kosovo': '科索沃',
    'Kuwait': '科威特',
    'Lao PDR': '老挝',
    'Lebanon': '黎巴嫩',
    'Liberia': '利比里亚',
    'Libya': '利比亚',
    'Sri Lanka': '斯里兰卡',
    'Lesotho': '莱索托',
    'Lithuania': '立陶宛',
    'Luxembourg': '卢森堡',
    'Latvia': '拉脱维亚',
    'Morocco': '摩洛哥',
    'Moldova': '摩尔多瓦',
    'Madagascar': '马达加斯加',
    'Mexico': '墨西哥',
    'Macedonia': '马其顿',
    'Mali': '马里',
    'Myanmar': '缅甸',
    'Montenegro': '黑山',
    'Mongolia': '蒙古',
    'Mozambique': '莫桑比克',
    'Mauritania': '毛里塔尼亚',
    'Malawi': '马拉维',
    'Malaysia': '马来西亚',
    'Namibia': '纳米比亚',
    'New Caledonia': '新喀里多尼亚',
    'Niger': '尼日尔',
    'Nigeria': '尼日利亚',
    'Nicaragua': '尼加拉瓜',
    'Netherlands': '荷兰',
    'Norway': '挪威',
    'Nepal': '尼泊尔',
    'New Zealand': '新西兰',
    'Oman': '阿曼',
    'Pakistan': '巴基斯坦',
    'Panama': '巴拿马',
    'Peru': '秘鲁',
    'Philippines': '菲律宾',
    'Papua New Guinea': '巴布亚新几内亚',
    'Poland': '波兰',
    'Puerto Rico': '波多黎各',
    'Dem. Rep. Korea': '朝鲜',
    'Portugal': '葡萄牙',
    'Paraguay': '巴拉圭',
    'Qatar': '卡塔尔',
    'Romania': '罗马尼亚',
    'Russia': '俄罗斯',
    'Rwanda': '卢旺达',
    'W. Sahara': '西撒哈拉',
    'Saudi Arabia': '沙特阿拉伯',
    'Sudan': '苏丹',
    'S. Sudan': '南苏丹',
    'Senegal': '塞内加尔',
    'Solomon Is.': '所罗门群岛',
    'Sierra Leone': '塞拉利昂',
    'El Salvador': '萨尔瓦多',
    'Somaliland': '索马里兰',
    'Somalia': '索马里',
    'Serbia': '塞尔维亚',
    'Suriname': '苏里南',
    'Slovakia': '斯洛伐克',
    'Slovenia': '斯洛文尼亚',
    'Sweden': '瑞典',
    'Swaziland': '斯威士兰',
    'Syria': '叙利亚',
    'Chad': '乍得',
    'Togo': '多哥',
    'Thailand': '泰国',
    'Tajikistan': '塔吉克斯坦',
    'Turkmenistan': '土库曼斯坦',
    'East Timor': '东帝汶',
    'Trinidad and Tobago': '特里尼达和多巴哥',
    'Tunisia': '突尼斯',
    'Turkey': '土耳其',
    'Tanzania': '坦桑尼亚',
    'Uganda': '乌干达',
    'Ukraine': '乌克兰',
    'Uruguay': '乌拉圭',
    'United States': '美国',
    'Uzbekistan': '乌兹别克斯坦',
    'Venezuela': '委内瑞拉',
    'Vietnam': '越南',
    'Vanuatu': '瓦努阿图',
    'West Bank': '西岸',
    'Yemen': '也门',
    'South Africa': '南非',
    'Zambia': '赞比亚',
    'Zimbabwe': '津巴布韦',
    'Comoros': '科摩罗'
}

map = Map(init_opts=opts.InitOpts(width="1900px", height="900px",
                                  bg_color="#ADD8E6", 
                                  page_title="全球疫情确诊人数"))  # 获得世界地图数据
map.add("确诊人数", [list(z) for z in zip(data_world['国家名称'], data_world['确诊人数'])],
        is_map_symbol_show=False,  # 添加确诊人数信息
        # 通过name_map来转化国家的中英文名称方便显示
        maptype="world", label_opts=opts.LabelOpts(is_show=False), name_map=name_map,
        itemstyle_opts=opts.ItemStyleOpts(color="rgb(49,60,72)"),
        ).set_global_opts(
    visualmap_opts=opts.VisualMapOpts(max_=1000000),  # 对视觉映射进行配置
)
map.render_notebook()  # 在notebook中显示


# 疫情增长数据分析

# In[9]:


country=data_area_times.sort_values('province_confirmedCount',
                                   ascending=False).drop_duplicates(subset='countryName',
                                                                   keep='first').head(6)['countryName']

#对于同一天采集的多个数据，只保留第一次出现的数据也就是最后一次更新的数据
country=list(country)
country


# In[10]:


#绘制折线图展现疫情分布
data_America=data_area_times[data_area_times['countryName']=='美国']
data_Brazil=data_area_times[data_area_times['countryName']=='巴西']
data_India=data_area_times[data_area_times['countryName']=='印度']
data_Russia=data_area_times[data_area_times['countryName']=='俄罗斯']
data_Peru=data_area_times[data_area_times['countryName']=='秘鲁']
data_Chile=data_area_times[data_area_times['countryName']=='智利']


timeindex=data_area_times.index
timeindex=timeindex.floor('D')#对于日期索引，只保留具体到那一天
data_area_times.index=timeindex

#美国
timeseries=pd.DataFrame(data_America.index)
timeseries.index=data_America.index
data_America=pd.concat([timeseries,data_America],axis=1)
#对美国数据进行处理，获得美国确诊人数的时间序列
data_America.drop_duplicates(subset='updateTime',
                            keep='first',
                            inplace=True)
data_America.drop('updateTime',axis=1,inplace=True)

#巴西
timeseries=pd.DataFrame(data_Brazil.index)
timeseries.index=data_Brazil.index
data_Brazil=pd.concat([timeseries,data_Brazil],axis=1)
#对巴西数据进行处理，获得巴西确诊人数的时间序列
data_Brazil.drop_duplicates(subset='updateTime',
                            keep='first',
                            inplace=True)
data_Brazil.drop('updateTime',axis=1,inplace=True)

#印度
timeseries=pd.DataFrame(data_India.index)
timeseries.index=data_India.index
data_India=pd.concat([timeseries,data_India],axis=1)
#对印度数据进行处理，获得印度确诊人数的时间序列
data_India.drop_duplicates(subset='updateTime',
                            keep='first',
                            inplace=True)
data_India.drop('updateTime',axis=1,inplace=True)

#俄罗斯
timeseries=pd.DataFrame(data_Russia.index)
timeseries.index=data_Russia.index
data_Russia=pd.concat([timeseries,data_Russia],axis=1)
#对俄罗斯数据进行处理，获得俄罗斯确诊人数的时间序列
data_Russia.drop_duplicates(subset='updateTime',
                            keep='first',
                            inplace=True)
data_Russia.drop('updateTime',axis=1,inplace=True)

#秘鲁
timeseries=pd.DataFrame(data_Peru.index)
timeseries.index=data_Peru.index
data_Peru=pd.concat([timeseries,data_Peru],axis=1)
#对秘鲁数据进行处理，获得秘鲁确诊人数的时间序列
data_Peru.drop_duplicates(subset='updateTime',
                            keep='first',
                            inplace=True)
data_Peru.drop('updateTime',axis=1,inplace=True)

#智利
timeseries=pd.DataFrame(data_Chile.index)
timeseries.index=data_Chile.index
data_Chile=pd.concat([timeseries,data_Chile],axis=1)
#对智利数据进行处理，获得智利确诊人数的时间序列
data_Chile.drop_duplicates(subset='updateTime',
                            keep='first',
                            inplace=True)
data_Chile.drop('updateTime',axis=1,inplace=True)

#画图
plt.title("世界疫情排行分布")
plt.rcParams['font.sans-serif']=['SimHei']#设置字体
plt.plot(data_America['province_confirmedCount'])
plt.plot(data_Brazil['province_confirmedCount'])
plt.plot(data_India['province_confirmedCount'])
plt.plot(data_Russia['province_confirmedCount'])
plt.plot(data_Peru['province_confirmedCount'])
plt.plot(data_Chile['province_confirmedCount'])
plt.legend(country)


# 新冠疫情新闻挖掘分析

# In[13]:


get_ipython().system('pip install wordcloud==1.8.0')


# In[11]:


import jieba
import re
from wordcloud import WordCloud

def word_cut(x): return jieba.lcut(x)  # 进行结巴分词

news = []
reg = "[^\u4e00-\u9fa5]"
for i in data_news['title']:
    if re.sub(reg, '', i) != '':  # 去掉英文数字和标点等无关字符，仅保留中文词组
        news.append(re.sub(reg, '', i))  # 用news列表汇总处理后的新闻标题

words = []
counts = {}
for i in news:
    words.append(word_cut(i))  # 对所有新闻进行分词
for word in words:
    for a_word in word:
        if len(a_word) == 1:
            continue
        else:
            counts[a_word] = counts.get(a_word, 0)+1  # 用字典存储对应分词的词频
words_sort = list(counts.items())
words_sort.sort(key=lambda x: x[1], reverse=True)

newcloud = WordCloud(font_path="C:/Users/21616/NotoSansCJK.otf",
                     background_color="white", width=600, height=300, max_words=50)  # 生成词云
newcloud.generate_from_frequencies(counts)
image = newcloud.to_image()  # 转换成图片
image


# In[12]:


#K-Means聚类 获得不同新闻词汇之间的联系
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

words=[]

for i in news:
    words.append(word_cut(i))
model = Word2Vec(words,sg=0 ,size=300, window=5, min_count=5)  # 词向量进行训练
keys = model.wv.vocab.keys()  # 获取词汇列表
wordvector = []
for key in keys:
    wordvector.append(model[key])  # 对词汇列表里的所有的词向量进行整合

distortions = []
for i in range(1, 40):
    word_kmeans = KMeans(n_clusters=i,
                         init='k-means++',
                         n_init=10,
                         max_iter=300,
                         random_state=0)  # 分别聚成1-40类
    word_kmeans.fit(wordvector)
    distortions.append(word_kmeans.inertia_)  # 算出样本距离最近的聚类中心的距离总和

plt.plot(range(1, 40), distortions, marker='o')  # 绘图
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
    


# In[13]:


word_kmeans=KMeans(n_clusters=10)#聚成10类
word_kmeans.fit(wordvector)

labels=word_kmeans.labels_

for num in range(0,10):
    text=[]
    for i in range(len(keys)):
        if labels[i] ==num:
            text.append(list(keys)[i])
    print(text)


# 疫情对行业影响时序建模分析

# In[14]:


#对不同行业分四类来展现
sum_GDP = ['国内生产总值', '第一产业增加值', '第二产业增加值', '第三产业增加值']
industry_GDP = ['农林牧渔业增加值', '工业增加值', '制造业增加值', '建筑业增加值']
industry2_GDP = ['批发和零售业增加值', '交通运输、仓储和邮政业增加值', '住宿和餐饮业增加值', '金融业增加值']
industry3_GDP = ['房地产业增加值', '信息传输、软件和信息技术服务业增加值','租赁和商务服务业增加值', '其他行业增加值']  

#分别用四个子图来展现数据变化情况
fig=plt.figure()
fig,axes=plt.subplots(2,2,figsize=(21,15))

axes[0][0].plot(data_economy[sum_GDP])
axes[0][0].legend(sum_GDP)
axes[0][1].plot(data_economy[industry_GDP])
axes[0][1].legend(industry_GDP)
axes[1][0].plot(data_economy[industry2_GDP])
axes[1][0].legend(industry2_GDP)
axes[1][1].plot(data_economy[industry3_GDP])
axes[1][1].legend(industry3_GDP)

plt.title('分行业GDP变化图')


# In[15]:


#通过时序分析的方法对16个行业数据进行预测，推测出 2020 年第一季度的数据与实际数据进行对比，来量化预测新冠疫情对经济的影响。
from statsmodels.graphics.tsaplots import plot_acf
from pandas.plotting import autocorrelation_plot
from statsmodels.sandbox.stats.diagnostic import acorr_ljungbox

GDP_type=['国内生产总值', '第一产业增加值', '第二产业增加值', '第三产业增加值', 
            '农林牧渔业增加值', '工业增加值', '制造业增加值', '建筑业增加值', '批发和零售业增加值',
            '交通运输、仓储和邮政业增加值', '住宿和餐饮业增加值', '金融业增加值', 
            '房地产业增加值', '信息传输、软件和信息技术服务业增加值', '租赁和商务服务业增加值', '其他行业增加值']

for i in GDP_type:
    each_data=data_economy[i][:-2]
    plt.figure(figsize=(30,6))
    ax1=plt.subplot(1,3,1)
    ax2=plt.subplot(1,3,2)
    ax3=plt.subplot(1,3,3)
    LB2,P2=acorr_ljungbox(each_data)#进行纯随机检验
    plot_acf(each_data,ax=ax1)
    autocorrelation_plot(each_data,ax=ax2)#进行平稳性检验
    ax3.plot(P2)


# In[16]:


from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.stattools import arma_order_select_ic

warnings.filterwarnings('ignore')
data_arma = pd.DataFrame(data_economy['国内生产总值'][:-2])  # 选取疫情期前的16个季度进行建模
a, b = arma_order_select_ic(data_arma, ic='hqic')['hqic_min_order']
arma = ARMA(data_arma, order=(a, b)).fit()  # 使用ARMA建模
rate1 = list(data_economy['国内生产总值'][-2] /
             arma.forecast(steps=1)[0])  # 获得疫情期当季度的预测值
rate1  # 实际值与预测值的比率


# In[17]:


#使用 pyecharts 模块中的水球图来进行可视化。
from pyecharts import options as opts
from pyecharts.charts import Liquid

c = (
    Liquid()
    .add("实际值/预测值", rate1, is_outline_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="第一季度国民生产总值实际值与预测值比例", 
                                               pos_left="center"))
)
c.render_notebook()


# In[18]:


#对不同行业的经济增长值进行建模分析
warnings.filterwarnings('ignore')
data_arma = pd.DataFrame(data_economy['工业增加值'][:-2])
a, b = arma_order_select_ic(data_arma, ic='hqic')['hqic_min_order']
arma = ARMA(data_arma, order=(a, b)).fit()
rate2 = list(data_economy['工业增加值'][-2]/arma.forecast(steps=1)[0])
c = (
    Liquid()
    .add("实际值/预测值", rate2, is_outline_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="工业增加值比例", pos_left="center"))
)
c.render_notebook()


# In[19]:


warnings.filterwarnings('ignore')
data_arma = pd.DataFrame(data_economy['制造业增加值'][:-2])
a, b = arma_order_select_ic(data_arma, ic='hqic')['hqic_min_order']
arma = ARMA(data_arma, order=(a, b)).fit()
rate3 = list(data_economy['制造业增加值'][-2]/arma.forecast(steps=1)[0])
c = (
    Liquid()
    .add("实际值/预测值", rate3, is_outline_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="制造业增加值", pos_left="center"))
)
c.render_notebook()


# In[20]:


data_arma = pd.DataFrame(data_economy['批发和零售业增加值'][:-2])
a, b = arma_order_select_ic(data_arma, ic='hqic')['hqic_min_order']
arma = ARMA(data_arma, order=(a, b)).fit()
rate4 = list(data_economy['批发和零售业增加值'][-2]/arma.forecast(steps=1)[0])
c = (
    Liquid()
    .add("实际值/预测值", rate4, is_outline_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="批发和零售业增加值", pos_left="center"))
)
c.render_notebook()


# In[21]:


data_arma = pd.DataFrame(data_economy['金融业增加值'][:-2])
a, b = arma_order_select_ic(data_arma, ic='hqic')['hqic_min_order']
arma = ARMA(data_arma, order=(a, b)).fit()
rate = list(data_economy['金融业增加值'][-2]/arma.forecast(steps=1)[0])
c = (
    Liquid()
    .add("实际值/预测值", rate, is_outline_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="金融业增加值", pos_left="center"))
)
c.render_notebook()


# In[22]:


data_arma = pd.DataFrame(data_economy['信息传输、软件和信息技术服务业增加值'][:-2])
a, b = arma_order_select_ic(data_arma, ic='hqic')['hqic_min_order']
arma = ARMA(data_arma, order=(a, b)).fit()
rate = list(data_economy['信息传输、软件和信息技术服务业增加值'][-2]/arma.forecast(steps=1)[0])
c = (
    Liquid()
    .add("实际值/预测值", rate, is_outline_show=False)
    .set_global_opts(title_opts=opts.TitleOpts(title="信息传输、软件和信息技术服务业增加值", 
                                               pos_left="center"))
)
c.render_notebook()


# In[ ]:




