# -*- coding: utf-8 -*-
""" this code refer to this article: http://www.codeproject.com/Articles/432194/How-to-Calculate-the-Chi-Squared-P-Value
 
Points of interest
 
- Well, I cannot see how to be made the original code in more Pythonic way... or improve legibility, if anyone could help...
 
It was need to use only Decimal, because float overflow in loop on lines 69 to 74. Not throw an error, but cause NaN and Infinite in some these variables (recomend debug to see for yourself)
 
- So Decimal seems to providing much more accuracy in calculations as far I could see... more than C++ Builder on my runs
 
-getcontext function is used only because I could use power method instead pow function. I see an advantage because I don't need to cast float to Decimal when using pow.
 
- same thing to Decimal exp method, only Decimal data used
 
- Bonus: here you found a C/C++ version tested on C++ Builder XE: http://pastebin.com/Jv85Eu7Y
 
- it's almost equal the original C source, exception to IsNan and IsInfinite wich from VCL Math.
 
"""
 
from decimal import Decimal, getcontext
#from math import gamma
 
A = Decimal('15')
 
def mygamma(z):
 
    """
       The constant SQRT2PI is defined as sqrt(2.0 * PI);
       For speed the constant is already defined in decimal
       form.  However, if you wish to ensure that you achieve
       maximum precision on your own machine, you can calculate
       it yourself using (sqrt(atan(1.0) * 8.0))
 
   """
 
    #const long double SQRT2PI = sqrtl(atanl(1.0) * 8.0);
    SQRT2PI = Decimal('2.5066282746310005024157652848110452530069867406099383')
 
    f = Decimal('1')
    sum_v = SQRT2PI
 
    sc = getcontext().power(z+A,z+Decimal('0.5'))
 
    sc *= Decimal(Decimal('-1') * (z+A)).exp()
 
    sc /= z
 
    for k in range(1,15):
        z+=Decimal('1')
        ck = getcontext().power(A - Decimal(k) , Decimal(k) - Decimal('0.5'))
        ck *= Decimal(A -Decimal(k)).exp()
        ck /= f
 
        sum_v += (ck / z)
 
        f *= (Decimal('-1') * k)
 
    return sum_v * sc
 
def approx_gamma(z):
 
    RECIP_E = Decimal('0.36787944117144232159552377016147')
    TWOPI = Decimal('6.283185307179586476925286766559')
 
    d = Decimal('1.0') / (Decimal('10.0') * z)
    d = Decimal('1.0') / ((Decimal('12') * z) - d)
    d = (d + z) * RECIP_E
    d = getcontext().power(d,z)
    d *= Decimal.sqrt(TWOPI / z)
 
    return d
 
def igf(s, z):
 
    if z < Decimal('0'):
        return Decimal('0')
 
    sc = Decimal('1') / s
    sc *= getcontext().power(z,s)
    sc *= Decimal(-z).exp()
 
    sum_v = Decimal('1')
    nom = Decimal('1')
    denom = Decimal('1')
 
    for i in range(0,200):
        nom *= z
        s+=Decimal('1')
        denom *= s
 
        sum_v += (nom / denom)
 
    return sum_v * sc
 
 
def chisqr(dof, cv):
 
    if cv < Decimal('0') or dof < Decimal('1'):
        return Decimal('0')
 
    k = dof * Decimal('0.5')
    x = cv * Decimal('0.5')
 
    if dof == Decimal('2'):
        # print Decimal(Decimal('-1') * x).exp()
        return Decimal(Decimal('-1') * x).exp()
 
    pvalue = igf(k,x)
 
    if pvalue.is_nan() or pvalue.is_infinite() or pvalue <= 1e-8:
        return 1e-14
 
    pvalue /= mygamma(k)       # res: 0.0636423441336337067152539023
    #pvalue /= approx_gamma(k)  # res: 0.0636423441307368208316220413
    #pvalue = Decimal(gamma(k)) # res: -2.670673575075121885604374585E+212
 
 
    # print 'Dof: %s Cv: %s = %s' % (dof, cv, Decimal('1') - pvalue)
    return Decimal('1') - pvalue
 
if __name__ == '__main__':
 
    chisqr(Decimal('255'), Decimal('290.285192'))
