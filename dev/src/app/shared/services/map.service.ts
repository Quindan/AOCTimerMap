import { Injectable, signal } from '@angular/core';
import { CustomMarker } from '../interface/marker.interface';
import { RESOURCE_CATEGORIES } from '../../map/enums/ressources';
import { getUnixTime } from 'date-fns';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  map!: L.Map;  
  markers: L.Marker[] = [];
  customMarkers: CustomMarker[] = [];
  selectedResources: string[] = [];
  selectedRarities: string[] = [];
  selectedRespawnIn: number = 0;

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

  showFilteredMap() {
    const now = getUnixTime(new Date());
    const filteredMarkers = this.markers.filter((marker) => {
      const customData = (marker as any).customData;
  
      // Si aucune ressource ou rareté n'est sélectionnée, ignorer ce filtre
      const matchesResource =
        this.selectedResources.length === 0 || this.selectedResources.includes(customData.type);
      const matchesRarity =
        this.selectedRarities.length === 0 || this.selectedRarities.includes(customData.rarity);

      const respawnIn = customData.alarmAfter - now;
      const isRespawnInRange = respawnIn > 0 && respawnIn < (this.selectedRespawnIn * 60);
      const matchesRespawnIn =   
        this.selectedRespawnIn === 0 || isRespawnInRange; 

      return customData && matchesResource && matchesRarity && matchesRespawnIn;
    });

    // Ajouter les markers filtrés à la carte
    filteredMarkers.forEach((marker) => marker.addTo(this.map));
          
    // Retirer les markers non filtrés de la carte
    this.markers
      .filter((marker) => !filteredMarkers.includes(marker))
      .forEach((marker) => this.map.removeLayer(marker));
    
  }
}
