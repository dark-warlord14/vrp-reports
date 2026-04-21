# UAF in blink::IDBFactoryClient::DeleteSuccess

| Field | Value |
|-------|-------|
| **Issue ID** | [40070305](https://issues.chromium.org/issues/40070305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2023-08-23 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu22.04  

mac 13.4.1  

chromium version:  

Chromium 118.0.5965.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1186949.zip)  

Chromium 118.0.5951.0

repro steps:  

1 ./chrome --user-data-dir=/tmp/xx <http://localhost:8000/poc.html> --disable-popup-blocking  

2 The browser will open the "about:blank" tab, and a print dialog box will pop up in this tab, click the close button on the tab. If the browser does not crash, it will open the "about:blank" tab again, and a print dialog box will pop up. Click the close button repeatedly until the browser crashes. In my environment, it takes about 6 clicks to reproduce UAF.

**Problem Description:**  

==2786337==ERROR: AddressSanitizer: heap-use-after-free on address 0x507000775c88 at pc 0x55eac42877aa bp 0x7ffc7c1968d0 sp 0x7ffc7c1968c8  

READ of size 1 at 0x507000775c88 thread T0 (chrome)  

#0 0x55eac42877a9 in IsAdTask ./../../third\_party/blink/renderer/core/probe/async\_task\_context.h:55:34  

#1 0x55eac42877a9 in blink::AdTracker::DidFinishAsyncTask(blink::probe::AsyncTaskContext\*) ./../../third\_party/blink/renderer/core/frame/ad\_tracker.cc:292:21  

#2 0x55eac6fe6a9e in blink::probe::AsyncTask::~AsyncTask() ./../../third\_party/blink/renderer/core/probe/core\_probes.cc:95:18  

#3 0x55eac9e71edd in blink::IDBFactoryClient::DeleteSuccess(long) ./../../third\_party/blink/renderer/modules/indexeddb/idb\_factory\_client.cc:134:1  

#4 0x55eab3522534 in blink::mojom::blink::IDBFactoryClientStubDispatch::Accept(blink::mojom::blink::IDBFactoryClient\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/indexeddb/indexeddb.mojom-blink.cc:0:0  

#5 0x55eab911e5b4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1016:54  

#6 0x55eab913bde9 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#7 0x55eab91236f5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#8 0x55eab914aaa9 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#9 0x55eab9148cd4 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#10 0x55eab913bde9 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#11 0x55eab91141dc in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:561:49  

#12 0x55eab91160f3 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:618:14  

#13 0x55eab9115aaa in OnHandleReadyInternal ./../../mojo/public/cpp/bindings/lib/connector.cc:451:3  

#14 0x55eab9115aaa in mojo::Connector::OnWatcherHandleReady(char const\*, unsigned int) ./../../mojo/public/cpp/bindings/lib/connector.cc:417:3  

#15 0x55eab9118d03 in Invoke<void (mojo::Connector::\*)(const char \*, unsigned int), mojo::Connector \*, const char \*, unsigned int> ./../../base/functional/bind\_internal.h:714:12  

#16 0x55eab9118d03 in MakeItSo<void (mojo::Connector::\*const &)(const char \*, unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<const char, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:893:12  

#17 0x55eab9118d03 in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::\* const&)(char const\*, unsigned int), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::\* const&)(char const\*, unsigned int), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>> const&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>, unsigned int&&) ./../../base/functional/bind\_internal.h:993:12  

#18 0x55eab91189e3 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(char const\*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:957:12  

#19 0x55eaa99252e9 in Run ./../../base/functional/callback.h:333:12  

#20 0x55eaa99252e9 in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple

**Additional Comments:**

\*\*Chrome version: \*\* 118.0.5951.0 \*\*Channel: \*\* Dev

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 553 B)
- [asan.log](attachments/asan.log) (text/plain, 43.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 24.9 KB)

## Timeline

### [Deleted User] (2023-08-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5993414358925312.

### hc...@google.com (2023-08-23)

Reproed against asan-linux-release-1186862 (chromium-118.0.5965.0-linux-asan.zip), asan log attached.

### hc...@google.com (2023-08-23)

estade@, could you take a look? I'm unsure if this is a indexdb bug or a printing bug (or something else entirely), but indexdb seems to be my best guess right now.

awscreen@ is cced in case this is a printing thing

Its at least a bug in linux, i don't know if its present in other platforms

Severity set to medium for now, need to figure out foundin.

### hc...@google.com (2023-08-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>IndexedDB]

### es...@chromium.org (2023-08-23)

When I open this page on ToT, I hit these DCHECKs before getting to the UAF:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/document.cc;l=907-908;drc=f126ce4d6c9840d999e6ddea3dee748c7729f69e
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;drc=b971f5b4f51ad8307f16b9a15362abc46eaec8a8;l=1096

+japhet because that seems worth looking into.

As far as fixing the UAF, this seems to do the trick: https://chromium-review.googlesource.com/c/chromium/src/+/4809007

This is a recent regression affecting M117 (event dispatch was changed to synchronous which affects the lifetimes of the relevant objects). Therefore we might consider merging the fix to m117.

### hc...@google.com (2023-08-24)

Setting Foundin to 117, thanks!

This should affect all platforms except iOS, yes?

### [Deleted User] (2023-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-24)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-08-24)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-08-24)

> This should affect all platforms except iOS, yes?

correct.

### gi...@appspot.gserviceaccount.com (2023-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33f1311820de86861fe42456a33692510ba4655c

commit 33f1311820de86861fe42456a33692510ba4655c
Author: Evan Stade <estade@chromium.org>
Date: Fri Aug 25 23:29:24 2023

IndexedDB: move AsyncTaskContext off of IDBFactoryClient

IDBRequest is the more natural place to track the async task, and in
fact, already does have an AsyncTaskContext. Use that one instead to
track events on its subclass, IDBOpenDBRequest.

Bug: 1475187
Change-Id: I1362b31a82cf080ac10a684af55e6fba875cd937
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4809007
Reviewed-by: Nathan Memmott <memmott@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1188592}

[modify] https://crrev.com/33f1311820de86861fe42456a33692510ba4655c/third_party/blink/renderer/modules/indexeddb/idb_request.h
[modify] https://crrev.com/33f1311820de86861fe42456a33692510ba4655c/third_party/blink/renderer/modules/indexeddb/idb_request.cc
[modify] https://crrev.com/33f1311820de86861fe42456a33692510ba4655c/third_party/blink/renderer/modules/indexeddb/idb_factory_client.cc
[modify] https://crrev.com/33f1311820de86861fe42456a33692510ba4655c/third_party/blink/renderer/modules/indexeddb/idb_factory_client.h
[modify] https://crrev.com/33f1311820de86861fe42456a33692510ba4655c/third_party/blink/renderer/modules/indexeddb/idb_open_db_request.cc


### [Deleted User] (2023-08-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-08-29)

This issue is marked as M117 Stable blocker and we are just 1 week away(Sep-05th) from M117 Early Stable promotion, Please evaluate the issues and if any it's a blocker consider it as P0 high priority and get them fixed as soon as possible if not please drop Releaseblocking label.

Note : Stable blockers prevent rolling out of M117 to Stable channel.

### es...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

Requesting merge to beta M117 because latest trunk commit (1188592) appears to be after beta branch point (1181205).

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-08-29)

Merge approved for M117! please merge to branch 5938. I know this is short notice, but if you can merge by EOD today MTV time (Tue Aug 29th), we can get this into the next beta release for M117! If not, it can go out with the beta/early stable release next week.

### pg...@google.com (2023-08-30)

Realized I did not specify a date for the stable release - please merge the fix by Thursday Aug 30 EOD (MTV time) to get this into M117 stable!

### gi...@appspot.gserviceaccount.com (2023-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5dcce910d2f729f13f41f036b0fb1cb5a9511ed4

commit 5dcce910d2f729f13f41f036b0fb1cb5a9511ed4
Author: Evan Stade <estade@chromium.org>
Date: Wed Aug 30 19:17:50 2023

[M117] IndexedDB: move AsyncTaskContext off of IDBFactoryClient

IDBRequest is the more natural place to track the async task, and in
fact, already does have an AsyncTaskContext. Use that one instead to
track events on its subclass, IDBOpenDBRequest.

(cherry picked from commit 33f1311820de86861fe42456a33692510ba4655c)

Bug: 1475187
Change-Id: I1362b31a82cf080ac10a684af55e6fba875cd937
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4809007
Reviewed-by: Nathan Memmott <memmott@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1188592}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4826396
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Auto-Submit: Evan Stade <estade@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Cr-Commit-Position: refs/branch-heads/5938@{#800}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/5dcce910d2f729f13f41f036b0fb1cb5a9511ed4/third_party/blink/renderer/modules/indexeddb/idb_request.h
[modify] https://crrev.com/5dcce910d2f729f13f41f036b0fb1cb5a9511ed4/third_party/blink/renderer/modules/indexeddb/idb_request.cc
[modify] https://crrev.com/5dcce910d2f729f13f41f036b0fb1cb5a9511ed4/third_party/blink/renderer/modules/indexeddb/idb_factory_client.cc
[modify] https://crrev.com/5dcce910d2f729f13f41f036b0fb1cb5a9511ed4/third_party/blink/renderer/modules/indexeddb/idb_factory_client.h
[modify] https://crrev.com/5dcce910d2f729f13f41f036b0fb1cb5a9511ed4/third_party/blink/renderer/modules/indexeddb/idb_open_db_request.cc


### [Deleted User] (2023-08-30)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-08-30)

1. Was this issue a regression for the milestone it was found in?
yes
2. Is this issue related to a change or feature merged after the latest LTS Milestone?
yes

### rz...@google.com (2023-09-12)

According to the https://crbug.com/chromium/1475187#c25, the issue affects a milestone newer than the latest LTS (117).

### rz...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $2,000 for this report of a moderately mitigated security bug in the renderer process. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1475187?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070305)*
