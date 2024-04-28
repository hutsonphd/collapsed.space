---
layout: default
parent: Books
id: "50776459"
fullTitle: Shape Up Stop Running in Circles and Ship Work that Matters
pages: "133"
cover: https://www.colemanm.org/images/books/singer-shape-up.jpg
datePublished: 2019-01-01
title: Shape Up
author:
  - "[[Ryan Singer]]"
avgRating: "4.28"
tags:
  - book
relations:
  - "[[Product Development]]"
  - "[[Software Development Methodologies]]"
  - "[[Risk Management]]"
  - "[[Project Management]]"
  - "[[Team Collaboration]]"
  - "[[Problem Solving]]"
  - "[[Time Management]]"
  - "[[Work Planning]]"
  - "[[Task Delegation]]"
  - "[[Bug Fixing Strategies]]"
---
![](https://www.colemanm.org/images/books/singer-shape-up.jpg)

{: .abstract}
>This is an online web book about how Basecamp does their work.  
>
>This book is a guide to how we do product development at Basecamp. It’s also a toolbox full of techniques that you can apply in your own way to your own process.
>
>Whether you’re a founder, CTO, product manager, designer, or developer, you’re probably here because of some common challenges that all software companies have to face.

[Link to Free eBook](https://basecamp.com/shapeup/shape-up.pdf)
## Takeaways
### Six-week cycles
Six weeks is long enough to build something meaningful start-to-finish and short enough that everyone can feel the deadline looming from the start, so they use the time wisely.
### Shape the work
…before giving it to a team. A small senior group works in parallel to the cycle teams. They define the key elements of a solution before we consider a project ready to bet on. Projects are defined at the right level of abstraction: concrete enough that the teams know what to do, yet abstract enough that they have room to work out the interesting details themselves.
### Give full responsibility
…to a small integrated team of designers and programmers. They define their own tasks, make adjustments to the scope, and work together to build vertical slices of the product one at a time. This is completely different from other methodologies, where managers chop up the work and programmers act like ticket-takers.
### Reduce risk
…in the shaping process by solving open questions _before_ we commit the project to a time box
### Shaping has four main steps
1. **Set boundaries.** First we figure out how much time the raw idea is worth and how to define the problem. This gives us the basic boundaries to shape into.
2. **Rough out the elements.** Then comes the creative work of sketching a solution. We do this at a higher level of abstraction than wireframes in order to move fast and explore a wide enough range of possibilities. The output of this step is an idea that solves the problem within the appetite but without all the fine details worked out.
3. **Address risks and rabbit holes.** Once we think we have a solution, we take a hard look at it to find holes or unanswered questions that could trip up the team. We amend the solution, cut things out of it, or specify details at certain tricky spots to prevent the team from getting stuck or wasting time.
    

![[Pasted image 20231027212632.png]]Rough outline of elements. Not a wireframe.
![[Pasted image 20231027212703.png]]
Full mocked up solution. Not ideal before work begins.
### 5 Ingredients of a pitch
1. **Problem** — The raw idea, a use case, or something we’ve seen that motivates us to work on this
2. **Appetite** — How much time we want to spend and how that constrains the solution
3. **Solution** — The core elements we came up with, presented in a form that’s easy for people to immediately understand
4. **Rabbit holes** — Details about the solution worth calling out to avoid problems
5. **No-gos** — Anything specifically excluded from the concept: functionality or use cases we intentionally aren’t covering to fit the appetite or make the problem tractable
![[Pasted image 20231027213135.png]]
### Bugs and Defects
1. **Use cool-down**. Ask any programmer if there are things they wish they could go back and fix and they’ll have a list to show you. The `cool-down`period between cycles gives them time to do exactly that. Six weeks is not long to wait for the majority of bugs, and two weeks every six weeks actually adds up to a lot of time for fixing them.
2. **Bring it to the betting table**. If a bug is too big to fix during cool-down, it can compete for resources at the betting table. Suppose a back-end process is slowing the app down and a programmer wants to change it from a synchronous step to an asynchronous job. The programmer can make the case for fixing it and shape the solution in a pitch. Then instead of interrupting other work, the people at the betting table can make a deliberate decision. Time should always be used strategically. There’s a huge difference between delaying other work to fix a bug versus deciding up front that the bug is worth the time to fix.
3. **Schedule a bug smash**. Once a year—usually around the holidays—we’ll dedicate a whole cycle to fixing bugs. We call it a “bug smash.” The holidays are a good time for this because it’s hard to get a normal project done when people are traveling or taking time off. The team can self-organize to pick off the most important bugs and solve long-standing issues in the front-end or back-end.