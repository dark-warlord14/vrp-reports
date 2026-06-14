# Heap-use-after-free in WebCore::DocumentV8Internal::getElementByIdMethodCallbackForMainWorld

| Field | Value |
|-------|-------|
| **Issue ID** | [40079791](https://issues.chromium.org/issues/40079791) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Platforms** | Linux |
| **Reporter** | dy...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2014-06-21 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0

Steps to reproduce the problem:
1. Open repro2.html
2. ???
3. PROFIT

What is the expected behavior?
I guess proper rendering but expectations usually depend on the situation.

What went wrong?
Sorry, for the time being I'm not able to provide any details.

Did this work before? N/A 

Chrome version: 35.0.1916.153 (Official Build 274914)  Channel: stable
OS Version: 35.0.1916.153
Flash Version: 

I don't currently have access to a debug build for further investigation. Reporting this as a security issue just in case.

It does upset renderer of up-to-date stable versions of chrome on Windows, OS X, and Linux .

dmesg on Ubuntu spit out this:
[ 1981.562754] traps: chrome[4838] general protection ip:7faa8ead32b2 sp:7fff1ee198c0 error:0 in chrome[7faa8bf90000+4f39000]

Dmesg on OS X did not spit anything.

## Attachments

- [repro2.html](attachments/repro2.html) (text/html, 616 B)
- [script-crash.html](attachments/script-crash.html) (text/html, 752 B)

## Timeline

### cl...@chromium.org (2014-06-23)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-06-23)

Repro'd under asan on 38.0.2066.0 

==6781==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c0000163c8 at pc 0x7f3123d56950 bp 0x7ffff94fa500 sp 0x7ffff94fa4f8
READ of size 8 at 0x60c0000163c8 thread T0 (chrome)
    #0 0x7f3123d5694f in WebCore::ScriptWrappable::containsWrapper() const /usr/local/google/tsepez/b1/src/out_asan/Release/../../third_party/WebKit/Source/bindings/v8/ScriptWrappable.h:205
    #1 0x7f3123d568fd in WebCore::ScriptWrappable::getRawValue() const /usr/local/google/tsepez/b1/src/out_asan/Release/../../third_party/WebKit/Source/bindings/v8/ScriptWrappable.h:232
    #2 0x7f3123d568cd in WebCore::ScriptWrappable::getPersistent(v8::Persistent<v8::Object, v8::NonCopyablePersistentTraits<v8::Object> >*) const /usr/local/google/tsepez/b1/src/out_asan/Release/../../third_party/WebKit/Source/bindings/v8/ScriptWrappable.h:227
    #3 0x7f31251ed6ca in WebCore::ScriptWrappable::setReturnValue(v8::ReturnValue<v8::Value>) /usr/local/google/tsepez/b1/src/out_asan/Release/../../third_party/WebKit/Source/bindings/v8/ScriptWrappable.h:157
    #4 0x7f31255bf483 in void WebCore::v8SetReturnValueForMainWorld<v8::FunctionCallbackInfo<v8::Value> >(v8::FunctionCallbackInfo<v8::Value> const&, WebCore::Element*) /usr/local/google/tsepez/b1/src/out_asan/Release/gen/blink/bindings/core/v8/V8Element.h:93
    #5 0x7f31255c85d5 in WebCore::DocumentV8Internal::getElementByIdMethodForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) /usr/local/google/tsepez/b1/src/out_asan/Release/gen/blink/bindings/core/v8/V8Document.cpp:3943
    #6 0x7f31255bac2c in WebCore::DocumentV8Internal::getElementByIdMethodCallbackForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) /usr/local/google/tsepez/b1/src/out_asan/Release/gen/blink/bindings/core/v8/V8Document.cpp:3949
    #7 0x7f3123d14cc4 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) /usr/local/google/tsepez/b1/src/out_asan/Release/../../v8/src/arguments.cc:33
    #8 0x7f312375bb3e in v8::internal::Object* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) /usr/local/google/tsepez/b1/src/out_asan/Release/../../v8/src/builtins.cc:1204
    #9 0x7f3123756ca5 in v8::internal::Builtin_HandleApiCall(int, v8::internal::Object**, v8::internal::Isolate*) /usr/local/google/tsepez/b1/src/out_asan/Release/../../v8/src/builtins.cc:1220

I will upload to CF.


### cl...@chromium.org (2014-06-23)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5635118016233472

### cl...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5635118016233472

Uploader: tsepez@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000004ba88
Crash State:
  - crash stack -
  WebCore::DocumentV8Internal::getElementByIdMethodCallbackForMainWorld
  v8::internal::FunctionCallbackArguments::Call
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv942xZU4sIpG-4mMEotZHxBPyN8Lc8mMxAPnkiIU40xNJlzdPNn4ESxa4Ej2FUBN74JWSVMgEB0T3UT_htllqNxBmcNOpWJeXAaFwJ2ig8xmG6sBHF_hrG-9fkIAVycuZB7mAT7okPYy8ugbwMyJ6E0KL4YA8g



### js...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-03)

[Comment Deleted]

### ti...@chromium.org (2014-07-08)

@haraken - can you please confirm that this bug on your radar?

### ha...@chromium.org (2014-07-09)

I noticed that this is a bug of Document::getElementById(). When getElementByIdMethodForMainWorld in V8Document.cpp calls Document::getElementById(), I confirmed that Document::getElementById() returns a dangling pointer. I'd guess there is a bug somewhere in TreeScope.

static void getElementByIdMethodForMainWorld(...) {
  ...;
  fprintf(stderr, "%p\n", impl->getElementById(elementId));
  if (impl->getElementById(elementId))
    fprintf(stderr, "%p\n", impl->getElementById(elementId)->firstChild());  // This can be 0xcdcdcdcdcd in repro2.html.
}

Elliott: Would you have a cycle to take a look at this one?


### cl...@chromium.org (2014-07-20)

[Comment Deleted]

### es...@chromium.org (2014-07-24)

I reduced this, what happens is:

1. Script is inserted but with an invalid type and an element for a child (not just text)
2. Script type is changed back to a valid one
3. child.remove() is called
4. ContainerNode::removeChild disconnects child from the tree.
5. ContainerNode::removeChild calls childrenChanged()
6. HTMLScriptElement::childrenChanged runs the script, which does script.remove()
7. The script is now removed from the tree.
8. notifyNodeRemoved is called with child
9. Element::removedFrom contains:

if (insertionPoint->isInTreeScope() && treeScope() == document()) {
  ...
  // remove element from the id table in tree scope by calling updateId.
  ...
}

but the insertionPoint is not in the tree anymore, so we skip that step and leave the child in the id map.

10. child wrapper is dropped, gc happens.
11. child is destroyed, but left in the id map as described above.
12. getElementById returns a free'd ptr.

This would have been fixed by https://src.chromium.org/viewvc/blink?revision=175732&view=revision but that got rolled out because I broke plugins/document-open.html (https://crbug.com/chromium/382160) and maybe some other plugin tests.

I'll see if I can fix that patch, the only alternative I can think of is to defer running script until after all the removal logic like we do with insertedInto and didNotifySubtreeInsertionsToDocument.

### es...@chromium.org (2014-07-24)

Interestingly Safari has the same bug, but doesn't crash for reasons I don't understand, their id map isn't holding RefPtrs. 

### es...@chromium.org (2014-07-24)

Patch https://codereview.chromium.org/418133003

### bu...@chromium.org (2014-07-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=178976

------------------------------------------------------------------
r178976 | esprehn@chromium.org | 2014-07-26T05:11:41.483386Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/script-remove-child-id-map.html?r1=178976&r2=178975&pathrev=178976
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLOptionElement.cpp?r1=178976&r2=178975&pathrev=178976
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ContainerNode.h?r1=178976&r2=178975&pathrev=178976
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/script-remove-child-id-map-expected.txt?r1=178976&r2=178975&pathrev=178976
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ContainerNode.cpp?r1=178976&r2=178975&pathrev=178976

Call insertedInto or removedFrom before childrenChanged

We must notify nodes that they were removed before calling childrenChanged
because childrenChanged could run script. If don't then the script can remove
the parent and then Element::removedFrom doesn't think the parent is
inTreeScope or inDocument so it'll fail to clean up the TreeScope hash maps
like the id map.

I tried this once before for a different reason in:
https://src.chromium.org/viewvc/blink?revision=175732&view=revision
but that got rolled out because it caused crashes http://crbug.com/382160

By looking at the code it appears that the reason for this is that
m_element in the WebPluginContainerImpl is a raw ptr, and so nothing is
keeping the element alive inside the UpdateSuspendScope. In this patch
I didn't remove the NodeVector, a future patch will attempt to do that.

Unfortunately even when I did remove the NodeVector I couldn't reproduce
the crashes mentioned in the bug, but by code inspection and the crash
stacks it appears to be the situation I described.

BUG=387389

Review URL: https://codereview.chromium.org/418133003
-----------------------------------------------------------------

### in...@chromium.org (2014-07-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6047580431581184

Fuzzer: Inferno_twister
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 1
Crash Address: 0x04c9ee3c
Crash State:
  - crash stack -
  blink::v8SetReturnValueForMainWorld<v8::PropertyCallbackInfo<v8::Value> >
  blink::DocumentV8Internal::getElementByIdMethodForMainWorld
  - free stack -
  operator delete[]
  blink::HTMLHeadingElement::`scalar deleting destructor'
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=284942:285011

Minimized Testcase (0.42 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95A2mpeonEglP-tq-NC0ls_U1XYENluOfhzU6X2I9z043hyNu7mAtyWYXANfTzE_82u6unBJDZ81_HQS1Ia0JKYADzQ-J2kmeJkMynTrnehvawj8Md91XVz2cmEG57uX08zRJh1Goj-OlqTmiOgWwzuk2CWuA
<script src=../../resources/js-test.js></script>

<script>
var script = document.createElement("script");
script.type = "dont-execute";
script.textContent = "script.remove()";
child = document.createElement("div");
child.id = "child";
script.appendChild(child);

document.documentElement.appendChild(script);

script.type = "";

child.remove();

child = null;
gc();

shouldBeNull("document.getElementById('child')");
</script>
>


Filer: inferno

### cl...@chromium.org (2014-07-28)

ClusterFuzz has detected this issue as fixed in range 285583:285741.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5635118016233472

Uploader: tsepez@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61000004ba88
Crash State:
  - crash stack -
  WebCore::DocumentV8Internal::getElementByIdMethodCallbackForMainWorld
  v8::internal::FunctionCallbackArguments::Call
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=246004:246020
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=285583:285741

Minimized Testcase (0.49 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv942xZU4sIpG-4mMEotZHxBPyN8Lc8mMxAPnkiIU40xNJlzdPNn4ESxa4Ej2FUBN74JWSVMgEB0T3UT_htllqNxBmcNOpWJeXAaFwJ2ig8xmG6sBHF_hrG-9fkIAVycuZB7mAT7okPYy8ugbwMyJ6E0KL4YA8g
<body>
<script>
(function() {
	{
	}

	script = document.createElement("script");
	script.type = "foo";
	script.textContent = "document.implementation.createHTMLDocument().body.appendChild(script)";
	element = document.createElement(("script"));
	element.id = "xxx";
	script.appendChild(element);
	document.body.appendChild(script);

	script.type = "";
	script.removeChild(element);
	
	element = null;
	setTimeout(function() {
		!!document.getElementById("xxx");
		location.reload();
	}, 0);
}())
</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-08-02)

Merge-Requested for M37. train for M36 patch merge is gone.

### am...@chromium.org (2014-08-06)

merge approved for m37 branch 2062

### in...@chromium.org (2014-08-07)

Elliot, can you please merge to m37 soon, we are cutting branch on tuesday.

### in...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-11)

Elliot, friendly ping for merge. I was getting merge conflict while merging to m37, so unsure if this patch is safe to merge to m37 or not. We have until tmrw before the m37 build cuts, so please take a look.

### es...@chromium.org (2014-08-11)

This is a pretty difficult merge, I think I managed it: https://codereview.chromium.org/465593003 but I somehow need to add a removedFrom method to HTMLOptionElement.h and I'm not sure how to do that drover.

### in...@chromium.org (2014-08-11)

I haven't added new files with drover. +cc Anthony would probably know.

### am...@chromium.org (2014-08-12)

If it's not viable with Drover, the following page may be of assistance...

https://wiki.corp.google.com/twiki/bin/view/Main/ChromeReleaseBranches

### es...@chromium.org (2014-08-12)

I can't seem to make this work in my checkout, it either wants me to pull down the entire SVN repo (which is going to take hours) or reconfigure my entire checkout. Can someone else do this merge?

### am...@chromium.org (2014-08-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-12)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180117

------------------------------------------------------------------
r180117 | chrome-bot@google.com | 2014-08-12T23:15:06.102321Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/core/html/HTMLOptionElement.h?r1=180117&r2=180116&pathrev=180117
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/core/dom/ContainerNode.cpp?r1=180117&r2=180116&pathrev=180117
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/core/html/HTMLOptionElement.cpp?r1=180117&r2=180116&pathrev=180117

Merge 178976 "Call insertedInto or removedFrom before childrenCh..."

> Call insertedInto or removedFrom before childrenChanged
> 
> We must notify nodes that they were removed before calling childrenChanged
> because childrenChanged could run script. If don't then the script can remove
> the parent and then Element::removedFrom doesn't think the parent is
> inTreeScope or inDocument so it'll fail to clean up the TreeScope hash maps
> like the id map.
> 
> I tried this once before for a different reason in:
> https://src.chromium.org/viewvc/blink?revision=175732&view=revision
> but that got rolled out because it caused crashes http://crbug.com/382160
> 
> By looking at the code it appears that the reason for this is that
> m_element in the WebPluginContainerImpl is a raw ptr, and so nothing is
> keeping the element alive inside the UpdateSuspendScope. In this patch
> I didn't remove the NodeVector, a future patch will attempt to do that.
> 
> Unfortunately even when I did remove the NodeVector I couldn't reproduce
> the crashes mentioned in the bug, but by code inspection and the crash
> stacks it appears to be the situation I described.
> 
> BUG=387389
> 
> Review URL: https://codereview.chromium.org/418133003

TBR=esprehn@chromium.org

Review URL: https://codereview.chromium.org/465593003


-----------------------------------------------------------------

### in...@chromium.org (2014-08-13)

Looks like you figured it out. Thanks a lot Elliot.

### mb...@chromium.org (2014-08-22)

Thanks for the report, dyjakan! This qualifies for a $2000 reward. Someone will be reaching out to you soon with additional details.

How would you like to be credited when we mention this bug in our release notes?

### dy...@gmail.com (2014-08-22)

Thank you; for credits please use my name (Andrzej Dyjak).

### ti...@chromium.org (2014-09-18)

Andrzej,

Apologies for the delay - someone from our finance team should be in touch to collect payment details next week. Please email me directly if this doesn't happen.

Congratulations on the reward!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2014-10-21)

Processing via our e-payment system can take up to a month, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-11-01)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/387389?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079791)*
