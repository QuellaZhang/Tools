param(
    [Parameter(Mandatory=$false)]
    [String]$organization ='xxx',
    [Parameter(Mandatory=$false)]
    [String]$project ='xxx'
)

# 1. Get the latest MSVC-CI-NIGHTLY run id of prpd/fe from 
$pipeline= az pipelines runs list --branch prod/fe --pipeline-ids xxx --top 1 --organization $organization --project $project | ConvertFrom-Json
$nightlyCIRunId = $pipeline.id
Write-Host "nightlyCIRunId = $nightlyCIRunId"
Write-Host "Get the latest run ID of MSVC-CI-NIGHTLY: 'xxx'."
Write-Host

# 2. Get the "Trigger Test Runs" log url.
$nightlyCIRunInfor = az pipelines runs show --id $nightlyCIRunId --organization $organization --project $project | ConvertFrom-Json
$logUrl = $nightlyCIRunInfor.logs.url
$triggerTestRunsLogUrl = $logUrl + "/685"
Write-Host "$triggerTestRunsLogUrl"

# 3. Fetch the "Trigger Test Runs" log.
$personalAccessToken = "xxx"

$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$personalAccessToken"))
$headers = @{
    Authorization = "Basic $base64AuthInfo"
}

# Send a request and get the log content
$response = Invoke-RestMethod -Uri $triggerTestRunsLogUrl -Headers $headers -Method Get

# Save log content to a file
$logFilePath = "pipeline_log.html"
$response | Out-File -FilePath $logFilePath -Encoding UTF8
Write-Host "Logs have been saved in $logFilePath"
Write-Host

# 4. Filter run links(except RWC related)
$file = "pipeline_log.html"
$lines = Get-Content -Path $file
$lines = $lines | Where-Object { ($_ -match "Queued new Build for definition") -and ($_ -notmatch "rwc") }

$succeeded = 0
$failed = 0

foreach ($line in $lines) {
    if ($line -match "Queued new Build for definition (\S+): (https://devdiv.visualstudio.com/.+?buildId=(\d+))") {
        # Extract PipelineName and RunId
        $pipelineName = $matches[1]
        $runLink = $matches[2]
        $runId = $matches[3]

        $jsonContent = az pipelines runs show --id $runId --organization $organization --project $project | ConvertFrom-Json
        $runResults = $jsonContent.result

        Write-Host "PipelineName = $pipelineName"
        Write-Host "RunLink = $runLink"
        Write-Host "RunId = $runId"

        if ($runResults -eq 'succeeded')
        {
            $succeeded += 1
            Write-Host "runResults = $runResults"
        }
        else
        {
            $failed += 1
            Write-Host "runResults = $runResults" -ForegroundColor Red
        }

        Write-Host ""
    }
}

Write-Host "succeeded = $succeeded"
if ($failed -eq 0)
{
    Write-Host "failed = $failed"
}
else
{
    Write-Host "failed = $failed" -ForegroundColor Red
}