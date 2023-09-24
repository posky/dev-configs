$OriginPath = Join-Path -Path "$HOME" -ChildPath "AppData/Roaming/Code/User/keybindings.json"
$DestinationPath = Split-Path $MyInvocation.MyCommand.Path -Parent
Copy-Item -Path $OriginPath -Destination $DestinationPath