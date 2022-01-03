import random
import pandas
import string
import matplotlib.pyplot as plt

testinde = list(string.ascii_lowercase[:20])
testphys = random.sample(range(1, 30), 20)
testinfo = random.sample(range(1, 30), 20)
testcase = random.sample(range(20, 1000), 20)
testdf = pandas.DataFrame({'phys': testphys, 'info': testinfo, 'case': testcase}, index=testinde)

# testplt1 = plt.scatter(x=testdf['phys'], y=testdf['info'], c=testdf['case'], cmap='Reds', s=testdf['case'])
# plt.show()

testplt1 = testdf.plot.scatter(x='phys', y='info', c='case', colormap='Reds', s=testdf['case'], figsize=(10, 8))
testplt1.set_xlabel('physical accessibility index')
testplt1.set_ylabel('information accessibility index')
plt.savefig('scripts/testplt1.png')