package week2

object worksheet1 {
1+3                                               //> res0: Int(4) = 4

def sum(f: Int => Int, a: Int, b: Int): Int =
	if (a>b) 0
	else f(a) + sum(f, a+1, b)                //> sum: (f: Int => Int, a: Int, b: Int)Int


def id(x:Int):Int = x;                            //> id: (x: Int)Int

def sumInts(a:Int, b:Int) =  sum(id, a, b)        //> sumInts: (a: Int, b: Int)Int

sumInts(1, 6)                                     //> res1: Int = 21


(x:Int) => x*x*x                                  //> res2: Int => Int = week2.worksheet1$$$Lambda$9/1239731077@2133c8f8

(x: Int, y: Int)=>x+y                             //> res3: (Int, Int) => Int = week2.worksheet1$$$Lambda$10/997110508@1e643faf

def sumInts1(a: Int, b: Int) = sum(x=>x, a, b)    //> sumInts1: (a: Int, b: Int)Int

def sum1(f: Int => Int, a: Int , b:Int) = {
	def loop(a:Int, acc:Int): Int =
		if (a>b) acc
		else loop(a+1, f(a)+acc)
		
	loop(a,0)
}                                                 //> sum1: (f: Int => Int, a: Int, b: Int)Int

sumInts1( 3, 5)                                   //> res4: Int = 12


def sum2(f:Int=>Int): (Int, Int)=>Int = {
def sumF(a:Int, b:Int): Int =
	if (a>b) 0
	else f(a) + sumF(a+1,b)
	
sumF

}                                                 //> sum2: (f: Int => Int)(Int, Int) => Int

def sumInts2 = sum2(x=>x)                         //> sumInts2: => (Int, Int) => Int
sumInts2(1,10)                                    //> res5: Int = 55

sum2(x=>x)(1,10)                                  //> res6: Int = 55

def sum3(f: Int =>Int)(a:Int, b:Int):Int=
if (a>b) 0 else f(a)+ sum3(f)(a+1,b)              //> sum3: (f: Int => Int)(a: Int, b: Int)Int

sum3(x=>x*x)(1,10)                                //> res7: Int = 385

def product1(f:Int=> Int)(a:Int, b:Int):Int =
	if (a>b) 1
	else f(a)*product1(f)(a+1,b)              //> product1: (f: Int => Int)(a: Int, b: Int)Int
	
product1(x=>x*x)(3,4)                             //> res8: Int = 144

def fact(n:Int) = product1(x=>x)(1,n)             //> fact: (n: Int)Int

fact(5)                                           //> res9: Int = 120

def mapReduce(f: Int => Int, combine: (Int, Int) => Int, zero: Int)(a:Int, b:Int):Int =
	if (a>b) zero
	else combine(f(a), mapReduce(f,combine, zero)(a+1,b))
                                                  //> mapReduce: (f: Int => Int, combine: (Int, Int) => Int, zero: Int)(a: Int, b
                                                  //| : Int)Int
	
	
def product(f:Int => Int)(a:Int, b:Int):Int = mapReduce(f,(x,y)=>x*y,1)(a,b)
                                                  //> product: (f: Int => Int)(a: Int, b: Int)Int
def factorial(n:Int) = product(x=>x)(1,n)         //> factorial: (n: Int)Int

factorial(5)                                      //> res10: Int = 120







}