# Security: LayoutBlock Security DCHECK FAILED

| Field | Value |
|-------|-------|
| **Issue ID** | [40085875](https://issues.chromium.org/issues/40085875) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | sj...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-11-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

this case security dcheck fail in <https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/layout/LayoutBlock.h?type=cs&q=Layoutblock.h&sq=package:chromium&l=570>

code in LayoutBlock.h:570  

DEFINE\_LAYOUT\_OBJECT\_TYPE\_CASTS(LayoutBlock, isLayoutBlock());

DEFINE\_LAYOUT\_OBJECT\_TYPE\_CASTS macro define in <https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/layout/LayoutObject.h?type=cs&sq=package:chromium&rcl=1478435172&l=2552>

code in LayoutObject.h:2552  

#define DEFINE\_LAYOUT\_OBJECT\_TYPE\_CASTS(thisType, predicate) \  

DEFINE\_TYPE\_CASTS(thisType, LayoutObject, object, object->predicate, \  

object.predicate)

} // namespace blink

DEFINE\_TYPE\_CASTS in define <https://cs.chromium.org/chromium/src/third_party/WebKit/Source/wtf/Assertions.h?q=DEFINE_TYPE_CASTS&sq=package:chromium&dr=CSs&l=292>

#define DEFINE\_TYPE\_CASTS(thisType, argumentType, argumentName, \  

pointerPredicate, referencePredicate) \  

inline thisType\* to##thisType(argumentType\* argumentName) { \  

SECURITY\_DCHECK(!argumentName || (pointerPredicate)); \  

return static\_cast<thisType\*>(argumentName); \  

} \  

inline const thisType\* to##thisType(const argumentType\* argumentName) { \  

SECURITY\_DCHECK(!argumentName || (pointerPredicate)); \  

return static\_cast<const thisType\*>(argumentName); \  

} \  

inline thisType& to##thisType(argumentType& argumentName) { \  

SECURITY\_DCHECK(referencePredicate); \  

return static\_cast<thisType&>(argumentName); \  

} \  

inline const thisType& to##thisType(const argumentType& argumentName) { \  

SECURITY\_DCHECK(referencePredicate); \  

return static\_cast<const thisType&>(argumentName); \  

} \  

void to##thisType(const thisType\*); \  

void to##thisType(const thisType&)

on IDA side, here  

.text:1B140106 loc\_1B140106: ; CODE XREF: ?absoluteVisualRect@LayoutInline@blink@@EBE?AVLayoutRect@2@XZ+2E2j  

.text:1B140106 mov ecx, ebx  

.text:1B140108 call dword ptr [edx] ; <--- return null  

.text:1B14010A mov ecx, ebx  

.text:1B14010C test al, al  

.text:1B14010E jnz short loc\_1B14013E  

.text:1B140110 mov ecx, [esi+14h]  

.text:1B140113 push 3  

.text:1B140115 push 23Ah  

.text:1B14011A push offset asc\_22A598A0 ; "../../third\_party/WebKit/Source\core/l"...  

.text:1B14011F call ??0LogMessage@logging@@QAE@PBDHH@Z  

.text:1B140124 push offset asc\_22A59900 ; "Security DCHECK failed: !object || (obj"... ; //just dcheck failed.  

.text:1B140129 push dword ptr [esi+30h]  

.text:1B14012C call ??$?6U?$char\_traits@D@std@@@std@@YAAAV?$basic\_ostream@DU?$char\_traits@D@std@@@0@AAV10@PBD@Z  

.text:1B140131 add esp, 8  

.text:1B140134 mov ecx, [esi+14h]  

.text:1B140137 call ??1LogMessage@logging@@QAE@XZ ; <--- hit here  

.text:1B14013C mov ecx, ebx

-------result -----

(c64.3828): WOW64 breakpoint - code 4000001f (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for C:\Users\jeonghoon\Desktop\win32-release\_asan-win32-release-430162\asan-win32-release-430162\chrome\_child.dll  

chrome\_child!base::debug::BreakDebugger+0xc:  

1519b9ac cc int 3

**VERSION**  

Chrome Version: win32-release-430162  

Operating System: Windows 10 Pro 64bit

**REPRODUCTION CASE**

<html>
<head>
<head>
<title>::: reproduce-14fc2a :::</title>
</head>
<script>
function start()
{
//make dom objects.
o13 = document.createElement('frameset');
o13.id = 'o13';
```
	o25 = document.createElement('time');  
	o25.id = 'o25';  

	o28 = document.createElement('listing');  
	o28.id = 'o28';  

	o161 = document.createElement('applet');  
	o161.id = 'o161';  

	o25.appendChild(o28.cloneNode(true));  
	o161.appendChild(o25.cloneNode(true));  
	document.body.appendChild(o161);  
	document.body.appendChild(o13);  
}  
</script>  

```
</head>
<body onload="start();">
</bdoy>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: stack trace

ChildEBP RetAddr Args to Child  

0173a558 14f4c620 41b58ab3 21095d3e 14f4bea0 chrome\_child!base::debug::BreakDebugger+0xc [C:\b\c\b\win\_asan\_release\src\base\debug\debugger\_win.cc @ 21]  

0173ac78 1af1013c 41b58ab3 2282a879 1af0feb4 chrome\_child!logging::LogMessage::~LogMessage+0x780 [C:\b\c\b\win\_asan\_release\src\base\logging.cc @ 748]  

(Inline) -------- -------- -------- -------- chrome\_child!blink::toLayoutBlock+0x16e [C:\b\c\b\win\_asan\_release\src\third\_party\WebKit\Source\core\layout\LayoutBlock.h @ 570]  

0173ae74 1bd9dbe2 0173aeb0 41b58ab3 22d7035a chrome\_child!blink::LayoutInline::absoluteVisualRect+0x288 [C:\b\c\b\win\_asan\_release\src\third\_party\WebKit\Source\core\layout\LayoutInline.cpp @ 1140]  

0173af80 1cb0db8e 0173bf60 0173c038 0173c03c chrome\_child!blink::AXLayoutObject::isOffScreen+0xd4 [C:\b\c\b\win\_asan\_release\src\third\_party\WebKit\Source\modules\accessibility\AXLayoutObject.cpp @ 382]  

0173af94 1cb0545e 0173c038 41b58ab3 231db885 chrome\_child!content::AXStateFromBlink+0xce [C:\b\c\b\win\_asan\_release\src\content\renderer\accessibility\blink\_ax\_enum\_conversion.cc @ 47]  

0173c030 1c862bb5 03f7c270 04a17f48 41b58ab3 chrome\_child!content::BlinkAXTreeSource::SerializeNode+0x3e6 [C:\b\c\b\win\_asan\_release\src\content\renderer\accessibility\blink\_ax\_tree\_source.cc @ 309]  

0173c510 1c8630f5 03f7c3b0 0173cd40 41b58ab3 chrome\_child!ui::AXTreeSerializer[blink::WebAXObject,content::AXContentNodeData,content::AXContentTreeData](javascript:void(0);)::SerializeChangedNodes+0xce5 [C:\b\c\b\win\_asan\_release\src\ui\accessibility\ax\_tree\_serializer.h @ 496]  

0173c9f0 1c85216d 03f7ba30 0173cd40 41b58ab3 chrome\_child!ui::AXTreeSerializer[blink::WebAXObject,content::AXContentNodeData,content::AXContentTreeData](javascript:void(0);)::SerializeChangedNodes+0x1225 [C:\b\c\b\win\_asan\_release\src\ui\accessibility\ax\_tree\_serializer.h @ 528]  

0173cc70 1c8580b6 03f7b110 0173cd40 41b58ab3 chrome\_child!ui::AXTreeSerializer[blink::WebAXObject,content::AXContentNodeData,content::AXContentTreeData](javascript:void(0);)::SerializeChanges+0xb3f [C:\b\c\b\win\_asan\_release\src\ui\accessibility\ax\_tree\_serializer.h @ 382]  

0173d194 15214068 0c244b60 41b58ab3 210f3239 chrome\_child!content::RenderAccessibilityImpl::SendPendingAccessibilityEvents+0x59c [C:\b\c\b\win\_asan\_release\src\content\renderer\accessibility\render\_accessibility\_impl.cc @ 346]  

(Inline) -------- -------- -------- -------- chrome\_child!base::internal::RunMixin+0x36 [C:\b\c\b\win\_asan\_release\src\base\callback.h @ 47]  

0173d3b0 190b86f2 21fddd20 0173d500 41b58ab3 chrome\_child!base::debug::TaskAnnotator::RunTask+0x408 [C:\b\c\b\win\_asan\_release\src\base\debug\task\_annotator.cc @ 50]  

0173d8f4 190b4131 03b09e10 41b58ab3 21fde676 chrome\_child!blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0xcf2 [C:\b\c\b\win\_asan\_release\src\third\_party\WebKit\Source\platform\scheduler\base\task\_queue\_manager.cc @ 378]  

0173dc6c 190bcb2f 00000000 00000000 00000001 chrome\_child!blink::scheduler::TaskQueueManager::DoWork+0x74d [C:\b\c\b\win\_asan\_release\src\third\_party\WebKit\Source\platform\scheduler\base\task\_queue\_manager.cc @ 253]  

(Inline) -------- -------- -------- -------- chrome\_child!base::internal::FunctorTraits+0x95 [C:\b\c\b\win\_asan\_release\src\base\bind\_internal.h @ 214]  

(Inline) -------- -------- -------- -------- chrome\_child!base::internal::InvokeHelper+0x135 [C:\b\c\b\win\_asan\_release\src\base\bind\_internal.h @ 289]  

(Inline) -------- -------- -------- -------- chrome\_child!base::internal::Invoker+0x135 [C:\b\c\b\win\_asan\_release\src\base\bind\_internal.h @ 361]  

0173dd14 15214068 03b09f50 41b58ab3 210f3239 chrome\_child!base::internal::Invoker<base::internal::BindState<void (blink::scheduler::TaskQueueManager::\*)(base::TimeTicks, bool) **attribute**((thiscall)),base::WeakPtr[blink::scheduler::TaskQueueManager](javascript:void(0);),base::TimeTicks,bool>,void ()>::Run+0x17b [C:\b\c\b\win\_asan\_release\src\base\bind\_internal.h @ 343]  

(Inline) -------- -------- -------- -------- chrome\_child!base::internal::RunMixin+0x36 [C:\b\c\b\win\_asan\_release\src\base\callback.h @ 47]  

0173df30 150681e1 210bc680 0173e290 41b58ab3 chrome\_child!base::debug::TaskAnnotator::RunTask+0x408 [C:\b\c\b\win\_asan\_release\src\base\debug\task\_annotator.cc @ 50]  

0173e284 15069e5d 0173e290 03a4c1b0 21d20fdb chrome\_child!base::MessageLoop::RunTask+0x801 [C:\b\c\b\win\_asan\_release\src\base\message\_loop\message\_loop.cc @ 413]  

(Inline) -------- -------- -------- -------- chrome\_child!base::MessageLoop::DeferOrRunPendingTask+0x51e [C:\b\c\b\win\_asan\_release\src\base\message\_loop\message\_loop.cc @ 422]  

0173e3f8 1521ca95 41b58ab3 210f4080 1521c6f0 chrome\_child!base::MessageLoop::DoWork+0x75d [C:\b\c\b\win\_asan\_release\src\base\message\_loop\message\_loop.cc @ 513]  

0173e4f4 1506742a 04709140 41b58ab3 210bc8f0 chrome\_child!base::MessagePumpDefault::Run+0x3a5 [C:\b\c\b\win\_asan\_release\src\base\message\_loop\message\_pump\_default.cc @ 35]  

0173e658 150ff03e 41b58ab3 210ccaac 150fee70 chrome\_child!base::MessageLoop::RunHandler+0x14a [C:\b\c\b\win\_asan\_release\src\base\message\_loop\message\_loop.cc @ 379]  

0173e738 1c7814a2 41b58ab3 231421a0 1c780f10 chrome\_child!base::RunLoop::Run+0x1ce [C:\b\c\b\win\_asan\_release\src\base\run\_loop.cc @ 36]  

0173ea54 14ed2b48 0173ed40 41b58ab3 2102c8ae chrome\_child!content::RendererMain+0x592 [C:\b\c\b\win\_asan\_release\src\content\renderer\renderer\_main.cc @ 198]  

0173ecac 14ed43e2 0173ecd0 0173ed40 0173edf0 chrome\_child!content::RunNamedProcessTypeMain+0x1e6 [C:\b\c\b\win\_asan\_release\src\content\app\content\_main\_runner.cc @ 408]  

0173edc0 14ed2695 0173ef60 664ae209 302e7dbc chrome\_child!content::ContentMainRunnerImpl::Run+0x21c [C:\b\c\b\win\_asan\_release\src\content\app\content\_main\_runner.cc @ 776]  

0173edd4 0fdd11bb 0173ee50 41b58ab3 201bc5c0 chrome\_child!content::ContentMain+0x75 [C:\b\c\b\win\_asan\_release\src\content\app\content\_main.cc @ 20]  

0173efc8 0081a3dc 00810000 0173f1c0 1c5c7f76 chrome\_child!ChromeMain+0x1bb [C:\b\c\b\win\_asan\_release\src\chrome\app\chrome\_main.cc @ 97]

## Attachments

- [tc.html](attachments/tc.html) (text/plain, 475 B)

## Timeline

### cl...@chromium.org (2016-11-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6265463412883456

### cl...@chromium.org (2016-11-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4913832725315584

### cl...@chromium.org (2016-11-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4805152856080384

### ri...@chromium.org (2016-11-10)

Hi, I'm unable to reproduce this bug on my end - would you mind taking a look to see if you can learn anything from stack trace, tkent@?

[Monorail components: Blink>Layout]

### tk...@chromium.org (2016-11-10)

eae@, can you triage this?

  for (LayoutBlock* currBlock = containingBlock();
       currBlock && currBlock->isAnonymousBlock();
       currBlock = toLayoutBlock(currBlock->nextSibling())) {

currBlock->nextSibling() isn't a LayoutBlock?


### ea...@chromium.org (2016-11-10)

Christian, could you look into this when you get a chance?

### [Deleted User] (2016-11-10)

Looks pretty shady to assume that the sibling of a LayoutBlock has to be a LayoutBlock too.

Example:
<span>
    <div></div>
</span>
<img style="display:block;">

Results in this:
*LayoutView 0x32db0b404010             	#document
  LayoutBlockFlow 0x32db0b41c010       	HTML
    LayoutBlockFlow 0x32db0b41c128     	BODY
      LayoutBlockFlow (anonymous) 0x32db0b41c240
        LayoutInline 0x32db0b46c010 continuation=0x32db0b41c588	SPAN
          LayoutText 0x32db0b424010    	#text "\n    "
      LayoutBlockFlow (anonymous) 0x32db0b41c588 continuation=0x32db0b46c0c8
        LayoutBlockFlow 0x32db0b41c470 	DIV
      LayoutBlockFlow (anonymous) 0x32db0b41c358
        LayoutInline 0x32db0b46c0c8    	SPAN
        LayoutText 0x32db0b4240c0      	#text "\n"
      LayoutImage 0x32db0b470010       	IMG style="display:block;"

Now, if you toLayoutBlock(0x32db0b41c358->nextSibling()), it will boom, since it's a LayoutImage.

I'd also say that the code deserves some documentation. :)

### [Deleted User] (2016-11-10)

The code was introduced by https://codereview.chromium.org/767283005

### sh...@chromium.org (2016-11-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-11-11)

Marking as impact stable based on https://crbug.com/chromium/662767#c8, thanks!

### ri...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-21)

cbiesinger: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2016-11-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5045799395524608

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-05)

cbiesinger: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sj...@gmail.com (2016-12-07)

sill alive?

### cb...@chromium.org (2016-12-15)

So isAnonymousBlock() returns true even though it's not a block? That seems bad?

That said, I can't actually reproduce this bug... Morten, since you did some investigation, do you want to take it?

### ro...@chromium.org (2016-12-15)

sjh21a - clusterfuzz can't reproduce your crash, nor can we. Can you attach a html file that reproduces the issue for you locally and we'll try that?

If I just rewrote the loop would someone LGTM that without a crashing testcase?

### sj...@gmail.com (2016-12-16)

check again this issue, ASAP.
thx :D

### [Deleted User] (2016-12-16)

Note that I haven't been able to reproduce any crash. The test case above is just something I imagined would cause trouble in LayoutInline::absoluteVisualRect(). I think you need to use spatial navigation to end up in that method.

Fixing it is super-easy, although it would be great to have a test case first, of course.

isAnonymousBlock() is not the problem. The problem is that we assume that a sibling of a LayoutBlock also is a LayoutBlock. But it could be a LayoutImage instead, for instance.

### sj...@gmail.com (2016-12-16)

i did check again in "asan-win32-release-438808" version.
it is no longer crash. can't not reproduce :)


### cb...@chromium.org (2016-12-16)

Morten, you're right, I misread the loop -- sorry.

### sh...@chromium.org (2017-01-06)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### ea...@chromium.org (2017-03-07)

If we can't figure out the root cause here let's at least change the security DCHECK to a CHECK.

### [Deleted User] (2017-03-07)

I finally managed to dream up a test case for this. You need an inline anchor element inside inside another inline. Inside the anchor there has to be a block, so that then engine sets up an inline continuation chain. The outer inline needs a sibling that's a block-displayed non-LayoutBlock, e.g. an img width display:block. And then you need to do stuff with spatial navigation.

I've come to the conclusion that the loop should be able to safely do toLayoutBlock(currBlock->nextSibling()), and that the bug is deeper down: we fail to find the end of the continuation chain, due to nested inlines.

Will file a CL soon.

### [Deleted User] (2017-03-07)

https://codereview.chromium.org/2738503004/

### bu...@chromium.org (2017-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e72c8c06b956706b54648589f807086d17340831

commit e72c8c06b956706b54648589f807086d17340831
Author: mstensho <mstensho@opera.com>
Date: Wed Mar 08 09:45:16 2017

Search the entire subtree when looking for the end of an inline continuation chain.

Inlines may be nested, so we may not find the last inline in the chain as a
direct child of the anonymous blocks. We need to search the entire subtree.
Don't do this with anonymous blocks that wrap block children (the block-level
DOM children of the inline-level objects), though. We're not going to find
anything interesting there.

This fix is speculative; the original bug report didn't come with a test case.

BUG=662767

Review-Url: https://codereview.chromium.org/2738503004
Cr-Commit-Position: refs/heads/master@{#455420}

[add] https://crrev.com/e72c8c06b956706b54648589f807086d17340831/third_party/WebKit/LayoutTests/fast/spatial-navigation/snav-div-in-anchor-and-img-crash.html
[modify] https://crrev.com/e72c8c06b956706b54648589f807086d17340831/third_party/WebKit/Source/core/layout/LayoutInline.cpp


### [Deleted User] (2017-03-08)

One thing I didn't notice, was that the description in this bug report actually contains a test case, albeit not reproducible out of the box. It would crash like a charm upon loading, if the --force-renderer-accessibility command line argument is specified, though.

It generates a tree like this:

*LayoutView 0x176fd4e04010             	#document
  LayoutBlockFlow 0x176fd4e1c010       	HTML
    LayoutBlockFlow 0x176fd4e1c140     	BODY
      LayoutBlockFlow (anonymous) 0x176fd4e1c3a0
        LayoutInline 0x176fd4e3c1a0 continuation=0x176fd4e3c650	APPLET id="o161"
          LayoutInline 0x176fd4e3c4c0 continuation=0x176fd4e1c4d0	TIME id="o25"
      LayoutBlockFlow (anonymous) 0x176fd4e1c4d0 continuation=0x176fd4e3c010
        LayoutBlockFlow 0x176fd4e1c600 	LISTING id="o28"
      LayoutBlockFlow (anonymous) 0x176fd4e1c270
        LayoutInline 0x176fd4e3c650    	APPLET id="o161"
          LayoutInline 0x176fd4e3c010  	TIME id="o25"
      LayoutFrameSet 0x176fd4e2c010    	FRAMESET id="o13"

I.e. similar to the test in the CL that just landed, only that it uses LayoutFrameSet instead of LayoutImage, none of them being LayoutBlock-based. Another difference is that there's no A element here, so we cannot exercise the code with spatial navigation, but with accessibility support it can be done. If we call LayoutInline::absoluteVisualRect() with the inner LayoutInline (0x176fd4e3c4c0), it'd fail to find the end of the continuation chain without my fix, just like the test case in my CL.

I have verified that the original test no longer crashes with my fix in, so closing.

### sh...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-13)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), bhthompson@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4bebd1dbc191a41fcc5cb6a64a5a832868686657

commit 4bebd1dbc191a41fcc5cb6a64a5a832868686657
Author: Morten Stenshorne <mstensho@opera.com>
Date: Mon Mar 13 20:48:34 2017

Search the entire subtree when looking for the end of an inline continuation chain.

Inlines may be nested, so we may not find the last inline in the chain as a
direct child of the anonymous blocks. We need to search the entire subtree.
Don't do this with anonymous blocks that wrap block children (the block-level
DOM children of the inline-level objects), though. We're not going to find
anything interesting there.

This fix is speculative; the original bug report didn't come with a test case.

BUG=662767

Review-Url: https://codereview.chromium.org/2738503004
Cr-Commit-Position: refs/heads/master@{#455420}
(cherry picked from commit e72c8c06b956706b54648589f807086d17340831)

Review-Url: https://codereview.chromium.org/2752483002 .
Cr-Commit-Position: refs/branch-heads/3029@{#163}
Cr-Branched-From: 939b32ee5ba05c396eef3fd992822fcca9a2e262-refs/heads/master@{#454471}

[add] https://crrev.com/4bebd1dbc191a41fcc5cb6a64a5a832868686657/third_party/WebKit/LayoutTests/fast/spatial-navigation/snav-div-in-anchor-and-img-crash.html
[modify] https://crrev.com/4bebd1dbc191a41fcc5cb6a64a5a832868686657/third_party/WebKit/Source/core/layout/LayoutInline.cpp


### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-15)

Congratulations! The panel decided to award $1,000 for this bug :-)

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sj...@gmail.com (2017-03-15)

oh..!? thx :D

### aw...@google.com (2017-03-22)

Externally reported high severity bug impacting Stable. Bake time in Dev: 8 days. Bake time in Beta: 6 days. Requesting inclusion in 57 stable update.

### aw...@google.com (2017-03-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2017-03-22)

Merge approved for M57 branch 3029.

### go...@chromium.org (2017-03-22)

Correction: M57 branch is 2987.

### bu...@chromium.org (2017-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/82a69bd443feb20d88e1adfbf77c5c657892484d

commit 82a69bd443feb20d88e1adfbf77c5c657892484d
Author: Morten Stenshorne <mstensho@opera.com>
Date: Wed Mar 22 18:34:34 2017

Search the entire subtree when looking for the end of an inline continuation chain.

Inlines may be nested, so we may not find the last inline in the chain as a
direct child of the anonymous blocks. We need to search the entire subtree.
Don't do this with anonymous blocks that wrap block children (the block-level
DOM children of the inline-level objects), though. We're not going to find
anything interesting there.

This fix is speculative; the original bug report didn't come with a test case.

BUG=662767

Review-Url: https://codereview.chromium.org/2738503004
Cr-Commit-Position: refs/heads/master@{#455420}
(cherry picked from commit e72c8c06b956706b54648589f807086d17340831)

Review-Url: https://codereview.chromium.org/2769703003 .
Cr-Commit-Position: refs/branch-heads/2987@{#862}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[add] https://crrev.com/82a69bd443feb20d88e1adfbf77c5c657892484d/third_party/WebKit/LayoutTests/fast/spatial-navigation/snav-div-in-anchor-and-img-crash.html
[modify] https://crrev.com/82a69bd443feb20d88e1adfbf77c5c657892484d/third_party/WebKit/Source/core/layout/LayoutInline.cpp


### aw...@google.com (2017-03-23)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/662767?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085875)*
