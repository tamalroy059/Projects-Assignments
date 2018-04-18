package week2

object scratch {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(75); 
  println("Welcome to the Scala worksheet")
  
  type Set = Int => Boolean;$skip(152); 

  /**
   * Indicates whether a set contains a given element.
   */
  def contains(s: Set, elem: Int): Boolean = s(elem);System.out.println("""contains: (s: week2.scratch.Set, elem: Int)Boolean""");$skip(156); 

  /**
   * Returns the set of the one given element.
   */
    def singletonSet(elem: Int): Set = {
      def retFun(a:Int) = a==elem
      retFun
      };System.out.println("""singletonSet: (elem: Int)week2.scratch.Set""");$skip(152); 
      
   
    def union(s: Set, t: Set): Set = {
      def retFunUnion(a:Int) = {
        contains(s,a)||contains(t,a)
      }
      retFunUnion
    };System.out.println("""union: (s: week2.scratch.Set, t: week2.scratch.Set)week2.scratch.Set""");$skip(62); 
    
  def singletonSet1(elem: Int): Set = {a:Int => a==elem};System.out.println("""singletonSet1: (elem: Int)week2.scratch.Set""");$skip(84); 
  
  def intersect(s: Set, t: Set): Set = {a:Int => contains(s,a) && contains(t,a)};System.out.println("""intersect: (s: week2.scratch.Set, t: week2.scratch.Set)week2.scratch.Set""")}
  
  
  
}
