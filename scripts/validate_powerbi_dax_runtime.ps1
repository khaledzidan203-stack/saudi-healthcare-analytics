$ErrorActionPreference = 'Stop'

$root = Split-Path $PSScriptRoot -Parent
$baselinePath = Join-Path $root 'outputs\validation\powerbi_dax_sql_baselines.json'
$outputPath = Join-Path $root 'outputs\validation\powerbi_dax_runtime_validation.json'

$msmdsrv = Get-Process msmdsrv | Select-Object -First 1
if (-not $msmdsrv) { throw 'No active Power BI Analysis Services process found.' }

$port = (Get-NetTCPConnection -State Listen -OwningProcess $msmdsrv.Id | Select-Object -First 1 -ExpandProperty LocalPort)
if (-not $port) { throw "No listening port found for msmdsrv process $($msmdsrv.Id)." }

$msmdPath = $msmdsrv.Path
$bin = Split-Path $msmdPath
$adomd = Get-ChildItem $bin -Filter 'Microsoft.PowerBI.AdomdClient.dll' | Select-Object -First 1
if (-not $adomd) { throw 'Microsoft.PowerBI.AdomdClient.dll was not found beside msmdsrv.' }
Add-Type -Path $adomd.FullName

$connection = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection "Data Source=localhost:$port;"
$connection.Open()

function Invoke-AdomdRows([string]$query) {
    $command = $connection.CreateCommand()
    $command.CommandText = $query
    $reader = $command.ExecuteReader()
    $rows = @()
    while ($reader.Read()) {
        $row = [ordered]@{}
        for ($i = 0; $i -lt $reader.FieldCount; $i++) {
            $value = $reader.GetValue($i)
            if ($value -is [DBNull]) { $value = $null }
            $row[$reader.GetName($i)] = $value
        }
        $rows += [pscustomobject]$row
    }
    $reader.Close()
    $reader.Dispose()
    return $rows
}

function Convert-Number($value) {
    if ($null -eq $value) { return $null }
    return [double]$value
}

function Get-RowField($row, [string]$name) {
    $property = $row.PSObject.Properties | Where-Object Name -eq $name | Select-Object -First 1
    if ($property) { return $property.Value }
    return $null
}

$baseline = Get-Content $baselinePath -Raw | ConvertFrom-Json
$measureNames = @(
    'Hospitals',
    'Beds',
    'Beds per 10,000 Population',
    'Workforce Count',
    'Saudi Workforce Share',
    'Encounters',
    'Encounters per Person',
    'Admissions',
    'Admissions per 100 Persons',
    'Red Crescent Cases',
    'Cases per Center',
    'Cases per Ambulance'
)

$results = @()
$runtimeFailures = @()
foreach ($measure in $measureNames) {
    try {
        $query = 'EVALUATE SUMMARIZECOLUMNS(''analytics DimYear''[YearValue], "Value", [' + $measure + ']) ORDER BY ''analytics DimYear''[YearValue]'
        $rows = Invoke-AdomdRows $query
        $expected = @($baseline.results | Where-Object { $_.kpi -eq $measure -or $_.kpi -like "* $measure" })
        if ($expected.Count -ne 1) { throw "SQL baseline not found for $measure" }
        $expectedRows = @($expected[0].sql_baseline)
        $comparisons = @()
        foreach ($expectedRow in $expectedRows) {
            $year = [int]$expectedRow.Year
            $daxRow = @($rows | Where-Object { [int](Get-RowField $_ 'analytics DimYear[YearValue]') -eq $year })
            if ($daxRow.Count -ne 1) {
                $comparisons += [pscustomobject][ordered]@{ Year = $year; SQL = [double]$expectedRow.Value; DAX = $null; Difference = $null; Status = 'FAIL' }
                continue
            }
            $sqlValue = [double]$expectedRow.Value
            $daxValue = Convert-Number (Get-RowField $daxRow[0] '[Value]')
            $difference = if ($null -eq $daxValue) { $null } else { $daxValue - $sqlValue }
            # SQL baselines are persisted to six decimal places; allow the corresponding
            # absolute rounding envelope while retaining a small relative tolerance.
            $tolerance = 1e-6 + (1e-9 * [Math]::Abs($sqlValue))
            $passed = $null -ne $daxValue -and [Math]::Abs($difference) -le $tolerance
            $comparisons += [pscustomobject][ordered]@{ Year = $year; SQL = $sqlValue; DAX = $daxValue; Difference = $difference; Status = if ($passed) { 'PASS' } else { 'FAIL' } }
        }
        $failed = @($comparisons | Where-Object Status -eq 'FAIL')
        if ($failed.Count -gt 0) { $runtimeFailures += $measure }
        $results += [pscustomobject][ordered]@{ Measure = $measure; Context = 'Year = 2021, 2022, 2023, 2024; all other filters unselected'; Comparisons = $comparisons; Status = if ($failed.Count -eq 0) { 'PASS' } else { 'FAIL' } }
    } catch {
        $runtimeFailures += $measure
        $results += [pscustomobject][ordered]@{ Measure = $measure; Context = 'Annual baseline context'; Comparisons = @(); Status = 'FAIL'; Error = $_.Exception.Message }
    }
}

$regressionRows = Invoke-AdomdRows @"
EVALUATE ROW(
    "Value",
    CALCULATE(
        SUM('analytics FactWorkforceNationality'[WorkforceCount]),
        'analytics DimYear'[YearValue] = 2021,
        'analytics FactWorkforceNationality'[Scope] = "MOH Total",
        'analytics DimWorkforceType'[WorkforceTypeName] = "Pharmacists",
        'analytics DimNationality'[NationalityName] = "Non-Saudi"
    )
)
"@
$regressionValue = Convert-Number (Get-RowField $regressionRows[0] '[Value]')
$regressionPass = $regressionValue -eq 131
if (-not $regressionPass) { $runtimeFailures += 'Known regression' }

$tables = @(Invoke-AdomdRows 'SELECT * FROM $SYSTEM.TMSCHEMA_TABLES')
$relationships = @(Invoke-AdomdRows 'SELECT * FROM $SYSTEM.TMSCHEMA_RELATIONSHIPS')
$measures = @(Invoke-AdomdRows 'SELECT * FROM $SYSTEM.TMSCHEMA_MEASURES')
$measuresTable = @($tables | Where-Object Name -eq '_Measures')
$measureTableId = if ($measuresTable.Count -eq 1) { [int]$measuresTable[0].ID } else { -1 }
$measureRelationships = @($relationships | Where-Object { [int]$_.FromTableID -eq $measureTableId -or [int]$_.ToTableID -eq $measureTableId })
$manyToMany = @($relationships | Where-Object { [int]$_.FromCardinality -eq 1 -and [int]$_.ToCardinality -eq 1 })
$bidirectional = @($relationships | Where-Object { [int]$_.CrossFilteringBehavior -eq 2 })
$inactive = @($relationships | Where-Object { $_.IsActive -ne $true })

$pagesPath = Join-Path $root 'powerbi\SaudiHealthcareAnalytics.Report\definition\pages\pages.json'
$pages = (Get-Content $pagesPath -Raw | ConvertFrom-Json).pageOrder
$visuals = @(Get-ChildItem (Join-Path $root 'powerbi\SaudiHealthcareAnalytics.Report\definition\pages') -Recurse -Filter visual.json -ErrorAction SilentlyContinue)

$metadataPass = $tables.Count -eq 10 -and $relationships.Count -eq 14 -and $measureTableId -ge 0 -and $measureRelationships.Count -eq 0 -and $manyToMany.Count -eq 0 -and $bidirectional.Count -eq 0 -and $inactive.Count -eq 0 -and $pages.Count -eq 1 -and $visuals.Count -eq 0 -and $measures.Count -eq 12
$overallPass = $runtimeFailures.Count -eq 0 -and $metadataPass

$output = [ordered]@{
    Status = if ($overallPass) { 'PASS' } else { 'FAIL' }
    Server = 'localhost'
    Port = [int]$port
    Database = $connection.Database
    MeasuresExecuted = $results.Count
    Results = $results
    KnownRegression = [ordered]@{ Context = '2021 / MOH Total / Pharmacists / Non-Saudi'; SQL = 131; DAX = $regressionValue; Difference = $regressionValue - 131; Status = if ($regressionPass) { 'PASS' } else { 'FAIL' } }
    Metadata = [ordered]@{ Tables = $tables.Count; Measures = $measures.Count; MeasuresTableRelationships = $measureRelationships.Count; Relationships = $relationships.Count; ManyToMany = $manyToMany.Count; Bidirectional = $bidirectional.Count; Inactive = $inactive.Count; Pages = $pages.Count; Visuals = $visuals.Count; Status = if ($metadataPass) { 'PASS' } else { 'FAIL' } }
    RuntimeFailures = $runtimeFailures
}
$output | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $outputPath -Encoding utf8
$connection.Close()

Write-Output "RUNTIME DAX VALIDATION: $($output.Status)"
Write-Output "Endpoint: localhost:$port"
Write-Output "Measures: $($results.Count)/12"
Write-Output "Regression: $regressionValue"
Write-Output "Relationships: $($relationships.Count); M:M=$($manyToMany.Count); bidirectional=$($bidirectional.Count); inactive=$($inactive.Count)"
if (-not $overallPass) { exit 1 }
