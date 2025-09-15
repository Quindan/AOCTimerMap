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
    redirectTo: 'map', // Redirige vers le chemin 'map' par défaut
    pathMatch: 'full',
  },
  {
    path: '**',
    redirectTo: 'map', // Redirige les chemins inconnus vers 'map'
  },
];
