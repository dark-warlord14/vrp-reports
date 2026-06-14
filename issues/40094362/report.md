# Security: JSC::Yarr regexp 32/48 to the left of 768 with workers

| Field | Value |
|-------|-------|
| **Issue ID** | [40094362](https://issues.chromium.org/issues/40094362) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2011-08-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

The repro itself is rather large, and it contains a lot of repetition, inside a lot of repetition and it takes a lot of tries to repro it.

But it does happen over and over with this file and not with others.

repro.html is the main file, and the others are the stock files from the chromium/webkit automated tests.

it only works with the http:// schema for me, (maybe because there are no workers in the file:// schema?)

the filesystem api is not needed for this, because it says in the output div:  

[Worker] This test requires FileSystem API.  

Got error from worker: Uncaught ReferenceError: requestFileSystem is not defined

**VERSION**

Chromium 15.0.864.0 (Developer Build 98444-dirty)  

OS Linux  

WebKit 535.2 (trunk@93707)  

JavaScript V8 3.5.8

64bit linux

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: worker thread, sad tab

==12910== ERROR: AddressSanitizer crashed on address 0x00007fffe5724450 at pc 0x7ffff669080b bp 0x7ffc56f05c70 sp 0x7ffc56f05c00  

READ of size 4 at 0x00007fffe5724450 thread T96  

#0 0x7ffff669080b in JSC::Yarr::Interpreter::matchDisjunction(JSC::Yarr::ByteDisjunction\*, JSC::Yarr::Interpreter::DisjunctionContext\*, bool) ???:0  

#1 0x7ffff668cdc5 in JSC::Yarr::Interpreter::interpret() ???:0  

#2 0x7ffff668c9e4 in JSC::Yarr::interpret(JSC::Yarr::BytecodePattern\*, unsigned short const\*, unsigned int, unsigned int,

0x00007fffe5724450 is located 48 bytes to the left of 768-byte region [0x00007fffe5724480,0x00007fffe5724780)  

allocated by thread T0 here:  

#0 0x7ffff6c7d7ea in malloc *asan\_rtl*  

#1 0x7ffff373cf2b in WTF::fastMalloc(unsigned long) ???:0  

#2 0x7ffff669b734 in WTF::Vector<JSC::Yarr::ByteTerm, 0ul>::reserveCapacity(unsigned long) ???:0  

#3 0x7ffff669811d in JSC::Yarr::ByteCompiler::regexBegin(unsigned int, unsigned int, bool) ???:0  

#4 0x7ffff668c1d8 in JSC::Yarr::ByteCompiler::compile(WTF::BumpPointerAllocator\*) ???:0

## Attachments

- [asan-worker.txt](attachments/asan-worker.txt) (text/plain; charset=us-ascii, 8.7 KB)
- [repro.html](attachments/repro.html) (text/plain; charset=us-ascii, 366 B)
- [worker-repro.zip](attachments/worker-repro.zip) (application/zip; charset=binary, 8.8 KB)

## Timeline

### ts...@chromium.org (2011-08-29)

[Empty comment from Monorail migration]

### ts...@chromium.org (2011-08-29)

[Empty comment from Monorail migration]

### ka...@google.com (2011-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2011-08-31)

Mind taking a look at https://crbug.com/chromium/72548?
I've seen some random race reports from JSC::Yarr on our TSan UI bot

### kc...@chromium.org (2011-08-31)

Interesting! 
The race reports in  https://crbug.com/chromium/72548 look extremely weird, but if there is an OOB access these race reports start making sense.

The initial comments by miaubiz@ about the required long repetition also suggest a race. 

### js...@chromium.org (2011-09-06)

[Empty comment from Monorail migration]

### ma...@google.com (2011-09-08)

[Empty comment from Monorail migration]

### ka...@google.com (2011-09-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-16)

@kareng: let's avoid assigning things to security@chromium.org for now. It makes it look like something is being worked on when in fact it is not :)

### [Deleted User] (2011-09-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-06)

It's a race condition in DOMImplementation::isXMLMIMEType. In a normal renderer the static local xmlTypeRegExp will always be initialized on the main thread. However, in a worker process you can have multiple threads racing to initialize xmlTypeRegExp, which can cause you to crash on a wild read when the initialization conflicts between two threads.

I'm inclined to bump this out of security queue given that it's a race to an OOB read where you don't control any input data and can't read back the value. However, I'll just bump it down to low-severity. It's an easy enough problem to fix. I just need to figure out the WebKit way to do it.


### in...@chromium.org (2011-10-08)

http://trac.webkit.org/changeset/96999

### js...@chromium.org (2011-10-08)

Bumping it up to medium since it can be triggered after xmlTypeRegExp is initialized, which gives control of at least the source string.

### in...@chromium.org (2011-10-09)

merged to m15 in r97020.

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-21)

https://bugs.webkit.org/show_bug.cgi?id=69665

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-16)

We're going over old bugs that might have missed going in front of the VRP panel.  The panel decided to award $1,000 for this bug!

### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/94487?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094362)*
