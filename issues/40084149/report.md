# Security: Universal XSS through adopting image elements

| Field | Value |
|-------|-------|
| **Issue ID** | [40084149](https://issues.chromium.org/issues/40084149) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader |
| **Reporter** | ma...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2016-04-21 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a node is being adopted, the tree scope adopter calls |didMoveToNewDocument| on each rescoped node in the tree. The HTMLImageElement implementation of |didMoveToNewDocument| calls the corresponding method on the related loader, which clears and stops observing the associated image resource. In special circumstances, when the adopted image is the last thing being loaded in the old document and the resource has been evicted from the memory cache, this may end up firing timers and events. This allows an attacker to violate a lot of invariants and corrupt the DOM tree.

**VERSION**  

Chrome 50.0.2661.87 (Stable)  

Chrome 51.0.2704.22 (Beta)  

Chrome 51.0.2704.19 (Dev)  

Chromium 52.0.2715.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.2 KB)

## Timeline

### va...@chromium.org (2016-04-22)

This looks somewhat similar to 541206 so assigning to dominicc@ and CC'ing dcheng@ since he appears to have fixed some of the other similar looking UXSS bugs.
Guys, please feel free to re-assign.

Based on [1], assigning P0 since it appears to be a UXSS.

[1]: https://sites.google.com/a/chromium.org/dev/developers/severity-guidelines

[Monorail components: Blink>HTML]

### va...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### ma...@gmail.com (2016-04-22)

UXSS is Security_Severity-High, P1 :-)

Btw, I've got a general fix that should cover all cases where Foo::didMoveToNewDocument (or any other function called by the adopter) does something funny -- please see https://codereview.chromium.org/1910403003

### va...@chromium.org (2016-04-22)

Corrected, thanks for pointing that out.

### dc...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-04-22)

+more loading people

### sh...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-04-23)

Taking a look. I will need help from someone familiar with loading.

Wow, this is an elaborate thing of beauty. Yes, this does look like reliable UXSS.

Could you explain more why blocking script in TreeScope adoption is right? I'm not confident that's a comprehensive fix; it will just cause script to run less, but maybe there are other ways to trigger script at that time.

Only having a superficial poke at the repro, the thing that seems broken is setting f.src to the s.svg and the activity it generates causes i1 to run its XSS javascript: URL despite that (line 45) being detected as XSS.

### do...@chromium.org (2016-04-25)

This hits a debug assert so there's some DOM bug in play:

[1:1:0425/143019:620674404080:FATAL:TreeScopeAdopter.cpp(112)] Check failed: node.treeScope() == oldScope(). 
#0 0x7f0f8904d91e base::debug::StackTrace::StackTrace()
#1 0x7f0f890ae20f logging::LogMessage::~LogMessage()
#2 0x7f0f81034d12 blink::TreeScopeAdopter::updateTreeScope()
#3 0x7f0f81034342 blink::TreeScopeAdopter::moveTreeToNewScope()
#4 0x7f0f81031765 blink::TreeScopeAdopter::execute()
#5 0x7f0f8103025c blink::TreeScope::adoptIfNeeded()
#6 0x7f0f80e8b0be blink::ContainerNode::appendChild()
#7 0x7f0f80fa563a blink::Node::appendChild()
#8 0x7f0f80d8aa81 blink::NodeV8Internal::appendChildMethodForMainWorld()
#9 0x7f0f80d86ee5 blink::NodeV8Internal::appendChildMethodCallbackForMainWorld()
#10 0x7f0f852bca1b v8::internal::FunctionCallbackArguments::Call()
#11 0x7f0f85343a04 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#12 0x7f0f853755d7 v8::internal::Builtin_Impl_HandleApiCall()
#13 0x7f0f8535074f v8::internal::Builtin_HandleApiCall()
#14 0x39451e908967 <unknown>


### ma...@gmail.com (2016-04-25)

> Could you explain more why blocking script in TreeScope adoption is right?

It's implicitly assumed that nothing will run script during node adoption -- some of the assertions depend on static variables, so any script could potentially affect them. However, the real problem is that you may end up with nodes attached to a DOM tree of document A and belonging to document B at the same time. This is a weird state that can cause an array of problems in layout, style, painting, compositing, frame handling, etc. In this case, Blink is confused because the corrupted node will lie about its owner document, and many functions, including Node::containsIncludingShadowDOM, will return wrong values.

> I'm not confident that's a comprehensive fix; it will just cause script to run less, but maybe there are other ways to trigger script at that time.

Running script isn't a problem in and of itself, running script at a wrong time is. This patch is comprehensive in that it ensures that node adoption is never interrupted with a rogue script. There's no guarantee that the scenario outlined in this bug is the only one leading to script execution when a node is being adopted, at least I can't give you one after looking at it :-)

> Only having a superficial poke at the repro, the thing that seems broken is setting f.src to the s.svg and the activity it generates causes i1 to run its XSS javascript: URL despite that (line 45) being detected as XSS.

Actually, it isn't detected, line 45 is just setting up what will be done after the corrupted iframe element is reattached. This is a result of the node corruption mentioned above -- things are already very broken at the time when the adoption is finished, which is what the patch is protecting against.

### do...@chromium.org (2016-04-25)

Thanks; I have been looking at this in the debugger and am starting to grok this. I agree we *should* block scripts during adoption; otherwise the tree scope adopter's assertions are not meaningful. Let's try it and see what breaks.

In general I think this is a loader problem. I don't see why it has to tie together things to do with loading the image, and events for the documents.

Kinuko, maybe someone on your team should take a look at this.

### dc...@chromium.org (2016-04-25)

What does the stack that called into v8 looked like? I haven't looked at this bug in detail, but at the very least, it seems like we /try/ to fire events asynchronously. It seems like the real bug here is that it's not actually running asynchronously?

### bu...@chromium.org (2016-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/146ff1bb11c88778d466bd7a49b544f2b5806ee0

commit 146ff1bb11c88778d466bd7a49b544f2b5806ee0
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Mon Apr 25 07:46:39 2016

Don't allow scripts to run when a node is being adopted.

Running a script in the middle of rescoping nodes can break a lot of invariants and leave DOM in an inconsistent state.

This patch adds a ScriptForbiddenScope in TreeScope::adoptIfNeeded to ensure it never happens.

BUG=605766

Review URL: https://codereview.chromium.org/1910403003

Cr-Commit-Position: refs/heads/master@{#389425}

[modify] https://crrev.com/146ff1bb11c88778d466bd7a49b544f2b5806ee0/third_party/WebKit/Source/core/dom/TreeScope.cpp


### do...@chromium.org (2016-04-25)

Breakpoint 9, blink::FrameLoader::checkCompleted (this=0xc5bed78d858) at ../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:593                                                                                                                      
593         m_frame->document()->setReadyState(Document::Complete);                                                                                                                                                                                           
(gdb) where                                                                                                                                                                                                                                                   
#0  blink::FrameLoader::checkCompleted (this=0xc5bed78d858) at ../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:593                                                                                                                                
#1  0x00007ff17892057a in blink::FrameFetchContext::didLoadResource (this=0x13573afeea48, resource=0xc5bed79a8f0) at ../../third_party/WebKit/Source/core/loader/FrameFetchContext.cpp:393                                                                    
#2  0x00007ff17872352f in blink::ResourceFetcher::didLoadResource (this=0xc5bed7900a8, resource=0xc5bed79a8f0) at ../../third_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:830                                                                          
#3  0x00007ff178733abd in blink::ResourceLoader::releaseResources (this=0x2ed8c865180) at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:80                                                                                                    
#4  0x00007ff178734999 in blink::ResourceLoader::cancel (this=0x2ed8c865180, error=...) at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:205                                                                                                  
#5  0x00007ff17873475a in blink::ResourceLoader::cancel (this=0x2ed8c865180) at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:166                                                                                                             
#6  0x00007ff178734714 in blink::ResourceLoader::cancelIfNotFinishing (this=0x2ed8c865180) at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:161                                                                                               
#7  0x00007ff1787110d3 in blink::Resource::cancelTimerFired (this=0xc5bed79a8f0, timer=0xc5bed79af18) at ../../third_party/WebKit/Source/core/fetch/Resource.cpp:719                                                                                          
#8  0x00007ff178713574 in blink::Resource::allClientsAndObserversRemoved (this=0xc5bed79a8f0) at ../../third_party/WebKit/Source/core/fetch/Resource.cpp:707                                                                                                  
#9  0x00007ff1786f890b in blink::ImageResource::allClientsAndObserversRemoved (this=0xc5bed79a8f0) at ../../third_party/WebKit/Source/core/fetch/ImageResource.cpp:215                                                                                        
#10 0x00007ff1787133e3 in blink::Resource::didRemoveClientOrObserver (this=0xc5bed79a8f0) at ../../third_party/WebKit/Source/core/fetch/Resource.cpp:686                                                                                                      
#11 0x00007ff1786f8507 in blink::ImageResource::removeObserver (this=0xc5bed79a8f0, observer=0xc5bed791f18) at ../../third_party/WebKit/Source/core/fetch/ImageResource.cpp:158                                                                               
#12 0x00007ff17892ec1e in blink::ImageLoader::setImageWithoutConsideringPendingLoadEvent (this=0xc5bed791f18, newImage=0x0) at ../../third_party/WebKit/Source/core/loader/ImageLoader.cpp:211                                                                
#13 0x00007ff17892ea9f in blink::ImageLoader::setImage (this=0xc5bed791f18, newImage=0x0) at ../../third_party/WebKit/Source/core/loader/ImageLoader.cpp:185                                                                                                  
#14 0x00007ff1789305df in blink::ImageLoader::elementDidMoveToNewDocument (this=0xc5bed791f18) at ../../third_party/WebKit/Source/core/loader/ImageLoader.cpp:614                                                                                             
#15 0x00007ff178199b68 in blink::HTMLImageElement::didMoveToNewDocument (this=0x799ee044c50, oldDocument=...) at ../../third_party/WebKit/Source/core/html/HTMLImageElement.cpp:553                                                                           
#16 0x00007ff17808af26 in blink::TreeScopeAdopter::moveNodeToNewDocument (this=0x7ffd3f023778, node=..., oldDocument=..., newDocument=...) at ../../third_party/WebKit/Source/core/dom/TreeScopeAdopter.cpp:136                                               
#17 0x00007ff17808a370 in blink::TreeScopeAdopter::moveTreeToNewScope (this=0x7ffd3f023778, root=...) at ../../third_party/WebKit/Source/core/dom/TreeScopeAdopter.cpp:53                                                                                     
#18 0x00007ff178087765 in blink::TreeScopeAdopter::execute (this=0x7ffd3f023778) at ../../third_party/WebKit/Source/core/dom/TreeScopeAdopter.h:39                                                                                                            
#19 0x00007ff17808625c in blink::TreeScope::adoptIfNeeded (this=0x799ee042520, node=...) at ../../third_party/WebKit/Source/core/dom/TreeScope.cpp:377                                                                                                        
#20 0x00007ff177f15e86 in blink::Document::adoptNode (this=0x799ee0424d0, source=0x799ee044be8, exceptionState=...) at ../../third_party/WebKit/Source/core/dom/Document.cpp:924                                                                              
#21 0x00007ff177d70411 in blink::DocumentV8Internal::adoptNodeMethod (info=...) at gen/blink/bindings/core/v8/V8Document.cpp:3766                                                                                                                             
#22 0x00007ff177d6d745 in blink::DocumentV8Internal::adoptNodeMethodCallback (info=...) at gen/blink/bindings/core/v8/V8Document.cpp:3776                                                                                                                     
#23 0x00007ff17c312a1b in v8::internal::FunctionCallbackArguments::Call (this=0x7ffd3f023ed8, f=0x7ff177d6d730 <blink::DocumentV8Internal::adoptNodeMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&)>) at ../../v8/src/api-arguments.cc:16          
#24 0x00007ff17c399a19 in v8::internal::(anonymous namespace)::HandleApiCallHelper<false> (isolate=0x29c3ed289020, args=...) at ../../v8/src/builtins.cc:4548                                                                                                 
#25 0x00007ff17c3cb5e7 in v8::internal::Builtin_Impl_HandleApiCall (args=..., isolate=0x29c3ed289020) at ../../v8/src/builtins.cc:4566                                                                                                                        
#26 0x00007ff17c3a676f in v8::internal::Builtin_HandleApiCall (args_length=<optimized out>, args_object=<optimized out>, isolate=0x29c3ed289020) at ../../v8/src/builtins.cc:4563

Calls m_frame->document()->setReadyState(Document::Complete) and we are off to the races.

### dc...@chromium.org (2016-04-25)

Doesn't the fix that just landed mean that we (incorrectly) won't run the event handlers at all in this case? IMO, the event handlers should be running: they just shouldn't be running node adoption.

### dc...@chromium.org (2016-04-25)

Running *during* node adoption, sorry for omitting a word.

### ma...@gmail.com (2016-04-25)

The conditions required to fire events in this particular case must be extremely unlikely to be met in practice (we're talking about adopting an image element in the middle of loading a revoked blob URL, which happens to be the last thing loaded in the document the element is adopted from, all carefully timed), so it shouldn't matter if the handlers are deferred or dropped.

### dc...@chromium.org (2016-04-25)

As a short-term fix, I'm OK with this but I don't think there's any debate over what the correct behavior is. At the very least, there needs to be:

- Comments about what a ScriptForbiddenScope is doing here: there's no reason (at first glance) why TreeScopeAdopter would end up running script.
- A test to cover this failure case.
- A followup bug filed to restore the correct behavior (once load events are fired async, which is a project loading team is working on) 

### ma...@gmail.com (2016-04-25)

Okay, I'll take care of the first 2 points tomorrow. I was intentionally vague in the commit to avoid making too much info public without an explicit approval.

### bu...@chromium.org (2016-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/146ff1bb11c88778d466bd7a49b544f2b5806ee0

commit 146ff1bb11c88778d466bd7a49b544f2b5806ee0
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Mon Apr 25 07:46:39 2016

Don't allow scripts to run when a node is being adopted.

Running a script in the middle of rescoping nodes can break a lot of invariants and leave DOM in an inconsistent state.

This patch adds a ScriptForbiddenScope in TreeScope::adoptIfNeeded to ensure it never happens.

BUG=605766

Review URL: https://codereview.chromium.org/1910403003

Cr-Commit-Position: refs/heads/master@{#389425}

[modify] https://crrev.com/146ff1bb11c88778d466bd7a49b544f2b5806ee0/third_party/WebKit/Source/core/dom/TreeScope.cpp


### es...@chromium.org (2016-04-25)

ScriptForbiddenScope will also make you crash when entering script, I see we made it just avoid running the script these days. I'm not sure that's such a good idea, it means we get weird correctness bugs instead.

We don't need to add comments about why ScriptForbiddenScope is needed in general, all components should litter those scopes at the top of operations where script running would be unexpected. ScriptForbiddenScope having side effects is a problem though, since now you can add it to change the behavior of the code and not just crash the process to avoid security bugs.

### do...@chromium.org (2016-04-25)

dcheng, esprehn, thank you for the comments. Particularly about adding a test and a failing test for the missing events. I hope/assume loading team will untangle the loader to post these events; I'm happy to help.

esprehn: Re: crashing or not; does that mean V8PerIsolateData.cpp beforeCallEnteredCallback is just a defense in depth? Long term do you think we should be particularly hunting these callstacks--if there's no crash, and no counter, these are going to be silent.

marius.mlynski thank you again for this detailed bug, repro, and patch. The assertion your repro trips can't be supported without blocking scripts, so either the assertion had to go or we should stop running scripts. So I think biting the bullet and preventing scripts is a good incremental improvement. If you could develop those tests that would be splendid!

[Monorail components: -Blink>HTML Blink>Loader]

### cl...@chromium.org (2016-04-26)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### do...@chromium.org (2016-04-26)

Not fixed. I think loading team needs to work on this.

### ki...@chromium.org (2016-04-26)

Thanks Marius for making a patch and esprehn/dcheng for giving informative comments. Putting aside the very long-term objective that makes load event fire async there seem to be a few things we could try:

- calling cancelTimerFired synchronously in Resource::allClientsAndObserversRemoved looks a bit wrong, might we be able to try making this particular part async

or if it turns out it doesn't work (or it seems to need more work) it looks like at least we should make the follow-up change suggested by esprehn on crrev.com/1910403003 and try adding tests.

Currently hiroshige@'s trying the former approach, tentatively assign this to him.

### dc...@chromium.org (2016-04-26)

I'll create a followup bug with kinuko@'s last comment. We should mark this as fixed for fix merging purposes.

### ki...@chromium.org (2016-04-26)

Yup, just noticed that we needed the simple, mergeable fix first.  Thanks!

### dc...@chromium.org (2016-04-26)

Filed https://crbug.com/chromium/606651 for following up on the remaining issues.

### dc...@chromium.org (2016-04-26)

Also, has this actually been merged to any release branch? I didn't see a merge commit comment on this issue, and I see the merge-merged-2716 label on a lot of random issues.

### ki...@chromium.org (2016-04-26)

Hmm, we might not have merged this yet?  I see two commit comments for the marius's fix and second one had merge-merged but the two look to point to the same commit object... (and M50 branch is 2661) adding Merge-Request-50 label

### ki...@chromium.org (2016-04-26)

Also: the change's just landed 25 hours ago, I guess we'll need to wait for a few more days before actually merging it.

### cl...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-26)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### bu...@chromium.org (2016-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/34d3807c8e69adcd5ac23f45572ccb83684d1dc1

commit 34d3807c8e69adcd5ac23f45572ccb83684d1dc1
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Mon May 02 02:15:11 2016

Move the ScriptForbiddenScope in TreeScope::adoptIfNeeded to the top of the function.

This patch addresses the review comments and adds an automated test.

BUG=605766

Review-Url: https://codereview.chromium.org/1921853004
Cr-Commit-Position: refs/heads/master@{#390885}

[add] https://crrev.com/34d3807c8e69adcd5ac23f45572ccb83684d1dc1/third_party/WebKit/LayoutTests/fast/events/image-adoption-events-expected.txt
[add] https://crrev.com/34d3807c8e69adcd5ac23f45572ccb83684d1dc1/third_party/WebKit/LayoutTests/fast/events/image-adoption-events.html
[modify] https://crrev.com/34d3807c8e69adcd5ac23f45572ccb83684d1dc1/third_party/WebKit/Source/core/dom/TreeScope.cpp


### va...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-05-06)

Before we approve merge to M50, Could you please confirm whether this bug is baked/verified in Canary and safe to merge?

### ti...@google.com (2016-05-06)

govind@: confirmed that this is safe to merge.

Tina - please merge to M50 so that we can make the cut.



### mb...@chromium.org (2016-05-06)

Given the bake time it's had, seems safe to me.

### go...@chromium.org (2016-05-06)

Approving merge to M50 branch 2661, based on https://crbug.com/chromium/605766#c37 and #38. Please merge asap (latest before 1:00 PM PST Monday), so we can take it for next week Stable refresh release. Thank you.

### bu...@chromium.org (2016-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73dd06077821b2beba42165c484913601d9e8643

commit 73dd06077821b2beba42165c484913601d9e8643
Author: Martin Barbella <mbarbella@chromium.org>
Date: Fri May 06 19:32:23 2016

Don't allow scripts to run when a node is being adopted.

Running a script in the middle of rescoping nodes can break a lot of invariants and leave DOM in an inconsistent state.

This patch adds a ScriptForbiddenScope in TreeScope::adoptIfNeeded to ensure it never happens.

BUG=605766

Review URL: https://codereview.chromium.org/1910403003

Cr-Commit-Position: refs/heads/master@{#389425}
(cherry picked from commit 146ff1bb11c88778d466bd7a49b544f2b5806ee0)

TBR=dominicc@chromium.org,esprehn@chromium.org

Review URL: https://codereview.chromium.org/1953323002 .

Cr-Commit-Position: refs/branch-heads/2661@{#665}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/73dd06077821b2beba42165c484913601d9e8643/third_party/WebKit/Source/core/dom/TreeScope.cpp


### go...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-05-12)

Congrats - $8,000 for this report: $7500 for the bug, $500 for the patch.

### sh...@chromium.org (2016-05-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### [Deleted User] (2020-07-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-20)

This issue was migrated from crbug.com/chromium/605766?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084149)*
