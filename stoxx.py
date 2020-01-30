#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import pandas as pd
import os,sys,argparse,datetime
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = 'browser'

def help(p = None):
    string = ''' helptext '''
    p = argparse.ArgumentParser(description=string,
            formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('name', metavar='name', type=str, nargs=1,
                    help='the name of the stock, e.g. bayer, infineon')
    p.add_argument('-p','--plot', help='plot to browser', action='count', default=False)
    p.add_argument('-v','--verbose', help='verbose', action='count', default=False)
    return p

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date

d = {};
d['wirecard']   = ['WDI.DE','2015-01-01']
d['bayer']      = ['BAYN.DE','1990-01-01','1997-10-17']
d['adidas']     = ['ADS.DE','2000-01-01']
d['infineon']   = ['IFX.DE','2000-01-01']

def load_stock_data(name):
    folder = 'stock_data'
    print('name       :',name)
    print('stock short:',d[name][0])
    print('data_from  :',d[name][1])
    filename = folder+'/'+d[name][0]+'.pkl'
    if not os.path.isdir('stock_data'):
        os.mkdir(folder)
    print('filename   :',filename)
    if os.path.isfile(filename):
        print('loading from',filename)
        df = pd.read_pickle(filename)
    else:
        print('downloading data from yahoo')
        df = yf.download(d[name][0],d[name][1])
        df = df.reset_index()
        df.to_pickle(filename)
    return df

def fig_add_stock_data(fig,df,title_text,low=True,high=True,open_=True,close=True):
    op=1.0
    fill='tonexty' # [ 'none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx', 'toself', 'tonext']
    fill='none'
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

def gd(days,df):
    ''' days [integer] for rolling average; e.g. GD200 '''
    return df.Close.rolling(days).mean()

def fig_add_gd(fig,days):
    '''
    fig: [plotly object]
    days [integer] for rolling average; e.g. GD200 '''
    gd_=gd(days=days,df=df)
    #df.insert(2, "GD"+str(days), gd_, True)
    fig.add_trace(go.Scatter(
                x=df.Date,
                y=gd_,
                name="GD"+str(days),
                line_color='black',
                opacity=0.8))
    return fig

def df_get_lastdate(df,idx=-1):
    date = str(df['Date'][df.index[idx]]).split()[0]
    print('lastdate     :',date)
    return datestr_to_datetiem(date)

def datestr_to_datetiem(date):
    y = int(date.split('-')[0])
    m = int(date.split('-')[1])
    d = int(date.split('-')[2])
    return datetime.date(y, m, d)

def df_get_firstdate(df,idx=0):
    date = str(df['Date'][df.index[idx]]).split()[0]
    print('firstdate    :',date)
    return datestr_to_datetiem(date)

def get_earnings_notrade(df,start_trading_at=False,verbose=True):
    ''' buy at first day, dont lock at stock, sell at the last day '''
    if start_trading_at == False:
        buy = df.dropna()['Open'][df.dropna().index[0]]
    else:
        #print('xx start_trading_at',start_trading_at)
        #print('start:',datetime.date(start_trading_at))
        #print('start2:',pd.Timestamp(datetime.date(1996, 12, 16)))
        #print(df['Date'] == datetime.date(start_trading_at))
        #buy = df[df.Date == pd.Timestamp(datetime.date(1996, 12, 16))].Open
        buy = float(df[df.Date == pd.Timestamp(start_trading_at)].Open)
    #print('buy (on first day):',buy,)
    sell  = df['Close'][df.index[-1]]
    #print('sell (on last day):',sell)
    earnings = sell - buy
    #print('earnings',earnings)
    print('earned (notrade):',str(np.round(100*earnings/buy,2))+" % first buy",start_trading_at,'for',buy,'sold for',sell,'on last day')
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

def get_earnings_gd(days,dff,args,fig,investment=20000,tradecost_buy_plus_sell = 15):
    '''
    sell: if any course drops below GD -> sell
            if "Open" ing price < GD --> sell for "Open"ing price
            if "Open" ing price > GD --> sell for GD
    buy:  if any course goes > GD -> buy
            take minimum of all prices, if minimum < GD -> buy for GD
                                        if minimum > GD -> buy for minimum
    '''
    df = dff.copy()
    gd_ = gd(days,df)
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
                if args.verbose:
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
            if args.verbose:
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
    print('earned (GD'+str(days).ljust(5)+'):',str(np.round(100*earnings_total/first_buy,2))+" %"+str(trades).ljust(3)+" first buy",first_buy_date,'for',first_buy,'sold for')
    return fig

if __name__ == '__main__':
    p = help()
    args = p.parse_args()
    for name in args.name:
        print('name',name)
        df = load_stock_data(name)
        start_trading_at = d[name][2]
        firstdate = df_get_firstdate(df)
        lastdate  = df_get_lastdate(df)
        start_trading_at = datestr_to_datetiem(d[name][2])
        print('start_trading_at:',start_trading_at)

        if args.plot:
            fig     = go.Figure()
            fig     = fig_add_stock_data(fig,df,name,low=True,high=True,open_=True,close=True)
            fig     = fig_add_gd(fig,200)
            fig     = fig_add_gd(fig,20)
        else:
            fig     = False

        # calculate diff strategies
        get_earnings_notrade(df,start_trading_at)
        fig = get_earnings_gd(200,df,args,fig)
        #fig = get_earnings_gd(150,df,args,fig)
        #fig = get_earnings_gd(100,df,args,fig)
        #fig = get_earnings_gd(50,df,args,fig)
        #fig = get_earnings_gd(20,df,args,fig)

        if args.plot:
            fig.show()
