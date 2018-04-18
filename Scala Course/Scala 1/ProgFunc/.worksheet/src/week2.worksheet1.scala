package week2

object worksheet1 {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(38); val res$0 = 
1+3;System.out.println("""res0: Int(4) = """ + $show(res$0));$skip(87); 

def sum(f: Int => Int, a: Int, b: Int): Int =
	if (a>b) 0
	else f(a) + sum(f, a+1, b);System.out.println("""sum: (f: Int => Int, a: Int, b: Int)Int""");$skip(25); 


def id(x:Int):Int = x;System.out.println("""id: (x: Int)Int""");$skip(44); ;

def sumInts(a:Int, b:Int) =  sum(id, a, b);System.out.println("""sumInts: (a: Int, b: Int)Int""");$skip(15); val res$1 = 

sumInts(1, 6);System.out.println("""res1: Int = """ + $show(res$1));$skip(19); val res$2 = 


(x:Int) => x*x*x;System.out.println("""res2: Int => Int = """ + $show(res$2));$skip(23); val res$3 = 

(x: Int, y: Int)=>x+y;System.out.println("""res3: (Int, Int) => Int = """ + $show(res$3));$skip(48); 

def sumInts1(a: Int, b: Int) = sum(x=>x, a, b);System.out.println("""sumInts1: (a: Int, b: Int)Int""");$skip(136); 

def sum1(f: Int => Int, a: Int , b:Int) = {
	def loop(a:Int, acc:Int): Int =
		if (a>b) acc
		else loop(a+1, f(a)+acc)
		
	loop(a,0)
};System.out.println("""sum1: (f: Int => Int, a: Int, b: Int)Int""");$skip(17); val res$4 = 

sumInts1( 3, 5);System.out.println("""res4: Int = """ + $show(res$4));$skip(121); 


def sum2(f:Int=>Int): (Int, Int)=>Int = {
def sumF(a:Int, b:Int): Int =
	if (a>b) 0
	else f(a) + sumF(a+1,b)
	
sumF

};System.out.println("""sum2: (f: Int => Int)(Int, Int) => Int""");$skip(27); 

def sumInts2 = sum2(x=>x);System.out.println("""sumInts2: => (Int, Int) => Int""");$skip(15); val res$5 = 
sumInts2(1,10);System.out.println("""res5: Int = """ + $show(res$5));$skip(18); val res$6 = 

sum2(x=>x)(1,10);System.out.println("""res6: Int = """ + $show(res$6));$skip(80); 

def sum3(f: Int =>Int)(a:Int, b:Int):Int=
if (a>b) 0 else f(a)+ sum3(f)(a+1,b);System.out.println("""sum3: (f: Int => Int)(a: Int, b: Int)Int""");$skip(20); val res$7 = 

sum3(x=>x*x)(1,10);System.out.println("""res7: Int = """ + $show(res$7));$skip(89); 

def product1(f:Int=> Int)(a:Int, b:Int):Int =
	if (a>b) 1
	else f(a)*product1(f)(a+1,b);System.out.println("""product1: (f: Int => Int)(a: Int, b: Int)Int""");$skip(24); val res$8 = 
	
product1(x=>x*x)(3,4);System.out.println("""res8: Int = """ + $show(res$8));$skip(39); 

def fact(n:Int) = product1(x=>x)(1,n);System.out.println("""fact: (n: Int)Int""");$skip(9); val res$9 = 

fact(5);System.out.println("""res9: Int = """ + $show(res$9));$skip(159); 

def mapReduce(f: Int => Int, combine: (Int, Int) => Int, zero: Int)(a:Int, b:Int):Int =
	if (a>b) zero
	else combine(f(a), mapReduce(f,combine, zero)(a+1,b));System.out.println("""mapReduce: (f: Int => Int, combine: (Int, Int) => Int, zero: Int)(a: Int, b: Int)Int""");$skip(81); 
	
	
def product(f:Int => Int)(a:Int, b:Int):Int = mapReduce(f,(x,y)=>x*y,1)(a,b);System.out.println("""product: (f: Int => Int)(a: Int, b: Int)Int""");$skip(42); 
def factorial(n:Int) = product(x=>x)(1,n);System.out.println("""factorial: (n: Int)Int""");$skip(14); val res$10 = 

factorial(5);System.out.println("""res10: Int = """ + $show(res$10))}







}
