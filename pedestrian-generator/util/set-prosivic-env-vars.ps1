# Permanently sets environment variables needed for prosivic python DDS for all users
[CmdletBinding()]
Param ( 
    $DDSPath = "C:\prosivic\DDS_API_2020\install\Release"
)

$NewPath = $env:path + ";" + $DDSPath
$NewPythonPath = If ([string]::isNullOrEmpty($env:pythonpath)) {$DDSPath} Else {$env:pythonpath + ";" + $DDSPath}

[Environment]::SetEnvironmentVariable("PATH", $NewPath, "Machine")
[Environment]::SetEnvironmentVariable("PYTHONPATH", $NewPythonPath, "Machine")

