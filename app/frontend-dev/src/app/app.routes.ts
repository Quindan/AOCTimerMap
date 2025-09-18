import { Routes } from '@angular/router';
import { MapComponent } from './map/map.component'; 
import { MapResolver } from './map/map.resolver';
import { NamedMobsComponent } from './named-mobs/named-mobs.component';
import { LandingComponent } from './landing/landing.component';

export const routes: Routes = [
  {
    path: '',
    component: LandingComponent, // Landing page at root
  },
  {
    path: 'map',
    component: MapComponent, // Map component
    resolve: { markerList: MapResolver },
  },
  {
    path: 'named-mobs',
    component: NamedMobsComponent, // Named Mobs component
  },
  {
    path: '**',
    component: LandingComponent, // Default to landing page for unknown paths
  },
];
