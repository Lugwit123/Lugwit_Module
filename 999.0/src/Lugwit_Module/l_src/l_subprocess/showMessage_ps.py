# coding:utf-8
import subprocess
import base64
import re
import os

def showMessageWin(text="", 
                   title=u'提示aa', 
                   fontName='Consolas', 
                   fontSize=12,
                   iconPath=r'',
                   timeout=5,
                   icon_size=(32,32)):
    if not text:
        text=u'''
程序崩溃，请联系开发人员 程序崩溃，请联系开发人员
程序崩溃，请联系开发人员sdasdsad
程序崩溃，请联系开发人员sadasdsadsa
程序崩溃，请联系开发人员dsadddddddddddddsa
程序崩溃，请联系开发人员sadasasdfffffffffff
        '''

    # 计算文本行数和宽度
    lines = text.count('\n')+1
    row_max_font_num = len(sorted(re.split('\r*\n',text),key=len)[-1])
    char_width = fontSize * 1.2 + 6
    char_height = fontSize * 1.4 + 6

    width = int(row_max_font_num * char_width) + 40
    width = 900 if width > 900 else width
    height = int(lines * char_height) + 120
    height = 900 if height > 900 else height
    text = text.replace('\n', '`n')

    ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$iconPath = '{iconPath}'
if ($iconPath -ne '') {{
    $image = New-Object System.Drawing.Icon($iconPath)
    $form.Icon = $image
}}

$form.Text = "{title}"
$form.Size = New-Object System.Drawing.Size({width},{height})
$form.StartPosition = "CenterScreen"

$richTextBox = New-Object System.Windows.Forms.RichTextBox
$richTextBox.BackColor = [System.Drawing.Color]::FromArgb(200,200,250)
$richTextBox.Text = @"
{text}
"@
$richTextBox.Font = New-Object System.Drawing.Font("{fontName}", {fontSize})
$richTextBox.Dock = "Fill"
$richTextBox.ReadOnly = $true

$okButton = New-Object System.Windows.Forms.Button
$okButton.Text = 'OK({timeout})'
$okButton.Dock = 'Bottom'
$okButton.BackColor = [System.Drawing.Color]::LightBlue
$okButton.ForeColor = [System.Drawing.Color]::DarkBlue


$extendButton = New-Object System.Windows.Forms.Button
$extendButton.Text = '延长30秒'
$extendButton.Dock = 'Bottom'
$extendButton.BackColor = [System.Drawing.Color]::LightGreen
$extendButton.ForeColor = [System.Drawing.Color]::DarkGreen


$extendButton.Add_Click({{
    # 点击“延长”按钮时将倒计时延长30秒
    $okButton.Text = "OK(30)"
}})


$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 1000

$okButton.Add_Click({{
    $form.Close()
}})

$timer.Add_Tick({{
    $seconds = [int]$okButton.Text.Substring(3, $okButton.Text.Length - 4) - 1
    $okButton.Text = "OK($seconds)"
    if ($seconds -le 0) {{
        $form.Close()
    }}
}})

$form.Controls.Add($richTextBox)
$form.Controls.Add($okButton)
$form.Controls.Add($extendButton)
$form.AcceptButton = $okButton

$form.Add_Load({{
    $timer.Start()
}})

$form.ShowDialog()
'''

    encoded_ps_script = base64.b64encode(ps_script.encode('utf-16le')).decode('ascii')
    subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded_ps_script], creationflags=0, shell=True)

if __name__ == "__main__":
    showMessageWin(timeout=10)
