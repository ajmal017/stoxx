# stoxx: simple tool summarizing a few indicators of your stock portfolio.

The stock data is loaded from yahoo. You can simply add the stocks (companies) you care for. RSI's and moving averages are summarized for your portfolio.

__How to get:__  
git clone https://github.com/glensk/stoxx

__How to use:__  
 * python stoxx                 (to get a summary of a few indicators of your portfolio)
 * python stoxx bayer -p        (to polot MA and stock price for a particular stock (here, bayer))

__Output:__  
| GD200  |  GD100  |  GD50   |  GD20   | Close   |RSI14 |RSI9  | RSI7 | 1D % |    | ID   | name           |
|--------|---------|---------|---------|---------|------|------|------|------|----|------|----------------|
|T T 69  | T T 109 | T T 288 | T T 443 | 36.82  $| 72.6 | 72.9 | 72.3 |  9.2 | -1 | ^VIX | Volatility     |
|F F 0   | F F -1  | F F -16 | F F -44 | 25917. $| 31.5 | 30.2 | 30.4 | -3.0 | -1 | ^DJI | DOW Jones      |
|T T 74  | T T 107 | T T 113 | F F -22 | 745.51 $| 51.9 | 47.7 | 45.8 |  0.3 | -1 | TSLA | Tesla          |
|T T 44  | T T 43  | T T 68  | T T 116 | 128.66 $| 60.6 | 59.0 | 57.3 |  0.0 | -1 | SEDG | SolarEdge      |  


* python stoxx bayer -p        (to polot MA and stock price for a particular stock (here, bayer))
![picture alt](/images/bayer_GD200.png "Bayer chart")

__TODO:__  
 * Implement TSI.
 * Implement MACD.
 
 
 __Note:__  
 [A much more complete analysis can be easily done on yahoo! finance following this link](https://finance.yahoo.com/chart/VAR1.SG#eyJpbnRlcnZhbCI6ImRheSIsInBlcmlvZGljaXR5IjoxLCJjYW5kbGVXaWR0aCI6My45ODQwNjM3NDUwMTk5MjAzLCJ2b2x1bWVVbmRlcmxheSI6dHJ1ZSwiYWRqIjp0cnVlLCJjcm9zc2hhaXIiOnRydWUsImNoYXJ0VHlwZSI6ImxpbmUiLCJleHRlbmRlZCI6ZmFsc2UsIm1hcmtldFNlc3Npb25zIjp7fSwiYWdncmVnYXRpb25UeXBlIjoib2hsYyIsImNoYXJ0U2NhbGUiOiJsaW5lYXIiLCJwYW5lbHMiOnsiY2hhcnQiOnsicGVyY2VudCI6MSwiZGlzcGxheSI6IlZBUjEuU0ciLCJjaGFydE5hbWUiOiJjaGFydCIsInRvcCI6MH19LCJzZXRTcGFuIjp7Im11bHRpcGxpZXIiOjEsImJhc2UiOiJ5ZWFyIiwicGVyaW9kaWNpdHkiOnsicGVyaW9kIjoxLCJpbnRlcnZhbCI6ImRheSJ9LCJtYWludGFpblBlcmlvZGljaXR5Ijp0cnVlLCJmb3JjZUxvYWQiOnRydWV9LCJsaW5lV2lkdGgiOjIsInN0cmlwZWRCYWNrZ3JvdWQiOnRydWUsImV2ZW50cyI6dHJ1ZSwiY29sb3IiOiIjMDA4MWYyIiwiZXZlbnRNYXAiOnsiY29ycG9yYXRlIjp7ImRpdnMiOnRydWUsInNwbGl0cyI6dHJ1ZX0sInNpZ0RldiI6e319LCJzeW1ib2xzIjpbeyJzeW1ib2wiOiJWQVIxLlNHIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IlZBUjEuU0cifSwicGVyaW9kaWNpdHkiOjEsImludGVydmFsIjoiZGF5IiwidGltZVVuaXQiOm51bGwsInNldFNwYW4iOnsibXVsdGlwbGllciI6MSwiYmFzZSI6InllYXIiLCJwZXJpb2RpY2l0eSI6eyJwZXJpb2QiOjEsImludGVydmFsIjoiZGF5In0sIm1haW50YWluUGVyaW9kaWNpdHkiOnRydWUsImZvcmNlTG9hZCI6dHJ1ZX19XSwiY3VzdG9tUmFuZ2UiOm51bGwsInRpbWVVbml0IjpudWxsLCJzdHVkaWVzIjp7InZvbCB1bmRyIjp7InR5cGUiOiJ2b2wgdW5kciIsImlucHV0cyI6eyJpZCI6InZvbCB1bmRyIiwiZGlzcGxheSI6InZvbCB1bmRyIn0sIm91dHB1dHMiOnsiVXAgVm9sdW1lIjoiIzAwYjA2MSIsIkRvd24gVm9sdW1lIjoiI0ZGMzMzQSJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJ3aWR0aEZhY3RvciI6MC40NSwiY2hhcnROYW1lIjoiY2hhcnQifX0sIuKAjG1h4oCMICgyMCxDLG1hLDApIjp7InR5cGUiOiJtYSIsImlucHV0cyI6eyJQZXJpb2QiOiIyMCIsIkZpZWxkIjoiQ2xvc2UiLCJUeXBlIjoic2ltcGxlIiwiT2Zmc2V0IjowLCJpZCI6IuKAjG1h4oCMICgyMCxDLG1hLDApIiwiZGlzcGxheSI6IuKAjG1h4oCMICgyMCxDLG1hLDApIn0sIm91dHB1dHMiOnsiTUEiOiIjZmZlNzg2In0sInBhbmVsIjoiY2hhcnQiLCJwYXJhbWV0ZXJzIjp7ImNoYXJ0TmFtZSI6ImNoYXJ0In19LCLigIxtYeKAjCAoMTAsQyxtYSwwKSI6eyJ0eXBlIjoibWEiLCJpbnB1dHMiOnsiUGVyaW9kIjoiMTAiLCJGaWVsZCI6IkNsb3NlIiwiVHlwZSI6InNpbXBsZSIsIk9mZnNldCI6MCwiaWQiOiLigIxtYeKAjCAoMTAsQyxtYSwwKSIsImRpc3BsYXkiOiLigIxtYeKAjCAoMTAsQyxtYSwwKSJ9LCJvdXRwdXRzIjp7Ik1BIjoiI2FkNmVmZiJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJjaGFydE5hbWUiOiJjaGFydCJ9fSwi4oCMbWHigIwgKDUsQyxtYSwwKSI6eyJ0eXBlIjoibWEiLCJpbnB1dHMiOnsiUGVyaW9kIjoiNSIsIkZpZWxkIjoiQ2xvc2UiLCJUeXBlIjoic2ltcGxlIiwiT2Zmc2V0IjowLCJpZCI6IuKAjG1h4oCMICg1LEMsbWEsMCkiLCJkaXNwbGF5Ijoi4oCMbWHigIwgKDUsQyxtYSwwKSJ9LCJvdXRwdXRzIjp7Ik1BIjoiIzY0ZjFkOSJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJjaGFydE5hbWUiOiJjaGFydCJ9fX19)
