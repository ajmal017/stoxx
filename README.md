# stoxx: simple tool summarizing a few indicators of your stock portfolio.

The stock data is loaded from yahoo. You can simply add the stocks (companies) you care for. RSI's and moving averages are summarized for your portfolioc. Plotting functionality for particular stock.

__How to get:__  
git clone https://github.com/glensk/stoxx

__How to use:__  
python stoxx                 # to get a summary of a few indicators of your portfolio
or 
python stoxx bayer -p        # to polot MA and stock price for a particular stock (here, bayer)

__Output:__  
 GD200    GD100    GD50     GD20     GD10      Close   | RSI14  RSI9 | RSI7 | 1D % | name |
------------------------------------------------------------------------------------------------------------------------------------------
T T 69   T T 109  T T 288  T T 443  T T 794  | 36.82  $| 72.6 | 72.9 | 72.3 |  9.2 | -1 | ^VIX      Volatility
F F 0    F F -1   F F -16  F F -44  F F -121 | 25917. $| 31.5 | 30.2 | 30.4 | -3.0 | -1 | ^DJI      DOW Jones
------------------------------------------------------------------------------------------------------------------------------------------
T T 74   T T 107  T T 113  F F -22  F F -142 | 745.51 $| 51.9 | 47.7 | 45.8 |  0.3 | -1 | TSLA      Tesla    
T T 44   T T 43   T T 68   T T 116  F T 154  | 128.66 $| 60.6 | 59.0 | 57.3 |  0.0 | -1 | SEDG      SolarEdge   
T T 18   T T 37   T T 28   F T 18   F F -74  | 33.6   €| 51.3 | 50.3 | 50.7 | 10.4 |    | ST5.F     STEICO     
T T 7    T T 32   F T 22   F T 13   F F -208 | 20.8   €| 43.4 | 38.9 | 36.5 |  2.9 |    | IQ8.F     Iqiyi    
T T 10   T T 30   F T 3    F T 52   F F -149 | 21.9   $| 42.1 | 34.7 | 28.7 | -4.5 | -1 | JKS       Jinkosolar  
...


![picture alt](/images/bayer_GD200.png "Bayer chart")

__TODO:__  
 * Implement TSI.
 * Implement MACD.
 
 
 __Note:__  
 [A much more complete analysis can be easily done on yahoo! finance following this link](https://finance.yahoo.com/chart/VAR1.SG#eyJpbnRlcnZhbCI6ImRheSIsInBlcmlvZGljaXR5IjoxLCJjYW5kbGVXaWR0aCI6My45ODQwNjM3NDUwMTk5MjAzLCJ2b2x1bWVVbmRlcmxheSI6dHJ1ZSwiYWRqIjp0cnVlLCJjcm9zc2hhaXIiOnRydWUsImNoYXJ0VHlwZSI6ImxpbmUiLCJleHRlbmRlZCI6ZmFsc2UsIm1hcmtldFNlc3Npb25zIjp7fSwiYWdncmVnYXRpb25UeXBlIjoib2hsYyIsImNoYXJ0U2NhbGUiOiJsaW5lYXIiLCJwYW5lbHMiOnsiY2hhcnQiOnsicGVyY2VudCI6MSwiZGlzcGxheSI6IlZBUjEuU0ciLCJjaGFydE5hbWUiOiJjaGFydCIsInRvcCI6MH19LCJzZXRTcGFuIjp7Im11bHRpcGxpZXIiOjEsImJhc2UiOiJ5ZWFyIiwicGVyaW9kaWNpdHkiOnsicGVyaW9kIjoxLCJpbnRlcnZhbCI6ImRheSJ9LCJtYWludGFpblBlcmlvZGljaXR5Ijp0cnVlLCJmb3JjZUxvYWQiOnRydWV9LCJsaW5lV2lkdGgiOjIsInN0cmlwZWRCYWNrZ3JvdWQiOnRydWUsImV2ZW50cyI6dHJ1ZSwiY29sb3IiOiIjMDA4MWYyIiwiZXZlbnRNYXAiOnsiY29ycG9yYXRlIjp7ImRpdnMiOnRydWUsInNwbGl0cyI6dHJ1ZX0sInNpZ0RldiI6e319LCJzeW1ib2xzIjpbeyJzeW1ib2wiOiJWQVIxLlNHIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IlZBUjEuU0cifSwicGVyaW9kaWNpdHkiOjEsImludGVydmFsIjoiZGF5IiwidGltZVVuaXQiOm51bGwsInNldFNwYW4iOnsibXVsdGlwbGllciI6MSwiYmFzZSI6InllYXIiLCJwZXJpb2RpY2l0eSI6eyJwZXJpb2QiOjEsImludGVydmFsIjoiZGF5In0sIm1haW50YWluUGVyaW9kaWNpdHkiOnRydWUsImZvcmNlTG9hZCI6dHJ1ZX19XSwiY3VzdG9tUmFuZ2UiOm51bGwsInRpbWVVbml0IjpudWxsLCJzdHVkaWVzIjp7InZvbCB1bmRyIjp7InR5cGUiOiJ2b2wgdW5kciIsImlucHV0cyI6eyJpZCI6InZvbCB1bmRyIiwiZGlzcGxheSI6InZvbCB1bmRyIn0sIm91dHB1dHMiOnsiVXAgVm9sdW1lIjoiIzAwYjA2MSIsIkRvd24gVm9sdW1lIjoiI0ZGMzMzQSJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJ3aWR0aEZhY3RvciI6MC40NSwiY2hhcnROYW1lIjoiY2hhcnQifX0sIuKAjG1h4oCMICgyMCxDLG1hLDApIjp7InR5cGUiOiJtYSIsImlucHV0cyI6eyJQZXJpb2QiOiIyMCIsIkZpZWxkIjoiQ2xvc2UiLCJUeXBlIjoic2ltcGxlIiwiT2Zmc2V0IjowLCJpZCI6IuKAjG1h4oCMICgyMCxDLG1hLDApIiwiZGlzcGxheSI6IuKAjG1h4oCMICgyMCxDLG1hLDApIn0sIm91dHB1dHMiOnsiTUEiOiIjZmZlNzg2In0sInBhbmVsIjoiY2hhcnQiLCJwYXJhbWV0ZXJzIjp7ImNoYXJ0TmFtZSI6ImNoYXJ0In19LCLigIxtYeKAjCAoMTAsQyxtYSwwKSI6eyJ0eXBlIjoibWEiLCJpbnB1dHMiOnsiUGVyaW9kIjoiMTAiLCJGaWVsZCI6IkNsb3NlIiwiVHlwZSI6InNpbXBsZSIsIk9mZnNldCI6MCwiaWQiOiLigIxtYeKAjCAoMTAsQyxtYSwwKSIsImRpc3BsYXkiOiLigIxtYeKAjCAoMTAsQyxtYSwwKSJ9LCJvdXRwdXRzIjp7Ik1BIjoiI2FkNmVmZiJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJjaGFydE5hbWUiOiJjaGFydCJ9fSwi4oCMbWHigIwgKDUsQyxtYSwwKSI6eyJ0eXBlIjoibWEiLCJpbnB1dHMiOnsiUGVyaW9kIjoiNSIsIkZpZWxkIjoiQ2xvc2UiLCJUeXBlIjoic2ltcGxlIiwiT2Zmc2V0IjowLCJpZCI6IuKAjG1h4oCMICg1LEMsbWEsMCkiLCJkaXNwbGF5Ijoi4oCMbWHigIwgKDUsQyxtYSwwKSJ9LCJvdXRwdXRzIjp7Ik1BIjoiIzY0ZjFkOSJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJjaGFydE5hbWUiOiJjaGFydCJ9fX19)
