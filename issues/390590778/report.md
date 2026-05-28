# Heap use-after-free in DirectSocket API

| Field | Value |
|-------|-------|
| **Issue ID** | [390590778](https://issues.chromium.org/issues/390590778) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls>Isolated |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | tk...@paloaltonetworks.com |
| **Assignee** | gr...@google.com |
| **Created** | 2025-01-18 |
| **Bounty** | $4,000.00 |

## Description

## VULNERABILITY DETAILS

The vulnerability is triggered when using `TCPSocket`/`UDPSocket`, which are available via the DirectSocket api for Isolated Web Apps.  

The issue lays within the usage of `base::BarrierCallback<ScriptValue>` by `blink::TCPSocket`/`blink::UDPSocket`:

```
  auto close_callback = base::BarrierCallback<ScriptValue>(
      /*num_callbacks=*/2,
      WTF::BindOnce(&TCPSocket::OnBothStreamsClosed, WrapWeakPersistent(this)));

```

The sockets expect the `BarrierCallback` to be called twice - once for the reader stream, and another time for the writer.  

When network communication errors occur, the streams are supposed to invoke the callback with a V8 exception object:

```
  auto exception = ScriptValue(
      script_state->GetIsolate(),
      V8ThrowDOMException::CreateOrDie(script_state->GetIsolate(),
                                       DOMExceptionCode::kNetworkError,
                                       String{"Stream aborted by the remote: " +
                                              net::ErrorToString(error_code)}));
  // …
  Controller()->error(script_state, exception);
  std::move(on_close_).Run(exception);

```

Once both of the streams are closed, the earliest observer error is used to reject the sockets’ |closed| promise:

```
void TCPSocket::OnBothStreamsClosed(std::vector<ScriptValue> args) {
  // …
  // Finds first actual exception and rejects |closed| with it.
  // If neither stream was errored, resolves |closed|.
  if (auto it = base::ranges::find_if_not(args, &ScriptValue::IsEmpty);
      it != args.end()) {
    GetClosedProperty().Reject(*it);

```

The issue is that after the first stream is closed with an exception, the V8 exception is stored inside an untraceable base::BarrierCallback, allowing for the exception to be freed upon the first garbage collection after the first stream closure.  

Once the second stream is closed, the sockets’ |closed| promise are rejected with the now free exception object (by `TCPSocket::OnBothStreamsClosed`).

## VERSION

Chrome Version: 132.0.6834.84  

Operating System: ChromeOS (and with flag for Windows and Mac too)

## REPRODUCTION CASE

See the attached signed isolated web app (pwa-iwa.swbn).  

Isolated web apps distribution is available via the admin console on ChromeOS devices.
This issue can be reproduced on any OS by enabling the Isolated Web App feature, then installing and running the attached IWA.  

Make sure you expose GC for v8 for the POC to work out of the box (`--js-flags=--expose-gc`)

Full steps to run the POC:

1. `python3 server.py`
2. `cd iwa`
3. `npm install`
4. `npm run start`
5. start `chrome.exe --js-flags="--expose-gc" --enable-features=IsolatedWebApps,IsolatedWebAppDevMode --install-isolated-web-app-from-url=http://localhost:4321`
6. navigate to `chrome://apps`
7. Open pwn-ipa

The core of the reproduction:

```
(async () => {
  const socket = new TCPSocket("127.0.0.1", 8080);
  const socketInfo = await socket.opened;
  const reader = socketInfo.readable.getReader();
  const writer = socketInfo.writable.getWriter();
  reader.closed.catch((e) => {
    console.info("trigger");
    gc();
    writer.close();
  });
  socket.closed.catch((e) => {
    console.info("got object  ", e);
  });
})();

```

The flow of the reproduction are:  

  1. Connect to the server  

  2. Cause a network error (RST sent by the server), closing the reader stream with an exception.  

  3. Once the reader stream is closed, trigger a Garbage Collection event.  

  4. Close the writer stream from JS to expose the UAF v8 exception to JavaScript.

Type of crash: tab  

Crash State: See asan.txt

### The proposed fix is attached as patch.txt

## CREDIT INFORMATION

Reporter credit: Tal Keren, Sam Agranat, Eran Rom, Edouard Bochin, Adam Hatsir of Palo Alto Networks.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.7 KB)
- [pwn-iwa.swbn](attachments/pwn-iwa.swbn) (application/octet-stream, 30.2 KB)
- [server.py](attachments/server.py) (text/x-python, 578 B)
- [pwn-iwa.zip](attachments/pwn-iwa.zip) (application/zip, 142.1 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 23.2 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 23.2 KB)

## Timeline

### tk...@paloaltonetworks.com (2025-01-20)

Reuploading the patch file as there was a small issue with it.

And I didn't specified it but the source of the bug is commit 9d0d8605f9544d89dd4fcb10c18c30dd69808b4a.

### ad...@google.com (2025-01-20)

Thanks for the very clear reproduction instructions. Reproduced on Linux (redshell) with 132. Rating this as S2 - it's a renderer UaF presumably with the precondition of an installed web app.

### gr...@google.com (2025-01-20)

Huge thanks for the clear write-up and the reproduction steps, much appreciated! The patch is at [crrev.com/c/6185420](https://chromium-review.googlesource.com/c/chromium/src/+/6185420) with some minor commentary.

### pe...@google.com (2025-01-20)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2025-01-21)

Project: chromium/src  

Branch: main  

Author: Andrew Rayskiy <[greengrape@google.com](mailto:greengrape@google.com)>  

Link:      <https://chromium-review.googlesource.com/6185420>

DirectSockets: Patch selected memory management issues

---


Expand for full commit details
```
DirectSockets: Patch selected memory management issues 
 
This CL replaces the untraceable stored ScriptValue with a local v8 
value for storing stream errors and redefines stream closure logic via 
explicit callbacks instead of relying on barrier callbacks (which do not 
support tracing as well). 
 
Credit to Tal Keren, Sam Agranat, Eran Rom, Edouard Bochin, Adam Hatsir 
of Palo Alto Networks for discovering this! 
 
Bug: 390590778 
Change-Id: I4a0a23e9755cacea60c50244c8c8bbece6b885c4 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6185420 
Reviewed-by: Simon Hangl <simonha@google.com> 
Commit-Queue: Andrew Rayskiy <greengrape@google.com> 
Cr-Commit-Position: refs/heads/main@{#1409087}

```

---

Files:

- M `third_party/blink/renderer/modules/direct_sockets/stream_wrapper.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper_unittest.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_writable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/udp_writable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_writable_stream_wrapper_unittest.cc`

---

Hash: 57d9ad01cee3ea5e242f46c2725b0707ed0baaac  

Date:  Tue Jan 21 09:13:00 2025


---

### am...@chromium.org (2025-02-03)

Adding Linux since this issue being assigned strictly OS=ChromeOS means it would not get picked up for Chromium security merge review or VRP, and this issue does appear to potentially impact other Desktop platforms.

### am...@chromium.org (2025-02-03)

Despite this fix having landed on 21 January, I'm not going to go ahead and merge review and approve it for 132 or 133 right now.
133 is being promoted to Stable and 132 is being promoted to Extended Stable on Tuesday. Given this timeline and that this issue is medium severity issue with a non-trivial fix, I don't plan on approving this fix for backmerge to 132/Extended Stable.
We can potentially consider backmerge to 133, but only after initial 133 Stable is released.

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for report of mildly mitigated memory corruption in a sandboxed process / the renderer + $1,000 patch bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations Palo Alto Networks team! Thank you for your efforts and reporting this issue -- and a patch -- to us. Nice work!

### am...@chromium.org (2025-02-14)

based on an off-bug discussion with greengrape@, it been noticed that this UAF is being triggered by different means in the wild on CrOS 133. Approving backmerge to 133.

### ap...@google.com (2025-02-14)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: Andrew Rayskiy <[greengrape@google.com](mailto:greengrape@google.com)>  

Link:      <https://chromium-review.googlesource.com/6268848>

[M133-Merge] DirectSockets: Patch selected memory management issues

---


Expand for full commit details
```
[M133-Merge] DirectSockets: Patch selected memory management issues 
 
This CL replaces the untraceable stored ScriptValue with a local v8 
value for storing stream errors and redefines stream closure logic via 
explicit callbacks instead of relying on barrier callbacks (which do not support tracing as well). 
 
(cherry picked from commit 57d9ad01cee3ea5e242f46c2725b0707ed0baaac) 
 
Bug: 390590778 
Change-Id: I4a0a23e9755cacea60c50244c8c8bbece6b885c4 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6185420 
Reviewed-by: Simon Hangl <simonha@google.com> 
Commit-Queue: Andrew Rayskiy <greengrape@google.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1409087} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6268848 
Reviewed-by: Amy Ressler <amyressler@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6943@{#1543} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `third_party/blink/renderer/modules/direct_sockets/stream_wrapper.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper_unittest.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_writable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/udp_writable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_writable_stream_wrapper_unittest.cc`

---

Hash: dd2a27d14c334cb5697dcedd148b4716c35c4015  

Date:  Fri Feb 14 11:01:16 2025


---

### pe...@google.com (2025-02-14)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ph...@google.com (2025-02-17)

Merge review required: M133 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### pe...@google.com (2025-02-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-02-19)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6275530
2. Low - There was no conflict.
3. 133
4. Yes. According to comment #2, the suspected CL is https://chromium-review.googlesource.com/c/chromium/src/+/3779544 that M132 contains. Thus, I think we need to merge the fix to M132 LTS. But, according to comment #9, they don't plan to merge back the fix to M132. I guess that LTS is different. Please let me know if we don't need to merge back the fix to M132 LTS. 


### ch...@google.com (2025-04-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2025-05-29)

Project: chromium/src  

Branch: refs/branch-heads/6834\_160  

Author: Andrew Rayskiy [greengrape@google.com](mailto:greengrape@google.com)  

Link:      <https://chromium-review.googlesource.com/6604433>

[CfM-R132] [M132-LTS] DirectSockets: Patch selected memory management issues

---


Expand for full commit details
```
     
    This CL replaces the untraceable stored ScriptValue with a local v8 
    value for storing stream errors and redefines stream closure logic via 
    explicit callbacks instead of relying on barrier callbacks (which do not 
    support tracing as well). 
     
    Credit to Tal Keren, Sam Agranat, Eran Rom, Edouard Bochin, Adam Hatsir 
    of Palo Alto Networks for discovering this! 
     
    (cherry picked from commit 57d9ad01cee3ea5e242f46c2725b0707ed0baaac) 
     
    (cherry picked from commit 69325c199e1e31e1fdd9131131694d545bc72da1) 
     
    Bug: 390590778 
    Change-Id: I4a0a23e9755cacea60c50244c8c8bbece6b885c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6185420 
    Reviewed-by: Simon Hangl <simonha@google.com> 
    Commit-Queue: Andrew Rayskiy <greengrape@google.com> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1409087} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6275530 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Andrew Rayskiy <greengrape@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/6834@{#5526} 
    Cr-Original-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561} 
    Signed-off-by: Kyle Williams <kdgwill@google.com> 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6604433 
    Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
    Owners-Override: Kyle Williams <kdgwill@chromium.org> 
    Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834_160@{#62} 
    Cr-Branched-From: cdae089eab830291f81deb011febbbdc520a019e-refs/branch-heads/6834@{#4409} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `third_party/blink/renderer/modules/direct_sockets/stream_wrapper.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper_unittest.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_server_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_writable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_readable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_socket.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_socket.h`
- M `third_party/blink/renderer/modules/direct_sockets/udp_writable_stream_wrapper.cc`
- M `third_party/blink/renderer/modules/direct_sockets/udp_writable_stream_wrapper_unittest.cc`

---

Hash: e27b7af6b1da8797767220b620c0a3e2436d2a91  

Date:  Thu May 29 20:08:44 2025


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390590778)*
