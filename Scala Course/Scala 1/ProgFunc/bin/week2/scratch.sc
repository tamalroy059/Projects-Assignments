package week2

object scratch {
  println("Welcome to the Scala worksheet")       //> Welcome to the Scala worksheet
  
  type Set = Int => Boolean

  /**
   * Indicates whether a set contains a given element.
   */
  def contains(s: Set, elem: Int): Boolean = s(elem)
                                                  //> contains: (s: week2.scratch.Set, elem: Int)Boolean

  /**
   * Returns the set of the one given element.
   */
    def singletonSet(elem: Int): Set = {
      def retFun(a:Int) = a==elem
      retFun
      }                                           //> singletonSet: (elem: Int)week2.scratch.Set
      
   
    def union(s: Set, t: Set): Set = {
      def retFunUnion(a:Int) = {
        contains(s,a)||contains(t,a)
      }
      retFunUnion
    }                                             //> union: (s: week2.scratch.Set, t: week2.scratch.Set)week2.scratch.Set
    
  def singletonSet1(elem: Int): Set = {a:Int => a==elem}
                                                  //> singletonSet1: (elem: Int)week2.scratch.Set
  
  def intersect(s: Set, t: Set): Set = {a:Int => contains(s,a) && contains(t,a)}
                                                  //> intersect: (s: week2.scratch.Set, t: week2.scratch.Set)week2.scratch.Set
  
  
  
}