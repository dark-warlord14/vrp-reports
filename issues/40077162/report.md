# RIP == 0 in WebCore::StyleResolver::matchAllRules

| Field | Value |
|-------|-------|
| **Issue ID** | [40077162](https://issues.chromium.org/issues/40077162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>CSS |
| **Reporter** | [Deleted User] |
| **Assignee** | ke...@chromium.org |
| **Created** | 2013-03-14 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1

Steps to reproduce the problem:
1. load testcase on webserver
2. point browser to tescase
3. wait for crash

What is the expected behavior?

What went wrong?
please see attached crash analysis 

#0  0x0000000000000000 in ?? ()
#1  0x00005555570759ca in WebCore::StyleResolver::matchAllRules(WebCore::StyleResolver::MatchResult&, bool) ()
#2  0x000055555707f213 in WebCore::StyleResolver::styleForElement(WebCore::Element*, WebCore::RenderStyle*, WebCore::StyleSharingBehavior, WebCore::RuleMatchingBehavior, WebCore::RenderRegion*) ()
#3  0x00005555568cbd24 in WebCore::Element::styleForRenderer() ()
#4  0x00005555568cc973 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ()
#5  0x00005555568ccb44 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ()
#6  0x00005555568ccb44 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ()
#7  0x00005555568aa3e0 in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) ()
#8  0x00005555568aa9be in WebCore::Document::updateStyleIfNeeded() ()
#9  0x0000555556e633ba in WebCore::ThreadTimers::sharedTimerFiredInternal() ()
#10 0x000055555627178d in base::Timer::RunScheduledTask() ()
#11 0x0000555556247d8e in MessageLoop::RunTask(base::PendingTask const&) ()
#12 0x000055555624b40b in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ()
#13 0x000055555624ba13 in MessageLoop::DoWork() ()
#14 0x000055555624c419 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ()
#15 0x0000555556259902 in base::RunLoop::Run() ()
#16 0x0000555556247224 in MessageLoop::Run() ()
#17 0x000055555835a09c in content::RendererMain(content::MainFunctionParams const&) ()
#18 0x000055555613733c in content::ContentMainRunnerImpl::Run() ()
#19 0x0000555556135861 in content::ContentMain(int, char const**, content::ContentMainDelegate*) ()
#20 0x0000555555c6b468 in ChromeMain ()
#21 0x0000555555c6a436 in main ()
rax            0x55555a88fed0	93825079508688
rbx            0x7fffffffc930	140737488341296
rcx            0x7fffffffcf64	140737488342884
rdx            0x0	0
rsi            0x7fffffffc930	140737488341296
rdi            0x31483c9baea0	54186324242080
rbp            0x7ffff7eb7f80	0x7ffff7eb7f80
rsp            0x7fffffffc8b8	0x7fffffffc8b8
r8             0x7fffffffc870	140737488341104
r9             0x31483c9fd000	54186324512768
r10            0xff	255
r11            0x0	0
r12            0x1	1
r13            0x31483c9baea0	54186324242080
r14            0x0	0
r15            0x0	0
rip            0x0	0
eflags         0x10246	[ PF ZF IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
#1  0x00005555570759ca in WebCore::StyleResolver::matchAllRules(WebCore::StyleResolver::MatchResult&, bool) ()
   0x5555570759c2 <_ZN7WebCore13StyleResolver13matchAllRulesERNS0_11MatchResultEb+114>:	mov    %ebp,%edi
   0x5555570759c4 <_ZN7WebCore13StyleResolver13matchAllRulesERNS0_11MatchResultEb+116>:	callq  *0x4e0(%rax)
=> 0x5555570759ca <_ZN7WebCore13StyleResolver13matchAllRulesERNS0_11MatchResultEb+122>:	test   %rax,%rax
   0x5555570759cd <_ZN7WebCore13StyleResolver13matchAllRulesERNS0_11MatchResultEb+125>:	
    je     0x5555570759fa <_ZN7WebCore13StyleResolver13matchAllRulesERNS0_11MatchResultEb+170>
0x55555a8903b0:	0	0	0	0
A debugging session is active.

	Inferior 1 [process 3519] will be killed.

Quit anyway? (y or n) 

Did this work before? N/A 

Chrome version: 25.0.1364.160 (Developer Build 25.0.1364.160-0ubuntu0.12.04.1) Ubuntu 12.04  Channel: stable
OS Version: ubuntu 12.04

## Attachments

- [chrome_2.html](attachments/chrome_2.html) (text/html; charset=us-ascii, 963 B)
- [chromium_crash.log](attachments/chromium_crash.log) (text/x-c; charset=us-ascii, 3.1 KB)
- deleted (application/octet-stream, 0 B)
- [chrome_reduced.html](attachments/chrome_reduced.html) (text/html; charset=us-ascii, 361 B)

## Timeline

### [Deleted User] (2013-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-15)

This testcase also crashes windows canary build

VERSION == 27.0.1440.0 (Official Build 187987) canary

0:014> g
(16cc.6e0): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for chrome.dll - 
chrome_54da0000!ovly_debug_event+0x15277d:
54f122a2 8b4c8b08        mov     ecx,dword ptr [ebx+ecx*4+8] ds:002b:0170e670=????????
0:000:x86> u eip
chrome_54da0000!ovly_debug_event+0x15277d:
54f122a2 8b4c8b08        mov     ecx,dword ptr [ebx+ecx*4+8]
54f122a6 c1e91c          shr     ecx,1Ch
54f122a9 80e101          and     cl,1
54f122ac 384d10          cmp     byte ptr [ebp+10h],cl
54f122af 0f85a0000000    jne     chrome_54da0000!ovly_debug_event+0x152830 (54f12355)
54f122b5 807d1400        cmp     byte ptr [ebp+14h],0
54f122b9 8a550f          mov     dl,byte ptr [ebp+0Fh]
54f122bc 741f            je      chrome_54da0000!ovly_debug_event+0x1527b8 (54f122dd)
0:000:x86> r
eax=01273a60 ebx=012717d0 ecx=001273a6 edx=012717d0 esi=00000000 edi=012717d8
eip=54f122a2 esp=002ae8f0 ebp=002ae914 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_54da0000!ovly_debug_event+0x15277d:
54f122a2 8b4c8b08        mov     ecx,dword ptr [ebx+ecx*4+8] ds:002b:0170e670=????????


### [Deleted User] (2013-03-15)

new crash at different address

0:010> g
(1a04.bec): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for chrome.dll - 
00000000 ??              ???
0:000:x86> u
00000000 ??              ???
           ^ Memory access error in 'u'
0:000:x86> k
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0037e818 58114dfd 0x0
0037e830 5810bf36 chrome_57fa0000!ovly_debug_event+0x1569ab
0037eb9c 580f5c45 chrome_57fa0000!ovly_debug_event+0x14dae4
0037ebcc 5812775f chrome_57fa0000!ovly_debug_event+0x1377f3
0037ec04 58127b0b chrome_57fa0000!ovly_debug_event+0x16930d
0037ec3c 58127b0b chrome_57fa0000!ovly_debug_event+0x1696b9
0037ec74 580cc5b4 chrome_57fa0000!ovly_debug_event+0x1696b9
0037ecc4 58126c2a chrome_57fa0000!ovly_debug_event+0x10e162
0037ecd8 5812b78b chrome_57fa0000!ovly_debug_event+0x1687d8
0037ed00 5812b303 chrome_57fa0000!ovly_debug_event+0x16d339
0037ed10 5812ab6f chrome_57fa0000!ovly_debug_event+0x16ceb1
0037ed30 58129389 chrome_57fa0000!ovly_debug_event+0x16c71d
0037edb0 580e1d22 chrome_57fa0000!ovly_debug_event+0x16af37
0037edcc 580e0536 chrome_57fa0000!ovly_debug_event+0x1238d0
0037edf0 582c33d4 chrome_57fa0000!ovly_debug_event+0x1220e4
0037ee4c 582c333e chrome_57fa0000!ovly_debug_event+0x304f82
0037ee78 581c5137 chrome_57fa0000!ovly_debug_event+0x304eec
0037eeb0 582c325b chrome_57fa0000!ovly_debug_event+0x206ce5
0037ef28 582c31c1 chrome_57fa0000!ovly_debug_event+0x304e09
0037ef38 582c31aa chrome_57fa0000!ovly_debug_event+0x304d6f
0037ef4c 582c315f chrome_57fa0000!ovly_debug_event+0x304d58
0037f018 582c2e2f chrome_57fa0000!ovly_debug_event+0x304d0d
0037f04c 582c2d99 chrome_57fa0000!ovly_debug_event+0x3049dd
0037f068 582c2b5d chrome_57fa0000!ovly_debug_event+0x304947
0037f0c0 581adb34 chrome_57fa0000!ovly_debug_event+0x30470b
0037f168 58063d06 chrome_57fa0000!ovly_debug_event+0x1ef6e2
0037f18c 58063a6d chrome_57fa0000!ovly_debug_event+0xa58b4
0037f1f8 57ffbaad chrome_57fa0000!ovly_debug_event+0xa561b
0037f23c 57fd933d chrome_57fa0000!ovly_debug_event+0x3d65b
0037f24c 57fd22f7 chrome_57fa0000!ovly_debug_event+0x1aeeb
0037f2a8 57fd2072 chrome_57fa0000!ovly_debug_event+0x13ea5
0037f3f8 57fd24dd chrome_57fa0000!ovly_debug_event+0x13c20
0037f424 57fd1cd2 chrome_57fa0000!ovly_debug_event+0x1408b
0037f448 57fd1c2a chrome_57fa0000!ovly_debug_event+0x13880
0037f45c 58003559 chrome_57fa0000!ovly_debug_event+0x137d8
0037f484 580208a0 chrome_57fa0000!ovly_debug_event+0x45107
0037f854 57fb8c97 chrome_57fa0000!ovly_debug_event+0x6244e
0037f868 57fb8c1e chrome_57fa0000!ChromeMain+0xe6cc
0037f8d4 57faa8f7 chrome_57fa0000!ChromeMain+0xe653
0037f8e4 57faa5e9 chrome_57fa0000!ChromeMain+0x32c
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\chrome.exe - 
0037f91c 012d4054 chrome_57fa0000!ChromeMain+0x1e
0037f994 012d6a4b chrome+0x24054
0037f9b8 012d6ab6 chrome!SetPrinterInfo+0x12b
0037fa00 0132f80d chrome!SetPrinterInfo+0x196
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for KERNEL32.dll - 
0037fa90 751533aa chrome!SetPrinterInfo+0x58eed
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for ntdll.dll - 
0037fa9c 773a9ed2 KERNEL32!BaseThreadInitThunk+0x12
0037fadc 773a9ea5 ntdll_77370000!RtlInitializeExceptionChain+0x63
0037faf4 00000000 ntdll_77370000!RtlInitializeExceptionChain+0x36
0:000:x86> ub chrome_57fa0000!ovly_debug_event+0x1569ab
chrome_57fa0000!ovly_debug_event+0x156990:
58114de2 57              push    edi
58114de3 8bc6            mov     eax,esi
58114de5 e84d8dffff      call    chrome_57fa0000!ovly_debug_event+0x14f6e5 (5810db37)
58114dea 83c410          add     esp,10h
58114ded 8b8b5c020000    mov     ecx,dword ptr [ebx+25Ch]
58114df3 8b01            mov     eax,dword ptr [ecx]
58114df5 8b906c020000    mov     edx,dword ptr [eax+26Ch]
58114dfb ffd2            call    edx


### sc...@gmail.com (2013-03-15)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-03-16)

Clusterfuzz isn't hitting anything, but the crash does trigger on canary and stable on Windows. Abhishek, is it possible this is a dupe of something fixed in the last day or so?

### pa...@chromium.org (2013-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-21)

its still works on 

canary 27.0.1447.3 (Official Build 18935

### [Deleted User] (2013-03-21)

asan build 188980 is not crasing testcase but canary buid 189352 does crashes chrome :| can someone tell me what happend !!!

### [Deleted User] (2013-03-25)

27.0.1451.6 (Official Build 190314) canary

### ae...@chromium.org (2013-03-25)

It reproduces for my 27.0.1428.0. Looks like NULL is called here:

void StyleResolver::matchAllRules(MatchResult& result, bool includeSMILProperties)
        ...
        if (m_state.styledElement()->isHTMLElement()) {


### js...@chromium.org (2013-03-26)

@inferno - you offered to take a closer look at this a little over a week ago since cluster-fuzz couldn't repro, but it looks like it may have slipped off your radar.

### js...@chromium.org (2013-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-02)

28.0.1459.0 (Official Build 191575) canary

### ke...@chromium.org (2013-04-05)

I think this is a bad cast. The crashing line is:
 addElementStyleProperties(m_state.styledElement()->additionalPresentationAttributeStyle());

additionalPresentationAttributeStyle() is a virtual function on StyledElement, but it looks like m_state.styledElement is just an Element object that doesn't have that function in its vtable.

### ke...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-08)

Why its not crashing asan builds any particular reason ?

### js...@chromium.org (2013-04-08)

ASAN won't necessarily detect a bad cast. Consider the case where the incorrectly cast value is a pointer to allocated memory that's interpreted in a way that wouldn't otherwise crash (say as a benign integer value).

### ke...@chromium.org (2013-04-08)

Interesting bug. It actually is a use-after-free, but isn't manifesting as one because the stale pointer doesn't immediately get dereferenced. Rather, it gets compared to a different pointer value, causing the StyleResolver to incorrectly believe that the old pointer and the new pointer are the same object. Since the old object and new object are of different types, this turns out looking like a bad cast.

### [Deleted User] (2013-04-12)

reduced testcase

### ke...@chromium.org (2013-04-12)

Great, thanks for that.

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2013-04-17)

Patch up for review: https://codereview.chromium.org/14064008

### bu...@chromium.org (2013-04-18)

------------------------------------------------------------------------
r148687 | inferno@chromium.org | 2013-04-18T21:24:31.749188Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/StyleResolver.cpp?r1=148687&r2=148686&pathrev=148687
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/reload-non-styled-element-crash-expected.txt?r1=148687&r2=148686&pathrev=148687
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/reload-non-styled-element-crash.html?r1=148687&r2=148686&pathrev=148687

Clear StyleResolver state before returning from styleForElement().

A cached element pointer in the resolver state was causing confusion because
in some cases a subsequent call to styleForElement() would use a pointer to
a different object that is at the same memory address as the previous one.

R=dglazkov@chromium.org
BUG=196393

Review URL: https://codereview.chromium.org/14064008

Patch from Ken Buchanan <kenrb@chromium.org>.
------------------------------------------------------------------------

### in...@chromium.org (2013-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-19)

I am not sure but canary build still crashes 

0:014> g
(1838.1690): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for chrome.dll - 
chrome_59b60000!ovly_debug_event+0x143c3e:
59cc3c74 8b448e08        mov     eax,dword ptr [esi+ecx*4+8] ds:002b:01f32b4c=????????


### ke...@chromium.org (2013-04-19)

Give it another day, the patch hasn't made it to canary yet.

### sc...@gmail.com (2013-04-22)

M27: https://src.chromium.org/viewvc/blink?view=rev&revision=148868

### pa...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-23)

testcase not crashing canary build anymore,cheers

### [Deleted User] (2013-05-02)

So whats the status now ? CVE assigned ? 

thanks,
Sachin

### ke...@chromium.org (2013-05-02)

Those are done in batches shortly before a stable update. This fix will move to Chrome stable channel with M27.

### sc...@gmail.com (2013-05-03)

@sachinshinde1102: very interesting bug, thank you!
And a $1000 Chromium Security Reward for uncovering this issue :D

What name should we use to credit you in our release notes?

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### [Deleted User] (2013-05-04)


"Sachin Shinde(@cons0ul)" will be fine

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/196393?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>CSS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077162)*
