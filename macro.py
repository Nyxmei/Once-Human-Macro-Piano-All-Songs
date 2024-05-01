import mido
import pyautogui
import time
import keyboard
import sys

def map_piano_note_to_key(note):
    # Define the mappings for piano keys to computer keyboard keys
    piano_G = ['ctrl', None, 'shift']
    piano_keymap = ['q', '2', 'w', '3', 'e', 'r', '5', 't', '6', 'y', '7',
                    'u', 'q', '3', 'w', '4', 'e', 'r', '5', 't', '6', 'y', '7', 'u', '=']

    if not(36 <= note <= 96):
        return '', ''

    if 36 <= note <= 59:
        change_G = piano_G[0]  # For F1 - Ctrl
        baseline = 36
    elif 60 <= note <= 83:
        change_G = None  # No special modifier for F2
        baseline = 60
    else:
        change_G = piano_G[2]  # For F3 - Shift
        baseline = 84

    key_index = note - baseline

    if change_G == 'ctrl' or change_G == 'shift':
        pass  # If Ctrl or Shift is to be turned off, do nothing
    elif change_G:
        pyautogui.keyDown(change_G)

    if 0 <= key_index < len(piano_keymap):
        key = piano_keymap[key_index]
        if key:
            pyautogui.press(key)

    if change_G and change_G != 'ctrl' and change_G != 'shift':
        pyautogui.keyUp(change_G)

    return '', ''

def play_midi(path, pitch_modulation=12):
    midi = mido.MidiFile(path)
    print("Press F5 to play. F6 to stop")
    keyboard.wait('F5')
    time.sleep(2)

    curr_pitch = 'f2'
    pyautogui.press(curr_pitch)
    pyautogui.PAUSE = 0

    for msg in midi.play():
        if msg.type == 'note_on' and msg.velocity != 0:
            pitch, key = map_piano_note_to_key(msg.note + pitch_modulation)
            if curr_pitch != pitch:
                pyautogui.press(pitch)
                curr_pitch = pitch
            if key:
                pyautogui.press(key)

        if keyboard.is_pressed('F6'):
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python macro.py 'path'")
        sys.exit(1)

    midi_path = sys.argv[1]
    play_midi(midi_path, pitch_modulation=10)
