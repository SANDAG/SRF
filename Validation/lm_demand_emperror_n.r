
Call:
lm(formula = EMP_AG_d ~ EMP_AG_DLUZ + EMP_TOTAL.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1256.73    -0.18    -0.02     0.22   370.76 

Coefficients:
                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)     0.0311749  0.0743219   0.419               0.675    
EMP_AG_DLUZ     0.0085163  0.0004443  19.166 <0.0000000000000002 ***
EMP_TOTAL.error 0.0036898  0.0002913  12.666 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 11.22 on 22999 degrees of freedom
Multiple R-squared:  0.02234,	Adjusted R-squared:  0.02225 
F-statistic: 262.8 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_AG_d ~ EMP_AG_DLUZ + EMP_TOTAL.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1256.73    -0.18    -0.02     0.22   370.76 

Coefficients:
                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)     0.0311749  0.0743219   0.419               0.675    
EMP_AG_DLUZ     0.0085163  0.0004443  19.166 <0.0000000000000002 ***
EMP_TOTAL.error 0.0036898  0.0002913  12.666 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 11.22 on 22999 degrees of freedom
Multiple R-squared:  0.02234,	Adjusted R-squared:  0.02225 
F-statistic: 262.8 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 446.5794


Call:
lm(formula = EMP_CONST_NON_BLDG_PROD_d ~ EMP_CONST_NON_BLDG_PROD_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-79.58  -0.05  -0.01   0.12 642.30 

Coefficients:
                              Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                  0.0333668  0.0432899   0.771               0.441    
EMP_CONST_NON_BLDG_PROD_DLUZ 0.0083069  0.0003091  26.878 <0.0000000000000002 ***
EMP_TOTAL.error              0.0005238  0.0001695   3.091               0.002 ** 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.527 on 22999 degrees of freedom
Multiple R-squared:  0.03091,	Adjusted R-squared:  0.03083 
F-statistic: 366.8 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_CONST_NON_BLDG_PROD_d ~ EMP_CONST_NON_BLDG_PROD_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-79.58  -0.05  -0.01   0.12 642.30 

Coefficients:
                              Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                  0.0333668  0.0432899   0.771               0.441    
EMP_CONST_NON_BLDG_PROD_DLUZ 0.0083069  0.0003091  26.878 <0.0000000000000002 ***
EMP_TOTAL.error              0.0005238  0.0001695   3.091               0.002 ** 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.527 on 22999 degrees of freedom
Multiple R-squared:  0.03091,	Adjusted R-squared:  0.03083 
F-statistic: 366.8 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 178.2564


Call:
lm(formula = EMP_CONST_NON_BLDG_OFFICE_d ~ EMP_CONST_NON_BLDG_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-35.382  -0.020  -0.011   0.047 104.994 

Coefficients:
                                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                    0.02032077 0.00916418   2.217              0.0266 *  
EMP_CONST_NON_BLDG_OFFICE_DLUZ 0.00936818 0.00037522  24.967 <0.0000000000000002 ***
EMP_TOTAL.error                0.00030825 0.00003528   8.738 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 1.356 on 22999 degrees of freedom
Multiple R-squared:  0.03081,	Adjusted R-squared:  0.03072 
F-statistic: 365.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_CONST_NON_BLDG_OFFICE_d ~ EMP_CONST_NON_BLDG_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-35.382  -0.020  -0.011   0.047 104.994 

Coefficients:
                                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                    0.02032077 0.00916418   2.217              0.0266 *  
EMP_CONST_NON_BLDG_OFFICE_DLUZ 0.00936818 0.00037522  24.967 <0.0000000000000002 ***
EMP_TOTAL.error                0.00030825 0.00003528   8.738 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 1.356 on 22999 degrees of freedom
Multiple R-squared:  0.03081,	Adjusted R-squared:  0.03072 
F-statistic: 365.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 302.9897


Call:
lm(formula = EMP_UTILITIES_PROD_d ~ EMP_UTILITIES_PROD_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-305.80   -0.52   -0.52   -0.23 1950.53 

Coefficients:
                         Estimate Std. Error t value             Pr(>|t|)    
(Intercept)             0.5246767  0.0911488   5.756        0.00000000871 ***
EMP_UTILITIES_PROD_DLUZ 0.0365218  0.0011850  30.820 < 0.0000000000000002 ***
EMP_TOTAL.error         0.0014179  0.0003562   3.981        0.00006884847 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 13.58 on 22999 degrees of freedom
Multiple R-squared:  0.04249,	Adjusted R-squared:  0.0424 
F-statistic: 510.2 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_UTILITIES_PROD_d ~ EMP_UTILITIES_PROD_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-305.80   -0.52   -0.52   -0.23 1950.53 

Coefficients:
                         Estimate Std. Error t value             Pr(>|t|)    
(Intercept)             0.5246767  0.0911488   5.756        0.00000000871 ***
EMP_UTILITIES_PROD_DLUZ 0.0365218  0.0011850  30.820 < 0.0000000000000002 ***
EMP_TOTAL.error         0.0014179  0.0003562   3.981        0.00006884847 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 13.58 on 22999 degrees of freedom
Multiple R-squared:  0.04249,	Adjusted R-squared:  0.0424 
F-statistic: 510.2 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 1014.115


Call:
lm(formula = EMP_UTILITIES_OFFICE_d ~ EMP_UTILITIES_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-578.75   -0.02   -0.02    0.08   47.12 

Coefficients:
                            Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                0.0180482  0.0414247   0.436               0.663    
EMP_UTILITIES_OFFICE_DLUZ  0.0080999  0.0003630  22.314 <0.0000000000000002 ***
EMP_TOTAL.error           -0.0000532  0.0001601  -0.332               0.740    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.148 on 22999 degrees of freedom
Multiple R-squared:  0.02128,	Adjusted R-squared:  0.02119 
F-statistic:   250 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_UTILITIES_OFFICE_d ~ EMP_UTILITIES_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-578.75   -0.02   -0.02    0.08   47.12 

Coefficients:
                            Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                0.0180482  0.0414247   0.436               0.663    
EMP_UTILITIES_OFFICE_DLUZ  0.0080999  0.0003630  22.314 <0.0000000000000002 ***
EMP_TOTAL.error           -0.0000532  0.0001601  -0.332               0.740    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.148 on 22999 degrees of freedom
Multiple R-squared:  0.02128,	Adjusted R-squared:  0.02119 
F-statistic:   250 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 1180.085


Call:
lm(formula = EMP_CONST_BLDG_PROD_d ~ EMP_CONST_BLDG_PROD_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-490.92   -0.94   -0.17    0.52  533.50 

Coefficients:
                          Estimate Std. Error t value            Pr(>|t|)    
(Intercept)              0.1011705  0.1150423   0.879               0.379    
EMP_CONST_BLDG_PROD_DLUZ 0.0071453  0.0005596  12.769 <0.0000000000000002 ***
EMP_TOTAL.error          0.0159881  0.0004522  35.355 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 17.4 on 22999 degrees of freedom
Multiple R-squared:  0.05929,	Adjusted R-squared:  0.05921 
F-statistic: 724.8 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_CONST_BLDG_PROD_d ~ EMP_CONST_BLDG_PROD_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-490.92   -0.94   -0.17    0.52  533.50 

Coefficients:
                          Estimate Std. Error t value            Pr(>|t|)    
(Intercept)              0.1011705  0.1150423   0.879               0.379    
EMP_CONST_BLDG_PROD_DLUZ 0.0071453  0.0005596  12.769 <0.0000000000000002 ***
EMP_TOTAL.error          0.0159881  0.0004522  35.355 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 17.4 on 22999 degrees of freedom
Multiple R-squared:  0.05929,	Adjusted R-squared:  0.05921 
F-statistic: 724.8 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 137.8549


Call:
lm(formula = EMP_CONST_BLDG_OFFICE_d ~ EMP_CONST_BLDG_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-273.272   -0.054    0.080    0.617  139.096 

Coefficients:
                            Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                0.0544539  0.0478085   1.139               0.255    
EMP_CONST_BLDG_OFFICE_DLUZ 0.0077898  0.0002727  28.563 <0.0000000000000002 ***
EMP_TOTAL.error            0.0035199  0.0001731  20.335 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.643 on 22999 degrees of freedom
Multiple R-squared:  0.0549,	Adjusted R-squared:  0.05482 
F-statistic:   668 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_CONST_BLDG_OFFICE_d ~ EMP_CONST_BLDG_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-273.272   -0.054    0.080    0.617  139.096 

Coefficients:
                            Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                0.0544539  0.0478085   1.139               0.255    
EMP_CONST_BLDG_OFFICE_DLUZ 0.0077898  0.0002727  28.563 <0.0000000000000002 ***
EMP_TOTAL.error            0.0035199  0.0001731  20.335 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.643 on 22999 degrees of freedom
Multiple R-squared:  0.0549,	Adjusted R-squared:  0.05482 
F-statistic:   668 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 374.5163


Call:
lm(formula = EMP_MFG_PROD_d ~ EMP_MFG_PROD_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-775.1   -0.7   -0.1    0.2 3525.2 

Coefficients:
                   Estimate Std. Error t value             Pr(>|t|)    
(Intercept)       0.0595890  0.2828577   0.211                0.833    
EMP_MFG_PROD_DLUZ 0.0103173  0.0003884  26.565 < 0.0000000000000002 ***
EMP_TOTAL.error   0.0069848  0.0011037   6.328       0.000000000253 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 42.51 on 22999 degrees of freedom
Multiple R-squared:  0.03146,	Adjusted R-squared:  0.03138 
F-statistic: 373.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_MFG_PROD_d ~ EMP_MFG_PROD_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-775.1   -0.7   -0.1    0.2 3525.2 

Coefficients:
                   Estimate Std. Error t value             Pr(>|t|)    
(Intercept)       0.0595890  0.2828577   0.211                0.833    
EMP_MFG_PROD_DLUZ 0.0103173  0.0003884  26.565 < 0.0000000000000002 ***
EMP_TOTAL.error   0.0069848  0.0011037   6.328       0.000000000253 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 42.51 on 22999 degrees of freedom
Multiple R-squared:  0.03146,	Adjusted R-squared:  0.03138 
F-statistic: 373.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 148.814


Call:
lm(formula = EMP_MFG_OFFICE_d ~ EMP_MFG_OFFICE_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1148.47     0.21     0.38     1.28   367.34 

Coefficients:
                      Estimate Std. Error t value            Pr(>|t|)    
(Intercept)         -0.1933110  0.1891830  -1.022               0.307    
EMP_MFG_OFFICE_DLUZ  0.0065857  0.0002292  28.730 <0.0000000000000002 ***
EMP_TOTAL.error      0.0086017  0.0006965  12.350 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 26.76 on 22999 degrees of freedom
Multiple R-squared:  0.04296,	Adjusted R-squared:  0.04288 
F-statistic: 516.2 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_MFG_OFFICE_d ~ EMP_MFG_OFFICE_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1148.47     0.21     0.38     1.28   367.34 

Coefficients:
                      Estimate Std. Error t value            Pr(>|t|)    
(Intercept)         -0.1933110  0.1891830  -1.022               0.307    
EMP_MFG_OFFICE_DLUZ  0.0065857  0.0002292  28.730 <0.0000000000000002 ***
EMP_TOTAL.error      0.0086017  0.0006965  12.350 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 26.76 on 22999 degrees of freedom
Multiple R-squared:  0.04296,	Adjusted R-squared:  0.04288 
F-statistic: 516.2 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 885.9396


Call:
lm(formula = EMP_WHSLE_WHS_d ~ EMP_WHSLE_WHS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-507.93   -0.20    0.07    1.02 1087.01 

Coefficients:
                    Estimate Std. Error t value            Pr(>|t|)    
(Intercept)        0.1579910  0.1291317   1.223               0.221    
EMP_WHSLE_WHS_DLUZ 0.0074186  0.0003819  19.424 <0.0000000000000002 ***
EMP_TOTAL.error    0.0047882  0.0004806   9.964 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 18.47 on 22999 degrees of freedom
Multiple R-squared:  0.02149,	Adjusted R-squared:  0.0214 
F-statistic: 252.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_WHSLE_WHS_d ~ EMP_WHSLE_WHS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-507.93   -0.20    0.07    1.02 1087.01 

Coefficients:
                    Estimate Std. Error t value            Pr(>|t|)    
(Intercept)        0.1579910  0.1291317   1.223               0.221    
EMP_WHSLE_WHS_DLUZ 0.0074186  0.0003819  19.424 <0.0000000000000002 ***
EMP_TOTAL.error    0.0047882  0.0004806   9.964 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 18.47 on 22999 degrees of freedom
Multiple R-squared:  0.02149,	Adjusted R-squared:  0.0214 
F-statistic: 252.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 231.7384


Call:
lm(formula = EMP_TRANS_d ~ EMP_TRANS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1353.49    -0.34    -0.08     0.79   901.47 

Coefficients:
                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)     0.3149990  0.1606812    1.96                0.05 *  
EMP_TRANS_DLUZ  0.0071248  0.0004574   15.58 <0.0000000000000002 ***
EMP_TOTAL.error 0.0211034  0.0005988   35.24 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 22.98 on 22999 degrees of freedom
Multiple R-squared:  0.06459,	Adjusted R-squared:  0.0645 
F-statistic:   794 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_TRANS_d ~ EMP_TRANS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1353.49    -0.34    -0.08     0.79   901.47 

Coefficients:
                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)     0.3149990  0.1606812    1.96                0.05 *  
EMP_TRANS_DLUZ  0.0071248  0.0004574   15.58 <0.0000000000000002 ***
EMP_TOTAL.error 0.0211034  0.0005988   35.24 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 22.98 on 22999 degrees of freedom
Multiple R-squared:  0.06459,	Adjusted R-squared:  0.0645 
F-statistic:   794 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 366.5446


Call:
lm(formula = EMP_RETAIL_d ~ EMP_RETAIL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-853.79   -1.48   -0.43    2.85 1834.19 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     1.0979065  0.2820132   3.893            0.0000992 ***
EMP_RETAIL_DLUZ 0.0077877  0.0004366  17.838 < 0.0000000000000002 ***
EMP_TOTAL.error 0.0215936  0.0010492  20.581 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 40.4 on 22999 degrees of freedom
Multiple R-squared:  0.03203,	Adjusted R-squared:  0.03194 
F-statistic: 380.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_RETAIL_d ~ EMP_RETAIL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-853.79   -1.48   -0.43    2.85 1834.19 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     1.0979065  0.2820132   3.893            0.0000992 ***
EMP_RETAIL_DLUZ 0.0077877  0.0004366  17.838 < 0.0000000000000002 ***
EMP_TOTAL.error 0.0215936  0.0010492  20.581 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 40.4 on 22999 degrees of freedom
Multiple R-squared:  0.03203,	Adjusted R-squared:  0.03194 
F-statistic: 380.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 140.8527


Call:
lm(formula = EMP_PROF_BUS_SVCS_d ~ EMP_PROF_BUS_SVCS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-1973.8    -3.7    -0.9     0.9  3402.4 

Coefficients:
                        Estimate Std. Error t value            Pr(>|t|)    
(Intercept)            1.0968132  0.5361649   2.046              0.0408 *  
EMP_PROF_BUS_SVCS_DLUZ 0.0062798  0.0002487  25.254 <0.0000000000000002 ***
EMP_TOTAL.error        0.0464555  0.0020909  22.218 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 80.53 on 22999 degrees of freedom
Multiple R-squared:  0.04673,	Adjusted R-squared:  0.04664 
F-statistic: 563.7 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PROF_BUS_SVCS_d ~ EMP_PROF_BUS_SVCS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-1973.8    -3.7    -0.9     0.9  3402.4 

Coefficients:
                        Estimate Std. Error t value            Pr(>|t|)    
(Intercept)            1.0968132  0.5361649   2.046              0.0408 *  
EMP_PROF_BUS_SVCS_DLUZ 0.0062798  0.0002487  25.254 <0.0000000000000002 ***
EMP_TOTAL.error        0.0464555  0.0020909  22.218 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 80.53 on 22999 degrees of freedom
Multiple R-squared:  0.04673,	Adjusted R-squared:  0.04664 
F-statistic: 563.7 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 112.9194


Call:
lm(formula = EMP_PROF_BUS_SVCS_BLDG_MAINT_d ~ EMP_PROF_BUS_SVCS_BLDG_MAINT_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1569.17    -0.54     0.23     1.42  2175.86 

Coefficients:
                                   Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                       0.4572359  0.2476598   1.846              0.0649 .  
EMP_PROF_BUS_SVCS_BLDG_MAINT_DLUZ 0.0090552  0.0003084  29.359 <0.0000000000000002 ***
EMP_TOTAL.error                   0.0131045  0.0009432  13.894 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 36.24 on 22999 degrees of freedom
Multiple R-squared:  0.04622,	Adjusted R-squared:  0.04614 
F-statistic: 557.3 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PROF_BUS_SVCS_BLDG_MAINT_d ~ EMP_PROF_BUS_SVCS_BLDG_MAINT_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1569.17    -0.54     0.23     1.42  2175.86 

Coefficients:
                                   Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                       0.4572359  0.2476598   1.846              0.0649 .  
EMP_PROF_BUS_SVCS_BLDG_MAINT_DLUZ 0.0090552  0.0003084  29.359 <0.0000000000000002 ***
EMP_TOTAL.error                   0.0131045  0.0009432  13.894 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 36.24 on 22999 degrees of freedom
Multiple R-squared:  0.04622,	Adjusted R-squared:  0.04614 
F-statistic: 557.3 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 189.5433


Call:
lm(formula = EMP_PVT_ED_K12_d ~ EMP_PVT_ED_K12_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-2055.79    -0.78    -0.09     1.69   568.19 

Coefficients:
                     Estimate Std. Error t value             Pr(>|t|)    
(Intercept)         0.5381863  0.1962066   2.743              0.00609 ** 
EMP_PVT_ED_K12_DLUZ 0.0178580  0.0005597  31.906 < 0.0000000000000002 ***
EMP_TOTAL.error     0.0298171  0.0007620  39.130 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 29.35 on 22999 degrees of freedom
Multiple R-squared:  0.09935,	Adjusted R-squared:  0.09927 
F-statistic:  1269 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PVT_ED_K12_d ~ EMP_PVT_ED_K12_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-2055.79    -0.78    -0.09     1.69   568.19 

Coefficients:
                     Estimate Std. Error t value             Pr(>|t|)    
(Intercept)         0.5381863  0.1962066   2.743              0.00609 ** 
EMP_PVT_ED_K12_DLUZ 0.0178580  0.0005597  31.906 < 0.0000000000000002 ***
EMP_TOTAL.error     0.0298171  0.0007620  39.130 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 29.35 on 22999 degrees of freedom
Multiple R-squared:  0.09935,	Adjusted R-squared:  0.09927 
F-statistic:  1269 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 741.579


Call:
lm(formula = EMP_PVT_ED_POST_K12_OTH_d ~ EMP_PVT_ED_POST_K12_OTH_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-6604.3    -6.6    -1.5     7.3  1801.5 

Coefficients:
                              Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                  7.6792962  0.6752257   11.37 <0.0000000000000002 ***
EMP_PVT_ED_POST_K12_OTH_DLUZ 0.0250432  0.0006963   35.97 <0.0000000000000002 ***
EMP_TOTAL.error              0.1008164  0.0023983   42.04 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 92.36 on 22999 degrees of freedom
Multiple R-squared:  0.1182,	Adjusted R-squared:  0.1181 
F-statistic:  1542 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PVT_ED_POST_K12_OTH_d ~ EMP_PVT_ED_POST_K12_OTH_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-6604.3    -6.6    -1.5     7.3  1801.5 

Coefficients:
                              Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                  7.6792962  0.6752257   11.37 <0.0000000000000002 ***
EMP_PVT_ED_POST_K12_OTH_DLUZ 0.0250432  0.0006963   35.97 <0.0000000000000002 ***
EMP_TOTAL.error              0.1008164  0.0023983   42.04 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 92.36 on 22999 degrees of freedom
Multiple R-squared:  0.1182,	Adjusted R-squared:  0.1181 
F-statistic:  1542 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 1439.666


Call:
lm(formula = EMP_HEALTH_d ~ EMP_HEALTH_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-6581.6    -0.7     0.8     4.5  6210.5 

Coefficients:
                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)     0.6478197  0.6318528   1.025               0.305    
EMP_HEALTH_DLUZ 0.0067223  0.0004614  14.568 <0.0000000000000002 ***
EMP_TOTAL.error 0.0664407  0.0022476  29.560 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 86.41 on 22999 degrees of freedom
Multiple R-squared:  0.04733,	Adjusted R-squared:  0.04725 
F-statistic: 571.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_HEALTH_d ~ EMP_HEALTH_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-6581.6    -0.7     0.8     4.5  6210.5 

Coefficients:
                 Estimate Std. Error t value            Pr(>|t|)    
(Intercept)     0.6478197  0.6318528   1.025               0.305    
EMP_HEALTH_DLUZ 0.0067223  0.0004614  14.568 <0.0000000000000002 ***
EMP_TOTAL.error 0.0664407  0.0022476  29.560 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 86.41 on 22999 degrees of freedom
Multiple R-squared:  0.04733,	Adjusted R-squared:  0.04725 
F-statistic: 571.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 252.5622


Call:
lm(formula = EMP_PERSONAL_SVCS_OFFICE_d ~ EMP_PERSONAL_SVCS_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-455.56   -0.58    0.03    0.43 1030.94 

Coefficients:
                               Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                   0.0008373  0.1042330   0.008               0.994    
EMP_PERSONAL_SVCS_OFFICE_DLUZ 0.0072868  0.0003245  22.459 <0.0000000000000002 ***
EMP_TOTAL.error               0.0055916  0.0004020  13.911 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 15.48 on 22999 degrees of freedom
Multiple R-squared:  0.02951,	Adjusted R-squared:  0.02942 
F-statistic: 349.6 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PERSONAL_SVCS_OFFICE_d ~ EMP_PERSONAL_SVCS_OFFICE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-455.56   -0.58    0.03    0.43 1030.94 

Coefficients:
                               Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                   0.0008373  0.1042330   0.008               0.994    
EMP_PERSONAL_SVCS_OFFICE_DLUZ 0.0072868  0.0003245  22.459 <0.0000000000000002 ***
EMP_TOTAL.error               0.0055916  0.0004020  13.911 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 15.48 on 22999 degrees of freedom
Multiple R-squared:  0.02951,	Adjusted R-squared:  0.02942 
F-statistic: 349.6 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 168.9014


Call:
lm(formula = EMP_AMUSEMENT_d ~ EMP_AMUSEMENT_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1686.39    -0.24     0.14     0.76  1792.47 

Coefficients:
                    Estimate Std. Error t value            Pr(>|t|)    
(Intercept)        0.2438395  0.2065784    1.18               0.238    
EMP_AMUSEMENT_DLUZ 0.0083813  0.0007251   11.56 <0.0000000000000002 ***
EMP_TOTAL.error    0.0129466  0.0007754   16.70 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 29.85 on 22999 degrees of freedom
Multiple R-squared:  0.01813,	Adjusted R-squared:  0.01805 
F-statistic: 212.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_AMUSEMENT_d ~ EMP_AMUSEMENT_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1686.39    -0.24     0.14     0.76  1792.47 

Coefficients:
                    Estimate Std. Error t value            Pr(>|t|)    
(Intercept)        0.2438395  0.2065784    1.18               0.238    
EMP_AMUSEMENT_DLUZ 0.0083813  0.0007251   11.56 <0.0000000000000002 ***
EMP_TOTAL.error    0.0129466  0.0007754   16.70 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 29.85 on 22999 degrees of freedom
Multiple R-squared:  0.01813,	Adjusted R-squared:  0.01805 
F-statistic: 212.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 208.4367


Call:
lm(formula = EMP_HOTEL_d ~ EMP_HOTEL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1127.61     0.19     0.24     0.45   992.85 

Coefficients:
                  Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     -0.1899080  0.1523892  -1.246                0.213    
EMP_HOTEL_DLUZ   0.0033519  0.0001917  17.485 < 0.0000000000000002 ***
EMP_TOTAL.error  0.0034103  0.0005892   5.788         0.0000000072 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 22.69 on 22999 degrees of freedom
Multiple R-squared:  0.01458,	Adjusted R-squared:  0.01449 
F-statistic: 170.1 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_HOTEL_d ~ EMP_HOTEL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1127.61     0.19     0.24     0.45   992.85 

Coefficients:
                  Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     -0.1899080  0.1523892  -1.246                0.213    
EMP_HOTEL_DLUZ   0.0033519  0.0001917  17.485 < 0.0000000000000002 ***
EMP_TOTAL.error  0.0034103  0.0005892   5.788         0.0000000072 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 22.69 on 22999 degrees of freedom
Multiple R-squared:  0.01458,	Adjusted R-squared:  0.01449 
F-statistic: 170.1 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 277.3434


Call:
lm(formula = EMP_RESTAURANT_BAR_d ~ EMP_RESTAURANT_BAR_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-707.21   -0.56    0.78    3.68 3153.15 

Coefficients:
                         Estimate Std. Error t value            Pr(>|t|)    
(Intercept)             0.5658811  0.3104677   1.823              0.0684 .  
EMP_RESTAURANT_BAR_DLUZ 0.0055887  0.0002685  20.816 <0.0000000000000002 ***
EMP_TOTAL.error         0.0131071  0.0010621  12.341 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 40.89 on 22999 degrees of freedom
Multiple R-squared:  0.02545,	Adjusted R-squared:  0.02536 
F-statistic: 300.3 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_RESTAURANT_BAR_d ~ EMP_RESTAURANT_BAR_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-707.21   -0.56    0.78    3.68 3153.15 

Coefficients:
                         Estimate Std. Error t value            Pr(>|t|)    
(Intercept)             0.5658811  0.3104677   1.823              0.0684 .  
EMP_RESTAURANT_BAR_DLUZ 0.0055887  0.0002685  20.816 <0.0000000000000002 ***
EMP_TOTAL.error         0.0131071  0.0010621  12.341 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 40.89 on 22999 degrees of freedom
Multiple R-squared:  0.02545,	Adjusted R-squared:  0.02536 
F-statistic: 300.3 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 258.5034


Call:
lm(formula = EMP_PERSONAL_SVCS_RETAIL_d ~ EMP_PERSONAL_SVCS_RETAIL_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-942.91   -3.48   -1.67   -0.95 2619.95 

Coefficients:
                               Estimate Std. Error t value             Pr(>|t|)    
(Intercept)                   1.3361325  0.2678334   4.989          0.000000612 ***
EMP_PERSONAL_SVCS_RETAIL_DLUZ 0.0055039  0.0002746  20.044 < 0.0000000000000002 ***
EMP_TOTAL.error               0.0714367  0.0009828  72.689 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 37.84 on 22999 degrees of freedom
Multiple R-squared:  0.1965,	Adjusted R-squared:  0.1964 
F-statistic:  2812 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PERSONAL_SVCS_RETAIL_d ~ EMP_PERSONAL_SVCS_RETAIL_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-942.91   -3.48   -1.67   -0.95 2619.95 

Coefficients:
                               Estimate Std. Error t value             Pr(>|t|)    
(Intercept)                   1.3361325  0.2678334   4.989          0.000000612 ***
EMP_PERSONAL_SVCS_RETAIL_DLUZ 0.0055039  0.0002746  20.044 < 0.0000000000000002 ***
EMP_TOTAL.error               0.0714367  0.0009828  72.689 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 37.84 on 22999 degrees of freedom
Multiple R-squared:  0.1965,	Adjusted R-squared:  0.1964 
F-statistic:  2812 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 181.657


Call:
lm(formula = EMP_RELIGIOUS_d ~ EMP_RELIGIOUS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
 -2.80  -0.37  -0.09  -0.03 385.76 

Coefficients:
                     Estimate Std. Error t value            Pr(>|t|)    
(Intercept)         0.0288771  0.0475884   0.607               0.544    
EMP_RELIGIOUS_DLUZ  0.0055590  0.0004369  12.724 <0.0000000000000002 ***
EMP_TOTAL.error    -0.0001668  0.0001611  -1.035               0.300    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.205 on 22999 degrees of freedom
Multiple R-squared:  0.007053,	Adjusted R-squared:  0.006967 
F-statistic: 81.68 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_RELIGIOUS_d ~ EMP_RELIGIOUS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
 -2.80  -0.37  -0.09  -0.03 385.76 

Coefficients:
                     Estimate Std. Error t value            Pr(>|t|)    
(Intercept)         0.0288771  0.0475884   0.607               0.544    
EMP_RELIGIOUS_DLUZ  0.0055590  0.0004369  12.724 <0.0000000000000002 ***
EMP_TOTAL.error    -0.0001668  0.0001611  -1.035               0.300    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.205 on 22999 degrees of freedom
Multiple R-squared:  0.007053,	Adjusted R-squared:  0.006967 
F-statistic: 81.68 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 187.9464


Call:
lm(formula = EMP_PVT_HH_d ~ EMP_PVT_HH_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
 -51.74   -1.62   -0.33    0.08 2358.31 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     0.0331413  0.1390597   0.238              0.81163    
EMP_PVT_HH_DLUZ 0.0055251  0.0002322  23.792 < 0.0000000000000002 ***
EMP_TOTAL.error 0.0014518  0.0005290   2.744              0.00607 ** 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 20.37 on 22999 degrees of freedom
Multiple R-squared:  0.02431,	Adjusted R-squared:  0.02422 
F-statistic: 286.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PVT_HH_d ~ EMP_PVT_HH_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
 -51.74   -1.62   -0.33    0.08 2358.31 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     0.0331413  0.1390597   0.238              0.81163    
EMP_PVT_HH_DLUZ 0.0055251  0.0002322  23.792 < 0.0000000000000002 ***
EMP_TOTAL.error 0.0014518  0.0005290   2.744              0.00607 ** 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 20.37 on 22999 degrees of freedom
Multiple R-squared:  0.02431,	Adjusted R-squared:  0.02422 
F-statistic: 286.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 178.9645


Call:
lm(formula = EMP_STATE_LOCAL_GOV_ENT_d ~ EMP_STATE_LOCAL_GOV_ENT_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-4720.9    -0.8    -0.6     0.1   767.7 

Coefficients:
                              Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                  0.6015750  0.2651707   2.269              0.0233 *  
EMP_STATE_LOCAL_GOV_ENT_DLUZ 0.0040574  0.0003646  11.129 <0.0000000000000002 ***
EMP_TOTAL.error              0.0585988  0.0010368  56.521 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 39.87 on 22999 degrees of freedom
Multiple R-squared:  0.1288,	Adjusted R-squared:  0.1287 
F-statistic:  1700 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_STATE_LOCAL_GOV_ENT_d ~ EMP_STATE_LOCAL_GOV_ENT_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-4720.9    -0.8    -0.6     0.1   767.7 

Coefficients:
                              Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                  0.6015750  0.2651707   2.269              0.0233 *  
EMP_STATE_LOCAL_GOV_ENT_DLUZ 0.0040574  0.0003646  11.129 <0.0000000000000002 ***
EMP_TOTAL.error              0.0585988  0.0010368  56.521 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 39.87 on 22999 degrees of freedom
Multiple R-squared:  0.1288,	Adjusted R-squared:  0.1287 
F-statistic:  1700 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 864.3334


Call:
lm(formula = EMP_FED_NON_MIL_d ~ EMP_FED_NON_MIL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1612.75    -0.77    -0.27    -0.17  1726.53 

Coefficients:
                      Estimate Std. Error t value            Pr(>|t|)    
(Intercept)          0.2222876  0.2291233    0.97               0.332    
EMP_FED_NON_MIL_DLUZ 0.0068927  0.0004117   16.74 <0.0000000000000002 ***
EMP_TOTAL.error      0.0236796  0.0008722   27.15 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 33.58 on 22999 degrees of freedom
Multiple R-squared:  0.04139,	Adjusted R-squared:  0.04131 
F-statistic: 496.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_FED_NON_MIL_d ~ EMP_FED_NON_MIL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-1612.75    -0.77    -0.27    -0.17  1726.53 

Coefficients:
                      Estimate Std. Error t value            Pr(>|t|)    
(Intercept)          0.2222876  0.2291233    0.97               0.332    
EMP_FED_NON_MIL_DLUZ 0.0068927  0.0004117   16.74 <0.0000000000000002 ***
EMP_TOTAL.error      0.0236796  0.0008722   27.15 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 33.58 on 22999 degrees of freedom
Multiple R-squared:  0.04139,	Adjusted R-squared:  0.04131 
F-statistic: 496.5 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 221.5899


Call:
lm(formula = EMP_FED_MIL_d ~ EMP_FED_MIL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-9313.3    -3.9    -3.6    -0.7  6132.3 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)      3.559432   0.999141   3.562             0.000368 ***
EMP_FED_MIL_DLUZ 0.028632   0.001174  24.396 < 0.0000000000000002 ***
EMP_TOTAL.error  0.355562   0.003908  90.979 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 150.4 on 22999 degrees of freedom
Multiple R-squared:  0.2825,	Adjusted R-squared:  0.2824 
F-statistic:  4527 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_FED_MIL_d ~ EMP_FED_MIL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-9313.3    -3.9    -3.6    -0.7  6132.3 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)      3.559432   0.999141   3.562             0.000368 ***
EMP_FED_MIL_DLUZ 0.028632   0.001174  24.396 < 0.0000000000000002 ***
EMP_TOTAL.error  0.355562   0.003908  90.979 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 150.4 on 22999 degrees of freedom
Multiple R-squared:  0.2825,	Adjusted R-squared:  0.2824 
F-statistic:  4527 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 814.8435


Call:
lm(formula = EMP_STATE_LOCAL_GOV_BLUE_d ~ EMP_STATE_LOCAL_GOV_BLUE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-997.04   -1.06   -0.63   -0.49 1577.74 

Coefficients:
                               Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                   0.5286201  0.2215446   2.386               0.017 *  
EMP_STATE_LOCAL_GOV_BLUE_DLUZ 0.0043600  0.0001701  25.637 <0.0000000000000002 ***
EMP_TOTAL.error               0.0206896  0.0008477  24.406 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 32.62 on 22999 degrees of freedom
Multiple R-squared:  0.04954,	Adjusted R-squared:  0.04946 
F-statistic: 599.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_STATE_LOCAL_GOV_BLUE_d ~ EMP_STATE_LOCAL_GOV_BLUE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-997.04   -1.06   -0.63   -0.49 1577.74 

Coefficients:
                               Estimate Std. Error t value            Pr(>|t|)    
(Intercept)                   0.5286201  0.2215446   2.386               0.017 *  
EMP_STATE_LOCAL_GOV_BLUE_DLUZ 0.0043600  0.0001701  25.637 <0.0000000000000002 ***
EMP_TOTAL.error               0.0206896  0.0008477  24.406 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 32.62 on 22999 degrees of freedom
Multiple R-squared:  0.04954,	Adjusted R-squared:  0.04946 
F-statistic: 599.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 192.0412


Call:
lm(formula = EMP_STATE_LOCAL_GOV_WHITE_d ~ EMP_STATE_LOCAL_GOV_WHITE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-3690.4    -0.8    -0.6    -0.3  1009.6 

Coefficients:
                                Estimate Std. Error t value             Pr(>|t|)    
(Intercept)                    0.5713743  0.2313026   2.470               0.0135 *  
EMP_STATE_LOCAL_GOV_WHITE_DLUZ 0.0036701  0.0004891   7.503   0.0000000000000645 ***
EMP_TOTAL.error                0.0489958  0.0008960  54.680 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 34.5 on 22999 degrees of freedom
Multiple R-squared:  0.1176,	Adjusted R-squared:  0.1175 
F-statistic:  1532 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_STATE_LOCAL_GOV_WHITE_d ~ EMP_STATE_LOCAL_GOV_WHITE_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-3690.4    -0.8    -0.6    -0.3  1009.6 

Coefficients:
                                Estimate Std. Error t value             Pr(>|t|)    
(Intercept)                    0.5713743  0.2313026   2.470               0.0135 *  
EMP_STATE_LOCAL_GOV_WHITE_DLUZ 0.0036701  0.0004891   7.503   0.0000000000000645 ***
EMP_TOTAL.error                0.0489958  0.0008960  54.680 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 34.5 on 22999 degrees of freedom
Multiple R-squared:  0.1176,	Adjusted R-squared:  0.1175 
F-statistic:  1532 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 323.8612


Call:
lm(formula = EMP_PUBLIC_ED_d ~ EMP_PUBLIC_ED_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-18.50  -1.51  -0.61  -0.19 812.38 

Coefficients:
                    Estimate Std. Error t value            Pr(>|t|)    
(Intercept)        0.1238110  0.1145430   1.081                0.28    
EMP_PUBLIC_ED_DLUZ 0.0063219  0.0004811  13.140 <0.0000000000000002 ***
EMP_TOTAL.error    0.0028274  0.0003393   8.333 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 13.07 on 22999 degrees of freedom
Multiple R-squared:  0.01045,	Adjusted R-squared:  0.01036 
F-statistic: 121.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_PUBLIC_ED_d ~ EMP_PUBLIC_ED_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-18.50  -1.51  -0.61  -0.19 812.38 

Coefficients:
                    Estimate Std. Error t value            Pr(>|t|)    
(Intercept)        0.1238110  0.1145430   1.081                0.28    
EMP_PUBLIC_ED_DLUZ 0.0063219  0.0004811  13.140 <0.0000000000000002 ***
EMP_TOTAL.error    0.0028274  0.0003393   8.333 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 13.07 on 22999 degrees of freedom
Multiple R-squared:  0.01045,	Adjusted R-squared:  0.01036 
F-statistic: 121.4 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 188.1683


Call:
lm(formula = EMP_OWN_OCC_DWELL_MGMT_d ~ EMP_OWN_OCC_DWELL_MGMT_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                            Estimate Std. Error t value Pr(>|t|)
(Intercept)                        0          0     NaN      NaN
EMP_OWN_OCC_DWELL_MGMT_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error                    0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA

$`lm.m2 summary`

Call:
lm(formula = EMP_OWN_OCC_DWELL_MGMT_d ~ EMP_OWN_OCC_DWELL_MGMT_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                            Estimate Std. Error t value Pr(>|t|)
(Intercept)                        0          0     NaN      NaN
EMP_OWN_OCC_DWELL_MGMT_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error                    0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA


$wape
[1] NaN


Call:
lm(formula = EMP_FED_GOV_ACCTS_d ~ EMP_FED_GOV_ACCTS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                       Estimate Std. Error t value Pr(>|t|)
(Intercept)                   0          0     NaN      NaN
EMP_FED_GOV_ACCTS_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error               0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA

$`lm.m2 summary`

Call:
lm(formula = EMP_FED_GOV_ACCTS_d ~ EMP_FED_GOV_ACCTS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                       Estimate Std. Error t value Pr(>|t|)
(Intercept)                   0          0     NaN      NaN
EMP_FED_GOV_ACCTS_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error               0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA


$wape
[1] NaN


Call:
lm(formula = EMP_ST_LCL_GOV_ACCTS_d ~ EMP_ST_LCL_GOV_ACCTS_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                          Estimate Std. Error t value Pr(>|t|)
(Intercept)                      0          0     NaN      NaN
EMP_ST_LCL_GOV_ACCTS_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error                  0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA

$`lm.m2 summary`

Call:
lm(formula = EMP_ST_LCL_GOV_ACCTS_d ~ EMP_ST_LCL_GOV_ACCTS_DLUZ + 
    EMP_TOTAL.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                          Estimate Std. Error t value Pr(>|t|)
(Intercept)                      0          0     NaN      NaN
EMP_ST_LCL_GOV_ACCTS_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error                  0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA


$wape
[1] NaN


Call:
lm(formula = EMP_CAP_ACCTS_d ~ EMP_CAP_ACCTS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                   Estimate Std. Error t value Pr(>|t|)
(Intercept)               0          0     NaN      NaN
EMP_CAP_ACCTS_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error           0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA

$`lm.m2 summary`

Call:
lm(formula = EMP_CAP_ACCTS_d ~ EMP_CAP_ACCTS_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
     0      0      0      0      0 

Coefficients: (1 not defined because of singularities)
                   Estimate Std. Error t value Pr(>|t|)
(Intercept)               0          0     NaN      NaN
EMP_CAP_ACCTS_DLUZ       NA         NA      NA       NA
EMP_TOTAL.error           0          0     NaN      NaN

Residual standard error: 0 on 23000 degrees of freedom
Multiple R-squared:    NaN,	Adjusted R-squared:    NaN 
F-statistic:   NaN on 1 and 23000 DF,  p-value: NA


$wape
[1] NaN


Call:
lm(formula = EMP_TOTAL_d ~ EMP_TOTAL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-8298.0    -9.5    -3.4     8.1  6285.8 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     8.2043959  1.2480927   6.574      0.0000000000502 ***
EMP_TOTAL_DLUZ  0.0066283  0.0003333  19.885 < 0.0000000000000002 ***
EMP_TOTAL.error 0.9685357  0.0045695 211.955 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 175.3 on 22999 degrees of freedom
Multiple R-squared:  0.669,	Adjusted R-squared:  0.6689 
F-statistic: 2.324e+04 on 2 and 22999 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = EMP_TOTAL_d ~ EMP_TOTAL_DLUZ + EMP_TOTAL.error, 
    data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-8298.0    -9.5    -3.4     8.1  6285.8 

Coefficients:
                 Estimate Std. Error t value             Pr(>|t|)    
(Intercept)     8.2043959  1.2480927   6.574      0.0000000000502 ***
EMP_TOTAL_DLUZ  0.0066283  0.0003333  19.885 < 0.0000000000000002 ***
EMP_TOTAL.error 0.9685357  0.0045695 211.955 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 175.3 on 22999 degrees of freedom
Multiple R-squared:  0.669,	Adjusted R-squared:  0.6689 
F-statistic: 2.324e+04 on 2 and 22999 DF,  p-value: < 0.00000000000000022


$wape
[1] 51.96417


Call:
lm(formula = I1_d ~ I1_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-138.095   -1.623   -0.050    1.411  141.080 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0006383  0.0482885   0.013               0.989    
I1_DLUZ     0.0042775  0.0001015  42.137 <0.0000000000000002 ***
HS_SF.error 0.0448747  0.0038567  11.635 <0.0000000000000002 ***
HS_MF.error 0.0969125  0.0017246  56.195 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 7.088 on 22998 degrees of freedom
Multiple R-squared:  0.1836,	Adjusted R-squared:  0.1835 
F-statistic:  1725 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I1_d ~ I1_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-138.095   -1.623   -0.050    1.411  141.080 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0006383  0.0482885   0.013               0.989    
I1_DLUZ     0.0042775  0.0001015  42.137 <0.0000000000000002 ***
HS_SF.error 0.0448747  0.0038567  11.635 <0.0000000000000002 ***
HS_MF.error 0.0969125  0.0017246  56.195 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 7.088 on 22998 degrees of freedom
Multiple R-squared:  0.1836,	Adjusted R-squared:  0.1835 
F-statistic:  1725 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 81.60464


Call:
lm(formula = I2_d ~ I2_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-737.25   -2.65   -0.51    1.77  188.82 

Coefficients:
             Estimate Std. Error t value             Pr(>|t|)    
(Intercept) 0.2321477  0.0670571   3.462             0.000537 ***
I2_DLUZ     0.0052813  0.0001306  40.425 < 0.0000000000000002 ***
HS_SF.error 0.0700557  0.0055106  12.713 < 0.0000000000000002 ***
HS_MF.error 0.0741206  0.0024626  30.098 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 10.13 on 22998 degrees of freedom
Multiple R-squared:  0.105,	Adjusted R-squared:  0.1049 
F-statistic: 899.4 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I2_d ~ I2_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-737.25   -2.65   -0.51    1.77  188.82 

Coefficients:
             Estimate Std. Error t value             Pr(>|t|)    
(Intercept) 0.2321477  0.0670571   3.462             0.000537 ***
I2_DLUZ     0.0052813  0.0001306  40.425 < 0.0000000000000002 ***
HS_SF.error 0.0700557  0.0055106  12.713 < 0.0000000000000002 ***
HS_MF.error 0.0741206  0.0024626  30.098 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 10.13 on 22998 degrees of freedom
Multiple R-squared:  0.105,	Adjusted R-squared:  0.1049 
F-statistic: 899.4 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 73.06064


Call:
lm(formula = I3_d ~ I3_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-84.058  -1.886  -0.222   0.887  83.218 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0855543  0.0460082    1.86               0.063 .  
I3_DLUZ     0.0038779  0.0001754   22.11 <0.0000000000000002 ***
HS_SF.error 0.0660902  0.0035834   18.44 <0.0000000000000002 ***
HS_MF.error 0.0843594  0.0016007   52.70 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.585 on 22998 degrees of freedom
Multiple R-squared:  0.1311,	Adjusted R-squared:  0.131 
F-statistic:  1157 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I3_d ~ I3_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-84.058  -1.886  -0.222   0.887  83.218 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0855543  0.0460082    1.86               0.063 .  
I3_DLUZ     0.0038779  0.0001754   22.11 <0.0000000000000002 ***
HS_SF.error 0.0660902  0.0035834   18.44 <0.0000000000000002 ***
HS_MF.error 0.0843594  0.0016007   52.70 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.585 on 22998 degrees of freedom
Multiple R-squared:  0.1311,	Adjusted R-squared:  0.131 
F-statistic:  1157 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 51.94336


Call:
lm(formula = I4_d ~ I4_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-64.856  -1.977  -0.315   0.982  82.739 

Coefficients:
             Estimate Std. Error t value             Pr(>|t|)    
(Intercept) 0.1567875  0.0449852   3.485             0.000492 ***
I4_DLUZ     0.0041426  0.0001979  20.935 < 0.0000000000000002 ***
HS_SF.error 0.0464497  0.0032664  14.220 < 0.0000000000000002 ***
HS_MF.error 0.0874270  0.0014594  59.908 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.003 on 22998 degrees of freedom
Multiple R-squared:  0.1523,	Adjusted R-squared:  0.1522 
F-statistic:  1377 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I4_d ~ I4_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-64.856  -1.977  -0.315   0.982  82.739 

Coefficients:
             Estimate Std. Error t value             Pr(>|t|)    
(Intercept) 0.1567875  0.0449852   3.485             0.000492 ***
I4_DLUZ     0.0041426  0.0001979  20.935 < 0.0000000000000002 ***
HS_SF.error 0.0464497  0.0032664  14.220 < 0.0000000000000002 ***
HS_MF.error 0.0874270  0.0014594  59.908 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.003 on 22998 degrees of freedom
Multiple R-squared:  0.1523,	Adjusted R-squared:  0.1522 
F-statistic:  1377 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 53.31216


Call:
lm(formula = I5_d ~ I5_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-67.40  -1.61  -0.20   0.99 433.92 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0316372  0.0453666   0.697               0.486    
I5_DLUZ     0.0047133  0.0002926  16.108 <0.0000000000000002 ***
HS_SF.error 0.0513202  0.0032880  15.608 <0.0000000000000002 ***
HS_MF.error 0.1017107  0.0014688  69.246 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.042 on 22998 degrees of freedom
Multiple R-squared:  0.1832,	Adjusted R-squared:  0.1831 
F-statistic:  1720 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I5_d ~ I5_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-67.40  -1.61  -0.20   0.99 433.92 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0316372  0.0453666   0.697               0.486    
I5_DLUZ     0.0047133  0.0002926  16.108 <0.0000000000000002 ***
HS_SF.error 0.0513202  0.0032880  15.608 <0.0000000000000002 ***
HS_MF.error 0.1017107  0.0014688  69.246 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.042 on 22998 degrees of freedom
Multiple R-squared:  0.1832,	Adjusted R-squared:  0.1831 
F-statistic:  1720 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 52.46787


Call:
lm(formula = I6_d ~ I6_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-83.36  -1.84  -0.18   1.35 386.06 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0161300  0.0493511   0.327               0.744    
I6_DLUZ     0.0047867  0.0002529  18.930 <0.0000000000000002 ***
HS_SF.error 0.1006930  0.0036674  27.456 <0.0000000000000002 ***
HS_MF.error 0.1227853  0.0016384  74.940 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.74 on 22998 degrees of freedom
Multiple R-squared:  0.216,	Adjusted R-squared:  0.2159 
F-statistic:  2112 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I6_d ~ I6_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
   Min     1Q Median     3Q    Max 
-83.36  -1.84  -0.18   1.35 386.06 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0161300  0.0493511   0.327               0.744    
I6_DLUZ     0.0047867  0.0002529  18.930 <0.0000000000000002 ***
HS_SF.error 0.1006930  0.0036674  27.456 <0.0000000000000002 ***
HS_MF.error 0.1227853  0.0016384  74.940 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.74 on 22998 degrees of freedom
Multiple R-squared:  0.216,	Adjusted R-squared:  0.2159 
F-statistic:  2112 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 47.63877


Call:
lm(formula = I7_d ~ I7_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-122.768   -1.467    0.076    1.161  189.853 

Coefficients:
             Estimate Std. Error t value             Pr(>|t|)    
(Intercept) -0.122236   0.039193  -3.119              0.00182 ** 
I7_DLUZ      0.005329   0.000240  22.201 < 0.0000000000000002 ***
HS_SF.error  0.088803   0.003218  27.593 < 0.0000000000000002 ***
HS_MF.error  0.096725   0.001438  67.254 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 5.915 on 22998 degrees of freedom
Multiple R-squared:  0.1893,	Adjusted R-squared:  0.1892 
F-statistic:  1790 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I7_d ~ I7_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
     Min       1Q   Median       3Q      Max 
-122.768   -1.467    0.076    1.161  189.853 

Coefficients:
             Estimate Std. Error t value             Pr(>|t|)    
(Intercept) -0.122236   0.039193  -3.119              0.00182 ** 
I7_DLUZ      0.005329   0.000240  22.201 < 0.0000000000000002 ***
HS_SF.error  0.088803   0.003218  27.593 < 0.0000000000000002 ***
HS_MF.error  0.096725   0.001438  67.254 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 5.915 on 22998 degrees of freedom
Multiple R-squared:  0.1893,	Adjusted R-squared:  0.1892 
F-statistic:  1790 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 59.10996


Call:
lm(formula = I8_d ~ I8_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-77.925  -1.153  -0.092   0.737 117.886 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0141766  0.0299936   0.473               0.636    
I8_DLUZ     0.0051515  0.0002484  20.737 <0.0000000000000002 ***
HS_SF.error 0.0694882  0.0023118  30.058 <0.0000000000000002 ***
HS_MF.error 0.0539001  0.0010331  52.172 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 4.248 on 22998 degrees of freedom
Multiple R-squared:  0.139,	Adjusted R-squared:  0.1389 
F-statistic:  1238 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I8_d ~ I8_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-77.925  -1.153  -0.092   0.737 117.886 

Coefficients:
             Estimate Std. Error t value            Pr(>|t|)    
(Intercept) 0.0141766  0.0299936   0.473               0.636    
I8_DLUZ     0.0051515  0.0002484  20.737 <0.0000000000000002 ***
HS_SF.error 0.0694882  0.0023118  30.058 <0.0000000000000002 ***
HS_MF.error 0.0539001  0.0010331  52.172 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 4.248 on 22998 degrees of freedom
Multiple R-squared:  0.139,	Adjusted R-squared:  0.1389 
F-statistic:  1238 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 63.82236


Call:
lm(formula = I9_d ~ I9_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-102.21   -2.73   -0.46    1.05  480.03 

Coefficients:
              Estimate Std. Error t value            Pr(>|t|)    
(Intercept) -0.0737872  0.0629682  -1.172               0.241    
I9_DLUZ      0.0061909  0.0001815  34.107 <0.0000000000000002 ***
HS_SF.error  0.0727874  0.0047145  15.439 <0.0000000000000002 ***
HS_MF.error  0.0895318  0.0021070  42.492 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 8.663 on 22998 degrees of freedom
Multiple R-squared:  0.1223,	Adjusted R-squared:  0.1221 
F-statistic:  1068 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I9_d ~ I9_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-102.21   -2.73   -0.46    1.05  480.03 

Coefficients:
              Estimate Std. Error t value            Pr(>|t|)    
(Intercept) -0.0737872  0.0629682  -1.172               0.241    
I9_DLUZ      0.0061909  0.0001815  34.107 <0.0000000000000002 ***
HS_SF.error  0.0727874  0.0047145  15.439 <0.0000000000000002 ***
HS_MF.error  0.0895318  0.0021070  42.492 <0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 8.663 on 22998 degrees of freedom
Multiple R-squared:  0.1223,	Adjusted R-squared:  0.1221 
F-statistic:  1068 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 90.11028


Call:
lm(formula = I10_d ~ I10_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-142.04   -2.87   -0.17    1.63  364.66 

Coefficients:
              Estimate Std. Error t value             Pr(>|t|)    
(Intercept) -0.2653369  0.0625735   -4.24            0.0000224 ***
I10_DLUZ     0.0065810  0.0001524   43.19 < 0.0000000000000002 ***
HS_SF.error  0.1708911  0.0051264   33.34 < 0.0000000000000002 ***
HS_MF.error  0.0899685  0.0022901   39.29 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 9.418 on 22998 degrees of freedom
Multiple R-squared:  0.1616,	Adjusted R-squared:  0.1615 
F-statistic:  1478 on 3 and 22998 DF,  p-value: < 0.00000000000000022

$`lm.m2 summary`

Call:
lm(formula = I10_d ~ I10_DLUZ + HS_SF.error + HS_MF.error, data = residual_comb)

Residuals:
    Min      1Q  Median      3Q     Max 
-142.04   -2.87   -0.17    1.63  364.66 

Coefficients:
              Estimate Std. Error t value             Pr(>|t|)    
(Intercept) -0.2653369  0.0625735   -4.24            0.0000224 ***
I10_DLUZ     0.0065810  0.0001524   43.19 < 0.0000000000000002 ***
HS_SF.error  0.1708911  0.0051264   33.34 < 0.0000000000000002 ***
HS_MF.error  0.0899685  0.0022901   39.29 < 0.0000000000000002 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 9.418 on 22998 degrees of freedom
Multiple R-squared:  0.1616,	Adjusted R-squared:  0.1615 
F-statistic:  1478 on 3 and 22998 DF,  p-value: < 0.00000000000000022


$wape
[1] 95.97247

