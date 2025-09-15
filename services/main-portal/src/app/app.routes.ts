import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./components/landing/landing.component').then(m => m.LandingComponent)
  },
  {
    path: 'api-docs',
    loadComponent: () => import('./components/api-docs/api-docs.component').then(m => m.ApiDocsComponent)
  },
  {
    path: '**',
    redirectTo: ''
  }
];
