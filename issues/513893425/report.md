# Windows PWA handler launcher filename can smuggle --utility-cmd-prefix from manifest name, causing Chrome to execute attacker-chosen wrapper on utility process launch.

| Field | Value |
|-------|-------|
| **Issue ID** | [513893425](https://issues.chromium.org/issues/513893425) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Windows |
| **Reporter** | ro...@gmail.com |
| **Assignee** | dm...@google.com |
| **Created** | 2026-05-16 |
| **Bounty** | $2,500.00 |

## Description

---

### Report description

Windows PWA handler launcher filename can smuggle --utility-cmd-prefix from manifest name, causing Chrome to execute attacker-chosen wrapper on utility process launch.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src>

---

### The problem

#### Please describe the technical details of the vulnerability

Bug location:
Chromium src:

- base/command\_line.cc
- chrome/browser/web\_applications/os\_integration/web\_app\_handler\_registration\_utils\_win.cc
- chrome/browser/web\_applications/chrome\_pwa\_launcher/chrome\_pwa\_launcher\_main.cc
- content/browser/service\_host/utility\_process\_host.cc

The problem:
On Windows, a manifest-controlled PWA name is used to build the app-specific launcher .exe filename. If the name contains --single-argument, Chromium's Windows parser matches that token inside the quoted executable path instead of the real shell-handler switch. The PWA launcher then passes the resulting tail to chrome.exe, where it is parsed as real switches. With --utility-cmd-prefix, Chrome launches an attacker-chosen wrapper when starting a utility process.

The cause:
base::CommandLine::ParseAsSingleArgument() searches the raw command line with raw\_command\_line\_string\_.find(single\_arg\_switch). This is unsafe when the quoted program path itself can contain --single-argument. PWA Windows file/protocol handler registration derives that program path from the web app's manifest name, which is attacker-controlled.

#### Impact analysis

An attacker-controlled website can offer a PWA for installation. After the user installs it and later invokes its registered protocol/file handler, Chrome can execute an attacker-chosen command as the current Windows user. No admin privileges are required. The confirmed PoC uses calc.exe as a benign wrapper.

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7778.168 stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Remote Code Execution (RCE)

#### How would you like to be publicly acknowledged for your report?

Daniel Rodríguez

## Attachments

- [Video.mp4](attachments/Video.mp4) (video/mp4, 3.3 MB)
- [icon.svg](attachments/icon.svg) (image/svg+xml, 278 B)
- [manifest.webmanifest](attachments/manifest.webmanifest) (application/octet-stream, 524 B)
- [sw.js](attachments/sw.js) (text/javascript, 89 B)
- [index.html](attachments/index.html) (text/html, 938 B)
- [trigger.html](attachments/trigger.html) (text/html, 758 B)
- [start_video_demo.ps1](attachments/start_video_demo.ps1) (application/octet-stream, 2.0 KB)
- [README.md](attachments/README.md) (text/markdown, 1.1 KB)
- [Recording 2026-05-17 012615.mp4](attachments/Recording 2026-05-17 012615.mp4) (video/mp4, 4.1 MB)
- [04-update-20260517.zip](attachments/04-update-20260517.zip) (application/zip, 142.7 KB)
- [Recording 2026-05-17 014408.mp4](attachments/Recording 2026-05-17 014408.mp4) (video/mp4, 2.5 MB)
- [Screenshot 2026-05-17 022100.png](attachments/Screenshot 2026-05-17 022100.png) (image/png, 30.3 KB)
- [FULL POC.zip](attachments/FULL POC.zip) (application/zip, 6.8 KB)
- [icon.svg](attachments/icon_76922258.svg) (image/svg+xml, 201 B)
- [index.html](attachments/index_76922259.html) (text/html, 2.2 KB)
- [manifest.webmanifest](attachments/manifest_76917075.webmanifest) (application/octet-stream, 550 B)
- [open-protocol.html](attachments/open-protocol.html) (text/html, 177 B)
- [sw.js](attachments/sw_76922260.js) (text/javascript, 42 B)
- [check.ps1](attachments/check.ps1) (application/octet-stream, 1.3 KB)
- [README.md](attachments/README_76922261.md) (text/markdown, 2.2 KB)
- [start.ps1](attachments/start.ps1) (application/octet-stream, 3.3 KB)
- [stop.ps1](attachments/stop.ps1) (application/octet-stream, 697 B)
- [icon.svg](attachments/icon_76923476.svg) (image/svg+xml, 235 B)
- [index.html](attachments/index_76922626.html) (text/html, 444 B)
- [manifest.webmanifest](attachments/manifest_76922265.webmanifest) (application/octet-stream, 534 B)
- [open-mailto.html](attachments/open-mailto.html) (text/html, 142 B)
- [sw.js](attachments/sw_76922627.js) (text/javascript, 42 B)

## Timeline

### ro...@gmail.com (2026-05-17)

# Update: profile-closed requirement removed, two-step PWA RCE confirmed

Hello Chrome Security team,

I have an important update for the Windows PWA handler launcher issue previously submitted in this package. The original report described the cleanest trigger as requiring the victim to install the PWA, close the Chrome profile, and later invoke the registered handler. I have now confirmed a shorter and higher-impact chain: the profile does **not** need to be closed.

## What changed

A manifest-controlled app name can include an additional no-value switch before the command-prefix sink:

```
Victim PWA --single-argument --headless --utility-cmd-prefix=<controlled-wrapper> inert

```

When the app-specific PWA handler launcher is invoked by Windows, the launcher filename is still parsed as part of the raw command line. The injected `--single-argument` causes the tail of the quoted launcher path to be reinterpreted as Chromium switches. Adding `--headless` is significant because Chrome creates a temporary `HeadlessChrome...` user-data-dir when no explicit `--user-data-dir` was supplied. That avoids the normal ProcessSingleton handoff to the already-running profile and allows `--utility-cmd-prefix` to affect utility process launch.

## Confirmed two-step exploit chain

1. Victim installs the malicious PWA.
2. Victim opens an external OS-dispatched `web+...://` protocol link registered by that PWA.

The original Chrome profile can remain open.

Confirmed run:

```
evidence\run-20260517T040209Z-protocol.json

```

Key facts from that run:

```
status=confirmed-installed-default-profile-protocol-headless-bypass
include_file_handler=false
registry_registered=true
registry_command_has_headless=true
registry_command_has_utility_prefix=true
registry_command_has_user_data_dir=false
original_chrome_alive_before_trigger=true
shell_trigger_ok=true
shell_marker_present=true

```

The marker process observed a utility-process launch with a temporary headless profile:

```
argv[0]=pwa_marker.exe
argv[1]=inert.exe" --profile-directory=Default --app-id=ljohneblpcmamjenkgdahjnbhapdenbn --single-argument web+pwaheadlessafbhaeacaj://open/
argv[2]=C:\Program Files\Google\Chrome\Application\chrome.exe
argv[8]=--user-data-dir=C:\Users\rodri\AppData\Local\Temp\HeadlessChrome27188322034515

```
## Optional file-handler variant

I also confirmed a second two-step variant:

1. Victim installs the malicious PWA.
2. Victim opens a file extension registered by the PWA file handler.

Confirmed run:

```
evidence\run-20260517T035754Z-file-handler.json

```

Key facts:

```
status=confirmed-installed-default-profile-file-handler-headless-bypass
file_registry_registered=true
file_registry_command_has_headless=true
file_registry_command_has_utility_prefix=true
file_registry_command_has_user_data_dir=false
original_chrome_alive_before_trigger=true
file_trigger_ok=true
file_marker_present=true

```
## Negative control

I also tested the proposed one-step path where the installed PWA page redirects or opens its own registered protocol from inside Chrome. That did **not** invoke the vulnerable OS launcher in the current test:

```
in_page_window_open_marker_present=false
in_page_redirect_marker_present=false

```

So the currently confirmed impact is a reliable two-step chain, not an install-only self-redirect chain.

## Updated PoCs included

This update directory contains the new PoC and evidence:

```
04-update-20260517\
  UPDATE.md
  evidence\
    pwa-two-step-protocol-headless-rce-20260517.md
    default-profile-headless-install-flow-20260517.txt
    run-20260517T040209Z-protocol.json
    run-20260517T035754Z-file-handler.json
  poc\
    pwa_arg_injection\
      run_default_profile_headless_flow.mjs
      fake_chrome_logger.rs
      bin\pwa_marker.exe
      manual_user_flow\
        start_manual_flow.ps1
        site\...

```

Automated protocol-only reproduction:

```
cd .\04-update-20260517\poc\pwa_arg_injection
$env:PWA_TMP_ROOT='C:\pwa'
$env:PWA_INCLUDE_FILE_HANDLER='0'
Remove-Item Env:\PWA_PROTOCOL_TRIGGER_DELAY_MS -ErrorAction SilentlyContinue
node .\run_default_profile_headless_flow.mjs

```

Expected result:

```
confirmed-installed-default-profile-protocol-headless-bypass

```

Manual calculator demo:

```
cd .\04-update-20260517\poc\pwa_arg_injection\manual_user_flow
powershell -ExecutionPolicy Bypass -File .\start_manual_flow.ps1

```

Then:

1. Install the opened PWA in normal Chrome.
2. Without closing Chrome, open the generated `Open PWA protocol trigger.url`.
3. Calculator opens.

## Updated impact statement

The exploit no longer requires the user to close the affected Chrome profile before the handler is invoked. The current confirmed user interaction is:

```
install malicious PWA -> open external registered protocol link

```

This still crosses from manifest-controlled web content into local process execution as the current Windows user through Chrome's PWA handler launcher and `--utility-cmd-prefix`.

### ro...@gmail.com (2026-05-17)

BTW: if Calculator keeps opening repeatedly during testing, terminate all Chrome processes. This happens when the injected headless Chrome instance remains alive and continues launching utility processes with the controlled prefix.

### ro...@gmail.com (2026-05-17)

Update: I confirmed that the installed PWA can auto-trigger its own registered protocol from the standalone PWA window.

After installation, the PWA opens its start\_url in standalone mode. The page detects `display-mode: standalone` and navigates once to `web+pwacalc://manual-user-trigger`. Chrome then shows the external protocol confirmation dialog for the installed PWA. If the user clicks “Open”, the vulnerable Windows PWA launcher is invoked and the previously confirmed `--headless --utility-cmd-prefix` chain executes.

This reduces the confirmed flow to:

1. User installs the malicious PWA.
2. The installed PWA auto-opens and triggers its registered protocol.
3. User accepts Chrome’s “Open app” protocol confirmation prompt.

The user no longer needs to close Chrome or manually open a separate trigger link/file. The remaining user interaction is accepting Chrome’s protocol confirmation dialog.

### ro...@gmail.com (2026-05-17)

### Additional finding: embedded NUL hides the injected switches in the external protocol prompt

I found that the PWA `manifest.name` can contain an embedded `\u0000` before the injected switches:

```
  "name": "PWATEST\u0000 --single-argument --headless --utility-cmd-prefix=calc.exe inert"

```

This preserves exploitation, but the external protocol confirmation dialog displays only the prefix before the NUL, e.g. PWATEST, while the underlying registered launcher path still contains the switch payload after sanitization.

This significantly improves the exploit UX/social-engineering impact: the user sees a benign app name in the confirmation prompt, not the suspicious Chromium switches.

### ch...@google.com (2026-05-17)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ts...@google.com (2026-05-18)

Windows-specific, setting found-in to extended-stable.

### ts...@google.com (2026-05-18)

Assigning per original author of code

### ct...@chromium.org (2026-05-18)

I wasn't able to reproduce with the original POC and steps, but using the update in the top of [Comment #2](https://issues.chromium.org/issues/513893425#comment2) I was able to reproduce:

1. Set up the included POC from [Comment #1](https://issues.chromium.org/issues/513893425#comment1), but change the name in the manifest to "PWA Calc Demo --single-argument --headless --utility-cmd-prefix=calc.exe inert" (the added `--headless` argument made it work for me)
2. Start a local test server from the POC directory (`python3 -m http.server 8000`)
3. Navigate Chrome to <http://127.0.0.1:8000/>
4. Click the "install" button in the omnibox and install the PWA
5. Close the PWA window
6. Navigate a tab to <http://127.0.0.1:8000/trigger.html> and click the "open web+ " button
7. See calc.exe pop

I couldn't get the null-bytes trick to really work -- it shows a "NUL" symbol rather than causing it to go off screen or anything.

Note that running the POC may cause an unceasing stream of calc.exe windows to appear, even if you close Chrome. Running `taskkill /F /IM "chrome.exe"` in powershell worked for me to stop it and then I closed all calc windows. You should then also uninstall the PWA.

Because this requires a fair bit of user interaction, dropping this to Sev-High (S-1). I haven't looked into all the followup comments however.

### ct...@chromium.org (2026-05-18)

Reporter: Do you have clear repro steps for a *user* triggering this from Chrome (without any harness manipulating Chrome, like the `node` steps or powershell steps in [Comment #2](https://issues.chromium.org/issues/513893425#comment2))? I *think* that maybe I ended up mostly following your repro steps in [Comment #4](https://issues.chromium.org/issues/513893425#comment4) but I'm not completely sure whether you have an even simpler repro. If this *does* require the usr to install a PWA and then click through an "open in PWA" dialog, then this seems S-1. If this could happen *just* from installing the PWA without any additional user interaction that would be useful information (not sure if it would bump it to S-0 though).

### dm...@google.com (2026-05-18)

@me...@google.com can you take a look? Or should one of us pick this up?

### dm...@google.com (2026-05-18)

oh sorry Jesse I posted this comment on the wrong bug - but same question, is this something you are able to own?

### ct...@chromium.org (2026-05-18)

In case it's helpful, I did some automated analysis with Gemini to try to trace the root cause here a little more thoroughly. The proposed fix it tacked on at the end seems off but I haven't thought through it very deeply.

**Prompt:**

```
You are an expert security researcher trying to understand how a reported bug in Chrome is working in the code. We have evidence that if a user on Windows installs a malicious PWA that has the name "PWA Calc Demo --single-argument --headless --utility-cmd-prefix=calc.exe inert", that PWA registers a protocol handler ("web+pwacal"), and then the user clicks a protocol link that triggers starting the PWA, then the arguments get smuggled through to Windows and cause the actual `calc.exe` to pop.

This is likely related to code in the following files:
- base/command_line.cc
- chrome/browser/web_applications/os_integration/web_app_handler_registration_utils_win.cc
- chrome/browser/web_applications/chrome_pwa_launcher/chrome_pwa_launcher_main.cc
- content/browser/service_host/utility_process_host.cc

Can you investigate and try to determine how this PWA title flows through this code to cause this and determine a root cause and code location?

```
Gemini Output:
# PWA Argument Smuggling Vulnerability Analysis (Windows)

This document analyzes a vulnerability in Google Chrome on Windows where a PWA with a specially crafted name can smuggle command-line arguments through the PWA launcher to the main Chrome process, ultimately leading to arbitrary code execution via utility process command prefix injection.

## Summary

When a PWA is installed on Windows, Chrome creates an app-specific launcher executable (a hard link to `chrome_pwa_launcher.exe`) whose filename is derived from the PWA's name. If the PWA name contains command-line arguments (e.g., `"--single-argument --headless --utility-cmd-prefix=calc.exe inert"`), these arguments become part of the launcher's filename.

When the PWA is launched via a registered protocol handler, Windows executes the launcher. The launcher then attempts to launch `chrome.exe` with the same arguments. Due to a parsing bug in `base::CommandLine` combined with how arguments are serialized and deserialized between processes, the arguments embedded in the launcher's filename are "smuggled" and interpreted as actual switches by `chrome.exe`. Specifically, the `--utility-cmd-prefix` switch is smuggled, which instructs Chrome to prepend a wrapper (in this case, `calc.exe`) when starting utility processes, resulting in arbitrary execution.

---

## Vulnerability Flow Analysis

### 1. PWA Registration and Launcher Creation

- **File:** [web\_app\_handler\_registration\_utils\_win.cc](javascript:void(0);)
- **Step:** During installation, `CreateAppLauncherFile` is called.
- **Mechanism:** It sanitizes the PWA name to create a filename using `GetAppSpecificLauncherFilename`. However, spaces, hyphens, and `=` are valid Windows filename characters, so they survive sanitization.
- **Result:** A launcher is created with a name like:
  `PWA Calc Demo --single-argument --utility-cmd-prefix=calc.exe inert.exe`

### 2. Protocol Handler Registration

- **File:** [web\_app\_protocol\_handler\_registration\_win.cc](javascript:void(0);)
- **Step:** `RegisterProtocolHandlersWithOSInBackground` registers the protocol handler in the Windows registry.
- **Mechanism:** It uses `ShellUtil::AddApplicationClass` to register the open command. It uses `GetCommandLineStringForShell()` which appends `--single-argument %1`.
- **Result:** The registry command is registered as:
  `"C:\path\to\PWA Calc Demo --single-argument --utility-cmd-prefix=calc.exe inert.exe" --profile-directory="Default" --app-id="malicious_app_id" --single-argument %1`

### 3. PWA Launch and Launcher Parsing Bug

- **File:** [chrome\_pwa\_launcher\_main.cc](javascript:void(0);) and [command\_line.cc](javascript:void(0);)
- **Step:** User triggers the protocol, Windows executes the launcher.
- **Mechanism:**
  1. The launcher starts. `base::CommandLine::Init` parses the command line from `GetCommandLineW()`.
  2. It encounters `--single-argument` at the end of the command line.
  3. It calls `CommandLine::ParseAsSingleArgument`.
  4. **CRITICAL BUG:** `ParseAsSingleArgument` searches the *entire* raw command line for `--single-argument`. It finds it first in the **program path** (since the PWA name contains it), not at the end.
  5. It extracts everything after that first match as a single argument:
     `arg` = `--utility-cmd-prefix=calc.exe inert.exe" --profile-directory="Default" --app-id="malicious_app_id" --single-argument "web+pwacal:link"`
     (Note the trailing quote `"` from the program path is included).
  6. This `arg` is appended to the launcher's `CommandLine` object as a non-switch argument (`argv[3]`).

### 4. Argument Forwarding and Serialization Mismatch

- **File:** [chrome\_pwa\_launcher\_main.cc](javascript:void(0);) and [command\_line.cc](javascript:void(0);)
- **Step:** Launcher calls `LaunchPwa` to start `chrome.exe`.
- **Mechanism:**
  1. It creates a new `CommandLine` for `chrome.exe` and appends the launcher's arguments using `AppendArguments(..., include_program=false)`.
  2. The launcher's `argv[3]` (the smuggled string) starts with `--`, so `CommandLine::AppendSwitchesAndArguments` treats it as a switch.
  3. It splits it at the first `=`:
     - `switch_string` = `--utility-cmd-prefix`
     - `switch_value` = `calc.exe inert.exe" --profile-directory="Default" ...`
  4. It adds this as switch `utility-cmd-prefix` to the new `CommandLine`.
  5. When serializing the command line for `chrome.exe` via `GetCommandLineString()`, it appends `switch_string` (unquoted) and the quoted `switch_value`:
     `... --utility-cmd-prefix="calc.exe inert.exe\" ..." ...`
  6. If the smuggled string had `--headless` before `--utility-cmd-prefix`, the `switch_string` would be `--headless --utility-cmd-prefix`. Because `GetCommandLineString` does **not** quote `switch_string` (assuming switch names cannot contain spaces), it serializes as:
     `... --headless --utility-cmd-prefix="calc.exe ..."`
     Notice the unquoted space between `--headless` and `--utility-cmd-prefix`.

### 5. Chrome Parsing and Exploitation

- **File:** [command\_line.cc](javascript:void(0);) and [utility\_process\_host.cc](javascript:void(0);)
- **Step:** `chrome.exe` starts and parses its command line.
- **Mechanism:**
  1. `CommandLineToArgvW` splits the command line.
  2. If `--headless` was present, it splits at the unquoted space:
     - Token A: `--headless`
     - Token B: `--utility-cmd-prefix=calc.exe inert.exe" ...`
  3. `chrome.exe`'s `CommandLine` now successfully parses the switch `utility-cmd-prefix` with value `calc.exe inert.exe" ...`.
  4. Later, when Chrome starts a utility process, `UtilityProcessHost::StartProcess` detects the `utility-cmd-prefix` switch.
  5. It calls `cmd_line->PrependWrapper(value)`.
  6. `PrependWrapper` splits the value by space. The first token is `calc.exe`.
  7. It prepends `calc.exe` to the utility process command line.
  8. The utility process is launched, executing `calc.exe` instead of the Chrome utility binary.

---

## Root Causes

1. **`CommandLine::ParseAsSingleArgument` Path Matching:** It searches the raw command line string from the beginning, allowing it to match switches inside the program path (which can be controlled via PWA names on Windows).
2. **Unquoted Switch Serialization:** `CommandLine::GetCommandLineString` does not quote switch names when serializing, assuming they cannot contain spaces. This allows argument splitting in the child process if a malformed switch name containing spaces is programmatically added.
3. **Permissive PWA Name Sanitization for Filenames:** The PWA launcher filename creation allows characters like spaces and hyphens, enabling command-line-like strings in the filename.

---

## Code Locations

- **`base/command_line.cc`:**
  - [`CommandLine::ParseAsSingleArgument`](javascript:void(0);) - Vulnerable search logic.
  - [`CommandLine::GetArgumentsStringInternal`](javascript:void(0);) - Missing quoting for `switch_string`.
- **`chrome/browser/web_applications/os_integration/web_app_handler_registration_utils_win.cc`:**
  - [`GetAppSpecificLauncherFilename`](javascript:void(0);) - Permissive sanitization.
- **`content/browser/service_host/utility_process_host.cc`:**
  - [`UtilityProcessHost::StartProcess`](javascript:void(0);) - Execution of the prepended wrapper.

---

## Proposed Fix (Conceptual)

The primary fix should be in `base/command_line.cc` to prevent `ParseAsSingleArgument` from matching inside the program path.

```
--- a/base/command_line.cc
+++ b/base/command_line.cc
@@ -783,8 +783,22 @@ void CommandLine::ParseAsSingleArgument(
   // Remove any previously parsed arguments.
   argv_.resize(static_cast<size_t>(begin_args_));
 
+  // Estimate the end of the program path in the raw command line to avoid
+  // matching switches inside the program path itself.
+  size_t program_end = 0;
+  if (!raw_command_line_string_.empty() && raw_command_line_string_[0] == L'"') {
+    program_end = raw_command_line_string_.find(L'"', 1);
+    if (program_end != StringType::npos) {
+      program_end++; // Move past the closing quote
+    } else {
+      program_end = 0;
+    }
+  } else {
+    program_end = raw_command_line_string_.find(L' ');
+    if (program_end == StringType::npos) {
+      program_end = 0;
+    }
+  }
+
   // Locate "--single-argument" in the process's raw command line. Results are
   // unpredictable if "--single-argument" appears as part of a previous
   // argument or switch.
   const size_t single_arg_switch_position =
-      raw_command_line_string_.find(single_arg_switch);
+      raw_command_line_string_.find(single_arg_switch, program_end);

```

### ro...@gmail.com (2026-05-18)

Hi!

Sorry for the delay in getting back to you.

I spent a significant amount of time trying to find a way to bypass that second user interaction (the protocol confirmation dialog) to achieve a pure, zero-click flow post-install. Unfortunately, I really couldn't achieve it. As it stands, the most direct reproduction flow strictly requires the user to install the PWA and then click "Open" on the protocol confirmation prompt when the PWA auto-triggers it.

Regarding the NUL byte trick, here is the minimal PoC. Depending on the exact Windows build or UI font rendering, the NUL byte might show up as a missing glyph, but it successfully truncates the visual string for the average user, hiding the injected arguments in the prompt.

In the manifest, you need to use this name: "name": "Null Byte PWA\u0000 --single-argument --headless --utility-cmd-prefix=calc.exe inert"

### ct...@chromium.org (2026-05-18)

Thanks, good to know that it seems (for now) like this requires the second prompt.

(Note: please attach files directly instead of in zips. I know it can be a pain for PWAs and stuff, but it is a requirement for us to be able to inspect and view them directly.)

### ro...@gmail.com (2026-05-18)

Yes, of course!

icon.svg, index.html, manifest.webmanifest, open-protocol.html and sw.js needs to be in the "site" folder

### ro...@gmail.com (2026-05-18)

This trigger is not limited to custom web+... protocols. Chromium PWAs can also register existing protocols such as mailto.

For example, the malicious PWA name could be:

Mail Client --single-argument --headless --utility-cmd-prefix=calc.exe inert

A realistic attacker could present the PWA as a mail client or webmail helper, then use a normal mailto: action from a webmail or email-related service. This would avoid Chrome’s custom-protocol confirmation prompt for an unknown web+... scheme.

Windows may still show its own “How do you want to open this?” chooser if there is no default mail handler or if the user needs to pick one. However, if the user selects the installed malicious PWA, the OS dispatch opens the app-specific PWA launcher, which is the vulnerable path. After that association/default choice, later mailto: triggers can open the PWA without the Chrome custom-protocol confirmation.

This does not remove all user interaction, but it broadens the realistic trigger surface, install the PWA, then click/use a normal email action.

### ro...@gmail.com (2026-05-18)

I tested them one by one. The only protocol that failed was nntp://.

What actually happens is that Chrome blocks nntp:// before anything is passed to Windows. In Chromium, the scheme is hardcoded as denied inside external\_protocol\_handler.cc under kDeniedSchemes, which is why Chrome shows:

Not allowed to launch 'nntp://example.invalid/comp.test'

So the failure does not necessarily mean the PWA registration itself failed. It means Chrome prevents websites from invoking that protocol handler in the first place.

| # | Protocol | App | Open | Trigger URL | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin` | PWA bitcoin | [Open](javascript:void(0);) | `bitcoin:bc1qexample0000000000000000000000000000000?amount=0` | confirmed |
| 2 | `cabal` | PWA cabal | [Open](javascript:void(0);) | `cabal:protocol-matrix-test` | confirmed |
| 3 | `dat` | PWA dat | [Open](javascript:void(0);) | `dat://example.invalid/protocol-matrix` | confirmed |
| 4 | `did` | PWA did | [Open](javascript:void(0);) | `did:example:protocol-matrix` | confirmed |
| 5 | `doi` | PWA doi | [Open](javascript:void(0);) | `doi:10.1000/182` | confirmed |
| 6 | `dweb` | PWA dweb | [Open](javascript:void(0);) | `dweb://example.invalid/protocol-matrix` | confirmed |
| 7 | `ethereum` | PWA ethereum | [Open](javascript:void(0);) | `ethereum:0x0000000000000000000000000000000000000000` | confirmed |
| 8 | `geo` | PWA geo | [Open](javascript:void(0);) | `geo:0,0?q=protocol-matrix` | confirmed |
| 9 | `hyper` | PWA hyper | [Open](javascript:void(0);) | `hyper://example.invalid/protocol-matrix` | confirmed |
| 10 | `im` | PWA im | [Open](javascript:void(0);) | `im:protocol-matrix-test` | confirmed |
| 11 | `ipfs` | PWA ipfs | [Open](javascript:void(0);) | `ipfs://example.invalid/protocol-matrix` | confirmed |
| 12 | `ipns` | PWA ipns | [Open](javascript:void(0);) | `ipns://example.invalid/protocol-matrix` | confirmed |
| 13 | `irc` | PWA irc | [Open](javascript:void(0);) | `irc://example.invalid/#protocol-matrix` | confirmed |
| 14 | `ircs` | PWA ircs | [Open](javascript:void(0);) | `ircs://example.invalid/#protocol-matrix` | confirmed |
| 15 | `magnet` | PWA magnet | [Open](javascript:void(0);) | `magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=protocol-matrix` | confirmed |
| 16 | `mailto` | PWA mailto | [Open](mailto:security-test@example.invalid?subject=protocol-matrix-mailto) | `mailto:security-test@example.invalid?subject=protocol-matrix-mailto` | confirmed |
| 17 | `matrix` | PWA matrix | [Open](javascript:void(0);) | `matrix:r/protocol-matrix:example.invalid?action=join` | confirmed |
| 18 | `mms` | PWA mms | [Open](javascript:void(0);) | `mms://example.invalid/protocol-matrix` | confirmed |
| 19 | `news` | PWA news | [Open](javascript:void(0);) | `news:comp.test` | confirmed |
| 20 | `nntp` | PWA nntp | [Open](javascript:void(0);) | `nntp://example.invalid/comp.test` | failed |
| 21 | `openpgp4fpr` | PWA openpgp4fpr | [Open](javascript:void(0);) | `openpgp4fpr:1234567890ABCDEF1234567890ABCDEF12345678` | confirmed |
| 22 | `sip` | PWA sip | [Open](javascript:void(0);) | `sip:test@example.invalid` | confirmed |
| 23 | `sms` | PWA sms | [Open](javascript:void(0);) | `sms:+15550101010?body=protocol-matrix-sms` | confirmed |
| 24 | `smsto` | PWA smsto | [Open](javascript:void(0);) | `smsto:+15550101010:protocol-matrix-smsto` | confirmed |
| 25 | `ssb` | PWA ssb | [Open](javascript:void(0);) | `ssb://example.invalid/protocol-matrix` | confirmed |
| 26 | `ssh` | PWA ssh | [Open](javascript:void(0);) | `ssh://example.invalid/protocol-matrix` | confirmed |
| 27 | `tel` | PWA tel | [Open](javascript:void(0);) | `tel:+15550101010` | confirmed |
| 28 | `urn` | PWA urn | [Open](javascript:void(0);) | `urn:example:protocol-matrix` | confirmed |
| 29 | `webcal` | PWA webcal | [Open](javascript:void(0);) | `webcal://example.invalid/calendar.ics` | confirmed |
| 30 | `wtai` | PWA wtai | [Open](javascript:void(0);) | `wtai://wp/mc;+15550101010` | confirmed |
| 31 | `xmpp` | PWA xmpp | [Open](javascript:void(0);) | `xmpp:test@example.invalid` | confirmed |
| 32 | `ftp` | PWA ftp | [Open](ftp://example.invalid/protocol-matrix) | `ftp://example.invalid/protocol-matrix` | confirmed |
| 33 | `ftps` | PWA ftps | [Open](javascript:void(0);) | `ftps://example.invalid/protocol-matrix` | confirmed |
| 34 | `sftp` | PWA sftp | [Open](javascript:void(0);) | `sftp://example.invalid/protocol-matrix` | confirmed |

### je...@google.com (2026-05-19)

Thanks for the report. I am a suitable owner for this bug. There's a lot of text here, so just to make sure I understand this correctly, it sounds like the flow is:

1. a PWA names itself e.g., "My PWA --single-argument --do-something-bad --etc" (for simplicity)
2. the PWA name is used as the filename for the PWA launcher: `My PWA --single-argument --do-something-bad --etc.exe`
3. the PWA launcher is registered as a file handler in the registry: `"My PWA --single-argument --do-something-bad --etc.exe" --app-id=123 --single-argument %1`
4. when the PWA launcher runs, it parses its command line from string; the first/phony `--single-argument` causes the command line to look like: `[My PWA], [--do-something-bad --etc.exe" --app-id=123 --single-argument %1]` [not sure about the quotes]
5. the PWA launcher launches Chrome [with the args it received](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/chrome_pwa_launcher/chrome_pwa_launcher_main.cc;l=47;drc=2d5c2bb09f8097db6d25775671524766c53649d7); `LaunchProcess()` re-stringifies the command line, resulting in `chrome.exe --do-something-bad --etc.exe --app-id=123 --single-argument %1`

Please feel free to correct me if I'm wrong.

If I recall, when `--single-argument` was introduced, it was considered safe because Chrome controls the file-handler registration code. The use of PWA names as executable paths does seem to break this assumption.

It seems like we could either sanitize PWA launcher names (e.g., replace hyphens with underscores) to sidestep this, or adjust `ParseAsSingleArgument` as proposed in [comment #13](https://issues.chromium.org/issues/513893425#comment13) (identify the program name upfront by looking for the first block of text being enclosed in quotes, or everything up to the first space). The latter seems reasonable to me, but I'm open to suggestions. CC'ing grt@ in case he has thoughts as another person familiar with this code.

### je...@google.com (2026-05-19)

Oops, just saw your draft CL dmurph@ - feel free to take this bug if you like. : )

### ro...@gmail.com (2026-05-19)

Yes, that flow is correct.

The key nuance is that the first `--single-argument` is inside the quoted launcher executable path, but `ParseAsSingleArgument()` searches the raw command-line string with `find()`. As a result, it matches the injected token in the launcher filename before the real registry-added `--single-argument %1`.

Example shape:

```
"...\My PWA --single-argument --headless --utility-cmd-prefix=calc.exe inert.exe" --app-id=123 --single-argument web+example://open

```

So the tail after the injected token is reinterpreted as Chrome arguments, including:
--headless --utility-cmd-prefix=calc.exe

For the fix, I agree the parser-side fix is important because it protects existing launcher registrations. The parser should bind to the actual shell-handler --single-argument argument, not the first raw substring occurrence in the full command line. Using app-id/profile-derived launcher filenames instead of manifest display names would also be good defense-in-depth.

### ch...@google.com (2026-05-19)

Setting milestone because of s0/s1 severity.

### gr...@chromium.org (2026-05-19)

I like the idea of fixing the parsing. From a pure correctness point of view, we shouldn't be looking for `--single-argument` within the portion of the command line that is the program name/path.

### ro...@gmail.com (2026-05-21)

Hello! I reviewed CL 7858094 and I think there is still a bypass through Windows ShellExecute placeholder expansion.

The patch skips the first quoted argv[0] by searching for the first raw `"` after index 1. However, if the PWA launcher filename contains `%1`, Windows appears to substitute `%1` even inside the quoted executable path. If the dispatched protocol URL contains a literal `"`, that quote is injected into argv[0], so the new skip logic stops early and the following raw `find("--single-argument")` can hit a manifest-controlled marker in the launcher filename.

Minimal shape:

Manifest name:
`Updated PoC %1\u0000 --single-argument --headless --utility-cmd-prefix=calc.exe #inert`

Sanitized launcher basename:
`Updated PoC %1 --single-argument --headless --utility-cmd-prefix=calc.exe inert.exe`

Internet Shortcut trigger:
`web+updatedpoc://open/"` 

Important: the trigger URL should contain `"` at the end.

I verified this with the patched `base::CommandLine` tests and with a patched `chrome_pwa_launcher.exe` forwarding to a dummy `chrome.exe`. The dummy browser receives `--headless` and `--utility-cmd-prefix=...` as real switches. I’m still building full Chromium locally to validate the final end-to-end calc marker, but that may take a few hours.

Can you try this on a full patched Windows Chromium build and confirm whether the utility prefix executes?
Thanks.

### ro...@gmail.com (2026-05-22)

Quick update: after ~14 hours of local build time and several Windows build/runtime issues, I got a patched Chromium build far enough to test the real chrome\_pwa\_launcher.exe path.

I still cannot cleanly confirm the final calc/utility-cmd-prefix marker in my local environment because the generated PWA launcher from this component/debug build needed multiple dependent DLLs copied beside the per-app launcher, and I’m still hitting local Windows/runtime execution issues after that.

However, Procmon confirms the important bypass behavior, ShellExecute starts the app-specific PWA launcher with the %1-expanded filename, and that launcher then starts the patched chrome.exe with attacker-controlled switches forwarded on the Chrome command line. The injected switches appear before the legitimate protocol URL tail, which means CL 7858094 raw quote skipping still accepts the fake --single-argument boundary.

I'll leave it to the team to reproduce the full chain on a stable release build, but the parser bypass is working.

### ro...@gmail.com (2026-05-27)

Hello again!

I reviewed the latest patchset change and I think a related placeholder-expansion case may still bypass it. (Patchset 12)

The new logic avoids matching `--single-argument` inside the original program path by estimating the end of `argv[0]` from `GetProgram().length()`, then searching the raw command line after that point.

However, Windows `ShellExecute` can expand `%1` inside the quoted launcher path before Chromium parses the command line.

Example manifest name:
`"Updated PoC %1\u0000 --single-argument --headless --utility-cmd-prefix=calc.exe inert"`

Example trigger URL:
`web+updatedpoc://open/"`

After `%1` expansion, the literal quote from the URL can terminate `argv[0]` early. `CommandLineToArgvW()` then sees the manifest-controlled payload as real `argv` entries, and the patched raw `find("--single-argument", switches_and_args_start)` can still select the manifest-controlled `--single-argument` instead of the registry-added one.

In an isolated reproduction using `CommandLineToArgvW()` plus the patched scan logic, the recovered single-argument tail becomes:
`--headless --utility-cmd-prefix=calc.exe inert.exe" --profile-directory=Default --app-id=<id> --single-argument web+updatedpoc://open/"`

So the attacker-controlled switches can still be parsed and forwarded by the PWA launcher.

I have not yet completed a full end-to-end patched Chromium retest, but the parser behavior appears to preserve the original primitive.

---

Also i think there is a second bypass variant that does not use `--single-argument` in the manifest name at all.

Manifest name: `Victim %1 --headless --utility-cmd-prefix=calc.exe %1 inert`
Trigger URL: `web+victim://open/"`

After ShellExecute expands `%1`, the two injected `"` from the URL create matched quote boundaries that expose `--headless, --utility-cmd-prefix=calc.exe`, and `--app-id` as separate argv entries. These switches are parsed by AppendSwitchesAndArguments before `--single-argument` is reached. The ParseAsSingleArgument fix works correctly, it finds the real `--single-argument`, but the dangerous switches are already in the switch map.

---

I have not completed a full end-to-end retest because I was unable to build Chromium locally with the patch applied (build/runtime issues on my Windows environment). If you could provide a patched test build or let me know when the fix lands in a canary/dev channel release, I can retest against that.

### dm...@google.com (2026-05-28)

I have updated the CL (<https://crrev.com/c/7858094>) to address these bypasses.

The fix now sanitizes the '%' character in the PWA launcher filenames, replacing it with a space. This ensures that '%1'
becomes ' 1' in the registered path, preventing Windows ShellExecute from expanding the protocol URL inside the program path
( argv[0] ).

This blocks both bypass variants you mentioned:

1. Updated PoC %1\0 ... -> The %1 is not expanded, so the quoted program path remains intact and the CommandLine parser
   correctly ignores the fake switches inside it.
2. Victim %1 ... %1 inert -> Similarly, no expansion occurs, preventing the quote-splitting behavior that allowed switches
   to escape argv[0] . I've also added unit tests covering these specific cases (including the embedded NUL byte and multiple %1 s) and verified
   they pass.

Replacing with ' ' is consistent with how we replace other illegal characters with a space.

### ro...@gmail.com (2026-05-28)

Perfect, it works!

One additional concern. Replacing `%` appears to protect newly generated PWA launcher filenames, but it may not migrate existing vulnerable registrations.

From my reading of the update path, launcher filenames are recomputed using the sanitized basename. As a result, a pre-patch launcher such as `Updated PoC %1 --single-argument ... .exe` could potentially remain present and registered, while the updater now looks for `Updated PoC 1 --single-argument ... .exe` and therefore misses it.

I have not verified this through a real upgrade scenario yet, but it may be worth explicitly migrating or cleaning up existing `%`-based registrations as well, especially since we do not know whether any such installations may already exist in the wild.

I'll continue testing the updated implementation and will let you know if I find anything else. From what I've seen so far, the mitigation looks significantly more robust, and I don't currently see an obvious way around it.

### ro...@gmail.com (2026-05-29)

Hello again! I tested the latest patchset and could not find a practical bypass for newly generated PWA launcher registrations.

I specifically retested the previous ShellExecute `%1` / quote-splitting paths, fake `--single-argument` placement, protocol and file-handler triggers, shortcut/menu/uninstall/notification-related surfaces, and several manifest-controlled fields. I also used an automated Python harness to generate and test thousands of variants around `%`, quotes, NULs, whitespace, switch prefixes, and repeated placeholders. None of those produced attacker-controlled switches before the real `--single-argument` boundary with the new `%` sanitization in place.

At this point I do not have another bypass for the updated implementation. The new approach looks robust against the bypass classes I was able to model and test.

### dx...@google.com (2026-05-30)

Project: chromium/src  

Branch:  main  

Author:  Dan Murphy [dmurph@chromium.org](mailto:dmurph@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7858094>

[base] Fix Windows CommandLine argument smuggling

---


Expand for full commit details
```
     
    A manifest-controlled PWA name on Windows can be crafted to inject 
    command-line arguments. ParseAsSingleArgument could match the "--single- 
    argument" switch inside the program path if it was quoted and contained 
    that string. 
     
    Fix this by estimating the end of the program path and searching for "-- 
    single-argument" only after that path. Also add CHECKs to ensure a valid 
    program path end is found. 
     
    Additionally, sanitize "%" characters in web app shortcut filenames on 
    Windows to avoid ShellExecute expansion issues. 
     
    TAG=agy 
    CONV=823a5c45-9cb2-45bc-a45b-4c02939fca02 
     
    Fixed: 513893425 
    Fixed: b:514442159 
    Test: base_unittests --gtest_filter=CommandLineTest.* 
    Test: unit_tests --gtest_filter=WebAppShortcutWinTest.* 
    Change-Id: Id209dc44104f919fb1a37118bc82d82d1f1b10c3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7858094 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Jesse McKenna <jessemckenna@google.com> 
    Commit-Queue: Daniel Murphy <dmurph@chromium.org> 
    Auto-Submit: Daniel Murphy <dmurph@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1638873}

```

---

Files:

- M `base/command_line.cc`
- M `base/command_line_unittest.cc`
- M `chrome/browser/web_applications/os_integration/web_app_shortcut_win.cc`
- M `chrome/browser/web_applications/os_integration/web_app_shortcut_win_unittest.cc`

---

Hash: [b9f096090bebe17e5088e11a5daca42e988865e9](https://chromiumdash.appspot.com/commit/b9f096090bebe17e5088e11a5daca42e988865e9)  

Date: Sat May 30 01:02:26 2026


---

### ch...@google.com (2026-05-31)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-31)

**M148** merge request created. **Please update [crbug/518353966](https://crbug.com/518353966) to have this merge reviewed.**

### ch...@google.com (2026-05-31)

**M149** merge request created. **Please update [crbug/518353223](https://crbug.com/518353223) to have this merge reviewed.**

### ro...@gmail.com (2026-05-31)

Hi!

I just retested the issue on Chrome for Testing Canary 150.0.7868.0, and the fresh install case looks fixed. Newly generated PWA launcher filenames now replace `%` with spaces as expected, and I could not reproduce the original calc/utility-cmd-prefix flow on a newly installed PWA.

One extra data point, i also tested the old-installation case and was able to confirm it end-to-end.
Test:

- Install the malicious PWA with a pre-fix Chrome for Testing build.
- The registered PWA launcher path contains `%1` and the injected switches.
- Update the profile’s `Last Browser` target to patched Canary 150.0.7868.0.
- Trigger the already-registered protocol handler.

Observed result:
The stale launcher registration remains unchanged, and patched Canary launches with `--headless --utility-cmd-prefix=calc.exe`. `calc.exe` is then observed as the utility-process wrapper.

I do not think this is likely to be a widely known attack vector, since the `%1` placeholder expansion angle came up only after testing the first fix. So this is probably more of an installed-base migration edge case than a fresh bypass. I’m sharing it mainly as additional information in case you want to migrate or clean up stale vulnerable PWA launcher registrations during update.

If preferred, I can file this separately as an installed-base migration issue.

### dm...@google.com (2026-06-01)

migration likely is s3/s4. I also think that on any app update, we search shortcuts for ones that have appid matches, and replace. so - this might be fixed via os integration syncing, which can happen for various reasons

### ro...@gmail.com (2026-06-01)

Understood, that makes sense. Thanks for the clarification and the great work on the patches!

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2500.00 for this report.

Rationale for this decision:
Medium Impact. Local privilege escalation.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ro...@gmail.com (2026-06-04)

Hello Chrome VRP Panel,

Thank you for the reward decision and for the work on fixing this issue.

I would like to respectfully request a reassessment of the reward amount for this report. Could you please add the Security-VRP-Reassessment-Request hotlist for panel review?

I understand that the final severity assessment considered the required user interaction. However, I believe the current $2,500 award may not fully reflect the practical impact and the contribution provided in this report.

The demonstrated issue was not a purely local primitive. Through UI truncation techniques (NUL bytes) and standard protocol triggers (e.g., mailto), the required user interaction was rendered highly deceptive. Attacker-controlled PWA manifest data could influence Chrome’s Windows PWA handler launcher flow and result in attacker-controlled native process execution as the current Windows user through Chrome-managed OS integration. This did not require prior local code execution or administrative privileges.

In addition to the initial working PoC, the report included root-cause analysis, a reduced explanation of the vulnerable command-line parsing behavior, multiple trigger variants, follow-up exploitability analysis, validation of patch behavior, and identification of cases that required additional hardening before the final fix. The issue was reproduced by the Chrome team, fixed in Chromium, and selected for merge to supported milestones.

Even if the panel keeps the final severity classification unchanged, I would appreciate reconsideration of whether the reward should be closer to the upper end of the applicable category, or adjusted to reflect the demonstrated web-to-native execution impact and the amount of fix-validation work provided.

Thank you again for reviewing.

### ch...@google.com (2026-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513893425)*
