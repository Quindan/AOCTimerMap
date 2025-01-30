import { Injectable, signal } from '@angular/core';
import { CustomMarker } from '../interface/marker.interface';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  map!: L.Map;  
  markers: L.Marker[] = [];
  customMarkers: CustomMarker[] = [];

  saveMarkerLocaly(marker: L.Marker) {
    this.markers.push(marker);
  }

  updateMarkerById(updatedMarkerData: L.Marker) {
    let foundMarker: L.Marker = this.markers.filter((marker) => marker.customData?.id === updatedMarkerData.customData?.id)[0];

    if (foundMarker) {
      foundMarker = updatedMarkerData
    }
  }

  clearAllMarkers(): void {
    this.markers.forEach(marker => this.map.removeLayer(marker)); 
    this.markers = [];     
  }

  removeMarkerLocaly(marker: L.Marker): void {
    // Supprimer le marqueur de la carte
    this.map.removeLayer(marker);

    // Retirer le marqueur du tableau
    this.markers = this.markers.filter(m => m !== marker);
    this.customMarkers = this.customMarkers.filter(cm => cm.id !== marker.customData?.id);
  }
}
