# stoxx: a simple tool to load and analyze stock data. 

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
 
 
 __Note:__  
 [A much more complete analysis can be easily done on yahoo! finance following this link](https://finance.yahoo.com/chart/VAR1.SG#eyJpbnRlcnZhbCI6ImRheSIsInBlcmlvZGljaXR5IjoxLCJjYW5kbGVXaWR0aCI6My45ODQwNjM3NDUwMTk5MjAzLCJ2b2x1bWVVbmRlcmxheSI6dHJ1ZSwiYWRqIjp0cnVlLCJjcm9zc2hhaXIiOnRydWUsImNoYXJ0VHlwZSI6ImxpbmUiLCJleHRlbmRlZCI6ZmFsc2UsIm1hcmtldFNlc3Npb25zIjp7fSwiYWdncmVnYXRpb25UeXBlIjoib2hsYyIsImNoYXJ0U2NhbGUiOiJsaW5lYXIiLCJwYW5lbHMiOnsiY2hhcnQiOnsicGVyY2VudCI6MSwiZGlzcGxheSI6IlZBUjEuU0ciLCJjaGFydE5hbWUiOiJjaGFydCIsInRvcCI6MH19LCJzZXRTcGFuIjp7Im11bHRpcGxpZXIiOjEsImJhc2UiOiJ5ZWFyIiwicGVyaW9kaWNpdHkiOnsicGVyaW9kIjoxLCJpbnRlcnZhbCI6ImRheSJ9LCJtYWludGFpblBlcmlvZGljaXR5Ijp0cnVlLCJmb3JjZUxvYWQiOnRydWV9LCJsaW5lV2lkdGgiOjIsInN0cmlwZWRCYWNrZ3JvdWQiOnRydWUsImV2ZW50cyI6dHJ1ZSwiY29sb3IiOiIjMDA4MWYyIiwiZXZlbnRNYXAiOnsiY29ycG9yYXRlIjp7ImRpdnMiOnRydWUsInNwbGl0cyI6dHJ1ZX0sInNpZ0RldiI6e319LCJzeW1ib2xzIjpbeyJzeW1ib2wiOiJWQVIxLlNHIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IlZBUjEuU0cifSwicGVyaW9kaWNpdHkiOjEsImludGVydmFsIjoiZGF5IiwidGltZVVuaXQiOm51bGwsInNldFNwYW4iOnsibXVsdGlwbGllciI6MSwiYmFzZSI6InllYXIiLCJwZXJpb2RpY2l0eSI6eyJwZXJpb2QiOjEsImludGVydmFsIjoiZGF5In0sIm1haW50YWluUGVyaW9kaWNpdHkiOnRydWUsImZvcmNlTG9hZCI6dHJ1ZX19XSwiY3VzdG9tUmFuZ2UiOm51bGwsInRpbWVVbml0IjpudWxsLCJzdHVkaWVzIjp7InZvbCB1bmRyIjp7InR5cGUiOiJ2b2wgdW5kciIsImlucHV0cyI6eyJpZCI6InZvbCB1bmRyIiwiZGlzcGxheSI6InZvbCB1bmRyIn0sIm91dHB1dHMiOnsiVXAgVm9sdW1lIjoiIzAwYjA2MSIsIkRvd24gVm9sdW1lIjoiI0ZGMzMzQSJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJ3aWR0aEZhY3RvciI6MC40NSwiY2hhcnROYW1lIjoiY2hhcnQifX0sIuKAjG1h4oCMICgyMCxDLG1hLDApIjp7InR5cGUiOiJtYSIsImlucHV0cyI6eyJQZXJpb2QiOiIyMCIsIkZpZWxkIjoiQ2xvc2UiLCJUeXBlIjoic2ltcGxlIiwiT2Zmc2V0IjowLCJpZCI6IuKAjG1h4oCMICgyMCxDLG1hLDApIiwiZGlzcGxheSI6IuKAjG1h4oCMICgyMCxDLG1hLDApIn0sIm91dHB1dHMiOnsiTUEiOiIjZmZlNzg2In0sInBhbmVsIjoiY2hhcnQiLCJwYXJhbWV0ZXJzIjp7ImNoYXJ0TmFtZSI6ImNoYXJ0In19LCLigIxtYeKAjCAoMTAsQyxtYSwwKSI6eyJ0eXBlIjoibWEiLCJpbnB1dHMiOnsiUGVyaW9kIjoiMTAiLCJGaWVsZCI6IkNsb3NlIiwiVHlwZSI6InNpbXBsZSIsIk9mZnNldCI6MCwiaWQiOiLigIxtYeKAjCAoMTAsQyxtYSwwKSIsImRpc3BsYXkiOiLigIxtYeKAjCAoMTAsQyxtYSwwKSJ9LCJvdXRwdXRzIjp7Ik1BIjoiI2FkNmVmZiJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJjaGFydE5hbWUiOiJjaGFydCJ9fSwi4oCMbWHigIwgKDUsQyxtYSwwKSI6eyJ0eXBlIjoibWEiLCJpbnB1dHMiOnsiUGVyaW9kIjoiNSIsIkZpZWxkIjoiQ2xvc2UiLCJUeXBlIjoic2ltcGxlIiwiT2Zmc2V0IjowLCJpZCI6IuKAjG1h4oCMICg1LEMsbWEsMCkiLCJkaXNwbGF5Ijoi4oCMbWHigIwgKDUsQyxtYSwwKSJ9LCJvdXRwdXRzIjp7Ik1BIjoiIzY0ZjFkOSJ9LCJwYW5lbCI6ImNoYXJ0IiwicGFyYW1ldGVycyI6eyJjaGFydE5hbWUiOiJjaGFydCJ9fX19){:target='_blank'}
