[Setup]
AppId={{A8F69B62-8F1A-4A76-BD91-123456789ABC}
AppName=Baixa Musica
AppVersion=1.3.0
AppPublisher=Baixa Music
DefaultDirName={autopf}\Baixa Musica
DefaultGroupName=Baixa Musica
OutputDir=..\Release\Windows
OutputBaseFilename=BaixaMusicaSetup v(1.3.0)
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Files]
Source: "..\Project\build\windows\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Baixa Musica"; Filename: "{app}\baixa_musica.exe"
Name: "{autodesktop}\Baixa Musica"; Filename: "{app}\baixa_musica.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\baixa_musica.exe"; Description: "Executar Baixa Musica"; Flags: nowait postinstall skipifsilent