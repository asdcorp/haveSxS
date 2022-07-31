function Get-DataHash {
    param (
        [String]$Data
    )

    $dataLower = $Data.ToLower()

    $hashes = @(0, 0, 0, 0)
    for($i = 0; $i+1 -le $Data.Length; $i++) {
        $h = $i % 4
        $char = $dataLower[$i]

        $hashes[$h] = [bigint]::Multiply($hashes[$h], 65599)
        $hashes[$h] = [bigint]::Add($hashes[$h], [byte][char]$char)
        $hashes[$h] = [bigint]::Remainder($hashes[$h], 4294967296)
    }

    $hashed = [bigint]::Multiply($hashes[0], 2087354105127)
    $hashed = [bigint]::Add($hashed, [bigint]::Multiply($hashes[1], 18446743919090729041))
    $hashed = [bigint]::Add($hashed, [bigint]::Multiply($hashes[2], 8589934583))
    $hashed = [bigint]::Add($hashed, $hashes[3])

    return [uint64]([bigint]::Remainder($hashed, 18446744073709551616))
}

function Get-PseudoKey {
    param (
        [HashTable]$Package,
        [Boolean]$Winners
    )

    $order = @(
        'name',
        'culture',
        'type',
        'version',
        'publicKeyToken',
        'processorArchitecture',
        'versionScope'
    )

    $data = @()
    foreach($x in $order) {
        if(-Not ($x -in $Package.Keys)) {
            continue
        }

        $data += ,@($x, $Package[$x])
    }

    $key = 0
    foreach($x in $data) {
        if(($true -eq $Winners) -and ($x[0] -eq 'version')) {
            continue
        }

        if($x[1] -eq 'none') {
            continue
        }

        $hashAttr = Get-DataHash -Data $x[0]
        $hashVal = Get-DataHash -Data $x[1]

        $bothHashes = [bigint]::Add([bigint]::Multiply($hashAttr, 8589934583), $hashVal)
        $key = [bigint]::Add([bigint]::Multiply($key, 8589934583), $bothHashes)
    }

    return '{0:x16}' -f [uint64]([bigint]::Remainder($key, 18446744073709551616))
}

function Get-SxsPackageName {
    param (
        [HashTable]$Package,
        [Boolean]$Winners
    )

    $pseudoKey = Get-PseudoKey -Package $Package -Winners $Winners
    $sxsName = @()

    $name = ($Package['name'] -replace '[^A-z0-9\-\._]', '')
    $culture = $Package['culture']

    if($name.Length -gt 40) {
        $name = ($name[0..18] -join '') + '..' + ($name[-19..-1] -join '')
    }

    if($culture.Length -gt 8) {
        $culture = ($culture[0..2] -join '') + '..' + ($culture[-3..-1] -join '')
    }

    $sxsName += $Package['processorArchitecture']
    $sxsName += $name
    $sxsName += $Package['publicKeyToken']

    if($false -eq $Winners) {
        $sxsName += $Package['version']
    }

    $sxsName += $culture
    $sxsName += $pseudoKey

    return ($sxsName -join '_').ToLower()
}
