package week1

object worksheet1 {
  1+2                                             //> res0: Int(3) = 3
  def abs(x:Double): Double = if (x<0) -x else x  //> abs: (x: Double)Double
  
  def sqrt(x:Double) = {
  
	  def sqrtIter(guess: Double): Double =
	  		if (isGoodEnough(guess)) guess
	  		else sqrtIter(improve(guess))
	  
	  def isGoodEnough(guess: Double): Boolean =
	  		abs(guess * guess - x)/x <0.001
	  		
	  	def improve(guess:Double): Double =
	  		(guess + x/guess)/2
	  		
	  	sqrtIter(1.0)
  }                                               //> sqrt: (x: Double)Double
  
  
  
  sqrt(4)                                         //> res1: Double = 2.000609756097561
  
  
  def gcd(a:Int, b:Int): Int = if (b==0) a else gcd(b,a%b)
                                                  //> gcd: (a: Int, b: Int)Int
  
  gcd(14,21)                                      //> res2: Int = 7
	
	def factorial(n:Int): Int = if (n==0) 1 else n * factorial(n-1)
                                                  //> factorial: (n: Int)Int
	
	factorial(24)                             //> res3: Int = -775946240
	
	
	def pascal(c: Int, r: Int): Int = {
      
      if (c==0 && r==0) 1
      else if (c>r || c<0 ) 0
      else pascal(c-1,r-1) + pascal(c,r-1)
      
    }                                             //> pascal: (c: Int, r: Int)Int
    
   pascal(1,3)                                    //> res4: Int = 3
	
	def balance(chars: List[Char]): Boolean = {
        def positionCount(position: Int, result: Int):Int = {
            if (position<0) result
            else if (chars(position)=='(') positionCount(position-1,result+1)
            else if (chars(position)==')') positionCount(position-1,result-1)
            else positionCount(position-1,result)
        }
        positionCount(chars.length-1, 0)==0
    }                                             //> balance: (chars: List[Char])Boolean
	
	
	def countChange(money: Int, coins: List[Int]): Int = {
      def loop(money: Int, coins: List[Int]): Int = {
        if (money<0 || coins.isEmpty) 0
        else if (money==0) 1
        else loop(money, coins.tail) + loop(money - coins.head, coins)
        }
      loop(money,coins)
      }                                           //> countChange: (money: Int, coins: List[Int])Int
    
    
    countChange(3,List(1,2))                      //> res5: Int = 2
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}