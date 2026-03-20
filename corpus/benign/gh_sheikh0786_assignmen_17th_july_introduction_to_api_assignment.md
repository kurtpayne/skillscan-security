---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sheikh0786/assignment
# corpus-url: https://github.com/sheikh0786/assignment/blob/e59f8511481a4479fa9c30d39a29d2f92e2c803c/17th%20July%20Introduction%20to%20API%20Assignment%20PW%20-%20Skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# 17th July Introduction to API Assignment  

===============================================================================================================================

-----------------------------------------------------------------17th July Introduction to API Assignment --------------------------------------------------------------------------------------

===============================================================================================================================

### 1. WAP to display current date and time in java?
Sol:
```java
import java.time.*;

public class dateTimeApi 
{
    public static void main(String[] args) 
    {
        LocalDate date = LocalDate.now();
            System.out.println(date);
        LocalTime time = LocalTime.now();
            System.out.println(time);
    }
}
```
===============================================================================================================================

### 2. Write a program to convert a date to a string in the format "MM/dd/yyyy"?
Sol:
```java
import java.time.*;
import java.time.format.DateTimeFormatter;
public class dateFormat 
{
    public static void main(String[] args) 
    {
        LocalDate date = LocalDate.now();
        System.out.println(date);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM/dd/yyyy");
        String formattedDate = date.format(formatter);
        System.out.println("Formatted Date: " + formattedDate);
    }    
}
```
==============================================================================================================================

3. What is the difference between collections and streams?Explain with an Example?
Ans:

Collections:

Data Structure: 
Collections represent a data structure that stores a collection of elements, such as a list, set, or map. They are typically used to hold and manage data.
Eager Evaluation: 
When you work with collections, you perform operations on the data eagerly, which means that the operations are executed immediately when called.
Mutability: 
Most collections are mutable, which means you can add, remove, or modify elements in the collection.
Imperative Style: 
You often use imperative code to work with collections, explicitly stating how to perform operations step by step.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

List<Integer> squaredNumbers = new ArrayList<>();
for (Integer num : numbers) {
    squaredNumbers.add(num * num);
}

System.out.println(squaredNumbers);
```

Streams:

Data Flow: 
Streams represent a sequence of data elements that can be processed in a functional style. They are not data structures themselves but can be created from collections or other sources.
Lazy Evaluation: 
Stream operations are evaluated lazily, meaning that they are not executed until you collect the results or trigger a terminal operation. This allows for more efficient processing and optimization.
Immutability: 
Streams themselves are generally immutable. They don't modify the source data but produce new streams or values.
Functional Style: 
You work with streams using a functional style, which involves defining what you want to do with the data rather than how to do it.
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

List<Integer> squaredNumbers = numbers.stream()
    .map(num -> num * num)
    .collect(Collectors.toList());

System.out.println(squaredNumbers);
```

==============================================================================================================================================

### 4. What is enums in java? explain with an example?
Ans:
In Java, an enum (short for "enumeration") is a special data type that is used to define a set of constant values. These constant values represent a fixed set of elements, and you can use enums to create a more structured and self-documenting way of working with such values. Enums are often used when you have a limited, well-defined set of options or choices.
```java
public class enumDemo 
{
    public enum DayOfWeek {
        MONDAY,
        TUESDAY,
        WEDNESDAY,
        THURSDAY,
        FRIDAY,
        SATURDAY,
        SUNDAY
        }
    public static void main(String[] args) 
    {
        for(DayOfWeek d:DayOfWeek.values())
            System.out.println(d);
            

    }
}
```

===============================================================================================================================

### 5. What are in built annotations in java?
Ans:
```
@SuppressWarnings
@FunctionalInterface
@Retention
@Target
@Documented
@Inherited
@Override
@Deprecated
```
==============================================================================================================================================