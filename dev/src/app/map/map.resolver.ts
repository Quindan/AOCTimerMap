import { inject, Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { Observable, of, tap } from 'rxjs';
import { MarkersApiService } from '../shared/services/markers-api.service';
import { MapService } from '../shared/services/map.service';

@Injectable({
  providedIn: 'root', // Resolver fourni à l'échelle de l'application
})
export class MapResolver implements Resolve<any> {
  #markersApiService = inject(MarkersApiService);
  #mapService = inject(MapService)   
  resolve(): Observable<any> {
    // Simule une récupération de données (remplacez par votre logique réelle)    
    return this.#markersApiService.getMarkers();
  }
}
