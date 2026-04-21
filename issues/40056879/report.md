# Security: Insufficient CORS Check Leads to Cross-Origin Size Leak via BackgroundFetch API

| Field | Value |
|-------|-------|
| **Issue ID** | [40056879](https://issues.chromium.org/issues/40056879) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-08-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue is similar to <https://crbug.com/chromium/915446>. By using the BackgroundFetch API it is possible to request a cross-origin site with cookies and leak the exact response size if the server responds with a `Access-Control-Allow-Origin: \*` header. Usually CORS requests with credentials are being blocked if the server response with a wildcard ACAO header.

**VERSION**  

Chrome Version: Version 92.0.4515.131 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**  

test.html

```
<script>  
  navigator.serviceWorker.ready.then(async (swReg) => {  
    swReg.backgroundFetch.fetch(  
      "test",  
      ["https://<some-site>"], // some site that sends a wildcard ACAO header  
    );  
  });  
  
  navigator.serviceWorker.register("sw.js");  
</script>  

```

sw.js

```
self.addEventListener("backgroundfetchsuccess", (e) => {  
  console.log(e.registration.downloaded);  
});  

```

**CREDIT INFORMATION**  

Reporter credit: Maurice Dauer

## Timeline

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-13)

Thanks for your report. I'm not entirely sure of the security implications of this but I agree this does look a lot like https://crbug.com/chromium/915446 so hopefully the people added to the bug can take a look and triage further.

[Monorail components: Blink>BackgroundFetch]

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-08-16)

Yep, I can recreate this. It doesn't just leak the length, it leaks the response too, so pri-1 feels correct.

Cookies can be set here: https://echo-cookie-test.glitch.me/
And here to bg-fetch something that depends on that cookie: https://static-misc-3.glitch.me/bg-fetch-test/

The CORS rules aren't being followed properly here.

Bg-fetch shouldn't send credentials to cross-origin resources unless the request credentials mode (https://fetch.spec.whatwg.org/#concept-request-credentials-mode) is "include".

If the request credentials mode is "include", the Access-Control-Allow-Credentials header must be "true", and the Access-Control-Allow-Origin header must be the request origin. Here are the steps: https://fetch.spec.whatwg.org/#cors-check

If bg-fetch is doing CORS differently, it might be worth checking it complies with the rest of CORS.

### la...@gmail.com (2021-08-16)

Also, since bg-fetch currently seems to be a top-level navigation, default cookies with `SameSite=Lax` are sent along the request, although only cookies with `SameSite=None` should be sent for CORS requests if I'm not mistaken.

### mk...@chromium.org (2021-08-16)

All of this sounds bad. The severity is still medium, but bypassing CORS is a high kind of medium. :) Sending `SameSite=Lax` along with these requests as well sounds like a separate (though probably related in the codebase, along with Fetch Metadata headers, etc) bug.

+yhirano@ for CORS.
+morlovich@ for samesite.

### ja...@chromium.org (2021-08-16)

Agreed. From what I understand, bg-fetch uses the 'download' codepath which, as you say, is a navigation.

Not all navigations are top-level, and downloads don't need to be top-level. But yeah, bg-fetch requests should be closer to fetch() than navigations.

### mk...@chromium.org (2021-08-16)

Actually +morlovich (and minus chlily :( ).

### ja...@chromium.org (2021-08-16)

It isn't a full CORS bypass, but it allows with-credentials when the destination only allows without-credentials. Still a big deal though.

### mk...@chromium.org (2021-08-16)

Right. I see it as falling into "A bypass of the same origin policy for pages that meet several preconditions" and not "A bug that allows full circumvention of the same origin policy.", so medium severity, not high severity. But still an issue I'd like to see fixed, and merged back to 94 if possible.

### yh...@chromium.org (2021-08-16)

I'm not familiar with BackgroundFetch. Is this a spec issue or an implementation issue?

### ja...@chromium.org (2021-08-16)

It's an implementation issue. The spec is correct in this regard.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### de...@chromium.org (2021-08-17)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-08-17)

Thanks Jake, I sent out a few fixes for this
- https://chromium-review.googlesource.com/c/chromium/src/+/3100108
- https://chromium-review.googlesource.com/c/chromium/src/+/3100646

I'm not sure about the severity of this, will this require merging back?

### gi...@appspot.gserviceaccount.com (2021-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1979a70b5318d35200b65435bed9475be7e4a462

commit 1979a70b5318d35200b65435bed9475be7e4a462
Author: Rayan Kanso <rayankans@google.com>
Date: Thu Aug 19 17:46:51 2021

Pass the credentials mode to the download service.

The default is still 'Allow' which will not affect any existing download
clients, however the clients will be able to customize the credentials
mode as needed.

Bug: 1239709
Change-Id: I2bbddf055b2832f5529bfce2f23cc19248e279bb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3100108
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#913455}

[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/database/DEPS
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/background_service/DEPS
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/background_service/download_params.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/download_create_info.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/download_item.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/content/public/test/fake_download_item.cc
[modify] https://crrev.com/1979a70b5318d35200b65435bed9475be7e4a462/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e49b65794098938907203cc55978ac41f3d43d8b

commit e49b65794098938907203cc55978ac41f3d43d8b
Author: Hui Yingst <nigi@chromium.org>
Date: Thu Aug 19 19:46:41 2021

Revert "Pass the credentials mode to the download service."

This reverts commit 1979a70b5318d35200b65435bed9475be7e4a462.

Reason for revert: Dependency issue in https://ci.chromium.org/p/chromium/builders/ci/linux-archive-dbg/22813
which caused the tree to close.

Original change's description:
> Pass the credentials mode to the download service.
>
> The default is still 'Allow' which will not affect any existing download
> clients, however the clients will be able to customize the credentials
> mode as needed.
>
> Bug: 1239709
> Change-Id: I2bbddf055b2832f5529bfce2f23cc19248e279bb
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3100108
> Commit-Queue: Rayan Kanso <rayankans@chromium.org>
> Reviewed-by: Xing Liu <xingliu@chromium.org>
> Reviewed-by: Reilly Grant <reillyg@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#913455}

Bug: 1239709
Change-Id: Ia84c5b701a5407c37e8c62ba993d4f685e56e51a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3108051
Commit-Queue: Olivia Yingst <huiyingst@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Olivia Yingst <huiyingst@google.com>
Owners-Override: Olivia Yingst <huiyingst@google.com>
Cr-Commit-Position: refs/heads/main@{#913506}

[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/database/DEPS
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/background_service/DEPS
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/background_service/download_params.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/download_create_info.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/download_item.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/content/public/test/fake_download_item.cc
[modify] https://crrev.com/e49b65794098938907203cc55978ac41f3d43d8b/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6e18e0def715b5ccf65855963273dff0ec64871e

commit 6e18e0def715b5ccf65855963273dff0ec64871e
Author: Rayan Kanso <rayankans@google.com>
Date: Fri Aug 20 17:27:49 2021

[Resubmit] Pass the credentials mode to the download service.

The default is still 'Allow' which will not affect any existing download
clients, however the clients will be able to customize the credentials
mode as needed.

This was already reviewed in https://chromium-review.googlesource.com/c/chromium/src/+/3100108
but was reverted due to a dependency issue. The CL adds an extra
dependency (diff against patchset 1 which contains the original submission)

Bug: 1239709
Change-Id: I074c7e096e326ea39d40905e65b79c781dc541ca
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110007
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/main@{#913861}

[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/database/DEPS
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/background_service/DEPS
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/background_service/download_params.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/BUILD.gn
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/download_create_info.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/download_item.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/content/public/test/fake_download_item.cc
[modify] https://crrev.com/6e18e0def715b5ccf65855963273dff0ec64871e/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/872af4e5af5d5ad03689ca643642720ecbad01dc

commit 872af4e5af5d5ad03689ca643642720ecbad01dc
Author: Yi Gu <yigu@chromium.org>
Date: Fri Aug 20 18:43:29 2021

Revert "[Resubmit] Pass the credentials mode to the download service."

This reverts commit 6e18e0def715b5ccf65855963273dff0ec64871e.

Reason for revert: Tree closure: https://logs.chromium.org/logs/chromium/buildbucket/cr-buildbucket/8838358063796181409/+/u/compile/raw_io.output_failure_summary_

Original change's description:
> [Resubmit] Pass the credentials mode to the download service.
>
> The default is still 'Allow' which will not affect any existing download
> clients, however the clients will be able to customize the credentials
> mode as needed.
>
> This was already reviewed in https://chromium-review.googlesource.com/c/chromium/src/+/3100108
> but was reverted due to a dependency issue. The CL adds an extra
> dependency (diff against patchset 1 which contains the original submission)
>
> Bug: 1239709
> Change-Id: I074c7e096e326ea39d40905e65b79c781dc541ca
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110007
> Reviewed-by: Reilly Grant <reillyg@chromium.org>
> Reviewed-by: Xing Liu <xingliu@chromium.org>
> Commit-Queue: Rayan Kanso <rayankans@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#913861}

Bug: 1239709
Change-Id: I82c40b1433aafcd71bea5a16ca6197b81c355151
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110756
Commit-Queue: Yi Gu <yigu@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Yi Gu <yigu@chromium.org>
Auto-Submit: Yi Gu <yigu@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#913907}

[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/database/DEPS
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/background_service/DEPS
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/background_service/download_params.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/BUILD.gn
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/download_create_info.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/download_item.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/content/public/test/fake_download_item.cc
[modify] https://crrev.com/872af4e5af5d5ad03689ca643642720ecbad01dc/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/12da809487100d8335a6f50dd6a814cdc92daae4

commit 12da809487100d8335a6f50dd6a814cdc92daae4
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Aug 23 19:11:03 2021

[Reland] Pass the credentials mode to the download service.

The default is still 'Allow' which will not affect any existing download
clients, however the clients will be able to customize the credentials
mode as needed.

The CL was reverted in https://chromium-review.googlesource.com/c/chromium/src/+/3110756.
Compilation error: https://logs.chromium.org/logs/chromium/buildbucket/cr-buildbucket/8838358063796181409/+/u/compile/raw_io.output_failure_summary_

Please review from Patchset 1 to see extra changes

Bug: 1239709
Change-Id: I486388759928ca503bec7ef17222a1fe53cd94b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3113020
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Auto-Submit: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#914449}

[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/database/DEPS
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/background_service/DEPS
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/background_service/download_params.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/BUILD.gn
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/download_create_info.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/download_item.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/content/public/test/fake_download_item.cc
[modify] https://crrev.com/12da809487100d8335a6f50dd6a814cdc92daae4/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/32d5b602e41f0add9f31c357c19a626af4deecdf

commit 32d5b602e41f0add9f31c357c19a626af4deecdf
Author: Kristi Park <kristipark@google.com>
Date: Mon Aug 23 21:01:15 2021

Revert "[Reland] Pass the credentials mode to the download service."

This reverts commit 12da809487100d8335a6f50dd6a814cdc92daae4.

Reason for revert: Compile failure https://cr-buildbucket.appspot.com/build/8838078851703480065

Original change's description:
> [Reland] Pass the credentials mode to the download service.
>
> The default is still 'Allow' which will not affect any existing download
> clients, however the clients will be able to customize the credentials
> mode as needed.
>
> The CL was reverted in https://chromium-review.googlesource.com/c/chromium/src/+/3110756.
> Compilation error: https://logs.chromium.org/logs/chromium/buildbucket/cr-buildbucket/8838358063796181409/+/u/compile/raw_io.output_failure_summary_
>
> Please review from Patchset 1 to see extra changes
>
> Bug: 1239709
> Change-Id: I486388759928ca503bec7ef17222a1fe53cd94b4
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3113020
> Reviewed-by: Xing Liu <xingliu@chromium.org>
> Reviewed-by: Reilly Grant <reillyg@chromium.org>
> Auto-Submit: Rayan Kanso <rayankans@chromium.org>
> Commit-Queue: Reilly Grant <reillyg@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#914449}

Bug: 1239709
Change-Id: I6ef6ee7e6e94d7f269db0b0a5ffb856565f43714
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114777
Auto-Submit: Kristi Park <kristipark@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Kristi Park <kristipark@google.com>
Reviewed-by: Travis Skare <skare@chromium.org>
Owners-Override: Kristi Park <kristipark@google.com>
Cr-Commit-Position: refs/heads/main@{#914514}

[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/database/DEPS
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/background_service/DEPS
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/background_service/download_params.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/BUILD.gn
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/download_create_info.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/download_item.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/content/public/test/fake_download_item.cc
[modify] https://crrev.com/32d5b602e41f0add9f31c357c19a626af4deecdf/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ac6fd82797687ced97d2a1a720563f2eeb488764

commit ac6fd82797687ced97d2a1a720563f2eeb488764
Author: Xing Liu <xingliu@chromium.org>
Date: Thu Aug 26 17:26:27 2021

[Reland] Pass the credentials mode to the download service.

This reverts commit 32d5b602e41f0add9f31c357c19a626af4deecdf.

Diff for the reland:
Fix build file dep issue in:
chrome/browser/ui/webui/download_shelf/BUILD.gn.

Bug: 1239709
Change-Id: Idac32394ac7aede29c01a3a97fa5bf9011f1d1ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3115460
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Yuheng Huang <yuhengh@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915631}

[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/chrome/browser/ui/webui/download_shelf/BUILD.gn
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/database/DEPS
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/background_service/DEPS
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/background_service/download_params.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/BUILD.gn
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/download_create_info.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/download_item.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/content/public/test/fake_download_item.cc
[modify] https://crrev.com/ac6fd82797687ced97d2a1a720563f2eeb488764/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83debf3955b418725b97f33c39023c05af6d694f

commit 83debf3955b418725b97f33c39023c05af6d694f
Author: Rayan Kanso <rayankans@google.com>
Date: Fri Aug 27 12:37:46 2021

[BackgroundFetch] Pass credentials mode to download service & apply CORS

The credentials mode will now be passed to the DownloadService. By
default, requests will use 'same-origin' as opposed to 'include'.

CORS checks related to credentials are also applied now, to avoid
exposing response bodies/progress when applicable.

Bug: 1239709, 711354
Change-Id: I03d9e375ce0565d128d7b5596909da713f5a68df
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3100646
Auto-Submit: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915927}

[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/components/background_fetch/background_fetch_delegate_base.h
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/background_fetch_cross_origin_filter.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/background_fetch_cross_origin_filter.h
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/background_fetch_cross_origin_filter_unittest.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/background_fetch_delegate_proxy.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/background_fetch_delegate_proxy_unittest.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/mock_background_fetch_delegate.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/browser/background_fetch/mock_background_fetch_delegate.h
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/public/browser/background_fetch_delegate.h
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/web_test/browser/web_test_background_fetch_delegate.cc
[modify] https://crrev.com/83debf3955b418725b97f33c39023c05af6d694f/content/web_test/browser/web_test_background_fetch_delegate.h


### la...@gmail.com (2021-08-28)

I have opened a separate issue (https://crbug.com/chromium/1244289) for the SameSite cookie bypass as suggested by https://crbug.com/chromium/1239709#c10, since it still works after the two commits fixing this issue and not only cookies with `SameSite=Lax` are sent, but also cookies with `SameSite=Strict`.

### ra...@chromium.org (2021-08-31)

I'll mark this as fixed for now then. Can someone with permission to access crbug.com/1244289 cc me on it so I can see the details?

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

Requesting merge to other stable M93 because latest trunk commit (915927) appears to be after other stable branch point (902210).

Requesting merge to beta M94 because latest trunk commit (915927) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-31)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-09-01)

1. Does your merge fit within the Merge Decision Guidelines?
Yes

2. Links to the CLs you are requesting to merge.
- https://chromium-review.googlesource.com/c/chromium/src/+/3115460
- https://chromium-review.googlesource.com/c/chromium/src/+/3100646

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No

5. Why are these changes required in this milestone after branch?
Security issue

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2021-09-02)

amyressler@ can you review this and see if this warrants a M94 merge?

### am...@chromium.org (2021-09-02)

these are pretty substantial and textually large changes, given these CLs have been on canary for almost a week now, let's go ahead and get them into beta; merge approved for M94, please merge to branch 4606 at soonest. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/978a8d2772dbab2ae7a7ccb974da6f6d4502533e

commit 978a8d2772dbab2ae7a7ccb974da6f6d4502533e
Author: Xing Liu <xingliu@chromium.org>
Date: Mon Sep 06 15:44:27 2021

[Reland] Pass the credentials mode to the download service.

This reverts commit 32d5b602e41f0add9f31c357c19a626af4deecdf.

Diff for the reland:
Fix build file dep issue in:
chrome/browser/ui/webui/download_shelf/BUILD.gn.

(cherry picked from commit ac6fd82797687ced97d2a1a720563f2eeb488764)

Bug: 1239709
Change-Id: Idac32394ac7aede29c01a3a97fa5bf9011f1d1ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3115460
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Yuheng Huang <yuhengh@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#915631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140209
Auto-Submit: Rayan Kanso <rayankans@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Richard Knoll <knollr@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: Robert Liao <robliao@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#786}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/chrome/browser/ui/webui/download_shelf/BUILD.gn
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/database/DEPS
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/database/download_db_conversions.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/database/download_db_conversions_unittest.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/database/in_progress/in_progress_info.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/database/in_progress/in_progress_info.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/database/proto/download_entry.proto
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/background_service/BUILD.gn
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/background_service/proto/request.proto
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/background_service/proto_conversions.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/background_service/proto_conversions_unittest.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/background_service/BUILD.gn
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/background_service/DEPS
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/background_service/download_params.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/BUILD.gn
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/download_create_info.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/download_item.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/content/public/test/fake_download_item.cc
[modify] https://crrev.com/978a8d2772dbab2ae7a7ccb974da6f6d4502533e/content/public/test/fake_download_item.h


### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b835de9c65493eed076b88dad896e603386d1988

commit b835de9c65493eed076b88dad896e603386d1988
Author: Rayan Kanso <rayankans@google.com>
Date: Tue Sep 07 20:34:32 2021

[BackgroundFetch] Pass credentials mode to download service & apply CORS

The credentials mode will now be passed to the DownloadService. By
default, requests will use 'same-origin' as opposed to 'include'.

CORS checks related to credentials are also applied now, to avoid
exposing response bodies/progress when applicable.

(cherry picked from commit 83debf3955b418725b97f33c39023c05af6d694f)

Bug: 1239709, 711354
Change-Id: I03d9e375ce0565d128d7b5596909da713f5a68df
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3100646
Auto-Submit: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#915927}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3141447
Cr-Commit-Position: refs/branch-heads/4606@{#836}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/components/background_fetch/background_fetch_delegate_base.h
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/background_fetch_cross_origin_filter.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/background_fetch_cross_origin_filter.h
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/background_fetch_cross_origin_filter_unittest.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/background_fetch_delegate_proxy.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/background_fetch_delegate_proxy_unittest.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/mock_background_fetch_delegate.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/browser/background_fetch/mock_background_fetch_delegate.h
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/public/browser/background_fetch_delegate.h
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/web_test/browser/web_test_background_fetch_delegate.cc
[modify] https://crrev.com/b835de9c65493eed076b88dad896e603386d1988/content/web_test/browser/web_test_background_fetch_delegate.h


### am...@chromium.org (2021-09-08)

even though this fixes a fairly consequential issue, I'm going to suggest we not merge this to M93 for inclusion in next week's stable refresh next. Since this is a non-trivial and rather large set of changes, and even weighing comments #8-11 and 13-14, this seems like a rather large set of fixes to include in a security refresh. 

M94 Stable channel release is currently planned for 21 September. Given that it's <2 weeks away, this seems reasonable to me. 
Please let me know if there are any issues are concerns that I may not be taking into consideration. 

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations, Maurice! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for this report and nice work! 

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-20)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), govind (iOS), geohsu (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1239709?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1237899]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056879)*
