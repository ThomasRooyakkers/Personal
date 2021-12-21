Param(
    # Parameter help description
    [Parameter(Mandatory= $true)]
    [string] $CSVFile,
    # Parameter help description
    [Parameter(Mandatory= $false)]
    [String] $OUTPath = ''
)


$webadres = Import-Csv $CSVFile -Delimiter ';'

$aantalpings = 0
$aantalipv6 = 0
Foreach ($website in  $webadres){
    $aantalpings +=1
    if ((Resolve-DnsName -name $website.Hostname).IP6Address -gt 0) {
        $aantalipv6 +=1
    }
}


if ($OUTPath -eq '') {
    write-host "Of the " $aantalpings " websites, there where " $aantalipv6 " websites with an IPv6 address."
    write-host
    write-host "Hostname".padright(20, " ") "IPv4".padright(95," ") "IPv6".padright(100," ")
    write-host "--------".padright(20, " ") "----".padright(95," ") "----".padright(100," ")
}
else{
    "`"Hostname`";`"IPv4`";`"IPv6`"" | Add-content $OUTPath                                    #Out-File -Encoding Ascii -append $OUTPath
}



foreach ($website in $webadres){
    $ip4 = (Resolve-DnsName -name $website.Hostname).IP4Address -join ", "
    $ip6 = (Resolve-DnsName -name $website.Hostname).IP6Address -Join ", "
    $websitename = $website.Hostname
    if ($OUTPath -eq '') {
        Write-Host $websitename.padRight(20,' ')  ($ip4).padright(95," ") ($ip6).padright(100," ")
    }
    else {
        "`"$websitename`";`"$ip4`";`"$ip6`""| Add-content $OUTPath                    #Out-File -Encoding Ascii -append $OUTPath
    }
}