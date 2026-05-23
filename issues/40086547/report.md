# Security: Out-of-bounds read in V8 Array.concat

| Field | Value |
|-------|-------|
| **Issue ID** | [40086547](https://issues.chromium.org/issues/40086547) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2017-01-18 |
| **Bounty** | $7,500.00 |

## Description

This is a dupe of 681761. I rewrote it to follow the security template, sorry :).

**VULNERABILITY DETAILS**  

During Array.concat() the `visitor` variable is created which is what is returned after the function is complete. The type of the `visitor` variable is determined by the first argument sent to `Array.prototype.concat.call`.

When the objects being passed to concat are being placed into `visitor`, if the visitor function is not a fixed\_array() `JSReceiver::CreateDataProperty` is called. This function can trigger callbacks in some instances.

When `JSReceiver::CreateDataProperty` is called on a JSProxy, after a long line of functions, eventually `JSProxy::DefineOwnProperty` is called which calls `Object::GetMethod` on the `defineProperty` property (`Object::GetMethod` triggers getters). It is possible to trigger this callback  

during Array.concat() by setting a getter `Object.prototype.__defineGetter__("defineProperty", evil_callback)`.

In this callback we can change the size of the `visitor` object in the middle of it's iteration. When this is paired with garbage collection it leads to on out of bounds read.

In the comment below I go into more detail about how these functions get called with specific lines of code and function names.

**VERSION** S  

Chrome Version: 55.0.2883.87 (Official Build) m (64-bit)  

Operating System: Microsoft Windows 10 Version 1607 (OS Build 14393.693)

Chrome Version: 57.0.2985.0 (Developer Build) (64-bit)  

Operating System: Ubuntu 14.04

note: There is DCHECK() in place to check for OOB in debug builds but this is disabled for Release builds

**REPRODUCTION CASE**  

I have included a few proofs of concept,  

poc1.html <--- This demonstrates the OOB read primitive to get a memory leak off the v8 heap  

poc2.html <--- Demonstrates a reliable crash  

poc3.html <--- memory leak with floats converted to hex

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer process  

I have attached the output from debug running poc2.html in crash.log with DCHECK turned off

## Attachments

- poc1.html (text/plain, 839 B)
- poc2.html (text/plain, 3.4 KB)
- [poc3.html](attachments/poc3.html) (text/plain, 3.4 KB)
- crash.log (text/plain, 1.3 KB)
- linux_exploit.html (text/plain, 10.0 KB)
- windows_exploit.html (text/plain, 9.9 KB)

## Timeline

### bt...@gmail.com (2017-01-18)

p.s. Line numbers taken from commit e44e863e19ffca8ed95c0e395641ed1679482d12

From line 1340 of src/builtins/builtins-array.cc
BUILTIN(ArrayConcat) {
  ...
  Handle<Object> species;
  ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
      isolate, species, Object::ArraySpeciesConstructor(isolate, receiver)); <----- We have control over the species function (L#1370)
  ...
  return Slow_ArrayConcat(&args, species, isolate);
}

From line 1091 of src/builtins/builtins-array.cc
Object* Slow_ArrayConcat(...) {
  ...
  if (fast_case) {
    ...
  } else if (is_array_species) {
    ...
  } else {
    DCHECK(species->IsConstructor());
    Handle<Object> length(Smi::kZero, isolate);
    Handle<Object> storage_object;
    ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
        isolate, storage_object,
        Execution::New(isolate, species, species, 1, &length)); <----- Our species function is executed, giving us control of the storage object (L#1242)
    storage = storage_object;
  }

  ArrayConcatVisitor visitor(isolate, storage, fast_case); <----- visitor now holds a reference to our storage object (L#1246)

  for (int i = 0; i < argument_count; i++) {
  Handle<Object> obj((*args)[i], isolate);
  Maybe<bool> spreadable = IsConcatSpreadable(isolate, obj);
  MAYBE_RETURN(spreadable, isolate->heap()->exception());
  if (spreadable.FromJust()) {
    Handle<JSReceiver> object = Handle<JSReceiver>::cast(obj);
    if (!IterateElements(isolate, object, &visitor)) {            <----- IterateElements is called using our visitor (L#1254)
      return isolate->heap()->exception();
    }
  } else {
    if (!visitor.visit(0, obj)) return isolate->heap()->exception();
    visitor.increase_index_offset(1);
  }
  ...
}

Frome line 909 of src/builtins/builtins-array.cc
bool IterateElements(...) {
  ...
  ...

  case FAST_HOLEY_DOUBLE_ELEMENTS:
  case FAST_DOUBLE_ELEMENTS: {
    // Empty array is FixedArray but not FixedDoubleArray.
    if (length == 0) break;
    // Run through the elements FixedArray and use HasElement and GetElement
    // to check the prototype for missing elements.
    if (array->elements()->IsFixedArray()) {
      DCHECK(array->elements()->length() == 0);
      break;
    }
    Handle<FixedDoubleArray> elements(
        FixedDoubleArray::cast(array->elements()));
    int fast_length = static_cast<int>(length);
    DCHECK(fast_length <= elements->length());
    FOR_WITH_HANDLE_SCOPE(isolate, int, j = 0, j, j < fast_length, j++, {
      if (!elements->is_the_hole(j)) {
        double double_value = elements->get_scalar(j);              <-----
        Handle<Object> element_value =
            isolate->factory()->NewNumber(double_value);
        if (!visitor->visit(j, element_value)) return false;        <----- visitor->visit is called (L#1008)
      } else {
        Maybe<bool> maybe = JSReceiver::HasElement(array, j);
        if (!maybe.IsJust()) return false;
        if (maybe.FromJust()) {
          // Call GetElement on array, not its prototype, or getters won't
          // have the correct receiver.
          Handle<Object> element_value;
          ASSIGN_RETURN_ON_EXCEPTION_VALUE(
              isolate, element_value,
              JSReceiver::GetElement(isolate, array, j), false);
          if (!visitor->visit(j, element_value)) return false;     <----- visitor->visit is called (L#1019)
        }
      }
    });
    break;
  }
}


From line 582 in src/builtins/builtins-array.cc (function visit in class ArrayConcatVisitor)
if (!is_fixed_array()) {
  LookupIterator it(isolate_, storage_, index, LookupIterator::OWN);    <----- the iterator is built using our storage object from earlier (L#583)
  MAYBE_RETURN(
      JSReceiver::CreateDataProperty(&it, elm, Object::THROW_ON_ERROR),
      false);
  return true;
}

From line 6587 in src/objects.cc
Maybe<bool> JSReceiver::CreateDataProperty(LookupIterator* it,
                                           Handle<Object> value,
                                           ShouldThrow should_throw) {

  ...

  if (receiver->IsJSObject()) { <---- FAILED: Proxy is not a JSOBject
    return JSObject::CreateDataProperty(it, value, should_throw);
  }

  ...

  return JSReceiver::DefineOwnProperty(isolate, receiver, it->GetName(), <----- (L#6604)
                                       &new_desc, should_throw);
}

From line 6226 in src/objects.cc
Maybe<bool> JSReceiver::DefineOwnProperty(...) {
  ...

  if (object->IsJSProxy()) {
    return JSProxy::DefineOwnProperty(isolate, Handle<JSProxy>::cast(object), <----- called because we passed a Proxy (L#6236)
                                      key, desc, should_throw);
  }
  ...
}

From line 6846 in src/objects.cc
Maybe<bool> JSProxy::DefineOwnProperty(...) {
  STACK_CHECK(isolate, Nothing<bool>());
  if (key->IsSymbol() && Handle<Symbol>::cast(key)->IsPrivate()) {
    return SetPrivateProperty(isolate, proxy, Handle<Symbol>::cast(key), desc,
                              should_throw);
  }
  Handle<String> trap_name = isolate->factory()->defineProperty_string();     <----- "defineProperty" string (L#6855)

  DCHECK(key->IsName() || key->IsNumber());

  Handle<Object> handler(proxy->handler(), isolate);

  if (proxy->IsRevoked()) {
    isolate->Throw(*isolate->factory()->NewTypeError(
        MessageTemplate::kProxyRevoked, trap_name));
    return Nothing<bool>();
  }

  Handle<JSReceiver> target(proxy->target(), isolate);

  Handle<Object> trap;
  ASSIGN_RETURN_ON_EXCEPTION_VALUE(
      isolate, trap,
      Object::GetMethod(Handle<JSReceiver>::cast(handler), trap_name), <---- GetMethod calls GetProperty which triggers getters (L#6873)
      Nothing<bool>());
}

### pa...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6165994306535424

### cl...@chromium.org (2017-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5790886358417408

### pa...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Runtime]

### bt...@gmail.com (2017-01-19)

[Comment Deleted]

### bt...@gmail.com (2017-01-19)

[Comment Deleted]

### jo...@chromium.org (2017-01-19)

[Empty comment from Monorail migration]

### lg...@chromium.org (2017-01-20)

Adding triage labels.

I'm assuming V8 counts as "an out-of-bounds read in a renderer process" here.

### sh...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

### bt...@gmail.com (2017-01-23)

RCE Exploit in the renderer process:
I used this vulnerability to achieve code execution in the renderer process on x64.

Steps
=====
1.) Trigger the vulnerability on a normal FAST_DOUBLE type in Array.concat(). This is our initial memory leak. I managed to trigger garbage collection in a way so that pointer values to our own custom objects would appear in the resulting array.

2.) Using these pointers (represented as doubles) I found the address of an ArrayBuffer I allocated, a Text object I allocated, and an Array's backstore pointer that I had control of.

3.) Using the Array I controlled I created a fake ArrayBuffer using the leaked pointers (represented as doubles) from leaking the old ArrayBuffer I allocated legitimately. 

4.) Next I triggered the vulnerability again but this time on a FAST_ELEMENTS type. This gave me access to the fake ArrayBuffer I positioned in the heap (I gave it a very large byteLength). From here I could edit the fake ArrayBuffer's backstore pointer at any time because I still had a reference to the first Array that I used to build this fake ArrayBuffer. This gives us an arbitrary read/write.

5.) With the arbitrary read write I leaked the JIT address by finding a JSFunction on the heap. Then re-positioned the fake ArrayBuffer's backstore pointer to the JIT address, overwrote the contents of the RWX memory it with shellcode, and called the JSFunction. This gives us arbitrary code execution in the renderer process.


I've attached two exploits. One for linux and one for windows. 
The exploit for linux has shellcode that copies /etc/passwd to /tmp/aaa, the exploit for windows has shellcode that `int 3` quite a few times to trap the debugger.

For Linux I ran:
google-chrome --no-sandbox linux_exploit.html
or google-chrome --no-sandbox and navigated to the webserver

Linux
VERSION: 55.0.2883.87 (Official Build) (64-bit)
OS: Updated Ubuntu 14.04


For Windows I ran:
same as linux but on the alert attach Windbg to the renderer process when the alert pops up.

Windows
Chrome Version: 55.0.2883.87 (Official Build) m (64-bit)
Operating System: Microsoft Windows 10 Version 1607 (OS Build 14393.693)

### cb...@chromium.org (2017-01-23)

Will start with the fix today. Thanks for the detailed report!

### bt...@gmail.com (2017-01-24)

lgarron: jochen: Following that last comment I made about using this bug to get code execution in the renderer process I believe this could fall under 

"A bug that allows arbitrary code execution within the confines of the sandbox, such as renderer or GPU process memory corruption"

### pa...@chromium.org (2017-01-25)

#14 is correct. Bumping this to High.

### cb...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### cb...@chromium.org (2017-01-25)

[runtime] Fix Array.prototype.concat with complex @@species

Array.prototype.concat does not properly handle JSProxy species that will
modify the currently visited array.

BUG=682194

Review-Url: https://codereview.chromium.org/2655623004
Cr-Commit-Position: refs/heads/master@{#42640}
Committed: https://chromium.googlesource.com/v8/v8/+/e5608155aeb18a76fdb495d446efe1f9e33e749b

### cb...@chromium.org (2017-01-25)

Let's wait for it to bake a couple of days before we start the backmerging.

### sh...@chromium.org (2017-01-25)

This bug requires manual review: We are only 5 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2017-01-25)

+bustamante as FYI.

Is there a reason this didn't have a release block label?  Is this absolutely necessary for M56?  We're already starting to ship it...

### aw...@chromium.org (2017-01-25)

I'm OK not blocking 56 on this, but we should merge it into the branch after sufficient bake time so we pick it up if we spin for another reason.

### sh...@chromium.org (2017-01-26)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-26)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-01-26)

If possible, pls merge your change to M57 branch 2987 before 5:00 PM PT today (Thursday, 01/26) so we can pick it for tomorrow's Dev release.

### cb...@chromium.org (2017-01-26)

Merged: [runtime] Fix Array.prototype.concat with complex @@species

Revision: e5608155aeb18a76fdb495d446efe1f9e33e749b

BUG=682194
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Review-Url: https://codereview.chromium.org/2658113002
Cr-Commit-Position: refs/branch-heads/5.7@{#27}
Cr-Branched-From: 975e9a320b6eaf9f12280c35df98e013beb8f041-refs/heads/5.7.492@{#1}
Cr-Branched-From: 8d76f0e3465a84bbf0bceab114900fbe75844e1f-refs/heads/master@{#42426}
Committed: https://chromium.googlesource.com/v8/v8/+/fbcc5463a0e79ab95e150fbe4b804a8c6baa8ba2

### sh...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### bu...@google.com (2017-01-27)

Based on comments in #20 #21 and that the fix is fairly small, approving merge into M56.

### go...@chromium.org (2017-01-27)

Pls merge your change to M57 branch 2987 before 5:00 PM PT Monday (01/30) so we can pick it up for next week Last M57  Dev release. Thank you.

### am...@chromium.org (2017-01-28)

Krishna, it's already in M57, see c#25.

cbruni@, please merge ASAP on Monday your time.

### am...@chromium.org (2017-01-28)

Rather, please merge to M56 ASAP your time on Monday.

### cb...@chromium.org (2017-01-28)

will perform the merge tomorrow night.

### cb...@chromium.org (2017-01-30)

Too busy weekend, currently in MTV will do the backmerge tomorrow 7AM PST.

### aw...@chromium.org (2017-01-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2017-01-31)

This needs to be merged ASAP if you want it to make the next M56 stable release.

### cb...@chromium.org (2017-01-31)

Sorry, merge happened this morning:

Merged: [runtime] Fix Array.prototype.concat with complex @@species

Revision: e5608155aeb18a76fdb495d446efe1f9e33e749b

BUG=682194
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jkummerow@chromium.org

Review-Url: https://codereview.chromium.org/2666543004 .
Cr-Commit-Position: refs/branch-heads/5.6@{#92}
Cr-Branched-From: bdd3886218dfe76e8560eb8a18401942452ae859-refs/heads/5.6.326@{#1}
Cr-Branched-From: 879f6599eee6e1dfcbe9a24bf688b261c03e9558-refs/heads/master@{#41014}
Committed: https://chromium.googlesource.com/v8/v8/+/8b0e98df72e727f29cd4f67a67492b3fd4c2fa2e

### sh...@chromium.org (2017-01-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Congratulations! The panel decided to award $7,500 for this great report!  A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### of...@google.com (2017-03-17)

This also affects Node.js v7.x (V8 5.1), and v6.x (V8 5.5) – although the security impact is not high. I will handle releasing the fix on the Node.js side.

### aw...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### of...@google.com (2017-05-01)

https://github.com/nodejs/node/pull/12779

### of...@google.com (2017-10-11)

Node v6.x PR: https://github.com/nodejs/node/pull/16133

### jk...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### cb...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-06-26)

This issue was migrated from crbug.com/chromium/682194?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/681761, crbug.com/chromium/804971]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086547)*
