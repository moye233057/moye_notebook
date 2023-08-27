#### datetime格式转时间戳
```
import datetime

now = datetime.datetime.now()
timestamp = now.timestamp()

print("当前时间：", now)
print("时间戳：", timestamp)
```

#### 将两个时间戳相减，得到它们之间的秒数差。然后可以通过除以 86400（一天的秒数）得到它们之间的天数差；余数再除以 3600（一小时的秒数）就得到剩余的小时数
```
import datetime

# 获取当前时间戳
now_timestamp = datetime.datetime.now().timestamp()

# 假设有一个早于当前时间2天3小时的时间戳
earlier_timestamp = now_timestamp - (2 * 24 * 3600) - (3 * 3600)

# 计算相差的秒数
diff_seconds = now_timestamp - earlier_timestamp

# 计算天数和小时数
days = int(diff_seconds / 86400)
hours = int((diff_seconds % 86400) / 3600)

print("相差天数：", days)
print("相差小时数：", hours)
```