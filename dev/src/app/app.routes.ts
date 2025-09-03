import { Routes } from '@angular/router';
import { MapComponent } from './map/map.component'; 
import { MapResolver } from './map/map.resolver'; 

export const routes: Routes = [
  {
    path: 'map',
    component: MapComponent, // Charge le composant Map
    resolve: { markerList: MapResolver }, // Associe le resolver
  },
  {
    path: '',
    redirectTo: 'map', // Redirige vers le chemin 'map' par défaut
    pathMatch: 'full',
  },
  {
    path: '**',
    redirectTo: 'map', // Redirige les chemins inconnus vers 'map'
  },
];
