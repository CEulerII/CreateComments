from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

# #线性
# def func_linear(x, a, b):
#     return a * x+ b
# #二次
# def func_poly_2(x, a, b, c):
#     return a*x*x + b*x + c
# #三次
# def func_poly_3(x, a, b, c , d):
#     return a*x*x*x + b*x*x + c*x + d
# #幂函数
# def func_power(x, a, b):
#     return x**a + b
# #指数函数
# def func_exp(x, a, b):
#     return a**x + b
def func_5PL(x,a,b,c,d,m):
    try:
        return abs(d+(a-d)*(1+(x/c)**b)**(-m))
    except Exception:
        pass

# 待拟合点
xdata = [1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	15,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36,	37,	38,	39,	40,	41,	42,	43,	44,	45,	46,	47,	48,	49,	50,	51,	52,	53,	54,	55,	56,	57,	58,	59,	60,	61,	62,	63,	64,	65,	66,	67,	68,	69,	70,	71,	72,	73,	74,	75,	76,	77,	78,	79,	80,	81,	82,	83,	84,	85,	86,	87,	88,	89,	90,	91,	92,	93,	94,	95,	96,	97,	98,	99,	100]

ydata = [1,	1,	2,	3,	3,	4,	4,	10,	8,	6,	8,	12,	9,	12,	16,	15,	15,	9,	13,	13,	12,	13,	13,	5,	32,	33,	27,	22,	32,	23,	20,	18,	21,	51,	30,	52,	70,	13,	421,	30,	85,	65,	70,	75,	84,	138,	91,	70,	41,	89,	80,	83,	67,	113,	151,	85,	107,	100,	100,	170,	65,	36,	75,	164,	91,	85,	200,	154,	144,	73,	135,	198,	337,	153,	88,	119,	175,	172,	228,	151,	168,	157,	169,	168,	224,	271,	189,	144,	185,	199,	237,	176,	124,	256,	186,	267,	274,	234,	305,	175]
    
x = list(np.arange(0, 100, 0.01))

# 绘制散点
plt.scatter(xdata[:], ydata[:], 25, "red")

# popt数组中，存放的就是待求的参数a,b,c,......
# popt, pcov = curve_fit(func_linear, xdata, ydata)
# y1 = [func_linear(i, popt[0], popt[1]) for i in x]
# plt.plot(x, y1, 'r')


# popt, pcov = curve_fit(func_poly_2, xdata, ydata)
# y2 = [func_poly_2(i, popt[0], popt[1], popt[2] ) for i in x]
# plt.plot(x, y2, 'g')

# popt, pcov = curve_fit(func_poly_3, xdata, ydata)
# y3 = [func_poly_3(i, popt[0], popt[1], popt[2] ,popt[3]) for i in x]
# plt.plot(x, y3, 'b')

# popt, pcov = curve_fit(func_power, xdata, ydata)
# y4 = [func_power(i, popt[0], popt[1]) for i in x]
# plt.plot(x, y4, 'y')

# popt, pcov = curve_fit(func_exp, xdata, ydata)
# y5 = [func_exp(i, popt[0], popt[1]) for i in x]
# plt.plot(x, y5, 'c')

param_bounds=([-np.inf,-np.inf,0,-np.inf,-np.inf],[np.inf,0,np.inf,np.inf,np.inf])
# param_bounds=([-1,-np.inf,0,-np.inf,-np.inf],[1,np.inf,np.inf,np.inf,np.inf])

popt, pcov = curve_fit(func_5PL, xdata, ydata , maxfev=10000, bounds=param_bounds,check_finite=True)
#根据函数的特征，c一定是大于0的，b一定小于0的(b<0确保x趋近0的时候，函数值为0)，由于b<0，x>0，所以确保收敛有定义，c一定是大于0的。
#要不就是a非常小，限制-1,1应该是可以的，同样c大于零，b不限制。一般用上面的方法就可以了。上面那种在x=0附近比较准确。
y6 = [func_5PL(i, popt[0], popt[1],popt[2] ,popt[3],popt[4]) for i in x]
print("a="+str(popt[0]))
print("b="+str(popt[1]))
print("c="+str(popt[2]))
print("d="+str(popt[3]))
print("m="+str(popt[4]))

mean = np.mean(ydata)
ss_tot = np.sum((ydata - mean) ** 2)
ss_res = np.sum((ydata - func_5PL(xdata, *popt)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

print("R^2="+str(r_squared))
plt.plot(x, y6, 'black',label='a=%5.5f, \nb=%5.5f, \nc=%5.5f, \nd=%5.5f, \nm=%5.5f' % tuple(popt)+'\nR^2='+str(round(r_squared,10)))
plt.xlabel('xlabel')
plt.ylabel('ylabel')
plt.legend(prop={'family' : 'Arial', 'size' : 8})
plt.show()