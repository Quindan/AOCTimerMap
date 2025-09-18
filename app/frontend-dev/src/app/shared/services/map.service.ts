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

  // Coordinate transformation function
  // Calibrated using Wormwig and Ysshokk reference points for better accuracy
  private transformNamedMobCoordinates(location_x: number, location_y: number): [number, number] {
    // Reference point 1: Wormwig
    // Map coords: lat=-226.875, lng=133.9375
    // Named mob coords: location_x=-706687.07770862, location_y=520419.79012307
    
    // Reference point 2: Ysshokk
    // Map coords: lat=-238.3125, lng=154.125
    // Named mob coords: location_x=-620215.59419062, location_y=562506.7933321
    
    // Calculate transformation using both reference points for better accuracy
    const ref1MapLat = -226.875;
    const ref1MapLng = 133.9375;
    const ref1NamedX = -706687.07770862;
    const ref1NamedY = 520419.79012307;
    
    const ref2MapLat = -238.3125;
    const ref2MapLng = 154.125;
    const ref2NamedX = -620215.59419062;
    const ref2NamedY = 562506.7933321;
    
    // Calculate scale factors using both reference points
    // X to Lng transformation
    const deltaLng = ref2MapLng - ref1MapLng;
    const deltaNamedX = ref2NamedX - ref1NamedX;
    const scaleX = deltaLng / deltaNamedX;
    
    // Y to Lat transformation
    const deltaLat = ref2MapLat - ref1MapLat;
    const deltaNamedY = ref2NamedY - ref1NamedY;
    const scaleY = deltaLat / deltaNamedY;
    
    // Calculate offset using reference point 1
    const offsetLng = ref1MapLng - (ref1NamedX * scaleX);
    const offsetLat = ref1MapLat - (ref1NamedY * scaleY);
    
    // Transform coordinates using the calculated scale and offset
    const lng = (location_x * scaleX) + offsetLng;
    const lat = (location_y * scaleY) + offsetLat;
    
    console.log(`Transforming coordinates: [${location_x}, ${location_y}] -> [${lat.toFixed(5)}, ${lng.toFixed(5)}]`);
    
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
    
    // Determine marker color based on special drop category
    let markerClass = 'named-mob-marker';
    let markerColor = '#FFD700'; // Default gold
    
    switch (mob.special_drop_category) {
      case 'initiate':
        markerClass += ' marker-initiate';
        markerColor = '#10B981'; // Green (Uncommon)
        break;
      case 'adept':
        markerClass += ' marker-adept';
        markerColor = '#3B82F6'; // Blue (Rare)
        break;
      case 'radiant':
        markerClass += ' marker-radiant';
        markerColor = '#FCD34D'; // Yellow (Epic)
        break;
      case 'noSpecialDrop':
        markerClass += ' marker-no-drops';
        markerColor = '#9CA3AF'; // Grey (No drops)
        break;
      default:
        markerClass += ' marker-default';
        break;
    }

    // Calculate timer progress for visual overlay
    const timerInfo = this.calculateTimerProgress(mob);
    const shadowPath = this.generateShadowPath(timerInfo.progressPercent);
    const minutesLeft = timerInfo.minutesLeft;
    
    // Get first item for marker display (weapon priority)
    let markerItemIcon = '';
    if (mob.special_items && mob.special_items.length > 0) {
      const weaponItem = mob.special_items.find((item: any) => item.item_type === 'Weapon') || mob.special_items[0];
      const safeItemName = weaponItem.item_name.toLowerCase().replace(/[^a-zA-Z0-9_-]/g, '_');
      const iconPath = `/assets/icons/items/${safeItemName}.webp`;
      markerItemIcon = `<img src="${iconPath}" alt="${weaponItem.item_name}" style="position: absolute; top: 6px; left: 6px; width: 36px; height: 36px; opacity: 0.8; z-index: 3; border-radius: 50%;" onerror="this.style.display='none'">`;
    }

    const icon = L.divIcon({
      className: `custom-marker ${markerClass}`,
      html: `
        <div style="position: relative; width: 48px; height: 48px;">
          <!-- Timer shadow overlay -->
          <svg width="48" height="48" viewBox="0 0 48 48" style="position: absolute; top: 0; left: 0; z-index: 1;">
            <circle cx="24" cy="24" r="22" fill="${markerColor}" stroke="white" stroke-width="2"/>
            ${timerInfo.isActive && shadowPath ? `<path d="${shadowPath}" fill="rgba(0,0,0,0.8)" stroke="none"/>` : ''}
          </svg>
          <!-- Item icon overlay -->
          ${markerItemIcon}
          <!-- Timer text at 3 o'clock -->
          ${minutesLeft > 0 ? `<div style="position: absolute; top: 50%; right: -12px; transform: translateY(-50%); background: rgba(0,0,0,0.9); color: white; font-size: 14px; font-weight: bold; padding: 3px 6px; border-radius: 3px; z-index: 999; border: 1px solid white;">${minutesLeft}</div>` : ''}
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
          <h4>Special Drops:</h4>
          ${mob.special_items.map((item: any) => {
            const safeItemName = item.item_name.toLowerCase().replace(/[^a-zA-Z0-9_-]/g, '_');
            const iconPath = `/assets/icons/items/${safeItemName}.webp`;
            return `
            <div class="drop-item">
              <img src="${iconPath}" alt="${item.item_name}" style="width: 24px; height: 24px; margin-right: 8px; vertical-align: middle;" onerror="this.style.display='none'">
              <a href="${item.item_url}" target="_blank" class="codex-tooltip-link">
                <span class="drop-name">${item.item_name}</span>
                ${item.drop_chance ? `<span class="drop-chance">${item.drop_chance}</span>` : ''}
              </a>
            </div>
          `;
          }).join('')}
        </div>
      `;
    }

        // Add popup with enhanced info, special drops, and timer controls
        const timerStatus = timerInfo.isActive ? 
          `Timer active: ${minutesLeft} minutes left` : 
          'Timer not active';
          
      marker.bindPopup(`
        <div class="named-mob-popup">
          <h3>${mob.name} <span style="color: #666; font-size: 0.8em;">(Level ${mob.level || 'Unknown'})</span></h3>
            <div class="mob-info">
              <p><strong>Level:</strong> ${mob.level || 'Unknown'}</p>
              <p><strong>Respawn Time:</strong> ${displayTimeRange}</p>
              <p><strong>Respawn Timer:</strong> ${minRespawnMinutes} minutes</p>
              <p><strong>Timer Status:</strong> ${timerStatus}</p>
              <p><strong>Last Spawn:</strong> ${mob.last_killed_time ? new Date(mob.last_killed_time * 1000).toLocaleString() : 'Never recorded'}</p>
              <p><strong>Next Spawn:</strong> ${timerInfo.isActive && mob.last_killed_time ? new Date((mob.last_killed_time + minRespawnMinutes * 60) * 1000).toLocaleString() : 'Unknown'}</p>
            </div>
            <div class="timer-controls" style="margin: 10px 0; padding: 10px; background: #3a3a3a !important; border-radius: 5px;">
              <button onclick="window.resetTimer(${mob.id})" style="background: #dc3545; color: white; border: none; padding: 12px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; width: 70%; margin-bottom: 8px; font-size: 16px;">
                Reset Timer
              </button>
              <label style="display: inline-flex; align-items: center; font-size: 0.9em; color: #fff !important;">
                <input type="checkbox" id="notify-${mob.id}" ${mob.notify_when_ready ? 'checked' : ''} 
                       onchange="window.toggleNotification(${mob.id}, this.checked)" style="margin-right: 5px;">
                <span style="color: #fff !important;">🔔 Bip when ready</span>
              </label>
            </div>
            ${specialDropsHtml}
            <div class="mob-links">
              ${mob.codex_url ? `<p><a href="${mob.codex_url}" target="_blank" class="codex-link codex-tooltip-link">📖 View in Codex</a></p>` : ''}
            </div>
             <div class="mob-controls" style="display: none; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
               <label style="display: flex; align-items: center; font-size: 0.9em; color: #666;">
                 <input type="checkbox" id="hide-${mob.id}" style="margin-right: 8px;" 
                        onchange="window.hideMob(${mob.id}, this.checked)">
                 Hide this named mob from map
               </label>
             </div>
        <div class="debug-info" style="font-size: 0.8em; color: #666; margin-top: 10px;">
          <details>
            <summary>Debug Info</summary>
            <p>Original Coords: [${mob.location_x}, ${mob.location_y}]</p>
            <p>Map Coords: [${lat.toFixed(5)}, ${lng.toFixed(5)}]</p>
            <p>Source: ${mob.coordinate_source || 'legacy'}</p>
          </details>
        </div>
      </div>
    `);

    this.namedMobMarkers.push(marker);
    return marker;
  }

  private calculateTimerProgress(mob: any): {isActive: boolean, progressPercent: number, minutesLeft: number} {
    if (!mob.timer_active || !mob.last_killed_time) {
      return {isActive: false, progressPercent: 0, minutesLeft: 0};
    }

    const currentTime = Math.floor(Date.now() / 1000);
    const elapsedSeconds = currentTime - mob.last_killed_time;
    
    // Parse respawn time to get minimum timer duration
    let minTimerMinutes = 15; // Default
    if (mob.respawn_time) {
      const rangeMatch = mob.respawn_time.match(/(\d+)\s*-\s*(\d+)/);
      const singleMatch = mob.respawn_time.match(/(\d+)/);
      
      if (rangeMatch) {
        const firstNum = parseInt(rangeMatch[1]);
        // Check if it's in seconds
        if (mob.respawn_time.includes('second')) {
          minTimerMinutes = Math.ceil(firstNum / 60);
        } else {
          minTimerMinutes = firstNum; // Assume minutes
        }
      } else if (singleMatch) {
        const number = parseInt(singleMatch[1]);
        if (mob.respawn_time.includes('second')) {
          minTimerMinutes = Math.ceil(number / 60);
        } else {
          minTimerMinutes = number; // Assume minutes
        }
      }
    }
    
    const timerDurationSeconds = minTimerMinutes * 60;
    const minutesLeft = Math.max(0, Math.ceil((timerDurationSeconds - elapsedSeconds) / 60));
    
    // For timers > 1 hour, only start showing shadow when 1 hour left
    if (minTimerMinutes > 60 && minutesLeft > 60) {
      return {isActive: false, progressPercent: 0, minutesLeft: minutesLeft};
    }
    
    // Calculate progress (0 = just started, 1 = timer complete)
    const effectiveTimerMinutes = minTimerMinutes > 60 ? 60 : minTimerMinutes;
    const effectiveElapsed = Math.min(elapsedSeconds, effectiveTimerMinutes * 60);
    const progressPercent = effectiveElapsed / (effectiveTimerMinutes * 60);
    
    // Debug logging
    console.log(`Timer debug for ${mob.name}: elapsed=${elapsedSeconds}s, timer=${minTimerMinutes}min, progress=${progressPercent}, minutesLeft=${minutesLeft}, isActive=${true}`);
    
    return {
      isActive: true,
      progressPercent: Math.min(1, progressPercent),
      minutesLeft: minutesLeft
    };
  }

  private generateShadowPath(progressPercent: number): string {
    console.log(`Generating shadow path: progressPercent=${progressPercent}`);
    
    if (progressPercent <= 0) {
      console.log('No shadow: progress <= 0');
      return '';
    }
    
    if (progressPercent >= 1) {
      // Timer complete - return to normal (no shadow)
      console.log('Timer complete: returning to normal');
      return '';
    }
    
    // CORRECTED: Shadow shows ELAPSED time, starts at 12 and goes clockwise
    // When 15min left on 15min timer: 0min elapsed = no shadow
    // When 10min left on 15min timer: 5min elapsed = shadow from 12 to 2 o'clock
    // When 0min left: full shadow
    const angle = progressPercent * 360;
    const radians = (angle - 90) * (Math.PI / 180); // -90 to start at 12 o'clock
    
    const x = 24 + 22 * Math.cos(radians);
    const y = 24 + 22 * Math.sin(radians);
    
    const largeArc = angle > 180 ? 1 : 0;
    
    const path = `M 24,24 L 24,2 A 22,22 0 ${largeArc},1 ${x},${y} Z`;
    console.log(`Shadow path generated: angle=${angle}°, path=${path}`);
    return path;
  }

  refreshNamedMobMarkers(): void {
    // Clear existing named mob markers
    this.namedMobMarkers.forEach(marker => {
      this.map.removeLayer(marker);
    });
    this.namedMobMarkers = [];
    
    // Reload named mob markers
    this.loadNamedMobMarkers();
  }
}
