package recfun

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
   * Exercise 1
   */
    def pascal(c: Int, r: Int): Int = {

      if (c==0 && r==0) 1
      else if (c>r || c<0 ) 0
      else pascal(c-1,r-1) + pascal(c,r-1)
    
    }
  
  /**
   * Exercise 2
   */
    def balance(chars: List[Char]): Boolean = {
        def positionCount(position: Int, result: Int):Int = {
            if (position<0) result
            else if (chars(position)=='(') positionCount(position-1,result+1)
            else if (chars(position)==')') positionCount(position-1,result-1)
            else positionCount(position-1,result)
        }
        positionCount(chars.length-1, 0)==0
    }
      
  /**
   * Exercise 3
   */
    def countChange(money: Int, coins: List[Int]): Int = {
      def loop(money: Int, coins: List[Int]): Int = {
        if (money<0 || coins.isEmpty) 0
        else if (money==0) 1
        else loop(money, coins.tail) + loop(money - coins.head, coins)
        }
      loop(money,coins)
      }
    
  }