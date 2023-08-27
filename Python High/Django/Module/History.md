#### 修改历史记录
```
def changehiswords(text, username):
    """
    功能：放在搜索接口末尾，用于记录搜索文本更新在历史记录最前，最多存放20条
    参数：
    text：str.搜索的文本
    username：str.历史记录属于的用户     
    """
    # 保证新记录为字符串
    text = str(text)
    # 若要记入历史记录的文本有多个空格，变为一个
    text = re.sub(' +', ' ', text)
    # 根据用户名找到当前用户的历史记录存放表
    try:
        profile = UserProfile.objects.filter(user__username=username)[0]
    except:
        return responseJson(200, None, 'maybe no this user')
    # 获取旧的历史记录
    histext = profile.history
    # 若旧的历史记录文本有多个空格，变为一个
    histext = re.sub(' +', ' ', histext)
    # 如果历史记录不是空的，用单个空格分离得到各个搜索词
    # 再去除分离得到的列表的空值，防止当只有一个词的时候切割出空值
    if histext != '':
        histext = histext.split(' ')
        histext = list(filter(None, histext))
    # 如果本次搜索的内容不在历史记录切割出的列表中，需要在后面添加
    if text not in histext:
        # 如果记录的历史记录超过20个，去掉最早的记录，加上最新的记录，否则直接加在后面
        if len(histext) > 20:
            histext.pop()
            histext = ' '.join(histext)
            newhis = text + ' ' + histext
        else:
            histext = ' '.join(histext)
            newhis = text + ' ' + histext
    # 如果本次搜索的内容在历史记录的文本中，将该文本提到最前面
    else:
        # 首先要去除与新记录相同的旧记录
        histext = filter(lambda x: x != text, histext)
        histext = ' '.join(histext)
        # 将新记录放在历史记录最前面
        newhis = text + ' ' + histext
    # 保存修改后的历史记录
    profile.history = newhis
    profile.save(update_fields=['history'])
    # 历史记录有改动，清除该用户的历史记录redis缓存
    conn = get_redis_connection('default')
    history_key = 'patentinfer_history_%s' % username
    conn.delete(history_key)
```

#### 获取用户历史记录接口
```
def getuserhistory(request):
    username = request.POST.get('username')
    conn = get_redis_connection('default')
    history_key = 'patentinfer_history_%s' % username
    res = conn.get(history_key)
    if not res:
        try:
            profile = UserProfile.objects.filter(user__username=username)[0]
        except:
            return responseJson(200, None, 'maybe no this user')
        histext = profile.history
        # 历史记录以单个空格分隔开
        histext = histext.split(' ')
        # 去除空值
        histext = list(filter(None, histext))
        conn.set(history_key, " ".join(histext))
    else:
        histext = res.decode("utf-8").split(" ")
    return responseJson(200, histext, '历史记录')
```