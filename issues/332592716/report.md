# heap-use-after-free on ModelExecutionManager::ExecuteModel

| Field | Value |
|-------|-------|
| **Issue ID** | [332592716](https://issues.chromium.org/issues/332592716) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>OptimizationGuide |
| **Platforms** | Mac |
| **Chrome Version** | 123.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | so...@google.com |
| **Created** | 2024-04-03 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

Steps to reproduce problem

1. apply the patch.diff.
2. host the poc.html with `python3 -m http.server 8000`
3. run chrome with `--enable-blink-features=ModelExecutionAPI --enable-features=EnableModelExecutionAPI`
4. more you can see video

# Problem Description

RCA Analysis:
[0]. in function `CreateGenericSession`, the session will be create. and passed to ModelExecutionSession as unique\_ptr. so it lifetime may outlive the browser.

```
void ModelManagerImpl::CreateGenericSession(
    mojo::PendingReceiver<blink::mojom::ModelGenericSession> receiver,
    blink::mojom::ModelGenericSessionSamplingParamsPtr sampling_params,
    CreateGenericSessionCallback callback) {
  content::BrowserContext* browser_context = browser_context_.get();
[...]
  optimization_guide::SessionConfigParams config_params =
      optimization_guide::SessionConfigParams{.disable_server_fallback = true};
  if (sampling_params) {
    config_params.sampling_params = optimization_guide::SamplingParams{
        .top_k = sampling_params->top_k,
        .temperature = sampling_params->temperature};
  }

  std::unique_ptr<optimization_guide::OptimizationGuideModelExecutor::Session>
      session = service->StartSession( //  <---- session create
          optimization_guide::proto::ModelExecutionFeature::
              MODEL_EXECUTION_FEATURE_TEST,
          config_params);
  // TODO(leimy): after this check is done by optimization guide and we can
  // return that from `CanStartModelExecutionSession()`, we should replace this
  // block by a CHECK, and stop returning any boolean value from this method.
  if (!session) {
    std::move(callback).Run(/*success=*/false);
    return;
  }
  // The new `ModelExecutionSession` shares the same lifetime with the
  // `receiver`.
  mojo::MakeSelfOwnedReceiver(
      std::make_unique<ModelExecutionSession>(std::move(session)), // [0]. <---- ModelExecutionSession lifetime will bind to pipe, beacause there didn't oberserve lifetime of pipe. so maybe ModelExecutionSession outlive keyservice. 
      std::move(receiver));
  std::move(callback).Run(/*success=*/true);
}

```

[2]. in `StartSession`, an `execute_fn` will passed to `SessionImpl constructor` as member. it use `this` as argument.

```
std::unique_ptr<OptimizationGuideModelExecutor::Session>
ModelExecutionManager::StartSession(
    proto::ModelExecutionFeature feature,
    const std::optional<SessionConfigParams>& config_params) {
  bool disable_server_fallback =
      config_params && config_params->disable_server_fallback;
  ExecuteRemoteFn execute_fn =
      disable_server_fallback
          ? base::BindRepeating(&NoOpExecuteRemoteFn)
          : base::BindRepeating(&ModelExecutionManager::ExecuteModel,
                                base::Unretained(this)); //<---- this
  if (on_device_model_service_controller_) {
    auto session = on_device_model_service_controller_->CreateSession(
        feature, execute_fn, optimization_guide_logger_.get(),     //<-- execute_fn 
        model_quality_uploader_service_, config_params);
    if (session) {
      RecordSessionUsedRemoteExecutionHistogram(feature, /*is_remote=*/false);
      return session;
    }
  }

  if (disable_server_fallback) {
    return nullptr;
  }

  RecordSessionUsedRemoteExecutionHistogram(feature, /*is_remote=*/true);
  return std::make_unique<SessionImpl>(
      base::DoNothing(), feature, std::nullopt, nullptr, nullptr,
      /*safety_config=*/std::nullopt, std::move(execute_fn),                    //[2]<-- execute_fn 
      optimization_guide_logger_.get(), model_quality_uploader_service_,
      config_params);
}

```
```
SessionImpl::SessionImpl(
    StartSessionFn start_session_fn,
    proto::ModelExecutionFeature feature,
    std::optional<proto::OnDeviceModelVersions> on_device_model_versions,
    scoped_refptr<const OnDeviceModelFeatureAdapter> adapter,
    base::WeakPtr<OnDeviceModelServiceController> controller,
    const std::optional<proto::FeatureTextSafetyConfiguration>& safety_config,
    ExecuteRemoteFn execute_remote_fn,
    OptimizationGuideLogger* optimization_guide_logger,
    base::WeakPtr<ModelQualityLogsUploaderService>
        model_quality_uploader_service,
    const std::optional<SessionConfigParams>& config_params)
    : controller_(controller),
      feature_(feature),
      on_device_model_versions_(on_device_model_versions),
      safety_config_(safety_config),
      execute_remote_fn_(std::move(execute_remote_fn)), //[2] <-- execute_remote_fn
      optimization_guide_logger_(optimization_guide_logger),
      model_quality_uploader_service_(model_quality_uploader_service),
      sampling_params_(
    [...]

```

[3]. But ModelExecutionManager will be a member of OptimizationGuideKeyedService and its lifecycle will also be related to KeyedService.

```
void OptimizationGuideKeyedService::Initialize() {
[...]
      model_execution_manager_ =
          std::make_unique<optimization_guide::ModelExecutionManager>(
              url_loader_factory,
              IdentityManagerFactory::GetForProfile(profile),
              std::move(service_controller), this,
              optimization_guide_logger_.get(),
              model_quality_logs_uploader_service_
                  ? model_quality_logs_uploader_serv

# Summary
heap-use-after-free on ModelExecutionManager::ExecuteModel

# Additional Data
Category: Security \
Chrome Channel: Not sure \
Regression: N/A

```

## Attachments

- [poc.html](attachments/poc.html) (text/html, 211 B)
- [vedio.mov](attachments/vedio.mov) (video/quicktime, 29.8 MB)
- [asan.log](attachments/asan.log) (text/plain, 26.4 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 886 B)

## Timeline

### li...@gmail.com (2024-04-03)

[3]. But ModelExecutionManager will be a member of OptimizationGuideKeyedService and its lifecycle will also be related to KeyedService.

```
void OptimizationGuideKeyedService::Initialize() {
[...]
      model_execution_manager_ =
          std::make_unique<optimization_guide::ModelExecutionManager>(
              url_loader_factory,
              IdentityManagerFactory::GetForProfile(profile),
              std::move(service_controller), this,
              optimization_guide_logger_.get(),
              model_quality_logs_uploader_service_
                  ? model_quality_logs_uploader_service_->GetWeakPtr()
                  : nullptr);
    }
[...]

```

[4].in `ModelExecutionSession::Execute`,`ExecuteModel` will be called. finally call `execute_remote_fn_`. beacause of the pipe outlive the `KeyedService`, if we close broser, then call `execute_remote_fn_` will lead to uaf.

```
void ModelExecutionSession::Execute(
    const std::string& input,
    mojo::PendingRemote<blink::mojom::ModelStreamingResponder> responder) {
  mojo::RemoteSetElementId responder_id =
      responder_set_.Add(std::move(responder));
  optimization_guide::proto::StringValue request;
  request.set_value(input);
  session_->ExecuteModel( //<--- [4].
      request,
      base::BindRepeating(&ModelExecutionSession::ModelExecutionCallback,
                          weak_ptr_factory_.GetWeakPtr(), responder_id));
}

```
```
void SessionImpl::ExecuteModel(
    const google::protobuf::MessageLite& request_metadata,
    optimization_guide::OptimizationGuideModelExecutionResultStreamingCallback
        callback) {
 [...]

  if (!ShouldUseOnDeviceModel()) {
    DestroyOnDeviceState();
    execute_remote_fn_.Run(
        feature_, *last_message_,
        /*log_ai_data_request=*/nullptr,
        base::BindOnce(&InvokeStreamingCallbackWithRemoteResult,
                       std::move(callback)));
    return;
  }

[...]
}

```

fix suggestion

```
  ExecuteRemoteFn execute_fn =
      disable_server_fallback
          ? base::BindRepeating(&NoOpExecuteRemoteFn)
          : base::BindRepeating(&ModelExecutionManager::ExecuteModel,
-                                base::Unretained(this));
+                                weak_ptr_factory_.GetWeakPtr()); //<---- this
    

```

bitset: `https://source.chromium.org/chromium/chromium/src/+/75276294eaa004884ef986e0746cb898a279ff77`

### li...@gmail.com (2024-04-03)

Notice:
0. Patch.diff offer is just a better trigger because there are other paths to pass fn to SessionImpl

1. Although ASAN displays' MiraclePtr Status: PRODUCTED ', I believe this is related to asynchronous unretained (this), mainly when this is destroyed before the task runs. Therefore, I do not think this is MiraclePtr, so it may be considered to have higher utilization.

### es...@chromium.org (2024-04-03)

Thanks for the report!

Could you please explain further how you could trigger this without applying patch.diff?

SecurityImpact-None because it is in a disabled feature.

### es...@chromium.org (2024-04-03)

(Tentatively triaged as S1/High because we downgrade severity both for requiring browser shutdown, and for MiraclePtr protection [applicable per ASAN, but reporter claim it isn't necessarily]. We'll only want to treat this as a security bug if we think it is exploitable without applying patch.diff.)

### ap...@google.com (2024-04-05)

Project: chromium/src
Branch: main

commit b65aeaf711eceaa675c33594f47143e2af3733ee
Author: Sophie Chang <sophiechang@chromium.org>
Date:   Fri Apr 05 15:19:33 2024

    Change ExecuteRemoteFn to use weak_ptr instead of base::Unretained
    
    Bug: 332592716
    Change-Id: I6d5323913d5785d619bed56b85cdb42e2a8cd1a7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5421869
    Reviewed-by: Scott Violet <sky@chromium.org>
    Commit-Queue: Sophie Chang <sophiechang@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1283150}

M       components/optimization_guide/core/model_execution/model_execution_manager.cc
M       components/optimization_guide/core/model_execution/on_device_model_service_controller.cc
M       components/optimization_guide/core/model_execution/on_device_model_service_controller.h
M       components/optimization_guide/core/model_execution/on_device_model_service_controller_unittest.cc
M       components/optimization_guide/core/model_execution/session_impl.cc
M       components/optimization_guide/core/model_execution/session_impl.h
M       components/optimization_guide/core/optimization_guide_logger.h

https://chromium-review.googlesource.com/5421869


### li...@gmail.com (2024-04-06)

RE: #4
sorry,very busy these days beacuse of holiday. As you can see, the SessionImpl constructor must pass the execute\_fn as argument, so as long as execute\_fn is passed, the POC I provided will crash.as you said, it must close the browser. but i think it didn't wrapped by MiraclePtr. beacause the pattern of `unretained(this)`. my patch just make it easily to trigger, i found vulnablilty code exist long time. even more days. It's not easy to find it. because it hidden deeply.

### li...@gmail.com (2024-04-06)

btw, i want to know Why set p4 to match S1.

### am...@chromium.org (2024-04-09)

this bug is considered highly mitigated, but it is still considered S1, high severity; however, this issue is in a non-enabled feature which is considered P4 / security\_impact-none, since it does not impact users at this time and the SLO is only for the issue to be resolved before ModelExecutionAPI is enabled / launched

### am...@google.com (2024-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-11)

Congratulations! The Chrome VRP Panel has decided to award you $2,000 for this report of highly mitigated memory corruption + $1,000 bisect bonus. The reward amount was decided based on the mitigations of BRP protection + shutdown. In our assessment we could find nothing to suggest that MiraclePtr / BRP protection is not applicable here as it appears the crash occurred inside a callback and held by bind specifically for unretained. If you can demonstrate how BRP is not applicable here and is a fully exploitable UAF, we are happy to reassess for potentially higher reward.
Thanks for your efforts and reporting this issue to us!

### pe...@google.com (2024-07-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/332592716)*
