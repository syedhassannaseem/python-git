import win32com.client as wincl

speaker_number = 0
spk = wincl.Dispatch("SAPI.SpVoice")
vcs = spk.GetVoices()
SVSFlag = 11
print(vcs.Item (speaker_number) .GetAttribute ("Name")) # speaker name
spk.Voice
spk.SetVoice(vcs.Item(speaker_number)) # set voice (see Windows Text-to-Speech settings)
students = [
    "Abdullah","Hassan","Ahmad"
]
for lt in students:
 spk.Speak(f"shoutout to {lt}")