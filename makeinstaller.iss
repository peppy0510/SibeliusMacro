; http://www.jrsoftware.org/ishelp/index.php

[Setup]
AppName="SibeliusMacro"
AppVerName="SibeliusMacro 0.2.0"
DefaultDirName="{pf}\SibeliusMacro"
DefaultGroupName="SibeliusMacro"
AppVersion="0.2.0"
AppCopyright="Taehong Kim"
AppPublisher="Taehong Kim"
UninstallDisplayIcon="{app}\SibeliusMacro.exe"
Compression=lzma2/max
SolidCompression=yes
OutputDir="dist"
OutputBaseFilename="SibeliusMacro-0.2.0-Setup"
; VersionInfoVersion="0.2.0"
VersionInfoProductVersion="0.2.0"
VersionInfoCompany="Taehong Kim"
VersionInfoCopyright="Taehong Kim"
ArchitecturesInstallIn64BitMode="x64"

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\SibeliusMacro"; Filename: "{app}\SibeliusMacro.exe"
Name: "{commondesktop}\SibeliusMacro"; Filename: "{app}\SibeliusMacro.exe"
