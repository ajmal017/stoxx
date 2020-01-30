# stoxx: a simple tool to analyze stock data. 

The stock data is loaded from yahoo and simple analysis can be performed as e.g. the 20/200 days moving average (in German: GD20, GD200)).

__How to get:__  
git clone https://github.com/glensk/stoxx

__How to use:__  
python stoxx bayer -p

__Output:__  
earned (notrade): 130.08 % first buy 1997-10-17 for 32.70539855957031 sold for 75.25 on last day.  
earned (GD200  ): 379.25 %159 first buy 1997-10-22 00:00:00 for 34.81869888305664 sold for.  
earned (GD150  ): 412.03 %199 first buy 1998-01-02 00:00:00 for 34.46851060231527 sold for.  
earned (GD100  ): 405.58 %313 first buy 1997-12-30 00:00:00 for 33.96329879760742 sold for.  
earned (GD50   ): 614.82 %421 first buy 1997-11-20 00:00:00 for 33.2036018371582 sold for.  
earned (GD20   ): 1044.8 %700 first buy 1997-11-17 00:00:00 for 31.246200561523438 sold for.  

![picture alt](/images/bayer_GD200.png "Bayer chart")

__TODO:__  
 * Check if GD200 is correct (compare to boerse.de, dont consider intra day).
 * Update stock data.
 * Implement other criteria.
 * Print wins/losses in plot. 
 * Show several stocks.
 * get rid of red/green line at bottom of plot.
