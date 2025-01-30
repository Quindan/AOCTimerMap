import { inject, Injectable } from '@angular/core';
import { Observable, of, throwError, timer } from 'rxjs';
import { catchError, delay, map, tap } from 'rxjs/operators';
import { CustomMarker } from '../interface/marker.interface';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

export type Point = { lat: number; lng: number };

@Injectable({
  providedIn: 'root',
})
export class MarkersApiService {
  #baseUrl = environment.apiUrl;

  http = inject(HttpClient);

  // Liste des markers mockée
  private markers: CustomMarker[] = [
    {
      id: 10001,
      label: 'Marker 1',
      lat: -236,
      lng: 103,
      startTime: 1738104985,
      alarmAfter: 1738105825,
      inGameCoord: 'A1',
      type: 'giant_bluebell',
      rarity: 'common',
      missing: true,
    },
    {
      id: 10002,
      label: 'Marker 2',
      lat: -230,
      lng: 131,
      startTime: 1737897805, // Exemple de timestamp UNIX
      alarmAfter: 1737904689, // 10 minutes
      inGameCoord: 'B3',
      type: 'moonbell',
      rarity: 'rare',
      missing: false,
    },
    {
      id: 10003,
      label: 'Marker 3',
      lat: -230,
      lng: 153,
      startTime: 1738068205, // Exemple de timestamp UNIX
      alarmAfter: 1738070905, // 20 minutes
      inGameCoord: 'C7',
      type: 'giant_bluebell',
      rarity: 'epic',
      missing: false,
    },
  ];

  constructor() {}

  /**
   * Récupère la liste des markers avec un délai simulé
   * @returns Un observable émettant un tableau de markers
   */
  getMarkers(): Observable<CustomMarker[]> {
    return this.http.get<CustomMarker[]>(`${this.#baseUrl}`).pipe(
      catchError((error) => {
        console.error('API Error:', error);
        return throwError(() => new Error('An error occurred while creating the marker.'));
      })
    );
  }

  /**
   * Create a new marker
   * @param marker The marker data to create
   */
  createMarker(marker: CustomMarker): Observable<{ success: boolean; marker: CustomMarker }> {
    return this.http.post<{ success: boolean; marker: CustomMarker }>(
      `${this.#baseUrl}?action=create`,
      marker
    ).pipe(
      tap((success) => {
        console.log(success)
      }),
      catchError((error) => {
        console.log(error);
        return throwError(() => new Error('An error occurred while creating the marker.'))
      }
    ));
  }

  /**
   * Update an existing marker
   * @param id The ID of the marker to update
   * @param updatedData The updated marker data
   */
  updateMarker(id: number, updatedData: Partial<CustomMarker>): Observable<{ success: boolean }> {
    const payload = { ...updatedData, id };
    return this.http.post<{ success: boolean }>(
      `${this.#baseUrl}?action=update`,
      payload
    ).pipe(
      catchError((error) => {
        console.log(error);
        return throwError(() => new Error('An error occurred while updating the marker.'))
      })
    );
  }

  /**
   * Delete a marker by ID
   * @param id The ID of the marker to delete
   */
  deleteMarker(id: number): Observable<{ success: boolean }> {
    return this.http.post<{ success: boolean }>(
      `${this.#baseUrl}?action=delete`,
      { id }
    ).pipe(
      tap(success => {
        console.log(success)
      }),
      catchError((error) => {
        console.log(error);
        return throwError(() => new Error('An error occurred while deleting the marker.'))
      })
    );
  }
}
