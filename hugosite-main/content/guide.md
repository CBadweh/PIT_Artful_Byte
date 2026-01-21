+++
title = "Learning Embedded by Building"
url = "/embedded-guide"
draft = false
type = "page"
categories = []
tags = []
[_build]
  list = "never"
+++

Getting into embedded systems can feel overwhelming since it covers everything from designing integrated circuits and PCBs to FPGA development, firmware, applications, operating systems, and more. It’s easy to spend more time researching than actually building. In my experience, the best way to cut through that kind of confusion is to simply pick something and focus on it. This short guide is my attempt to show one way of doing that: by approaching your learning as a series of projects.

I’ve worked in embedded for about seven years, mostly in software and more recently some hardware. That gives me enough background to have something to say, but not the whole picture, so this guide is naturally shaped by my personal experience. The upside is that you get a practical, personal take from someone who has been doing the work. The trade-off is that it doesn't cover everything like a [broad roadmap](https://github.com/m3y54m/Embedded-Engineering-Roadmap) (great reference!) might.

I do plan to keep this updated, so if something isn’t clear or if you have questions, send a message to _niklas@artfulbytes.com_.

# 🙋‍♂️ How I got into embedded
I didn't grow up soldering or coding like some do. I spent most of my youth playing video games. Luckily I still gravitated toward technical subjects and ended up studying computer engineering, but it wasn't until my final year that I realized embedded systems might be for me. Even after years of study, I saw myself as a practical person and felt frustrated at how theoretical most of engineering was. Many of my peers went into pure programming or web development, where there were plenty of opportunities. I thought about it too, but I wasn’t sure it would satisfy my practical side or my curiosity about how things really work.

At first embedded seemed just as abstract, but doing small projects on my own made it click. I understood that embedded engineers bring hardware and software together in the devices around us. Sure, it is still heavy on theory, but the link to the physical world through building circuits, testing boards, debugging code, and seeing something come alive gave me the connection I was searching for.

Looking back, doing projects was not only how I learned embedded, but also how I discovered that I enjoyed it. If you are unsure whether it’s for you, the best way to find out is to try. And today it’s easier than ever to experiment on your own, with affordable components, PCB services, and plenty of resources online to guide you.

# 👨🏻‍💻 Start with programming
I know this is a guide about embedded, but don’t pick up any hardware just yet if you have little or no programming experience. If I were starting again, this is where I’d begin. I’m biased, since most of my work has been in embedded software. A hardware-oriented person might suggest starting with electronics, but here’s why I think programming first is the better entry point.

First, programming is low-risk. No matter where you end up in embedded, it will be useful, and even outside the field it’s a valuable skill. When you later do your own embedded projects, you’ll quickly hit a wall without it. The barrier to entry is also low: all you need is a computer. You can be writing and running code right away instead of reading theory or buying extra gear.

Second, learn one thing at a time. Learning programming and embedded at once won’t make you faster; it only adds confusion. The principles of programming are the same whether your code runs on a PC or on a microcontroller. If you start on your own computer, you separate the programming itself from the added complexity of hardware. That clarity helps you know what’s what when you do move onto a board later.

## First Python
So programming it is. But which language? I would start with a high-level one like Python and focus on learning the basics: loops, conditionals, functions, and program flow. Starting with Python instead of C is also about learning one thing at a time. Python lets you concentrate on programming itself without getting stuck in low-level details too early. It is also a language I still use often for automation, scripting, and as a general tool, so it is useful to know beyond learning. With so many good tutorials available, it makes a very approachable entry point into programming.

I would start with a basic Python tutorial, something popular, whether it is on YouTube, Udemy, or somewhere else. I often learn better by hearing the same thing from different tutors, so I would not be afraid to bounce between a couple until one clicks. Once I had the basics down, I would get out of tutorial land and move on to projects.

I would begin with something really simple. If I did not have a project in mind, I would search for “Python project list” and pick something that felt doable and interesting, like a calculator, a to-do list, or a tic-tac-toe game. It does not need to be unique or impressive. The point is to practice. Once I had done a few small ones, I would move on to something a little bigger and try to implement things myself instead of leaning too much on libraries.

## Then C
After Python, I would move on to C. Despite other languages like C++ and Rust, C is the dominant language in embedded even after fifty years, so there is no way around learning it. Coming from a language like Python, you will quickly notice how much tougher it feels. What takes one line in Python might take ten in C. That contrast is part of why I think starting with a higher-level language helps, it makes the value of C clearer.

C brings you right up against the hardware and how it works, which is critical for embedded. At this stage I would still avoid getting any embedded hardware. It is better to learn C in isolation and focus on understanding pointers and memory (they are essentially [how your code really controls hardware](https://youtu.be/sp3mMwo3PO0)), as well as how and why a C program is compiled.

Practically, I would approach C the same way as Python: start with a solid beginner tutorial to cover the basics, then move on to projects, growing from simple to more advanced ones. Re-implementing one of your Python projects in C is especially useful, since it makes the differences obvious.

_**NOTE:** Your choice of computer, operating system, or editor does not matter much at this stage. Use what you have, or pick what seems easiest, and get going. Tooling rabbit holes (Linux vs. Windows vs. Mac, Vim vs. Emacs) can wait._

_**NOTE:** I didn’t have ChatGPT when I was starting, but today I often use it as a tutor when learning._

# ⚙️ Pick up a microcontroller board
After doing a few projects in C and getting a basic grasp of programming, that’s when I would finally pick up a board. At that point you have enough foundation to make it useful rather than just confusing.

When I say “microcontroller board”, I mean those small printed circuit boards with a microcontroller on them. They are basically tiny computers, and they sit at the heart of most embedded systems today. Up until now your code has been running on a PC, which is a powerhouse compared to these chips. A board shifts the learning to hardware that is closer to what embedded engineers actually work with.

## First Arduino?
When it comes to picking a board, Arduino is hard to ignore. It’s by far the most popular microcontroller board (ecosystem) among hobbyist makers. They love it because it makes it easy to get something up and running quickly without worrying about the low-level details of the microcontroller.

Embedded engineers, on the other hand, mostly dislike Arduino. Those low-level details are the core of the work, and Arduino hides them away. To many engineers it feels more like a toy than a tool, something that doesn’t really teach you how embedded systems actually work. You almost never see an Arduino board inside a real product.

Honestly, I think the embedded engineers overreact. If you’ve never programmed a microcontroller board before, Arduino isn’t a bad place to start. It hides a lot of details and won’t teach you everything, but just like Python can be a stepping stone toward C, Arduino can be a stepping stone toward more capable boards. They’re cheap, easy to get, and handy to have around later for quick prototypes. I still use them sometimes for prototypes in my professional work. So by all means, pick one up and play around: blink some LEDs, read button inputs, and get that first feeling of controlling hardware. Maybe even get one of those Arduino starter kits and go through the projects there (good for learning some basic electronics too).

## Then a "real" board, but which one?
Regardless of whether you spend some time with an Arduino or not, sooner or later you’ll want a "real" embedded board.

Which one?

My short answer is _STM32_, but let me explain.

There are thousands of boards out there from different companies, each with their own pros and cons. In a professional setting, the choice often comes down to factors like performance, cost, and availability. For learning though, most of that does not matter. What matters is picking a board that makes learning smoother. Almost any board will work for the projects you do at the start, since at a fundamental level they all operate in similar ways. What you really want to learn are the general principles. Once you have worked with one microcontroller, it is much easier to pick up another, just like with programming languages.

When I was starting out, I overthought this part. I thought I had to find the best board for my project, because that is what professionals do, and I wanted to be a professional. But when learning is the goal, the choice mostly comes down to four things:

* **Simplicity:** A complex board can run simple projects too, but all the extra features become a distraction at the beginning. You end up spending energy figuring out which details are relevant and which to ignore, instead of just learning the basics.
* **Tooling:** The whole development environment matters, not just the IDE and compiler, but also the debugger, programmer, and how smooth it is to flash code and test. As a professional you sometimes have to put up with clunky or outdated tools because of cost or availability. As a learner, you do not need that pain.
* **Documentation:** Clear datasheets, application notes, and code examples are invaluable. Good documentation saves countless hours of guessing and searching.
* **Popularity:** The more widely a board is used, the more resources exist around it, such as tutorials, libraries, forums, courses, and ready-made code you can study. Even ChatGPT will have more to say about it.

STM32 checks almost all of those boxes. Tooling is solid, devkits with onboard debuggers, a decent vendor IDE, but also options to work from VS Code or use the toolchain directly from the command line. The documentation is strong, with readable and extensive datasheets and app notes. And STM32 is widely popular, which means endless tutorials, courses, and community support. The only drawback is complexity: even the smallest STM32 is more complex than what you’d ideally want as a first board. That makes the learning curve a little steeper. But because it does so well in the other areas, and its relevance in the industry, it's where I would start.

As for which STM32 to get, there are many options. If following a course or tutorial, I would buy exactly what they use. Otherwise, I’d start with a Nucleo board like the Nucleo-F303K8 or one of the Nucleo-64 boards. The STM32F4-Discovery is also a solid choice. These all come with everything you need on board, so you can plug in a USB cable and just start.

# 🛠️ Got a board, now what?
Once you have a board, the question is what to do with it. The answer is simple: build something. You learn embedded by doing, and even a tiny project gives your learning direction. Instead of “I’m learning this just because,” it becomes “I’m learning this so I can build that.” That shift keeps you focused and makes what you learn stick.

## Projects!
Tutorials, books, and courses are great, but treat them as tools to move your project forward. If you only consume material, you are not really building and not really learning.

The feedback loop should be:

Do → hit a question → look it up → apply it → keep going.

There is far too much to learn in embedded to ever know it all. Most of my work comes down to knowing some fundamentals and learning the rest on the go. Projects train the same habit by giving you a goal and pushing you to learn only what you need. In the beginning I would focus on those fundamentals by programming the microcontroller board as directly as possible. This is called bare-metal programming. Instead of relying on helper code, you write code that talk straight to the hardware. This forces you to actually understand the mechanisms and building blocks that make the microcontroller tick.

Sure, as an engineer I do not write bare-metal code all day. Real projects are often too complex for that, and it's impractical to not depend on code like drivers, libraries, or operating systems that others have already built. But the understanding I have of bare-metal is what lets me use those layers effectively and gives me the skills to debug, extend, or fix things when they do not work. If you jump into abstractions too early you can get things running, like with an Arduino, but without really understanding why.

For the first projects I would use what is already on the board, like LEDs and buttons. I would keep the projects small enough to code from scratch. If I needed ideas, I would browse project lists (Arduino ones are good at this stage) and copy what others have built, maybe with a small twist to make it unique or more challenging.

## A project example
To exemplify what I mean, let’s imagine I want to build a lamp that turns on and off when you press a button. It sounds trivial, but even for a project this small, there is plenty to figure out.

The first step is just getting the board to do anything. The vendor usually has a getting started guide with instructions on downloading the IDE and running a sample program. With an STM32 that would mean installing STM32CubeIDE, compiling a blink example, flashing it to the board, and checking that the LED actually blinks. At that point I would not understand much, but at least I would know that I can build and run code on the board.

_**NOTE:** If you feel adventurous at this point, you can try building and flashing from the command line with the toolchain directly. But start with the manufacturer’s IDE since it’s the easiest way to get going._

Since I want to control an LED for my project, I would look into how that works. In the code from the sample program I might see something called GPIO being toggled. That would make me search _“what is GPIO”_ and read a bit about it. Then I would try changing the code to make the LED blink in different patterns, just to see that I can. Most likely at this stage I would be using the vendor’s helper code (HAL drivers), and that is fine. But I might also take the chance to open the datasheet, find the GPIO registers, and try [writing to them directly](https://youtu.be/sp3mMwo3PO0). It is a good exercise to see what is really happening under the hood.

Next comes the button. I might already have figured out the on-board button is connected to another GPIO pin and that GPIOs can act as input not just outputs. I would refer to the board documentation to figure out which pin it is connected to. Then I would modify my code to configure that pin as input and confirm that I can read its state. Perhaps I would start by reading it in a loop and turning the LED on when the state is high. From there I would add logic to toggle it on each press. When it behaves oddly I would search for why and discover button bounce, and from there discover concepts like delays, polling, or interrupts.

At that point the basic lamp would work, but I could keep extending it. Maybe I want the LED to turn off automatically after a few minutes, so I look up how to keep track of time and find something called timers. Or I want to count how many times the button has been pressed, and then figure out how to send that number to my computer over USB, which introduces me to UART. Then I realize the count disappears when I unplug the board, which leads me to learn about [how microcontroller memory works](https://www.youtube.com/watch?v=hyIEUCIVhQQ). Maybe I want to dim the LED instead of just on or off, so I read about PWM and try that.

Even a small project like this makes me look things up and learn step by step. Each feature I come up with reveals another building block or mechanism, and because it is for the project, I immediately see its purpose. That is the power of learning by building.

# 🚀 Beyond the board
Soon I would run out of things to do with just a microcontroller board alone. Then it's time to start adding outside parts.

Continuing the lamp project: instead of pressing a button, maybe I want the LED to turn on when the room gets dark. A quick search would lead me to photoresistors, which change their resistance with light. I would learn that they produce a voltage that the microcontroller can read through something called an ADC. That would be my first extra component and the point where I start learning some basic electronics.

_**NOTE:** At this stage it is natural to start building a small embedded toolbox and lab. That means picking up basic electronics parts like a breadboard, wires, resistors, and capacitors. Tools come gradually too: a multimeter first, then as the need comes up maybe a power supply or a logic analyzer. Soldering tools and oscilloscope can wait._

At some point I might want the lamp to turn on or off at certain times of day. That would have me pick up a DS3231 real-time clock on a breakout board, which talks I2C. Or I might want to show the current time or the lamp’s state on a small display, such as an ST7735 TFT, which talks SPI. Parts like these would naturally have me learn about the standard communication protocols in embedded systems.

_**NOTE:** Use Arduino projects as inspiration for widely used parts. You might even get them working on an Arduino first and then replicate with your own board. STM32 Nucleo boards are also compatible with many Arduino shields._

The lamp was just one example, but many projects would teach the same fundamentals. A microcontroller only has so many building blocks, and each project gives you another angle on them. Over time the overlap adds up, and you gradually build a clear mental model of how they fit together and how to use them.

# 👉 Where to go from here
Once you’ve found a way into embedded and built a few small projects, the main thing is simply to keep going. At face value there isn’t much more to learning embedded systems than doing just that. Build things, solve problems, and let each project push you into the next thing you need to learn.

As you do that, you’ll organically expand your skills and tools. Don’t try to load up everything at once. Let projects pull in what you need, when you need it. That might mean learning a new software practice, picking up a lab instrument, or diving deeper into electronics. Adding these gradually keeps the focus on building, not on preparing endlessly.

More concretely, after you’ve tried some bare-metal microcontroller projects, a few broad directions to explore are

* **Go sideways (learn other microcontrollers)**
    - Working with different boards and architectures broadens your perspective. Simpler 8-bit MCUs can make fundamentals clearer, and you quickly realize that most microcontrollers share more similarities than differences.

* **Go down (learn more hardware)**
    - Dig deeper into how things actually work. Write assembly and learn more about the inside of a CPU. Try programmable hardware like FPGAs and get closer to integrated circuit design. Spend more time with electronics and design a PCB of your own. Or branch into mechanical aspects, like designing an enclosure or experimenting with 3D printing.
    - _**NOTE:** This side of embedded has become far more accessible in recent years. Open-source tools like KiCad and low-cost manufacturing services make it realistic for a single person to design and build hardware. I think every embedded engineer should design and bring up at least one PCB. It is fun, rewarding, and eye-opening._

* **Go up (learn more software)**
    - Move further up the stack from bare-metal into real-time operating systems such as FreeRTOS or Zephyr, or even embedded Linux. This exposes you to larger and more complex systems, and gives you a sense of how software is structured at scale.

## Double down
At some point you will need to pick an area and double down. There is too much for anyone to master completely. Early on it is good to keep an open mind and explore. I started almost entirely with low-level software, but over the years I’ve touched on many areas, and more recently I’ve focused on hardware design too. I still like to explore outside my main focus for breadth.

Learning embedded is not a straight path. It is not a roadmap where you master one topic and move on. More often you will touch something, set it aside, and come back later. Some projects lean heavier on electronics, some on programming, and some will seem like wasted time. That is all part of it.

## Consider a degree
Hobby projects are powerful, but they only go so far. They don’t face the same constraints as real systems like volume, cost, size, and power. That is why they can feel like a pretend game. My [embedded project series](https://www.youtube.com/playlist?list=PLS_iNJJVTtiRV0DZRDcTHnvAuDrKGPN40) is an example of this: I spent weeks programming a sumo robot bare-metal with professional practices even though I could have built something similar with an Arduino in a few days.

If you want to go beyond hobby projects, that usually means studying. Not because school is where you truly learn embedded — most of what I use day to day I learned outside or on the job — but because a university education gives you a broader engineering foundation and the stamp many companies still want. It also gives you the breathing room to solely focus on learning over a fixed timespan instead of having to squeeze it in on the side. Even if you decide to study, it is worth starting to build on your own first because it gives you a stronger sense of purpose going in. And once you are studying, keep building alongside it as the hands-on projects will teach you the most, and are valuable to show later.

## Closing thoughts
This was my take on learning embedded. It’s not the whole picture, and it wasn’t meant to be. I just wanted to suggest one possible way into the field and give a push toward learning through projects. If this guide has done that, then in my eyes it has done what it was supposed to do.

