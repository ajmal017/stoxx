#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from __future__ import print_function
from  builtins import any as b_any
import numpy as np
import pandas as pd
import os,sys,argparse,datetime,string
import pickle
from termcolor import colored, cprint
import numba as nb


import yfinance as yf
import html5lib,bs4 # sometimes necessary by yfincance
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = 'browser'

def help(p = None):
    string = ''' helptext '''
    p = argparse.ArgumentParser(description=string,
            formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('name', metavar='name', type=str, nargs='*',
                    help='the name of the stock, e.g. bayer, infineon')
    p.add_argument('-p','--plot', help='plot to browser', action='count', default=False)
    p.add_argument('-pdp','--plot_derivative_pressure_intraday', help='plot derivative pressure', action='count', default=False)

    p.add_argument('-all','--all', help='evaluate for allstocks.', action='count',default=False)
    p.add_argument('-two','--two', help='load only two teststocks, not all stocks.', action='count', default=False)
    p.add_argument('-best','--best', help='show only best stocks and owned ones', action='count', default=False)


    p.add_argument('-s','--sortbyGD', help='sortby e.g. 40 == GD40', type=int, nargs=1, default=False)
    p.add_argument('-startdate','--startdate', help='select the start date of the dataset e.g. \'2020-01-13\'; default=False', type=str, default='2019-01-01')
    p.add_argument('-maxdate','--maxdate', help='select the date for evaluation e.g. \'2020-01-08\'; default=last date', type=str, default=False)
    p.add_argument('-d','--details', help='show stock details', action='count', default=False)
    p.add_argument('-v','--verbose', help='verbose', action='count', default=False)
    return p

def stocks_to_load(args):
    ''' list of considered stocks '''
    d = {};
    #print('xargs.name',args.name)
    #print('xargs.all ',args.all)
    #print('xargs.two ',args.two)
    #if args.two == 1 or args.all == 1:
    if True:
        d['DOW Jones']      = ['^DJI','T']
        d['Volatility']     = ['^VIX','T']
        d['Microsoft']      = ['MSFT']
        d['Millennial Lithium Corp'] = ['MLNLF',"M",'wenn es sich faengt, kaufen']
        d['Adidas']         = ['ADS.DE']
        d['Infineon']       = ['IFX.DE',"M"]
        d['Albemarle']      = ['ALB',"M","H","KGV_15.3"]
        d['Wirecard']       = ['WDI.DE','!','H', 20, 'HU9TMK_2.01_KO70.38', 'verkaufe bei ~130']
        d['Dexcom']         = ['DXCM',"Kaufen wenn GD100=GD200, Verkaufen wenn Kurse stabil und RSI kleiner wird"]
        d['Blizzard']       = ['AIY.DU',"!"]
        d['Iqiyi']          = ['IQ8.F',"M",'H','KGV_-28','MC4YZ4_2.67_KO17.19$  Spread 1.8%']
        d['Ayden']          = ['1N8.MU']
        d['Lufthansa']      = ['LHA.DE',"!",'KGV_4','H','verkaufe bei 12-13']
        d['Disney']         = ['DIS']
        d['Samsung SDI']    = ['XSDG.SG',"M","spread 2% !!!","KGV_14.5","look at 956311"]
        d['Bayer']          = ['BAYN.DE',"KGV_8.5"]
        d['BYD']            = ['BYDDF',"M",'H','MC1UM8_2.67_KO28.39HDK','KGV_60']
        d['Evotec SE']      = ['EVT.DE',        20]
        d['GDS Holdings']   = ['GDS',"M","!" ':Wait until rsi < 60 oder 55']
        d['Netflix']        = ['NFLX',"M","K",'KGV_28']
        d['Livent']         = ['LTHM',"M","H","spread 0.5% ab 16:00",'KGV_25']
        d['Cloudera']       = ['CLDR',"M",'small buy will get ±10%']
        d['Uber']           = ['UBER', 'Kost_0.25% günstig.']
        d['Teladoc DE']     = ['4LL.SG',    15, 'B','+', "spread 1.4%",'RSI7,B~50,S78']
        d['Teladoc']        = ['TDOC',      15, 'B','+', "spread 1.4%"]
        d['Tal Education']  = ['TAL',      "B", 'spread 1%']
        d['Lennar']         = ['LEN','!',20, 'GA944R_3.07_KO40.114__Kaufen bei rsi 37 oder > GD20']
        d['LennarDE']       = ['LNN.F']
        d['Micron Technology'] = ['MU',"!", 'CP4U6F_2.93_KO31.86USD MACD 12,26,9 ! works well!']
        d['Stryker']        = ['SYK',"KGV_17.2"]
        d['PSI Software']   = ['PSAN.F',"M",'KGV_18.7 erloese stark steigend']
        d['Sixt']           = ['SIX2.DE',"KGV_15.14"]
        d['Enphase Energy'] = ['ENPH','M','K','KGV_32']
        d['Baidu']          = ['BIDU']
        d['LPKF Laser']     = ['LPK.F']
        d['Teamviewer']     = ['TMV.DE']
        d['Coca-Cola']      = ['KO']
        d['Tylertech']      = ['TYP.SG']
        d['Tesla']          = ['TSLA',"M",'H','KGV_52','spread 0.1%, look at RSI 9']
        d['Tesla_DE']       = ['TL0.DE','H','B','KGV_52',"spread 0.1%"]
        d['Qualcomm']       = ['QCI.SG']
        d['STEICO']         = ['ST5.F','S',"H","KGV_20.7"]
        d['Google']         = ['ABEA.BE']
        d['Alibaba']        = ['AHLA.DE']
        d['Nvidia']         = ['NVD.DE','!','+','KGV_25']
        d['Docusign']       = ['DOCU','!',"In moment zu teuer"]
        d['DocusignDE']     = ['DS3.F','!',"Im moment zu teuer"]
        d['Msciworld']      = ['XDWD.DE']
        d['Red Electrica']  = ['RDEIY']
        d['Visa']           = ['V']
        d['Enel']           = ['ENLAY',     20, "H",'HX792H_2.33_KO4.62EUR',"KGV_13.64 "]
        d['Zimmerbio']      = ['ZBH']
        #d['Nevro']          = ['NVRO',      40, 20.2]
        d['Nevro NVRO']      = ['1N7.BE',"KGV_No, verkaufe da umsaetze ruecklaeufig."]
        d['SolarEdge']      = ['SEDG',"M",'Q',"H","spread 0.5%","MC3DKC_2.2_KO67.5$",'KGV_18.8']
        d['Occidental Petroleum']  = ['OXY']
        d['Hella GmbH']     = ['HLE.DE']
        d['QIAGEN']         = ['QIA.DE','!']
        d['IBM']            = ['IBM',"KGV_9.4"]
        d['MSCI World ETF'] = ['URTH']
        d['MSCI Emerging Markets ETF'] = ['EEM']
        d['Apple']          = ['AAPL']
        d['Splunk']         = ['SPLK']
        d['Bestbuy']        = ['BBY']
        d['OHB']            = ['OHB.DE','KGV_18.61']
        d['DICAsset']       = ['DIC.DE']
        d['Airbus']         = ['AIR.BE','KGV_11.63']
        d['Zebra']          = ['ZBRA']
        d['Autodesk']       = ['ADSK']
        d['Paycom']         = ['PAYC']
        d['Cisco']          = ['CSCO']
        d['Varta']          = ['VAR1.DE',"M",'H','C','DF4S5M_3.4_KO60.78 KOSTEN_aktie_0.3%',"KGV_17"]
        d['Jinkosolar']     = ['JKS',"M","H","KGV_6.2","MF9LH1_2.1_KO12.0$","spread 1.25% ab 16:00"]
        d['secunet']        = ['YSN.DE','M']
        d['Vestas']         = ['VWDRY',"M"]
        d['Novo Nordisk']   = ['NOVC.DE']
        d['Panasonic']      = ['PCRFY']
        d['Powercell Sweden'] = ['27W.SG']
        d['Siemens']        = ["SIE.DE","KGV_10.35"]
        d['KS']             = ["SDF.DE"]
        d['Merck']          = ["MRK.DE"]
        d['HeidelCem']      = ["HEI.DE",'KGV_7.8']
        d['Henkel']         = ["HEN3.DE"]
        d['Thyssen']        = ["TKA.DE",'!']
        d['Plug Power']     = ["PLUG",'M',"KGV_-35"]
        d['Allianz']        = ["ALV.DE"]
        d['BMW']            = ["BMW.DE"]
        d['Beiersdorf']     = ["BEI.DE"]
        d['DtBank']         = ["DBK.DE"]
        d['Lanxess']        = ["LXS.DE",'KGV_11.23']
        d['Coba']           = ["CBK.DE"]
        d['Conti']          = ["CON.DE"]
        d['Basf']           = ["BAS.DE",'KGV_12.5']
        d['Daimler']        = ["DAI.DE"]
        d['Fresenius']      = ["FRE.DE"]
        d['FreseniusM']     = ["FME.DE"]
        d['Linde']          = ["LIN.DE"]
        d['DeutBoer']       = ["DB1.DE"]
        d['VW']             = ["VOW.DE"]
        d['Adidas']         = ["ADS.DE"]
        d['DtPost']         = ["DPW.DE",'B','KGV_10','Kaufen wenn steigt']
        d['SAP']            = ["SAP.DE",'KGV_15']
        d['MRueck']         = ["MUV2.DE"]
        d['Telekom']        = ["DTE.DE"]
        d['RWE']            = ["RWE.DE",'+','KGV_15.3']
        d['Eon']            = ["EOAN.DE"]
        d['ZYNGA']          = ['ZNGA',"M"]
        d['Ynvisible']      = ['1XNA.F','H']

    if args.verbose > 1:
        print('d',d)
    if args.all == 1:
        pass
    elif args.two == 1:
        e = {}
        for idx,i in enumerate(d):
            #print('i:',i,'d[i]:', d[i])
            e[i] = d[i]
            if idx == 1:
                break
        d = e
    elif len(args.name) >= 1:
        e = {}
        for idx,i in enumerate(d):
            #print('i:',i,'d[i]:', d[i])
            if i.lower() in [x.lower() for x in args.name]:
                e[i] = d[i]
        d = e
    return d

def load_stock_data(name,args): #,dlower):
    folder = 'stock_data'
    if args.details:
        print('name             :',name)

    #if len(dlower[name.lower()]) > 0:
    ID = d[name][0]
    #try:
    #    #ID = dlower[name][0]
    #else:
    #    sys.exit('did not find ID for:'+name)
    if args.details:
        print('ID (yahooname)   :',ID)
    #print('data_from  :',dlower[name][1])
    filename = folder+'/'+ID+'.pkl'
    filename_ticker = folder+'/'+ID+'_ticker.pkl'
    if not os.path.isdir('stock_data'):
        os.mkdir(folder)
    if args.details:
        print('filename         :',filename)
    if os.path.isfile(filename): #and os.path.isfile(filename_ticker):
        if args.details:
            print('loading from     :',filename)
        df = pd.read_pickle(filename)
    else:
        #if args.details:
        print('downloading',name,'data from yahoo',ID)

        way = 'slow' # 'fast'
        #way = 'fast'  # loaded tesla to
        # save stocks data
        if way == 'slow': # takes too long
            df = yf.download(ID) #,dlower[name][1])
            df = df.reset_index()
            df.to_pickle(filename)
            lastdate  = df_get_lastdate(df,args)
            print('lastdate',lastdate)

        # save info
        ticker = yf.Ticker(ID)
        #print('ticker done')
        if way == 'fast': # takes too long
            try:
                #print('save obj:',filename_ticker)
                #save_obj(ticker.info, filename_ticker)
                #print('download histhory')
                df = ticker.history(period="max")
                #print('reset index')
                df = df.reset_index()
                #print('df to pickle save')
                df.to_pickle(filename)
                lastdate  = df_get_lastdate(df,args)
            except (IndexError,ValueError):
                sys.exit('did not work out for',name)

        if args.details:
            print('saved to         :',filename)
    #print('df')
    #print(df)
    if args.maxdate:
        #df = df[(df['Date'] > '2020-01-08')]
        #print('args.maxdate',args.maxdate)
        df = df[(df['Date'] <= args.maxdate)]
    if args.startdate:
        df = df[(df['Date'] >= args.startdate)]
    #print(df)
    #sys.exit()
    return df,ID

def save_obj(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename ):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def fig_add_stock_data(fig,df,title_text,low=True,high=True,open_=True,close=True):
    op=1.0
    op=0.5
    fill='tonexty' # [ 'none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx', 'toself', 'tonext']
    #fill='none'
    if low == True:
        fig.add_trace(go.Scatter(
                x=df.Date,
                y=df['High'],
                name="High",
                line_color='deepskyblue',
                opacity=op
                ))

    if high == True:
        fig.add_trace(go.Scatter(
                x=df.Date,
                y=df['Low'],
                name="Low",
                line_color='deepskyblue',
                opacity=op,
                fill=fill))

    if open_ == True:
        fig.add_trace(go.Scatter(
                x=df.Date,
                y=df['Open'],
                name="Open",
                line_color='green',
                opacity=op))

    if close == True:
        fig.add_trace(go.Scatter(
                x=df.Date,
                y=df['Close'],
                name="Close",
                line_color='red',
                opacity=op))

    fig.update_layout(
            title_text=title_text,
            xaxis_rangeslider_visible=False)
            #yaxis_rangeslider_visible=True)
    return fig

def GD(days,df):
    ''' Gleitender Durchschnitt:
        days [integer] for rolling average; e.g. GD200;
        shift is one since we can obtain the rolling mean only "at the end of the day; however, if we load it in the morning, then we can use all data'''
    return df.Close.rolling(days).mean() #.shift(1)

def MA(days,df):
    ''' moving average '''
    return GD(days,df)

def SMA(days,df):
    ''' simple moving average '''
    return GD(days,df)

def GDd(days,df):
    return GD(days,df).diff()

def EWM(days,df):
    return df.Close.ewm(com=days).mean()

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow


def EWMA(days,df):
    EWM(days,df)

def fig_add_GD(fig,days):
    '''
    fig: [plotly object]
    days [integer] for rolling average; e.g. GD200 '''
    gd_=GD(days=days,df=df)
    #df.insert(2, "GD"+str(days), gd_, True)
    fig.add_trace(go.Scatter(
                x=df.Date,
                y=gd_,
                name="GD"+str(days),
                line_color='black',
                opacity=0.8))
    return fig

def df_get_lastdate(df,args=False,idx=-1):
    date = str(df['Date'][df.index[idx]]).split()[0]
    if args.details:
        print('lastdate         :',date)
    return datestr_to_datetiem(date)

def datestr_to_datetiem(date):
    y = int(date.split('-')[0])
    m = int(date.split('-')[1])
    d = int(date.split('-')[2])
    return datetime.date(y, m, d)

def df_get_firstdate(df,args=False,idx=0):
    date = str(df['Date'][df.index[idx]]).split()[0]
    if args.details:
        print('firstdate        :',date)
    return datestr_to_datetiem(date)

def get_earnings_notrade(df,start_trading_at=False,verbose=True):
    ''' buy at first day, dont lock at stock, sell at the last day '''
    #print('sta1',start_trading_at)
    #print('sta2',type(start_trading_at))
    #print('sta2',str(start_trading_at))
    #print('df',df)
    if start_trading_at == False:
        buy = df.dropna()['Open'][df.dropna().index[0]]
    else:
        #print('xx start_trading_at',start_trading_at)
        #print('start:',datetime.date(start_trading_at))
        #print('start2:',pd.Timestamp(datetime.date(1996, 12, 16)))
        #print(df['Date'] == datetime.date(start_trading_at))
        #buy = df[df.Date == pd.Timestamp(datetime.date(1996, 12, 16))].Open
        for i in np.arange(1000):
            #print('i',i,start_trading_at)
            if len(df[df.Date == pd.Timestamp(start_trading_at)]) > 0:
                break
            else:
                start_trading_at = start_trading_at + datetime.timedelta(days=1)

        buy = float(df[df.Date == pd.Timestamp(str(start_trading_at))].Open)
    #print('buy (on first day):',buy,)
    sell  = df['Close'][df.index[-1]]
    #print('sell (on last day):',sell)
    earnings = sell - buy
    #print('sta4',start_trading_at)
    #print('earnings',earnings)
    print('earned (notrade):',str(np.round(100*earnings/buy,2))+" % ",start_trading_at,'for',np.round(buy,2),'sold for',np.round(sell,2),'on last day')
    #print('----------------------------------')
    return earnings


def module_buy_sell(kriterium):
    '''
    returns np.array mit +1,0,-1
    with +1 for a buy
         -1 for a sell

    kriterium e.g. (df['Close']-df['GD'] )>0


    days: anzahl der tage die am anfang geskipped wird
    '''
    days = 300
    days = 0
    #print "kriterium max:",kriterium.max()
    #print "kriterium min:",kriterium.min()
    df_buy_sell_all = np.insert(np.diff(kriterium.astype(int)), 0, 0, axis=0)  # -> int
    #print "kurs>GD max:",df_buy_sell_all.max()
    #print "kurs>GD min:",df_buy_sell_all.min()


    skip_first_x_days= np.ones(kriterium.shape[0])
    skip_first_x_days[:days] = 0
    check = df_buy_sell_all * skip_first_x_days

    # for making -0 to 0
    #def make_minus_zero_to_zero(check):
    #    y = check.round()
    #    y[y==0.] = 0.
    #    check = np.copy(y)
    #    return check

    ######################################################################################
    # check that first action is a buy
    # this works since I got an error for dax, 10 days GD
    ######################################################################################
    index_first_action = np.where(check)[0][0]
    print('index_first_action',index_first_action)
    print('chk index_first_action',check[index_first_action])
    if check[index_first_action] != 1:  # 1 = buy, -1 is sell
        check[index_first_action] = 0

    ######################################################################################
    # check that last action is a sell
    # this works since I got the error for dax, 20 days GD
    ######################################################################################
    index_last_action = np.where(check)[0][-1]
    if check[index_last_action] != -1:  # 1 = buy, -1 is sell
        #print '--> index_last_action',index_last_action
        #df['check'] = check
        #df['buy_sell_all>days'][index_last_action] = 0
        check[index_last_action] = 0
        #print 'show buy_sell_all>days indizes:',np.where(df['buy_sell_all>days'])[0]
        #sys.exit("last transaction, index = "+str(index_last_action)+", has to be a sell")

    return check

def get_earnings(kurse,algo):
    '''
    gibt gewimme / verluste aus
    gibt anzahl gewinn/ verlusttrades an
    kurse: df.Close
    algo : (df['Close']-SMA(df.Close,270))>0
    '''
    kaufe_verkaufe = module_buy_sell( algo )
    print("kaufe_verkaufe:",kaufe_verkaufe)

    ######################################################################################
    # get index erster kauf
    idx_ek = np.where(kaufe_verkaufe)[0][0]
    #print "edx_ek:",idx_ek

    ######################################################################################
    # get index letzter verkauf
    idx_lv = np.where(kaufe_verkaufe)[0][-1]
    #print "edx_lv:",idx_lv

    ######################################################################################
    # alle buys (nur zur info)
    ######################################################################################
    alle_buys = np.where(kaufe_verkaufe==1)[0]
    alle_sells = np.where(kaufe_verkaufe==-1)[0]
    #print "alle_buys:",alle_buys
    #print "alle_sells",alle_sells
    check1 = kurse * kaufe_verkaufe * -1

    ######################################################################################
    # gewinne_verluste (nur zur info)
    ######################################################################################
    gewinne_verluste = np.zeros(kaufe_verkaufe.shape[0])
    gewinne_verluste = np.empty(kaufe_verkaufe.shape[0])
    gewinne_verluste[:] = np.NAN
    for idx,i in enumerate(alle_sells):
        gewinne_verluste[i] = check1[alle_sells[idx]] + check1[alle_buys[idx]]
        # print "idx:",idx,"i=",i,"alle_sells[idx]",alle_sells[idx],"alle_buys[idx]",alle_buys[idx]
    ######################################################################################
    # gewinntrades/verlusttrades
    gewinntrades_idx = np.where(gewinne_verluste > 0)[0]
    verlusttrades_idx = np.where(gewinne_verluste < 0)[0]
    g = gewinntrades_idx.shape[0]
    v = verlusttrades_idx.shape[0]
    #print "einfacher GD:  gewinntrades_idx",gewinntrades_idx
    print("einfacher GD:  trades anzahl       :",g+v,"\t",np.nansum(gewinne_verluste), "\t\t dow/dax:",(kurse[idx_lv]-kurse[idx_ek]))
    print("einfacher GD:  gewinntrades anzahl :",g,"\t", np.sum(gewinne_verluste[gewinne_verluste > 0]))
    print("einfacher GD:  verlusttrades anzahl:",v,"\t", np.sum(gewinne_verluste[gewinne_verluste < 0]))

    performancegain = np.sum(check1)/(kurse[idx_lv]-kurse[idx_ek])-1

    return gewinne_verluste, performancegain

def earnings(earnings_total,first_buy,investment=20000,tradecost_buy_plus_sell = 15):
    return np.round(100*earnings_total/first_buy,2)

def get_earnings_GD(days,dff,args,fig,investment=20000,tradecost_buy_plus_sell = 15):
    '''
    sell: if any course drops below GD -> sell
            if "Open" ing price < GD --> sell for "Open"ing price
            if "Open" ing price > GD --> sell for GD
    buy:  if any course goes > GD -> buy
            take minimum of all prices, if minimum < GD -> buy for GD
                                        if minimum > GD -> buy for minimum
    '''
    df = dff.copy()
    gd_ = GD(days,df)
    y_max = df[["Open", "Close","High","Low"]].max(axis=1)
    y_min = df[["Open", "Close","High","Low"]].min(axis=1)
    df.insert(1, "buy", 0., True)
    df.insert(1, "sell", 0., True)
    df.insert(1, "earnings", 0., True)
    df.insert(1, "GD"+str(days), gd_, True)
    #df = df.drop(np.arange(210,len(df)))
    #df = df.drop(np.arange(0,199))

    # get fist buy
    kriterium_buy = (y_max-gd_)>0
    kriterium_sell = (df.Low-gd_)<0
    have_stocks = False
    have_stocks_bought_for = False
    earnings_total = 0
    trades = 0
    first_buy = False
    first_buy_date = False
    for idx, row in df.iterrows():
        # skip days before start_trading_at variable
        if idx == 0: continue
        if df['Date'][idx] < start_trading_at:
            #print('skipping',idx)
            continue
        ############################################################
        # buy, if we were < GD the day before and are today > GD
        #       in fact we dont know the "Close"ing price
        #       but in case the 'Closing'price would drop below GD, we would sell again.
        ############################################################
        if have_stocks == False and df['Close'][idx-1] < gd_[idx-1] and y_max[idx] > gd_[idx]:
            # print(df.loc[idx:idx])
            # but if > GD at the beginning of the day.
            if df['Open'][idx] > gd_[idx]:
                # if open course > gd, buy for open
                df.loc[idx,'buy'] = df['Open'][idx]
                have_stocks = True
                trades += 1
            elif df['Open'][idx] < gd_[idx] and df['Close'][idx] > gd_[idx]:
                # here it is ok to use Close, we dont know Close but we buy wen price > GD
                # and in case the price should have dropped below GD we would have sold again, for GD.
                df.loc[idx,'buy'] = gd_[idx]
                have_stocks = True
                trades += 1
            elif df['Open'][idx] < gd_[idx] and df['Close'][idx] < gd_[idx]:
                # we never buy below GD or sell if it drops below
                trades += 1
            if have_stocks == True:
                have_stocks_bought_for = df.loc[idx,'buy']
                if first_buy == False:
                    first_buy = df.loc[idx,'buy']
                    first_buy_date = df.loc[idx,'Date']
                if args.verbose > 1:
                    print('buy  : idx',idx,'|',df['Date'][idx],df['buy'][idx],df.loc[idx,'buy'])
            # continue # to make sure not to sell at the same day
        ############################################################
        # sell, if we were > GD the day before and are today < GD
        #       although in principle we dont know the 'Close'ing price
        #       we would rebuy if the 'Closing' prince went > GD
        ############################################################
        if have_stocks == True and df['Close'][idx] < gd_[idx]:
            df.loc[idx,'sell'] = gd_[idx]
            have_stocks = False
            earnings_trade = df.loc[idx,'sell'] - have_stocks_bought_for
            earnings_total = earnings_total + earnings_trade
            if args.verbose > 1:
                print('sell : idx',idx,'|',df['Date'][idx],df['sell'][idx],df.loc[idx,'sell'],'trade',np.round(earnings_trade,5),'earn_tot',np.round(earnings_total,5))

    #print('evaluated, have_stocks:',have_stocks,'earn_tot',np.round(earnings_total,5))
    if args.plot:
        fig.add_trace(go.Scatter(
                    mode='markers',
                    marker=dict(size=10,color='green'),
                    x=df.Date,
                    y=df.buy,
                    name="buy_"+str(days)))
        fig.add_trace(go.Scatter(
                    mode='markers',
                    marker=dict(size=5,color='red'),
                    x=df.Date,
                    y=df.sell,
                    name="sell_"+str(days)))
    if args.verbose:
        print('earned in % (GD'+str(days).ljust(5)+'):',str(np.round(100*earnings_total/first_buy,2))+" %. Trades:"+str(trades).ljust(3)) #+" first buy",first_buy_date,'for',first_buy,'sold for')
    return fig

def check_course_and_derivative(days,df):
    GD200_all   = GD(days,df)
    GD200       = GD200_all.iloc[-1]
    GD200d_all  = GD200_all.diff()
    #print('xx')
    #print(GD200_all.diff())
    #print('GDxx',GD200_all.diff().iloc[-1])
    GD200d      = GD200d_all.iloc[-1]
    YL          = df.Close.iloc[-1]
    der         = np.round(10000*GD200d/GD200,0)

    if np.isnan(der): # == np.nan:
        pass
    else:
        #print('der',der,type(der))
        der = int(der)
    return YL, np.round(GD200,2), der

def print_colored(TrueFalse):
    if TrueFalse == True:
        return printturquise('T') #rue ')
    else:
        return printred('F') #alse')

def pf(zahl,length=4):
    #print('zahl',zahl)
    if np.isnan(zahl):
        pass
    else:
        zahl = int(zahl)
    out = str(zahl).ljust(length)
    #print('len(out',len(out),zahl)
    return out

def pc(TrueFalse):
    return print_colored(TrueFalse)

def pcc(name,pcc,ljust=10):
    if name in pcc:
        name = name + " "*(10-len(name))
        #print('name:'+name+":",len(name))
        return printblue(name).ljust(ljust)
    else:
        return name.ljust(ljust)

def pHAVE(HAVE,digits):
    if HAVE == False:
        return str(" ").ljust(digits)
    else:
        return str(HAVE).ljust(digits)

def pcH(name,MARK=False,ljust=10):
    name = name.strip() + " "*(ljust-len(name.strip()))
    #print('name',name,'MARK',MARK,'ljust',ljust)

    # The most important ones should be on top
    if len({"S","V"}.intersection(MARK)) > 0:       return "  "+printredbackground(name).ljust(ljust)
    if len({"B","K"}.intersection(MARK)) > 0:       return "  "+printgreenbackground(name).ljust(ljust)
    if len({"C"}.intersection(MARK)) > 0:           return "  "+printpinkbackground(name).ljust(ljust)
    if len({"H"}.intersection(MARK)) > 0:           return "  "+printblue(name).ljust(ljust)
    if len({"+"}.intersection(MARK)) > 0:           return "+ "+printturquise(name).ljust(ljust)

    if len({'!'}.intersection(MARK)) > 0:           return '! '+(name).ljust(ljust)
    if len({"M"}.intersection(MARK)) > 0:           return "* "+(name).ljust(ljust)
    else: #have == False:
                                                    return "  "+name.ljust(ljust)

def printoutcolor(mycolor,var):
    #ENDC = '\x1b[0m'
    ENDC = '\033[0m'
    if len(var) == 1:
        return mycolor + str(var[0]) + ENDC
    else:
        return mycolor + str(var) + ENDC

def printred(*var):
    ''' print(my.printred("min_at "+str(min_at)+" min_at_orig "+str(min_at_orig)+' (min id '+str(min_at_id)),"this is just an output") '''
    red = '\033[31m'
    return printoutcolor(red,var)

def printgreen(*var):
    ''' print(my.printred("min_at "+str(min_at)+" min_at_orig "+str(min_at_orig)+' (min id '+str(min_at_id)),"this is just an output") '''
    red = '\033[32m'
    #return printoutcolor(red,var)
    #return printoutcolor('\x1b[6;30;42m',var)
    return printoutcolor('\x1b[0;32;6m',var)

def printgreenbackground(*var):
    return printoutcolor('\x1b[6;30;42m',var)
def printpinkbackground(*var):
    return printoutcolor('\x1b[6;30;45m',var)

def printredbackground(*var):
    return printoutcolor('\x1b[0;30;41m',var)

def printturquise(*var):
    return printoutcolor('\x1b[0;36;6m',var)

def printblue(*var):
    red = '\033[34m'
    return printoutcolor(red,var)


def pr(var):
    return printred(var)

def pg(var):
    return printgreen(var)

def printhorizontal():
    print('-'*140)


def print_stoploss(stoploss,HAVE,YL,GD40,GD20,GD15,GD10,GD7):
    #print('stoploss',stoploss,'type',type(stoploss))
    #print(GD10)
    if HAVE == False:
        text = "  "
    else:
        col = 'red'
        if stoploss == 7 and YL > GD7:
            col = 'green'
        if stoploss == 10 and YL > GD10:
            col = 'green'
        if stoploss == 15 and YL > GD15:
            col = 'green'
        if stoploss == 20 and YL > GD20:
            col = 'green'
        if stoploss == 40 and YL > GD40:
            col = 'green'
        text = colored(str(stoploss).ljust(2), col, attrs=['reverse', 'blink'])
    return text

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    out = ret[n - 1:] / n
    #print('lo',len(out))
    #print('li',len(a))
    for i in np.arange(len(a)-len(out)):
        #print('i',i)
        out = np.append(out,out[-1])
    #print('lo2',len(out))
    #print('li2',len(a))
    #sys.exit()
    return out

def get_rsi_timeseries(prices, n=14,atl=False):
    '''
    same as get_rsi( array, n = 14 ) but much slower
    from https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
    # RSI = 100 - (100 / (1 + RS))
    # where RS = (Wilder-smoothed n-period average of gains / Wilder-smoothed n-period average of -losses)
    # Note that losses above should be positive values
    # Wilder-smoothing = ((previous smoothed avg * (n-1)) + current value to average) / n
    # For the very first "previous smoothed avg" (aka the seed value), we start with a straight average.
    # Therefore, our first RSI value will be for the n+2nd period:
    #     0: first delta is nan
    #     1:
    #     ...
    #     n: lookback period for first Wilder smoothing seed value
    #     n+1: first RSI
    '''
    # First, calculate the gain or loss from one price to the next. The first value is nan so replace with 0.
    deltas = (prices-prices.shift(1)).fillna(0)
    if atl == True:
        deltas = ((prices-prices.shift(1))/prices.shift(1)).fillna(0)
    # Calculate the straight average seed values.
    # The first delta is always zero, so we will use a slice of the first n deltas starting at 1,
    # and filter only deltas > 0 to get gains and deltas < 0 to get losses
    avg_of_gains = deltas[1:n+1][deltas > 0].sum() / n
    avg_of_losses = -deltas[1:n+1][deltas < 0].sum() / n

    # Set up pd.Series container for RSI values
    rsi_series = pd.Series(0.0, deltas.index)

    # Now calculate RSI using the Wilder smoothing method, starting with n+1 delta.
    up = lambda x: x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        avg_of_gains = ((avg_of_gains * (n-1)) + up(d)) / n
        avg_of_losses = ((avg_of_losses * (n-1)) + down(d)) / n
        if avg_of_losses != 0:
            rs = avg_of_gains / avg_of_losses
            rsi_series[i] = 100 - (100 / (1 + rs))
        else:
            rsi_series[i] = 100
        i += 1

    return rsi_series

@nb.jit(fastmath=True, nopython=True)
def calc_rsi( array, deltas, avg_gain, avg_loss, n ):
    '''# Use Wilder smoothing method'''
    up   = lambda x:  x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in deltas[n+1:]:
        avg_gain = ((avg_gain * (n-1)) + up(d)) / n
        avg_loss = ((avg_loss * (n-1)) + down(d)) / n
        if avg_loss != 0:
            rs = avg_gain / avg_loss
            array[i] = 100 - (100 / (1 + rs))
        else:
            array[i] = 100
        i += 1

    return array

def get_rsi( array, n = 14,atl=False ):
    deltas = np.append([0],np.diff(array))
    if atl==True:
        deltas = deltas/array.to_numpy()

    avg_gain =  np.sum(deltas[1:n+1].clip(min=0)) / n
    avg_loss = -np.sum(deltas[1:n+1].clip(max=0)) / n

    array = np.empty(deltas.shape[0])
    array.fill(np.nan)

    array = calc_rsi( array, deltas, avg_gain, avg_loss, n )
    return array

def print_GD(days,df):
    YL, GD200, GD200d = check_course_and_derivative(days,df)
    return pc(YL>GD200),pc(GD200d>0),pf(GD200d)

def lHAVE_HEBEL(liste,word):
    #print('liste',liste)
    #print('word',word,len(word))
    HAVE = False
    HEBEL = ""
    for idx,i in enumerate(liste):
        if idx > 0:
            if type(i) == str:
                if len(i) > 2:
                    if i[0:2] == "H_":
                        HAVE = int(i[2:])
                    else:
                        HEBEL = i
            #print('i',i,word in i)
    return HAVE,HEBEL


if __name__ == '__main__':
    todays_day = datetime.datetime.today().day
    p = help()
    args = p.parse_args()
    d = stocks_to_load(args)  # this decides if two or all
    if args.verbose:
        for idx,i in enumerate(d):
            print('dict key:',i,'dict value:',d[i])


    # what to sort by
    #print('args.sortbyGD',args.sortbyGD)
    if args.sortbyGD == False:
        sortbyGD = 100
    else:
        sortbyGD = args.sortbyGD[0]



    #print('args.name',args.name)
    if args.verbose: print('args.name',args.name)
    outlist = []
    o = {};
    df_all = {};
    for name in d:
        df,ID = load_stock_data(name,args) #,dlower)
        if args.verbose > 1:
            print('dflen',len(df),'name',name,'ID',ID)
        df_all[ID] = df

        firstdate = df_get_firstdate(df,args)
        lastdate  = df_get_lastdate(df,args)
        start_trading_at = firstdate + datetime.timedelta(days=200)
        if args.details:
            print('start_trading_at :',start_trading_at)

        if args.plot:
            fig     = go.Figure()
            fig     = fig_add_stock_data(fig,df,name,low=True,high=True,open_=True,close=True)
            fig     = fig_add_GD(fig,40)
            fig     = fig_add_GD(fig,15)
        else:
            fig     = False

        # calculate diff strategies
        #get_earnings_notrade(df,start_trading_at)
        #fig = get_earnings_GD(200,df,args,fig)
        #stopploss = ""
        #if len(dlower[name]) > 2:
        #    stoploss = dlower[name][1]
        YL,  GD40, sortby = check_course_and_derivative(sortbyGD,df)
        outlist.append([name,ID,sortby]) #,stoploss])



    if args.plot:
        fig.show()

    ###############################################################
    # sort how to show stock
    ###############################################################
    print('>>>>>>>>>>>>>>>>>>> sortbyGD >>>>>>>>>>>>>>>:',sortbyGD)
    dout = pd.DataFrame(outlist, columns = ['Name','ID','sortby'])
    dout = dout.sort_values(by=['sortby'], ascending=False,na_position='last')
    outlist_sorted_by_sortby = dout.values.tolist()
    #print('outlist',outlist_sorted_by_sortby)
    #sys.exit()

    if args.plot_derivative_pressure_intraday:
        fig     = go.Figure()

    idx = 0
    print_h1 = False
    print_h2 = False
    print_h3 = False

    for whichlist in ['T','H','R']:
        for name,ID,sortby in outlist_sorted_by_sortby:
            MARK = set(d[name]).intersection(set(list(string.ascii_uppercase)+['!']))
            #def continue_or_not(whichlist,MARK,show):
            #print('whichlist',whichlist,'name',name,'MARK',MARK,'hasT?',len({'T'}.intersection(MARK)))
            if whichlist == 'T':
                if len({'T'}.intersection(MARK)) > 0:
                    pass
                else:
                    continue

            if whichlist == 'H':
                if print_h2 == False:
                    printhorizontal()
                    print_h2 = True
                if len({'H'}.intersection(MARK)) > 0:
                    pass
                else:
                    continue

            if whichlist == 'R':
                if print_h3 == False:
                    printhorizontal()
                    print_h3 = True
                if len({'H','T'}.intersection(MARK)) == 0:
                    pass
                else:
                    continue

            #continue_or_not(whichlist,MARK,'T')
            #continue_or_not(whichlist,MARK,'H')

            idx += 1
            df = df_all[ID]
            Close = df.Close.iloc[-1]

            printit = True
            if print_h1: printit = False
            MARK = set(d[name]).intersection(set(list(string.ascii_uppercase)+['!']))
            #print('name',name,'set',set(d[name]),'set2',set(list(string.ascii_uppercase)+['!']))
            REST = set(d[name]).difference(set(list(string.ascii_uppercase)+['!','+']+[ID]))
            if len(REST) == 0: REST = ""
            #print('rest',REST)
            #print('MARK',MARK)
            if len(MARK) > 0: printit = True
            #print('name',name,'MARK',MARK)

            RSI14  = get_rsi(df.Close,n=14,atl=False)
            RSI20  = get_rsi(df.Close,n=20,atl=False)
            RSI14n = get_rsi(df.Close,n=14,atl=True)
            RSI9   = get_rsi(df.Close,n=9,atl=False)
            RSI7   = get_rsi(df.Close,n=7)
            RSI7n  = get_rsi(df.Close,n=7,atl=True)

            rsi14  = RSI14[-1]
            rsi14n = RSI14n[-1]
            rsi9   = RSI9[-1]
            rsi7   = RSI7[-1]
            rsi7n  = RSI7n[-1]

            if rsi14 < 20 or rsi14n < 20 or rsi9 < 18 or rsi7 < 15 or rsi7n < 15:
                printit = True


            if printit:
                invest = ""
                if args.plot_derivative_pressure_intraday:
                    dplotx= np.arange(0,240)
                    dploty= np.zeros(len(dplotx))
                    for idx_GDd,d_ in enumerate(dplotx):
                        tmp, GDxx, GDxxd = check_course_and_derivative(int(d_),df)
                        if np.isnan(GDxxd):
                            pass
                        else:
                            dploty[idx_GDd] =  GDxxd
                    #import matplotlib.pyplot as plt
                    #plt.plot(dplotx,dploty,label=name)
                    #plt.legend()
                    invest = int(dploty.sum()/100.)
                    if args.plot_derivative_pressure_intraday:
                        #fig.add_trace(go.Scatter(
                        #    x=dplotx,
                        #    y=dploty,
                        #    name=name)) #,
                            #opacity=0.8))
                        #dplotysmooth = moving_average(dploty,5)
                        #dplotysmooth10 = moving_average(dploty,1)
                        # this is only a first approximation ...
                        dplotysmooth20 = moving_average(dploty,20)
                        # my_smoothed_average:
                        # Base: e.g. 1/10 zu jeder seite
                        # GD200: 20 left and 20 right
                        # GD100: 10 left and 10 right
                        # GD20:  2 left and 2  right
                        ratio = 0.2
                        smoothed_mean = np.copy(dploty)
                        for gd,i in enumerate(dploty):
                            fenster = int(dplotx[gd]*ratio)
                            f_val = dploty[gd-fenster:gd+fenster]

                            smoothed_mean[gd] = dploty[gd-fenster:gd+fenster].mean()
                            #print('gd',gd,'dplotx[gd]:',dplotx[gd],'dploty[gd]:',dploty[gd],fenster,'smoothed',smoothed_mean[gd],'len',len(f_val))

                        #fig.add_trace(go.Scatter(
                        #    x=dplotx,
                        #    y=dplotysmooth20,
                        #    name=name+'_smooth20'))
                        fig.add_trace(go.Scatter(
                            x=dplotx[19:],
                            y=smoothed_mean[19:],
                            name=name+'_smooth20'))

                        #fig.show()
                        #sys.exit()


                printGD_nr = [ 200, 100, 50, 20]
                printGD2 = []
                for i in printGD_nr:
                    printGD2.append(print_GD(i,df)[0]) #+"|"
                    printGD2.append(print_GD(i,df)[1]) #+"|"
                    printGD2.append(print_GD(i,df)[2]) #+"|"


                if idx == 1:
                    a = " "
                    for i in printGD_nr:
                        a = a + "GD"+str(i).ljust(6)+"| "
                    a = a + " Close   |"
                    a = a + " RSI14 "
                    a = a + " RSI9 |"
                    a = a + " RSI7 |"
                    a = a + " 1D % |"
                    a = a + " name |"
                    print(a)
                    printhorizontal()


                la = 100*df.Close.diff().iloc[-1]/df.Close.iloc[-1]
                la = np.round(la,1)
                def lc(df,ljust=4):
                    la = 100*df.Close.diff().iloc[-1]/df.Close.iloc[-1]
                    la = np.round(la,1)
                    if la >=0:
                        if la == 0.0:
                            la = 0.0
                        if la > 10:
                            return printgreen(str(la))
                        else:
                            return printgreen(" "+str(la))
                    else:
                        if la < -10:
                            #print('la<10:',la)
                            return printred(int(la))+" "
                        else:
                            return printred(la)


                def printRSI(rsi,dig=1,ljust=3):
                    if 80 < rsi < 100:
                        return printred(str(np.round(rsi,dig)).ljust(ljust))+" |"
                    #elif rsi < 50:
                    elif 30 < rsi < 50:
                        return printgreen(str(np.round(rsi,dig)).ljust(ljust))+" |"
                    elif 0 < rsi < 30:
                        add = " "
                        if rsi < 10: add = "  "
                        return printturquise(str(np.round(rsi,dig)).ljust(ljust))+add+"|"
                    else:
                        return str(np.round(rsi,dig)).ljust(ljust)+" |"
                #lastdate  = df_get_lastdate(df,args)
                #lastday = int(lastdate.split('-')[2])

                lastday = df.Date.iloc[-1].day
                def dd(df,todays_day):
                    lastday = df.Date.iloc[-1].day
                    days_diff = lastday-todays_day
                    if days_diff == 0:
                        return "".ljust(2)
                    else:
                        return str(days_diff).ljust(2)

                def printClose(Close,short):
                    if short[-2:] in ['.F']:
                        a = "€"
                    elif short[-3:] in ['.SG','.DE']:
                        a = "€"
                    else:
                        a = '$'
                    dig = 2
                    if Close >= 1000:
                        dig = 1
                    if Close >= 10000:
                        dig = 0
                    if dig > 0:
                        out = str(np.round(Close,dig)).ljust(6)
                    else:
                        out = (str(int(Close))+'.').ljust(6)
                    if short == '^VIX' and Close > 18:
                        out = printred(out)
                    #print('sho',short)
                    return "| "+out+" "+a+"|"
                    #    return "| "+str(np.round(Close,dig)).ljust(6)+" "+a+"|"
                    #else:
                    #    return "| "+(str(int(Close))+'.').ljust(6)+" "+a+"|"

                #print('l-l',lastday-todays_day)
                # finally print the thing
                print(
                        *printGD2,
                    printClose(Close,d[name][0]),
                    #pHAVE(HAVE,2),'|',
                    printRSI(rsi14),
                    printRSI(rsi9),
                    printRSI(rsi7),
                    str(lc(df)).ljust(4),"|",
                    dd(df,todays_day),"|",
                    str(ID).ljust(7),
                    pcH(name,MARK,11),
                    REST
                    )
                if name.lower() == 'microsoft':
                    printhorizontal()
                    print_h1 = True

        if args.plot_derivative_pressure_intraday:
            fig.show()


