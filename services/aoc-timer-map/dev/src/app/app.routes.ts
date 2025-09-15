import { Routes } from '@angular/router';
import { MapComponent } from './map/map.component'; 
import { MapResolver } from './map/map.resolver';
import { NamedMobsComponent } from './named-mobs/named-mobs.component';

export const routes: Routes = [
  {
    path: 'map',
    component: MapComponent, // Charge le composant Map
    resolve: { markerList: MapResolver }, // Associe le resolver
  },
  {
    path: 'named-mobs',
    component: NamedMobsComponent, // Charge le composant Named Mobs
  },
  {
    path: '',
    component: MapComponent, // Default to map component for Angular app
    resolve: { markerList: MapResolver },
  },
  {
    path: '**',
    component: MapComponent, // Default to map component for unknown paths
    resolve: { markerList: MapResolver },
  },
];
