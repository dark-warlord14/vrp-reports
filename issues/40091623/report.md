# Renderer crash with javascript + setInterval

| Field | Value |
|-------|-------|
| **Issue ID** | [40091623](https://issues.chromium.org/issues/40091623) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | fs...@chromium.org |
| **Created** | 2011-06-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A fuzzed JS1k entry causes a nasty-looking renderer crash. This happens at least on 64-bit Linux. I couldn't reproduce the crash in 32-bit Debian.

I don't have a 64-bit Ubuntu at hand for a debug build. Submitting just the partially minimized plain crash for now to make sure this is spotted before the next stable.

**VERSION**  

Chrome Version: 12.0.742.91 (Official Build 87961) beta (and dev)  

Operating System: Linux (Debian 6.0.1 x86\_64)

**REPRODUCTION CASE**

1. $ google-chrome x.html x.html x.html x.html x.html x.html
2. at least one tab probably crashes

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x00007fffc7cc81f1 in ?? ()  

(gdb) bt  

#0 0x00007fffc7cc81f1 in ?? ()  

#1 0x0000000000000001 in ?? ()  

#2 0x0000000000000000 in ?? ()  

(gdb) x/10i $rip  

0x7fffc7cc81f1: mov 0xf(%r15,%r14,8),%r15  

0x7fffc7cc81f6: cmp -0x60(%r13),%r15  

0x7fffc7cc81fa: je 0x7fffc7cc87b0  

0x7fffc7cc8200: test $0x1,%r15b  

0x7fffc7cc8204: je 0x7fffc7cc87bd  

0x7fffc7cc820a: mov $0x7fffc7c5c549,%r10  

0x7fffc7cc8214: cmp %r10,-0x1(%r15)  

0x7fffc7cc8218: jne 0x7fffc7cc87ca  

0x7fffc7cc821e: mov 0x17(%r15),%rax  

0x7fffc7cc8222: mov 0xf(%r15),%r15  

(gdb) i r  

rax 0x7fffe81a1f69 140737087414121  

rbx 0x0 0  

rcx 0xaf00000000 751619276800  

rdx 0xaf 175  

rsi 0x7fffe7d00041 140737082556481  

rdi 0x7fffe81278a9 140737086912681  

rbp 0x7fffffffc978 0x7fffffffc978  

rsp 0x7fffffffc920 0x7fffffffc920  

r8 0xaf00000000 751619276800  

r9 0xffffffff 4294967295  

r10 0x7fffc7c5c549 140736545015113  

r11 0x0 0  

r12 0x100000000 4294967296  

r13 0x3ade2e0 61727456  

r14 0xffffffff 4294967295  

r15 0x7fffe81278a9 140737086912681  

rip 0x7fffc7cc81f1 0x7fffc7cc81f1  

eflags 0x10286 [ PF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

fctrl 0x37f 895  

fstat 0x0 0  

ftag 0xffff 65535  

fiseg 0x0 0  

fioff 0x0 0  

foseg 0x0 0  

fooff 0x0 0  

fop 0x0 0  

mxcsr 0x1fa5 [ IE ZE PE IM DM ZM OM UM PM ]

## Attachments

- [x.html](attachments/x.html) (text/html; charset=us-ascii, 1.1 KB)

## Timeline

### sc...@gmail.com (2011-06-07)

Yeah, crashes easily enough for me on 64-bit Ubuntu, 12.0.742.91 beta

https://crash/reportdetail?reportid=1a56b4dce05960cc

Hard to tell if it's medium or high severity.

### sc...@gmail.com (2011-06-07)

Fuzzing JS1k, nice idea

### sk...@chromium.org (2011-06-07)

...unless they have compressed script, in which case you'll want to decompress it first, or you'll be sure not to get any results.

Aki, are you aware that pouet.net has a section for JS demos that you may want to use as well?
http://pouet.net/prodlist.php?platform[]=JavaScript

I can get you decompressed source for some of them that I've reversed (and of course for the ones that I wrote).

### ts...@chromium.org (2011-06-07)

Minimizes to pure JS + setInterval:

<html>
  <body>
    <script>
gW=gH=175;
g=[];

for(var n=0; n<gW; n++){
  var l=[];
  for(var p=0; p<gH; p++){
    l.push(1)
  }
  g.push(l)
}

function k(a,b){
  if(a<0||b<0||a>=gW||b>=gH)
    return 0;
  return g[a][b];
}

setInterval(function(){
  for(var a=[],f=0; f<gW; f++){
    var b=[];
    for(var h=0; h<gH; h++){
      var e=0;
      for(var i=-1; i<=1; i++)
        for(var j=-1; j<=1; j++)
           e+=k(f+i,h+j);
      e=k(f,h)==1?1:0;
      b.push(e)
    }
    a.push(b)
  }
},100);
    </script>
  </body>
</html>



### ts...@chromium.org (2011-06-07)

[Empty comment from Monorail migration]

### ao...@gmail.com (2011-06-08)

@skylined thanks for the pointer. I got a poptart cat form pouet.net earlier, but there seem to be also other interesting things :) Decompressed JS demos would certainly be of use if you have time to send some (for example to aohelin@gmail.com).

### ag...@chromium.org (2011-06-08)

I'll have a look at this one.

### ag...@chromium.org (2011-06-08)

This is definitely bad. For some reason we do not get a bounds check for the array index on x64. This works correctly on ia32. I'll dig into it.

### ag...@chromium.org (2011-06-08)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-06-08)

Yeah, the poptartcat uses a png file to store JavaScript using gzip compression. Unless you use the decompressed source, you will mostly end up fuzzing gzip, rather than JS.

I'm sending you decompressed source for a ton of JS demos now.

### ag...@chromium.org (2011-06-08)

This does happen on ia32 as well. We lift a keyedload above its bounds check. Florian will take it from here.

### fs...@chromium.org (2011-06-09)

Fixed in V8 bleeding edge r8230, 3.2.10.17 and 3.3.10.9.



### sc...@gmail.com (2011-06-09)

Thanks for the quick fix, Florian :D

Can I assume you guys will take care of the merge to M12, M13 branches?

### ag...@chromium.org (2011-06-09)

Already done. Florian already merged to the 3.2 branch and 3.3 branch used for M12 and M13. :-)

### sc...@gmail.com (2011-06-16)

@aohelin: nice catch! And good fuzzing idea :) Repro a little large. A please to offer a $500 Chromium Security Reward!

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ao...@gmail.com (2011-06-16)

Great! This bounty goes to Red Cross.

I was going to continue reducing the repro on the 64-bit machine the following day, but you guys had already tracked it down and were fixing it by the time I got back to it. Congrats on yet another fast fix :)

### sc...@gmail.com (2011-06-19)

$1337 send to Red Cross.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bb887d2ccf8df5e44567581147f983f5c53cee21

commit bb887d2ccf8df5e44567581147f983f5c53cee21
Author: Adam Klein <adamk@chromium.org>
Date: Fri Nov 09 19:31:00 2018

[mjsunit] Remove very slow Crankshaft regression test

This test was adapted from a repro, and thus it's rather complex.
It takes over seven minutes to run on the arm64 sim debug bot,
and nearly five minutes on arm.

Given that it was originally accompanied by a very targeted fix in
Crankshaft, it strikes me that this probably isn't worth our CPU
time to continue running.

Bug: v8:7783, chromium:85177
Change-Id: Ibe85cc254aa754365404b5fbbf80bcb1f5a09c68
Reviewed-on: https://chromium-review.googlesource.com/c/1327188
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#57408}
[delete] https://crrev.com/f4a586f06e1f44c2614707bb34d6b9ad6f31698d/test/mjsunit/regress/regress-85177.js


### rs...@chromium.org (2018-11-09)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-09)

This issue was migrated from crbug.com/chromium/85177?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091623)*
