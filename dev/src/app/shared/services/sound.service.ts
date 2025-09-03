import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SoundService {

  constructor() { }

  playSound(sound: string) {
    const audio = new Audio(`assets/sounds/${sound}.mp3`);
    /*audio.play();
    audio.addEventListener('ended', () => audio.pause());*/
  }
}
