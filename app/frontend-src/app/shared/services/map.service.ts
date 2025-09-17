import { Injectable, signal } from '@angular/core';
import { CustomMarker } from '../interface/marker.interface';
import { RESOURCE_CATEGORIES } from '../../map/enums/ressources';
import { getUnixTime } from 'date-fns';
import * as L from 'leaflet';

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
  showNamedMobs: boolean = false;
  namedMobMarkers: L.Marker[] = [];

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
    // Only clear regular markers, not named mob markers
    this.markers.forEach(marker => {
      if (!(marker as any).isNamedMob && !(marker as any).isFromAPI) {
        this.map.removeLayer(marker);
      }
    }); 
    this.markers = this.markers.filter(marker => 
      (marker as any).isNamedMob || (marker as any).isFromAPI
    );     
  }

  removeMarkerLocaly(marker: L.Marker): void {
    // Prevent deletion of named mob markers
    if ((marker as any).isNamedMob || (marker as any).isFromAPI) {
      console.log('Cannot delete named mob markers - they are read-only');
      return;
    }

    // Supprimer le marqueur de la carte
    this.map.removeLayer(marker);

    // Retirer le marqueur du tableau
    this.markers = this.markers.filter(m => m !== marker);
    this.customMarkers = this.customMarkers.filter(cm => cm.id !== marker.customData?.id);
  }

  showFilteredMap() {
    const now = getUnixTime(new Date());
    const filteredMarkers = this.markers.filter((marker) => {
      const customData: CustomMarker = (marker as any).customData;
      
      // Skip named mob markers - they are handled separately
      if ((marker as any).isNamedMob || (marker as any).isFromAPI) {
        return false;
      }
  
      // Si aucune ressource ou rareté n'est sélectionnée, ignorer ce filtre
      const matchesResource =
        this.selectedResources.length === 0 || this.selectedResources.includes(customData.type);
      const matchesRarity =
        this.selectedRarities.length === 0 || this.selectedRarities.includes(customData.rarity);

      const respawnIn = customData.alarmAfter - now;
      // -3600 stand to display ressources that spawned 1h ago
      const isRespawnInRange = respawnIn > -3600 && respawnIn < (this.selectedRespawnIn * 60);
      const matchesRespawnIn =   
        this.selectedRespawnIn === 0 || isRespawnInRange; 

      return customData && matchesResource && matchesRarity && matchesRespawnIn;
    });

    // Ajouter les markers filtrés à la carte
    filteredMarkers.forEach((marker) => marker.addTo(this.map));
          
    // Retirer les markers non filtrés de la carte (but keep named mob markers)
    this.markers
      .filter((marker) => 
        !filteredMarkers.includes(marker) && 
        !(marker as any).isNamedMob && 
        !(marker as any).isFromAPI
      )
      .forEach((marker) => this.map.removeLayer(marker));

    // Handle named mob markers
    this.handleNamedMobMarkers();
  }

  handleNamedMobMarkers() {
    // Remove all named mob markers from map
    this.namedMobMarkers.forEach(marker => this.map.removeLayer(marker));
    this.namedMobMarkers = [];

    // Add named mob markers if enabled
    if (this.showNamedMobs) {
      this.loadNamedMobMarkers();
    }
  }

  loadNamedMobMarkers() {
    fetch('/named_mobs_api.php', {
      credentials: 'include'
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Named mobs API response:', data);
        if (data.success && data.data) {
          console.log(`Loading ${data.data.length} named mobs`);
          data.data.forEach((mob: any) => {
            if (mob.location_x !== null && mob.location_y !== null) {
              console.log(`Creating marker for ${mob.name} at [${mob.location_x}, ${mob.location_y}]`);
              this.createNamedMobMarker(mob);
            }
          });
          console.log(`Created ${this.namedMobMarkers.length} named mob markers`);
        } else {
          console.error('Invalid API response structure:', data);
        }
      })
      .catch(error => {
        console.error('Error loading named mobs:', error);
      });
  }

  // Coordinate transformation function - DEPRECATED
  // Now using pre-calculated map_lat/map_lng from triangulation
  private transformNamedMobCoordinates(location_x: number, location_y: number): [number, number] {
    console.warn('DEPRECATED: Using old coordinate transformation. Should use map_lat/map_lng instead.');
    
    // Fallback to old method if map coordinates not available
    // Reference point 1: Wormwig
    const ref1MapLat = -235.619140625;
    const ref1MapLng = 137.396484375;
    const ref1NamedX = -706687.07770862;
    const ref1NamedY = 520419.79012307;
    
    // Reference point 2: Ysshokk  
    const ref2MapLat = -239.0;
    const ref2MapLng = 144.375;
    const ref2NamedX = -620215.59419062;
    const ref2NamedY = 562506.7933321;
    
    // Calculate scale factors using both reference points
    const deltaLng = ref2MapLng - ref1MapLng;
    const deltaNamedX = ref2NamedX - ref1NamedX;
    const scaleX = deltaLng / deltaNamedX;
    
    const deltaLat = ref2MapLat - ref1MapLat;
    const deltaNamedY = ref2NamedY - ref1NamedY;
    const scaleY = deltaLat / deltaNamedY;
    
    // Calculate offset using reference point 1
    const offsetLng = ref1MapLng - (ref1NamedX * scaleX);
    const offsetLat = ref1MapLat - (ref1NamedY * scaleY);
    
    // Transform coordinates
    const lng = (location_x * scaleX) + offsetLng;
    const lat = (location_y * scaleY) + offsetLat;
    
    console.log(`Fallback transformation: [${location_x}, ${location_y}] -> [${lat.toFixed(5)}, ${lng.toFixed(5)}]`);
    
    return [lat, lng];
  }

  createNamedMobMarker(mob: any) {
    // Parse respawn time range (e.g., "30-45 minutes", "900 seconds", "30 minutes")
    let minRespawnMinutes = 30; // default
    let displayTimeRange = mob.respawn_time || 'Unknown';
    
    if (mob.respawn_time) {
      // Handle different formats: "30-45 minutes", "900 seconds", "30 minutes"
      const rangeMatch = mob.respawn_time.match(/(\d+)-(\d+)/);
      const singleMatch = mob.respawn_time.match(/(\d+)/);
      
      if (rangeMatch) {
        // Range format: "30-45 minutes" -> use minimum (30)
        minRespawnMinutes = parseInt(rangeMatch[1]);
        displayTimeRange = mob.respawn_time; // Show full range
      } else if (singleMatch) {
        // Single number: could be seconds or minutes
        const number = parseInt(singleMatch[1]);
        if (mob.respawn_time.includes('second')) {
          // Convert seconds to minutes
          minRespawnMinutes = Math.ceil(number / 60);
          displayTimeRange = `${minRespawnMinutes} minutes (from ${number} seconds)`;
        } else {
          // Already in minutes
          minRespawnMinutes = number;
          displayTimeRange = `${number} minutes`;
        }
      }
    }
    
    // Use pre-calculated map coordinates if available, otherwise fallback to transformation
    let lat: number, lng: number;
    
    if (mob.map_lat !== undefined && mob.map_lng !== undefined && mob.map_lat !== null && mob.map_lng !== null) {
      // Use triangulated coordinates (preferred)
      lat = mob.map_lat;
      lng = mob.map_lng;
      console.log(`Using triangulated coordinates for ${mob.name}: [${lat.toFixed(5)}, ${lng.toFixed(5)}]`);
    } else if (mob.location_x && mob.location_y) {
      // Fallback to old transformation method
      [lat, lng] = this.transformNamedMobCoordinates(mob.location_x, mob.location_y);
      console.warn(`Using fallback transformation for ${mob.name}: [${lat.toFixed(5)}, ${lng.toFixed(5)}]`);
    } else {
      console.error(`No coordinates available for ${mob.name}`);
      return null;
    }
    
    const icon = L.divIcon({
      className: 'custom-marker named-mob-marker',
      html: `
        <div class="marker-container">
          <div class="named-mob-icon">🏆</div>
          <div class="custom-badge badge-named"></div>
        </div>
      `,
      iconSize: [48, 48],
      iconAnchor: [24, 24]
    });

    const marker = L.marker([lat, lng], { icon })
      .addTo(this.map);

    // Store mob data - mark as non-deletable named mob
    (marker as any).mobData = mob;
    (marker as any).minRespawnMinutes = minRespawnMinutes;
    (marker as any).isNamedMob = true; // Flag to prevent deletion
    (marker as any).isFromAPI = true; // Flag to indicate it's from API

    // Parse special items from new table structure
    let specialDropsHtml = '';
    if (mob.special_items && mob.special_items.length > 0) {
      specialDropsHtml = `
        <div class="special-drops">
          <h4>🎁 Special Drops:</h4>
          ${mob.special_items.map((item: any) => `
            <div class="drop-item">
              <a href="${item.item_url}" target="_blank" class="codex-tooltip-link">
                <span class="drop-name">${item.item_name}</span>
                <span class="drop-rarity ${item.item_rarity.toLowerCase()}">${item.item_rarity}</span>
              </a>
            </div>
          `).join('')}
        </div>
      `;
    }

    // Add popup with enhanced info and special drops
    marker.bindPopup(`
      <div class="named-mob-popup">
        <h3>🏆 ${mob.name}</h3>
        <div class="mob-info">
          <p><strong>Level:</strong> ${mob.level || 'Unknown'}</p>
          <p><strong>Respawn:</strong> ${displayTimeRange}</p>
          <p><strong>Timer:</strong> ${minRespawnMinutes} min (minimum)</p>
        </div>
        ${specialDropsHtml}
        <div class="mob-links">
          ${mob.codex_url ? `<p><a href="${mob.codex_url}" target="_blank" class="codex-link">📖 View in Codex</a></p>` : ''}
        </div>
        <div class="debug-info" style="font-size: 0.8em; color: #666; margin-top: 10px;">
          <details>
            <summary>Debug Info</summary>
            <p>Map Coords: [${lat.toFixed(5)}, ${lng.toFixed(5)}]</p>
            <p>Source: ${mob.coordinate_source || 'legacy'}</p>
          </details>
        </div>
      </div>
    `);

    this.namedMobMarkers.push(marker);
    return marker;
  }
}
