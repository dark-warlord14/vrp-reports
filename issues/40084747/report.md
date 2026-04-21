# Security: use-after-free in AttachFilteredEvent on event_bindings.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40084747](https://issues.chromium.org/issues/40084747) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ji...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2016-07-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When processing smart pointers in AddEventMatcher(event\_filters.cc), it don't std::move the smart pointer on certain condition, like (see <--)  

On line 56  

EventFilter::MatcherID EventFilter::AddEventMatcher(  

const std::string& event\_name,  

std::unique\_ptr<EventMatcher> matcher <-- unique\_ptr) {  

MatcherID id = next\_id\_++;  

URLMatcherConditionSet::Vector condition\_sets;  

if (!CreateConditionSets(id, matcher.get(), &condition\_sets))  

return -1; <-- frees the EventMatcher matcher object

for (URLMatcherConditionSet::Vector::iterator it = condition\_sets.begin();  

it != condition\_sets.end(); it++) {  

condition\_set\_id\_to\_event\_matcher\_id\_.insert(  

std::make\_pair((\*it)->id(), id));  

}  

id\_to\_event\_name\_[id] = event\_name;  

event\_matchers\_[event\_name][id] = linked\_ptr<EventMatcherEntry>(  

new EventMatcherEntry(std::move(matcher) <-- correctly moved, &url\_matcher\_, condition\_sets));  

return id;  

}

This is the partial definition of EventMatcher class (event\_matcher.h).  

On line 23  

class EventMatcher {  

...  

std::unique\_ptr[base::DictionaryValue](javascript:void(0);) filter\_;  

...  

};

The filter\_ is wrapped in unique\_ptr, so freed when EventMatcher object frees.  

It results to use-after-free in AttachFilteredEvent on event\_bindings.cc.

On line 262  

std::unique\_ptr[base::DictionaryValue](javascript:void(0);) filter;  

...  

On line 277  

base::DictionaryValue\* filter\_weak = filter.get();  

int id = g\_event\_filter.Get().AddEventMatcher(  

event\_name, ParseEventMatcher(std::move(filter))); <-- Actually, ParseEventMatcher creates EventMatcher object mentioned above, with the filter\_ member provided to the argument. AddEventMatcher frees filter\_weak.  

...  

On line 283  

std::string extension\_id = context()->GetExtensionID();  

if (AddFilter(event\_name, extension\_id, \*filter\_weak)) { <-- boom 1  

bool lazy = ExtensionFrameHelper::IsContextForEventPage(context());  

content::RenderThread::Get()->Send(new ExtensionHostMsg\_AddFilteredListener(  

extension\_id, event\_name, \*filter\_weak, lazy)); <-- boom 2  

}

Actually, the Event object itself is exposed in Port object, which is returned by chrome.runtime.connect. WEB\_PAGE context can call it. Like,

var Event = chrome.runtime.connect('yo').onDisconnect.constructor;

And we can provide a invalid URL matcher.

var event = new Event('app.app', [], {supportsFilters: true}); <-- Abstraction of the event binding interface.  

event.addListener(function() {}, {url: [1]}); <-- Calls the AttachFilteredEvent method.

**VERSION**  

Chrome Version: 51.0.2704.84 stable 32bit  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

I've attached the PoC as a HTML file.

## Attachments

- [chrome_new1.html](attachments/chrome_new1.html) (text/plain, 321 B)

## Timeline

### ji...@gmail.com (2016-07-02)

FYI, it can cause heap BOF or changing EIP if it's sprayed by IPC message between free/use(used in Value::DeepCopy and sending IPC message on line 286).

This case was little for stable build but on canary build, and I don't know why..

8^(

### pa...@chromium.org (2016-07-03)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API]

### pa...@chromium.org (2016-07-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-17)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-31)

meacer: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2016-08-09)

jinmoteam@: Thanks for the report and apologies for the late response.

I'm bumping up the severity to high as this doesn't require an extension to be installed. 

### ji...@gmail.com (2016-08-09)

meacer@: thanks!

### me...@chromium.org (2016-08-11)

https://codereview.chromium.org/2236133002/

### bu...@chromium.org (2016-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ba011d9f8322c62633a069a59c2c5525e3ff46cc

commit ba011d9f8322c62633a069a59c2c5525e3ff46cc
Author: meacer <meacer@chromium.org>
Date: Fri Aug 12 00:23:40 2016

Ignore filtered event if an event matcher cannot be added.

BUG=625404

Review-Url: https://codereview.chromium.org/2236133002
Cr-Commit-Position: refs/heads/master@{#411472}

[modify] https://crrev.com/ba011d9f8322c62633a069a59c2c5525e3ff46cc/extensions/renderer/event_bindings.cc


### me...@chromium.org (2016-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-08-12)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-12)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### go...@chromium.org (2016-08-12)

Please merge your change by Monday (08/15) 5:00 PM PT so we can take it in for next week Beta release. Thank you.


### bu...@chromium.org (2016-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7de974664bfeefa2310ee0f350437f3fdf466b91

commit 7de974664bfeefa2310ee0f350437f3fdf466b91
Author: Mustafa Acer <meacer@chromium.org>
Date: Mon Aug 15 19:05:41 2016

Ignore filtered event if an event matcher cannot be added.

BUG=625404

Review-Url: https://codereview.chromium.org/2236133002
Cr-Commit-Position: refs/heads/master@{#411472}
(cherry picked from commit ba011d9f8322c62633a069a59c2c5525e3ff46cc)

Review URL: https://codereview.chromium.org/2250433002 .

Cr-Commit-Position: refs/branch-heads/2785@{#601}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/7de974664bfeefa2310ee0f350437f3fdf466b91/extensions/renderer/event_bindings.cc


### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

Congratulations! The panel decided to award $3,000 for this bug.  A member of our finance team will be in touch shortly with next steps.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-10-28)

btw can I disclose this publicly?

### sh...@chromium.org (2016-11-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/625404?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084747)*
