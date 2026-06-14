# Security: Persistent UXSS via SchemaRegistry 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084127](https://issues.chromium.org/issues/40084127) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-04-19 |
| **Bounty** | $7,500.00 |

## Description

Chrome version: 50.0.2661.75 (and still present on current HEAD, 52.0.2713.0)

The SchemaRegistry stores extension API schemas in a single v8::Context that lives until the RenderThread (=process?) is destroyed. Due to vulnerabilities in binding.js, these objects can be intercepted by malicious web pages. Since the object is persistent, this allows attackers to perform universal XSS in all frames and tabs that share this RenderThread (=process?).

See the attached proof of concept that shows an alert dialog on encrypted.google.com (in a frame, same tab or new tab).

The only requirements for exploitation are:
1. User should load attacker's page (e.g. via an advert in a frame).
2. The victim page (or a content script) accesses a property of the "chrome" object. In my exploit, I only hooked "chrome.runtime", but the method can be applied to any Chrome API.
3. The target page is loaded in the same process (e.g. by loading the victim pages in a frame, or by following links).

Clearly, this is easy to exploit so it should be fixed ASAP.

## Attachments

- [persistent-uxss.html](attachments/persistent-uxss.html) (text/plain, 6.6 KB)
- [persistent-uxss50.png](attachments/persistent-uxss50.png) (image/png, 25.0 KB)
- deleted (application/octet-stream, 0 B)
- [persistent-uxss-v2-52.0.2714.0.png](attachments/persistent-uxss-v2-52.0.2714.0.png) (image/png, 26.9 KB)
- [persistent-uxss-v2.html](attachments/persistent-uxss-v2.html) (text/plain, 6.5 KB)
- [frozen-schema-bypass.png](attachments/frozen-schema-bypass.png) (image/png, 163.3 KB)

## Timeline

### va...@chromium.org (2016-04-19)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1affd84d7a57f498ba529892b97721fcd2d47afb

commit 1affd84d7a57f498ba529892b97721fcd2d47afb
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Wed Apr 20 00:26:42 2016

[Extensions] Have Binding inherit from null proto

BUG=591164
BUG=604901

Review URL: https://codereview.chromium.org/1902003003

Cr-Commit-Position: refs/heads/master@{#388375}

[modify] https://crrev.com/1affd84d7a57f498ba529892b97721fcd2d47afb/extensions/renderer/resources/binding.js


### ro...@robwu.nl (2016-04-20)

Let's play whack a mole.
The above patch landed in Chrome 52.0.2713.0, and indeed blocks my previous exploit.
With a minor modification of the exploit, it works again in Chrome 52.0.2714.0.

JS can't be trusted, try to solve this in C++.

### ro...@robwu.nl (2016-04-20)

[Comment Deleted]

### ro...@robwu.nl (2016-04-20)

(fixed some misleading comments in the revised PoC, these were only for the original version)

### sh...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-04-21)

Devlin, I see that you've started with https://codereview.chromium.org/1906593002/. Freezing schemas is helpful, but not sufficient to completely resolve the UXSS vulnerability.

1. Once any object from the SchemaRegistry's v8::Context leaks to the web page, an attacker can retrieve the Function constructor via any inherit method, and run arbitrary code that persists even after the page is closed.
2. To use this for UXSS, the code from step 1 needs a reference to an object in another page.

Your implementation of DeepFreeze looks good, but it doesn't account for the fact that V8ValueConverter triggers property setters which can easily be achieved after step 1. Even with your patch, schema properties are leaked like a seeve, e.g. $Object.assign({}, rawSettingParam.properties) leaks all properties to the web page because {} inherits from the web page's Object.prototype.

To fix this, I consider an attacker model where the extension bindings are completely compromised. Then you have to look for a solution that prevents an attacker from getting access to more objects in the SchemaRegistry's v8::Context after getting a reference to a schema object. I believe that modifying DeepFreeze to assign a null prototype to every object achieves the goal, because then it is not possible to traverse prototypes to get into the SchemaRegistry's v8::Context.

In addition, you can also freeze built-in prototypes in the SchemaRegistry's context as an extra layer of defense, in case the above assumption is not true (e.g. when DeepFreeze skips an object).

### rd...@chromium.org (2016-04-21)

Good idea about setting schema's proto to null.  One question, though
> but it doesn't account for the fact that V8ValueConverter triggers property setters which can easily be achieved after step 1
In my experimentation, I haven't seen V8ValueConverter triggering property setters when it constructs the schema (which is good, because otherwise we'd have to set proto to null as we construct the schema, rather than afterwards in DeepFreeze()).  Am I missing something?

### rd...@chromium.org (2016-04-21)

Also, since it's fairly related to this bug, I'll mention that we also leak the schema through CustomBindingsObject, because we set the functionSchemas property on it.  This is trivially accessible through a CustomBindingsObject.__proto__, e.g.
chrome.storage.local.__proto__.functionSchemas

### ro...@robwu.nl (2016-04-21)

Here's a quick demo (steps 6 - 12 are shown in the screenshot):

1. Visit data:, (to make sure that you don't have any extensions running in that tab).
2. Open the developer tools
3. Type chrome.webstore. in the console (no need to press Enter; with the trailing dot - this causes binding.js to load).
4. Go to the Sources tab, select the Sources panel, click on "extensions::event_bindings".
5. Add a conditional breakpoint right after "var schemaRegistry = requireNative('schema_registry')", using the condition
   !(window.schemaRegistry = schemaRegistry)
   (to set a conditional breakpoint, right-click on the line number and select "Add conditional breakpoint...")
   (In Chrome 50., this is line 9 in extensions::event_bindings)

The breakpoint always evaluates to false so it is never triggered, but the variable is exported to the global scope for ease of debugging via the console.

6. Refresh the page. Now we're in a clean state without any extension modules.
7. Type chrome.webstore. to trigger the conditional breakpoint in extensions::event_bindings that leaks |schemaRegistry|.

Now, the proof of concept:
8. Run the following in the console.

schemaRegistry.GetSchema('events').constructor.constructor(`;
  Object.defineProperty(Object.prototype, 'types', {
    get() {},
    set(value) {
      if (Array.isArray(value)) {
        // platforms: [] to make sure that binding.js ignores this type.
        value.unshift({id: 'bogus', enum: ['hello_world']});
      }
      Object.defineProperty(this, 'types', {
        value: value,
      });
    },
  });
`)()

10. Reload the page (to show that this change is persistent) - this step is optional.
11. Type chrome.webstore in the console and press Enter.
12. Expand the printed object, and observe that the enum is visible.

Because schemas are loaded once and then cached, this only applies to NEW schemas. Hence I started with "chrome.webstore.", and then "chrome.runtime". This is less risky than my original exploit, but still concerning because the schema is shared with all contexts in the process, including content script contexts who can access more APIs (=schemas) besides chrome.webstore/runtime.

I didn't compile with your patch, but only read the code and assumed that it would be vulnerable to the attack that I described above. Follow the following steps and you'll probably reach the same conclusion.
1. Visit https://cs.chromium.org/%22v8%3A%3ALocal%3Cv8%3A%3AValue%3E%20value%20%3D%20v8_value_converter-%3EToV8Value(schema%2C%20context)%3B%22
2. Follow the implementation (now I'm using git links instead of codesearch so that the links stay valid).
   For a given object, the call trace would be this:
https://chromium.googlesource.com/chromium/src/+/c864f52514c7e8cf9992a524e0294b1cc32c1db5/content/child/v8_value_converter_impl.cc#155 V8ValueConverterImpl::ToV8Value
https://chromium.googlesource.com/chromium/src/+/c864f52514c7e8cf9992a524e0294b1cc32c1db5/content/child/v8_value_converter_impl.cc#172 V8ValueConverterImpl::ToV8ValueImpl
https://chromium.googlesource.com/chromium/src/+/c864f52514c7e8cf9992a524e0294b1cc32c1db5/content/child/v8_value_converter_impl.cc#211 V8ValueConverterImpl::ToV8ValueImpl, case dictionary
https://chromium.googlesource.com/chromium/src/+/c864f52514c7e8cf9992a524e0294b1cc32c1db5/content/child/v8_value_converter_impl.cc#250 V8ValueConverterImpl::ToV8Object
https://chromium.googlesource.com/chromium/src/+/c864f52514c7e8cf9992a524e0294b1cc32c1db5/content/child/v8_value_converter_impl.cc#264 V8ValueConverterImpl::ToV8Object, calls Set.

The setter at the end is wrapped in a try-catch. From that, I inferred that assigning a property may trigger setters.
https://chromium.googlesource.com/v8/v8/+/2cfac65eacd308ab83b8750b159d321f380b6cf2/src/api.cc#3572 v8::Object::Set
https://chromium.googlesource.com/v8/v8/+/2cfac65eacd308ab83b8750b159d321f380b6cf2/src/api.cc#3558 v8::Object::Set with v8::Context
https://chromium.googlesource.com/v8/v8/+/0ba934d7bff00298511e38139c7f1dda076fc179/src/runtime/runtime-object.cc#206 Runtime::SetObjectProperty
In Runtime::SetObjectProperty, the call to LookupIterator::PropertyOrElement retrieves the property using the DEFAULT configuration (= traverse the prototype chain).
After that, Runtime::SetObjectProperty is used to assign the property, which can trigger the inherit setter from my PoC.


### rd...@chromium.org (2016-04-21)

Ah, I see.  Nice find, Rob!  (Unrelated: conditional breakpoints == awesome.)  I was tripped up by the fact that constructing the schema object itself isn't subject to these getters/setters, but looking into it, it's because we do it in an isolated context in V8SchemaRegistry.  So it seems like adding the null prototype on the schema object should hopefully be pretty sufficient.

### bu...@chromium.org (2016-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5fb2548448bd1b76a59d941b729d7a7f90d53bc8

commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 21 23:19:24 2016

[Extensions] Finish freezing schema

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1906593002

Cr-Commit-Position: refs/heads/master@{#388945}

[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/binding.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/event.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/resources/utils.js
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fda8f6e80af3e5c08905624f356a75b05d27dd39

commit fda8f6e80af3e5c08905624f356a75b05d27dd39
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 22 01:17:37 2016

[Extensions] Sprinkle in some more null protos and defineProperty's

BUG=591164
BUG=604901

Review URL: https://codereview.chromium.org/1903273003

Cr-Commit-Position: refs/heads/master@{#388994}

[modify] https://crrev.com/fda8f6e80af3e5c08905624f356a75b05d27dd39/extensions/renderer/resources/binding.js


### ro...@robwu.nl (2016-04-27)

Verified to be fixed in 52.0.2719.0 (390054), using steps 1-7 from https://crbug.com/chromium/604901#c11 and running the following code snippet in the console:

(function visit(seen, o, path) {
  if (seen.includes(o) || o == null) return;
  if (o.__proto__ && !(o.__proto__ instanceof Object))
    console.log(path);
  if (['boolean', 'number', 'string'].includes(typeof o)) return;
  seen.push(o);
  for (var key in o)
     visit(seen, o[key], path + '.' + key);
})([], schemaRegistry.GetSchema('runtime'), '');
// Also tested 'webstore', 'storage' instead of 'runtime'

// Expected: No logged messages (= no leaked prototypes).
// Actual  : As expected in 52.0.2719.0; lots of logged messages in Chrome 50.0.2661.75.



Just merging 5fb2548448bd1b76a59d941b729d7a7f90d53bc8 is sufficient to resolve the vulnerability.

### ti...@google.com (2016-04-27)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### cl...@chromium.org (2016-04-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-04-28)

Please merge your change to M51 branch 2704 before 5:00 PM PST, tomorrow (Friday), so we can take it in for next week M51 beta release. Thank you.

### ro...@robwu.nl (2016-04-28)

Devlin, can you do the merge? I think that the patch might not apply cleanly because you had some other patches before it (e.g. the patch that did a shallow freeze of the schema).

### rd...@chromium.org (2016-04-28)

This is gonna be fun.
Merging:
- crrev.com/a794ae416acf94cb247d8ca0e8554863f5d9c1d8
- crrev.com/c089219d5f8794747f7ab7b966b4676f49532e1f
- crrev.com/585b125ef7168c104631e23ee5cad0108c838f52
- crrev.com/5fb2548448bd1b76a59d941b729d7a7f90d53bc8
- crrev.com/1affd84d7a57f498ba529892b97721fcd2d47afb

### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/970dbc743f2a107f14bb120341c322380a7c71cd

commit 970dbc743f2a107f14bb120341c322380a7c71cd
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 28 22:15:26 2016

[Extensions] Make Binding.generate() load the schema directly

Previously, Binding.generate would rely on a previously-loaded schema object
during generation. Instead, make it load the schema directly in generate() so
that it can't be mutated before use.

BUG=591164
BUG=604901

Review URL: https://codereview.chromium.org/1864353002

Cr-Commit-Position: refs/heads/master@{#386434}
(cherry picked from commit c089219d5f8794747f7ab7b966b4676f49532e1f)

Review URL: https://codereview.chromium.org/1930033003 .

Cr-Commit-Position: refs/branch-heads/2704@{#293}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/970dbc743f2a107f14bb120341c322380a7c71cd/extensions/renderer/resources/binding.js


### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f0f07d08bc3865436994b40aa620d8063fe7bbcc

commit f0f07d08bc3865436994b40aa620d8063fe7bbcc
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 28 22:26:20 2016

[Extensions] More bindings improvements

Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
and broaden test access checks.

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1899973002

Cr-Commit-Position: refs/heads/master@{#388353}
(cherry picked from commit 585b125ef7168c104631e23ee5cad0108c838f52)

Review URL: https://codereview.chromium.org/1930213002 .

Cr-Commit-Position: refs/branch-heads/2704@{#294}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/resources/binding.js
[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/script_context.cc
[modify] https://crrev.com/f0f07d08bc3865436994b40aa620d8063fe7bbcc/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ed087c3f125239baa798fbbceded413d529674ed

commit ed087c3f125239baa798fbbceded413d529674ed
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Apr 28 22:37:03 2016

[Extensions] Finish freezing schema

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1906593002

Cr-Commit-Position: refs/heads/master@{#388945}
(cherry picked from commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8)

Review URL: https://codereview.chromium.org/1928783005 .

Cr-Commit-Position: refs/branch-heads/2704@{#295}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/binding.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/event.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/resources/utils.js
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/ed087c3f125239baa798fbbceded413d529674ed/extensions/renderer/v8_schema_registry.cc


### rd...@chromium.org (2016-04-28)

Actually, that might be enough.  Now let's see if anything breaks with those three.

### rd...@chromium.org (2016-04-29)

Apparently the v8 roll adding SetIntegrityLevel isn't in M51.  Reverting.

### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3f9ac15b6c55ed5fd923c469baff869a418852eb

commit 3f9ac15b6c55ed5fd923c469baff869a418852eb
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 00:24:32 2016

Revert of [Extensions] Finish freezing schema (patchset #1 id:1 of https://codereview.chromium.org/1928783005/ )

Reason for revert:
Compile failure

Original issue's description:
> [Extensions] Finish freezing schema
>
> BUG=604901
> BUG=603725
> BUG=591164
>
> Review URL: https://codereview.chromium.org/1906593002
>
> Cr-Commit-Position: refs/heads/master@{#388945}
> (cherry picked from commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8)
>
> Committed: https://chromium.googlesource.com/chromium/src/+/ed087c3f125239baa798fbbceded413d529674ed

TBR=
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=604901

Review-Url: https://codereview.chromium.org/1928193002
Cr-Commit-Position: refs/branch-heads/2704@{#301}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/binding.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/event.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/resources/utils.js
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/3f9ac15b6c55ed5fd923c469baff869a418852eb/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0

commit 21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 00:33:47 2016

Revert of [Extensions] More bindings improvements (patchset #1 id:1 of https://codereview.chromium.org/1930213002/ )

Reason for revert:
Compile fail

Original issue's description:
> [Extensions] More bindings improvements
>
> Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
> and broaden test access checks.
>
> BUG=604901
> BUG=603725
> BUG=591164
>
> Review URL: https://codereview.chromium.org/1899973002
>
> Cr-Commit-Position: refs/heads/master@{#388353}
> (cherry picked from commit 585b125ef7168c104631e23ee5cad0108c838f52)
>
> Committed: https://chromium.googlesource.com/chromium/src/+/f0f07d08bc3865436994b40aa620d8063fe7bbcc

TBR=
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=604901

Review-Url: https://codereview.chromium.org/1926353002
Cr-Commit-Position: refs/branch-heads/2704@{#302}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/resources/binding.js
[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/script_context.cc
[modify] https://crrev.com/21f2505bca7ba0dc5ee8d0917ff9e2c4d336c6c0/extensions/renderer/v8_schema_registry.cc


### ro...@robwu.nl (2016-04-29)

SetIntegrityLevel seems to be in Chrome 50.0.2661.75 [1], and its API didn't change up until master [2], so I'd expect it to be available on M-51 as well. Where did you see that compilation error?

[1] https://chromium.googlesource.com/v8/v8.git/+blame/tags/5.0.71.32/src/objects.h#1869
[2] https://chromium.googlesource.com/v8/v8/+blame/1095835a61ae0b35d69f26aa59f76fa0a6ee96a9/src/objects.h#1900

### rd...@chromium.org (2016-04-29)

It's in the internal API, but not exposed publicly through v8/include/v8.h:
https://chromium.googlesource.com/v8/v8.git/+/tags/5.0.71.32/include/v8.h
It was added in https://chromium.googlesource.com/v8/v8.git/+/93c60dca132a30d58a8a6c7ee2b0e1937b5bb331

### rd...@chromium.org (2016-04-29)

+Adam for v8 knowledge.  Background: we'd like to merge security fixes that rely on SetIntegrityLevel() back to M51, but M51 doesn't have SetIntegrityLevel() exposed.  What's the process for doing something like this?  Cherry-picking into v8's older version, then updating M51's deps, then merging the patches that use it?  Is that feasible?

### ad...@chromium.org (2016-04-29)

If we wanted to do this, then the set of steps is slightly shorter:

1. Merge https://codereview.chromium.org/1889903003 into the v8 5.1 branch
2. Merge the dependent patch into the M51 Chromium branch

Chromium release builds always use HEAD of the associated v8 branch (M51 -> 5.1 in this case).

Adding jochen@ as the author of that patch and hablich@ as our v8 release guru. I can't think of a case where we've merged API changes back, though I don't see any reason it wouldn't just work, though.


### ad...@chromium.org (2016-04-29)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-04-29)

It's just forwarding an existing API, so I'm supportive of merging

### ha...@chromium.org (2016-04-29)

process outlined in #31 is correct. Please note we don't DEPS HEAD into Chromium but an lkgr ref like:

https://chromium.googlesource.com/v8/v8/+log/5.1-lkgr

It takes ~ 10 minutes that this ref is updated.

We normally do not merge API changes back. It seems it is not breaking the API, what about ABI compat?

I will rely on Jochen's assessment.

### rd...@chromium.org (2016-04-29)

Cool.  Adam/Jochen, would one of you want to do the v8 merge?  (I'm assuming the process is different than that of chromium.)

### ad...@chromium.org (2016-04-29)

Happy to take care of the merge on the v8 side.

### ad...@chromium.org (2016-04-29)

Merged in  https://chromium.googlesource.com/v8/v8.git/+/f81c34e6bd3add59b7a1f465159d9f5863312373

### rd...@chromium.org (2016-04-29)

Awesome, thanks Adam!  I'll merge the dependent patches in a few minutes.

### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53

commit a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 20:48:30 2016

[Extensions] More bindings improvements

Explicitly freeze the schema in chrome, pass safe arguments to GetAvailability,
and broaden test access checks.

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1899973002

Cr-Commit-Position: refs/heads/master@{#388353}
(cherry picked from commit 585b125ef7168c104631e23ee5cad0108c838f52)

Review URL: https://codereview.chromium.org/1930163004 .

Cr-Commit-Position: refs/branch-heads/2704@{#314}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/module_system_test.cc
[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/resources/binding.js
[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/script_context.cc
[modify] https://crrev.com/a7f8dfd50a1e2410dd4053a21c4c0c17c67dfc53/extensions/renderer/v8_schema_registry.cc


### bu...@chromium.org (2016-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f73ae8fbece36f9f964e2b83f893ef708cca6e2

commit 6f73ae8fbece36f9f964e2b83f893ef708cca6e2
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 29 20:53:36 2016

[Extensions] Finish freezing schema

BUG=604901
BUG=603725
BUG=591164

Review URL: https://codereview.chromium.org/1906593002

Cr-Commit-Position: refs/heads/master@{#388945}
(cherry picked from commit 5fb2548448bd1b76a59d941b729d7a7f90d53bc8)

Review URL: https://codereview.chromium.org/1936673002 .

Cr-Commit-Position: refs/branch-heads/2704@{#315}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/chrome/test/data/extensions/api_test/stubs_app/background.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/binding.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/event.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/json_schema.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/schema_utils.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/storage_area.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/resources/utils.js
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/6f73ae8fbece36f9f964e2b83f893ef708cca6e2/extensions/renderer/v8_schema_registry.cc


### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Congrats Rob - $7,500 for this report. I'll add this to the next payment run. Thanks again!

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-04)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/604901?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/4846]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084127)*
