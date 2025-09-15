import { Injectable, signal } from '@angular/core';
import moment from 'moment';
import { CustomMarker } from '../interface/marker.interface';
import L from 'leaflet';

declare module 'leaflet' {
  interface Marker {
    customData?: CustomMarker;
  }
}

@Injectable({
  providedIn: 'root'
})
export class TimersService {

  timers = new Map<L.Marker, { alarmAfter: number }>(); // Stocker le temps restant pour chaque marqueur

  // Initialise un timer calé sur l'heure
  startTimer(marker: L.Marker, startTime: number, alarmAfter: number): void {
    /*const now = moment();
    const durationParsed = moment.duration(timer);
    const targetTime = now.clone().add(durationParsed).format('HH:mm:ss');*/ // Calcule l'heure cible

    this.timers.set(marker, { alarmAfter }); // Associe le signal au marqueur
  }

  // Arrête un timer
  /*stopTimer(marker: L.Marker): void {
    if (this.timers.has(marker)) {
      this.timers.delete(marker); // Supprime le timer
    }
  }*/

  // Récupère le signal du temps restant pour un marqueur
  /*getTargetTime(marker: L.Marker): any {
    const timer = this.timers.get(marker);
    return timer ? timer.alarmAfter : 0;
  }*/

  /**
   * Show gather alert 15 minutes before timer ends
   * @param marker 
   * @returns 
   */
  showGatherAlert(marker: L.Marker): boolean {
    const now = moment();
    const targetTime = moment.unix(marker.customData?.alarmAfter || 0);
    const targetTimeMinus15 = moment(targetTime).subtract(15, 'minutes');
    if (
      now.isAfter(targetTimeMinus15) &&
      now.isBefore(targetTime)
    ) {
      return true;
    }
    return false;
  }

  // Calculate remaining time
  updateRemainingTimeInMarkerPopup(marker: L.Marker) {
    const markerId = L.stamp(marker);
    const timerElement = document.getElementById(`timer-${markerId}`);
    if (timerElement) {
      const now = moment().unix();
      const remainingTimeStamp = marker.customData ? marker.customData.alarmAfter - now : 0;
      const remainingTime = moment.duration(remainingTimeStamp, "seconds");
      const formattedTimeLeft = remainingTimeStamp <= 0 ? `` : `${remainingTime.hours()}h${remainingTime.minutes()}m${remainingTime.seconds()}s`;
      timerElement.innerText = remainingTimeStamp > 0 ? formattedTimeLeft : "Expiré";
    }
  }

  updateProgress(marker: L.Marker) {
    const startTime = marker.customData?.startTime || 0;
    const targetTime = marker.customData?.alarmAfter || 0;
    const progression = this.calculateProgression(startTime, targetTime);
    
    marker.getElement()?.style.setProperty('--progress', progression.toString());     
  }

  private calculateProgression(startTime: number, targetTime: number): number {
    const now = moment().unix(); // Timestamp actuel en secondes
  
    if (now <= startTime) {
      return 0; // Avant le début
    }
  
    if (now >= targetTime) {
      return 1; // Après la fin
    }
  
    // Calculer la progression entre 0 et 1
    return (now - startTime) / (targetTime - startTime);
  }

  formatTimeWithMoment(seconds: any): string {    
    const duration = moment.duration(seconds, 'seconds'); // Convertit les secondes en durée
    return moment.utc(duration.asMilliseconds()).format('HH:mm:ss'); // Formate en HH:mm:ss
  };
}
