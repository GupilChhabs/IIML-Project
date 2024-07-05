import numpy as np 
import pandas as pd 
import statsmodels.api as sm
from xlwt import Workbook
from datetime import datetime
import yfinance as yf


wb=Workbook()
sheet2=wb.add_sheet('Sheet 2')
sheet2.write(0,0,'Tickers')

for i in range(12):
    sheet2.write(0,i+1,'Month '+str(i+1))
wb.save("C:/Users/gupil/OneDrive/Documents/output2.xls")  

start_date=datetime(2023,1,1)
end_date=datetime(2023,12,31)

stocks=pd.read_csv('C:/Users/gupil/Downloads/nasdaq_screener_1719874092364 (1).csv')
tickrs=stocks['Symbol'][:10]
print(tickrs)

ff=pd.read_csv('C:/Users/gupil/Downloads/ffdaily.csv')
ff=ff.dropna()
ff = ff.loc[:, ~ff.columns.str.contains('^Unnamed')]

j=1
for tickr in tickrs:
    data=yf.download(tickr,start=start_date,end=end_date)
    sheet2.write(j,0,tickr)
    data.dropna()
    #print(tickr)
    ret=(np.array(data.Close[1:])/np.array(data.Close[:-1])-1)*100
    volume=np.array(data.Volume[1:])*1e-6
    d0=data.index
    ff.index=d0
    t1=pd.DataFrame(ret,index=d0[1:],columns=['ret']) 
    t2=pd.DataFrame(volume,index=d0[1:],columns=['volume']) 
    t3=pd.merge(t1,t2,left_index=True,right_index=True) 
    pns=pd.merge(t3,ff,left_index=True,right_index=True)
    pns=pns.rename(columns={'Mkt-RF':'MKTRF'})
    month=[]
    for x in data.index:
        y=str(x)
        month.append(y[5:7])
        z=np.array(month)
        z=pd.to_numeric(z[1:])
    pns['months']=z
    grouped = pns.groupby('months')
    dfs = {group: grouped.get_group(group) for group in grouped.groups}
    for i in dfs:
        df=dfs[i]
        y=df.ret[1:]-(df.MKTRF[1:]+df.RF[1:])
        x1=df.ret[:-1]
        x2=np.sign(np.array (df.ret[:-1]-df.MKTRF[:-1]-df.RF[:-1]))*np.array(df.volume[:-1])
        x3=[x1,x2]
        n=np.size(x3)
        x=np.reshape(x3,[n//2,2])
        x=sm.add_constant(x)
        res=sm.OLS(y,x).fit()
        x=res.params.iloc[2]
        sheet2.write(j,i,x)
    j=j+1
wb.save("C:/Users/gupil/OneDrive/Documents/output2.xls")