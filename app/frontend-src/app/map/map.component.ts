import { Component, AfterViewInit, inject, effect, DestroyRef, signal } from '@angular/core';
import * as L from 'leaflet';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { MarkerFormComponent } from '../marker-form/marker-form.component';

import { DialogService } from '../shared/services/dialog.service';
import { MatDialog } from '@angular/material/dialog';
import { MapService } from '../shared/services/map.service';
import { TimersService } from '../shared/services/timers.service';

import moment from 'moment';
import { MarkersApiService } from '../shared/services/markers-api.service';
import { MapFiltersComponent } from '../map-filters/map-filters.component';
import { ActivatedRoute } from '@angular/router';
import { CustomMarker, MarkerForm } from '../shared/interface/marker.interface';
import { interval, switchMap, takeUntil, tap, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { SoundService } from '../shared/services/sound.service';
import { RessourcesService } from '../shared/services/ressources.service';
import { HelpComponent } from '../help/help.component';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  imports: [MapFiltersComponent, HelpComponent, MatIconModule, MatButtonModule, MatSnackBarModule]
})
export class MapComponent implements AfterViewInit {
  dialogService = inject(DialogService);
  #mapService = inject(MapService);
  #markerApiService = inject(MarkersApiService);
  #ressourcesService = inject(RessourcesService);
  #dialog = inject(MatDialog);
  #timersService = inject(TimersService);
  #route = inject(ActivatedRoute);
  #destroyRef = inject(DestroyRef);
  #soundService = inject(SoundService);
  #snackBar = inject(MatSnackBar);

  private offlineNotified = false;
 
 
  constructor() {
    const data = this.#route.snapshot.data['markerList'];
    this.#mapService.customMarkers = data || [];
  }

  ngAfterViewInit(): void {
    this.initMap();
    this.mapClickEvent();    
  }

  private initMap(): void {
    const tileSize = 512; 
    const minZoom = 4;
    const maxZoom = 9;

    this.#mapService.map = L.map('map', {
      center: [-240, 128], 
      zoom: minZoom, 
      minZoom: minZoom,
      maxZoom: maxZoom,
      crs: L.CRS.Simple  
    });

    // Ajouter les tuiles
    const tiles = L.tileLayer('https://cdn.ashescodex.com/map/20250826/{z}/{x}/{y}.webp', {
      tileSize: tileSize,
      minZoom: minZoom,
      maxZoom: maxZoom,
      noWrap: true, 
    }).on('tileerror', (e) => {
      console.warn('Tuile manquante : ', e.tile.src);
    });

    // Ajoute la couche de tuiles à la carte
    tiles.addTo(this.#mapService.map);

    this.moveZoomControlToRight();

    this.#mapService.map.whenReady(() => {
      this.#mapService.map.invalidateSize();

      this.initAllMarkers();   

      // Refresh map with markers styles updated
      this.refreshMap();   
      this.updateMarkersGatherAlert();
      interval(120000).pipe( // 2 minutes instead of 5 seconds
        switchMap(() => this.refreshMap()),
        tap(() => {
          this.updateMarkersGatherAlert();
          // Update map if filters are selected
          this.#mapService.showFilteredMap();
        }),
        takeUntilDestroyed(this.#destroyRef)
      ).subscribe();
    });
  }

  refreshMap() {
    return this.#markerApiService.getMarkers().pipe(
      tap(markers => {
        this.refreshMarkersList(markers);
        if (this.offlineNotified) {
          this.offlineNotified = false;
        }
      }), // Met à jour la liste des markers
      // En cas d'erreur, éviter d'interrompre l'intervalle et renvoyer un tableau vide
      catchError((err) => {
        console.warn('Refresh markers échoué, fallback []', err);
        if (!this.offlineNotified) {
          this.#snackBar.open('API indisponible. Mode hors-ligne actif.', 'OK', { duration: 5000 });
          this.offlineNotified = true;
        }
        return of([]);
      }),
      takeUntilDestroyed(this.#destroyRef) // Stoppe l'intervalle quand le composant est détruit
    )
  }

  moveZoomControlToRight(): void {
    setTimeout(() => {
      const zoomControl = document.querySelector('.leaflet-control-zoom');
      if (zoomControl) {
        // Trouver le conteneur parent qui a les classes leaflet-top leaflet-left
        const parentDiv = zoomControl.parentElement;
        if (parentDiv) {
          parentDiv.classList.remove('leaflet-left');
          parentDiv.classList.add('leaflet-right');
        }
      }
    }, 100); // Attendre un peu pour que Leaflet charge les contrôles
  }

  mapClickEvent() {
    this.#mapService.map.on('click', (event: L.LeafletMouseEvent) => {
      const dialogRef = this.openMarkerDialog();
      dialogRef.afterClosed().subscribe((result: MarkerForm) => {        
        if (result) {
          const marker: CustomMarker = {
            label: result.label,
            lat: event.latlng.lat,
            lng: event.latlng.lng,
            startTime: moment().unix(),
            alarmAfter: moment().add(result.timer, 'hours').unix(),
            inGameCoord: result.coord,
            type: result.type,
            rarity: result.rarity,
            missing: false,
          }
          this.addMarker(marker, true);
        }        
      });
    });
  }

   // Ouvrir la dialog au clic sur la carte
   private openMarkerDialog(marker?: L.Marker) {
    const data = marker;
    return this.#dialog.open(MarkerFormComponent, {
      width: '400px',
      data: data, // Si vous souhaitez passer des données à la dialog
    });
  }

  private initAllMarkers() {
    this.#mapService.customMarkers.forEach((customMarker) => {
      this.addMarker(customMarker, false);
    })
  }

  private updateMarkersGatherAlert() {
    this.#mapService.markers.forEach((marker) => {
      const showGatherAlert = this.#timersService.showGatherAlert(marker);
      this.#timersService.updateProgress(marker);
      if (showGatherAlert) { 
        this.addBadge(marker);
        this.#soundService.playSound('alert');
      } else {
        this.removeBadge(marker);
      }
    })   
  }

  /**
   * Refresh les markers
   * @param markersFromDatabase 
   */
  private refreshMarkersList(markersFromDatabase: CustomMarker[]): void {
    // If local marker found check if it needs an update 
    markersFromDatabase.forEach(dbMarker => {
      const localMarkerFound = this.#mapService.markers.find((localMarker) => localMarker?.customData && dbMarker.id === localMarker?.customData.id);
      if (localMarkerFound) {
        const isUpdated = JSON.stringify(localMarkerFound.customData) !== JSON.stringify(dbMarker);
        if (isUpdated) {
          localMarkerFound.customData = { ...dbMarker };
          this.refreshMarkerInfo(localMarkerFound);
        }
      }

      // Ajout des nouveaux marqueurs existant en base mais pas en local
      const exists = this.#mapService.markers.some(
        (existingMarker) => existingMarker.customData?.id === dbMarker.id
      );
  
      if (!exists) {
        this.addMarker(dbMarker, false);
      }
      
    });

    // If local marker not found in database remove it from the map
    this.#mapService.markers.forEach((localMarker) => {
      const dbMarkerFound = markersFromDatabase.find((dbMarker) => localMarker?.customData && dbMarker.id === localMarker?.customData.id);
      //  this.addMarker(dbMarkerFound, false);
     
      if (!dbMarkerFound) {        
        this.#mapService.removeMarkerLocaly(localMarker);
      }
    });
  }
  

  private addMarker(customMarkerInfo: CustomMarker, newMarker: boolean): void {
    const icon = this.getIconType(customMarkerInfo.type, customMarkerInfo.rarity);
    const marker = L.marker(new L.LatLng(customMarkerInfo.lat, customMarkerInfo.lng), { icon: icon }).addTo(this.#mapService.map);
    (marker as any).customData = customMarkerInfo;
    
    this.#timersService.startTimer(marker, customMarkerInfo.startTime, customMarkerInfo.alarmAfter);
    this.markerClickEvent(marker);
    this.markerPopupEvent(marker);

    this.refreshMarkerInfo(marker);

    // Ajouter le marqueur à la liste local et sauvegarde en base s'il est nouveau
    this.#mapService.saveMarkerLocaly(marker);
    if (newMarker) {      
      this.#markerApiService.createMarker(customMarkerInfo).pipe(
        tap((addedMarker: any) => {
          // update marker with  
          marker.customData = addedMarker.marker;
        }),      
        takeUntilDestroyed(this.#destroyRef)
      ).subscribe();
    }      
  }

  private markerClickEvent(marker: L.Marker) {
    marker.on('click', (event: L.LeafletMouseEvent) => {
      const dialogRef = this.openMarkerDialog(marker);
      dialogRef.afterClosed().subscribe((result: MarkerForm) => {
        const updateTimer = result && result.updateTimer;
        if (result) {
          const customMarkerInfo: CustomMarker = {
            label: result.label,
            lat: event.latlng.lat,
            lng: event.latlng.lng,
            startTime: updateTimer ? moment().unix() : marker.customData!.startTime,
            alarmAfter: updateTimer
              ? moment().add(result.timer, 'hours').unix()
              : marker.customData!.alarmAfter,
            inGameCoord: result.coord,
            type: result.type,
            rarity: result.rarity,
            missing: false,
          }
          this.updateMarker(marker, customMarkerInfo);          
        }        
      });
    });    
  }

  private updateMarker(marker: L.Marker, updatedMarkerInfo: CustomMarker) {  
    const markerId = marker.customData?.id!;

    this.#markerApiService.updateMarker(markerId, updatedMarkerInfo).pipe(
      tap(() => {
        marker.customData = { ...marker.customData, ...updatedMarkerInfo }; // permet de conserver l'id dans marker.customData
        this.refreshMarkerInfo(marker);
      }),      
      takeUntilDestroyed(this.#destroyRef)
    ).subscribe();
  }

  private refreshMarkerInfo(marker: any) {
    const customMarkerInfo = marker.customData;
    this.markerBindPopup(marker, customMarkerInfo);
    const icon = this.getIconType(customMarkerInfo.type, customMarkerInfo.rarity);
    marker.setIcon(icon);
  }

  private markerBindPopup(marker: L.Marker, customMarkerInfo: CustomMarker) {
    const creationDate = moment.unix(customMarkerInfo.startTime).format('DD/MM/YYYY HH:mm:ss');
    const repopTime = moment.unix(customMarkerInfo.alarmAfter).format('DD/MM/YYYY HH:mm:ss');
    const rarity = customMarkerInfo?.rarity ? customMarkerInfo.rarity.toLowerCase() : '';
    const label = customMarkerInfo.label ? `<b>Label : ${customMarkerInfo.label}</b><br>` : '';
    const markerId = L.stamp(marker);
    marker.bindPopup(`
      <!--Lat: ${customMarkerInfo.lat.toFixed(5)}, Lng: ${customMarkerInfo.lng.toFixed(5)}<br>-->
      ${label}
      <!--<b>Coordonnées en jeu : ${customMarkerInfo.inGameCoord}</b><br>-->
      <b>Création : ${creationDate}</b><br>
      <b class="capitalize">Type : ${customMarkerInfo.type.replace('_', ' ')} </b><br>
      <b>Rarity : ${rarity} </b><br>
      <b>Repop cible : ${repopTime} </b><br>
      <b>Temps restant: <span id="timer-${markerId}">Calcul...</span></b><br>`, {
        className: `bg-${rarity}`,
      });      
  }

  // Gestion des mouse in mouse out
  private markerPopupEvent(marker: L.Marker) {
    let timerInterval: any = null;
  
    // Utilisation d'une fonction fléchée pour conserver `this`
    marker.on('mouseover', () => {
      marker.openPopup();
  
      // Mettre à jour immédiatement la popup
      this.#timersService.updateRemainingTimeInMarkerPopup(marker);
  
      // Rafraîchir toutes les secondes
      timerInterval = setInterval(() => {
        this.#timersService.updateRemainingTimeInMarkerPopup(marker);
      }, 1000);
    });
  
    // Arrêter l'intervalle au `mouseout`
    marker.on('mouseout', () => {
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
      marker.closePopup();
    });
  }

  private getIconType(type: string, rarity: string) {
    // const iconUrl = RessourceImageLinks[type as keyof typeof RessourceImageLinks] || '';
    const iconUrl = this.#ressourcesService.getResourceIcon(type);
    rarity = rarity ? 'badge-'+rarity.toLowerCase() : '';
    return L.divIcon({
      className: `custom-marker custom-marker-progress`,
      html: `
        <div class="marker-container">
          <img src="${iconUrl}" alt="marker-icon" class="marker-image rounded-full" />
          <div class="custom-badge ${rarity}"></div>
          <div class="custom-badge-position"></div>
        </div>
      `,
      iconSize: [64, 64],
      iconAnchor: [32, 10]
    });
  }

  private addBadge(marker: L.Marker): void {
    const element = marker.getElement();
    if (element) {
      element.classList.add(`badge-timer-ended`);
    }
  }
  
  private removeBadge(marker: L.Marker): void {
    const element = marker.getElement();
    if (element) {
      element.classList.remove('badge-timer-ended');
    }
  }

}

